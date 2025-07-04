# Faction Reputation App

A simple app for TTRPGs that allow a DM to track the rep their party has with various orgs/groups.

I made this *solely* to start to learn Python.

## TODOs

- [x] Add removing of a group
- [x] Add notifications that data was loaded in/saved elsewhere
- [x] Customizable file names
- [x] Upload JSON

## Tech Stack

Written in Python with [customtkinter](https://customtkinter.tomschimansky.com/).

## Getting Started

1. Open the code in VS Code.
2. Open the terminal and enter in the following command:
    - python3 -m venv FRA
    - source FRA/bin/activate
    - pip3 install customtkinter
3. Run 'python3 app.py' to run the code

## Building the App

- Ensure you are in the venv for FRA
- pyinstaller is install in the venv: 'pip install pyinstaller'
- Run 'pyinstaller --noconfirm --onefile --windowed app.py'
