# Python Password manager
Password manager with CRUD operations created using Python

## Versions

There are 2 versions:

* cli.py is the command line version (deprecated)

* gui.py is the graphical version created using TkInter (up to date)


## Run

1. Create a user environment variable _PM_PASSWORD_ that stores hashed master password:

  * Run hash.py file

  * Use function hashPassword(_password_) to generate sha256 hash

  * Use function storeHash(_hash_) to store hash in _PM_PASSWORD_

  * Verify using verifyPassword(_password_)

2. Run gui.py

## Screenshots

Entering master password:

![image](https://user-images.githubusercontent.com/31571314/77235043-a6934a00-6bd8-11ea-8b03-0cfbb41f611f.png)

Main window:

![image](https://user-images.githubusercontent.com/31571314/77235078-dcd0c980-6bd8-11ea-8dfb-4b35e3a43570.png)

Display table:

![image](https://user-images.githubusercontent.com/31571314/77235121-3f29ca00-6bd9-11ea-89b7-651a9580aac2.png)

Dialogs:

![image](https://user-images.githubusercontent.com/31571314/77235172-a0ea3400-6bd9-11ea-8167-4cc1a6976eeb.png)


