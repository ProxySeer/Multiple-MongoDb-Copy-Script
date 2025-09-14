Mongo Multi DB Transfer (Python)

Copy or rename multiple MongoDB databases between servers using a streamed mongodump | mongorestore pipeline.


You’ll be prompted for:

SOURCE MongoDB connection string

TARGET MongoDB connection string

Whether to keep names or rename per DB

The script:

Prints all mongodump | mongorestore commands to the console

Also saves them to mongo_copy_commands.bat (handy on Windows).
On Linux/macOS, just copy the printed commands into your shell.
