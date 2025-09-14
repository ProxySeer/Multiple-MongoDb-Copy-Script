Mongo Multi DB Transfer

Copy or rename multiple MongoDB databases between clusters using a streamed mongodump | mongorestore pipeline. Generates a Windows batch file for repeatable runs.

What it does

Reads a list of database names from db.dat

Asks for source and target MongoDB connection strings

Lets you choose:

Same names on target, or

Custom rename per database (uses --nsFrom/--nsTo)

Builds streamed dump→restore commands (--archive --gzip) with --drop

Prints commands to console and writes mongo_copy_commands.bat
