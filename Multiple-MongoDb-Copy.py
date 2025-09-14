import sys
from pathlib import Path

DB_FILE = "db.dat"
OUT_FILE = "mongo_copy_commands.bat"

def read_db_list(db_file: str):
 p = Path(db_file)
 if not p.exists():
 print(f"ERROR: '{db_file}' not found.")
 input("\nPress Enter to exit...")
 sys.exit(1)
 with p.open("r", encoding="utf-8") as f:
 return [ln.strip() for ln in f if ln.strip()]

def ask(prompt: str) -> str:
 try:
 return input(prompt).strip()
 except EOFError:
 return ""

def build_cmd_same_name(src_uri: str, dst_uri: str, db: str) -> str:
 return (
 f'mongodump --uri "{src_uri}" --db {db} --archive --gzip | '
 f'mongorestore --uri "{dst_uri}" --archive --gzip --drop'
 )

def build_cmd_rename(src_uri: str, dst_uri: str, src_db: str, dst_db: str) -> str:
 return (
 f'mongodump --uri "{src_uri}" --db {src_db} --archive --gzip | '
 f'mongorestore --uri "{dst_uri}" --archive --gzip '
 f'--nsFrom "{src_db}.*" --nsTo "{dst_db}.*" --drop'
 )

def main():
 dbs = read_db_list(DB_FILE)

 src_uri = ask("Enter SOURCE MongoDB connection string: ")
 dst_uri = ask("Enter TARGET MongoDB connection string: ")

 print("\nRename options:")
 print(" 1) Keep same database names")
 print(" 2) Enter custom new name per database")
 mode = ask("Choose 1 / 2: ")

 rename_map = {}
 if mode == "2":
 for d in dbs:
 new_name = ask(f"New name for '{d}' (leave blank to keep same): ")
 rename_map[d] = new_name if new_name else d
 else:
 rename_map = {d: d for d in dbs}

 commands = []
 for d in dbs:
 target_db = rename_map[d]
 if target_db == d:
 commands.append(build_cmd_same_name(src_uri, dst_uri, d))
 else:
 commands.append(build_cmd_rename(src_uri, dst_uri, d, target_db))

 print("\n=== Generated Commands ===\n")
 for cmd in commands:
 print(cmd + "\n")

 out = Path(OUT_FILE)
 with out.open("w", encoding="utf-8") as f:
 f.write("@echo off\nsetlocal\n\n")
 for d, cmd in zip(dbs, commands):
 f.write(f'echo ===== {d} =====\n')
 f.write(cmd + "\n\n")
 f.write("echo All done.\nendlocal\n")

 print(f"Commands also saved to: {out.resolve()}")
 input("\nPress Enter to exit...")

if __name__ == "__main__":
 main()