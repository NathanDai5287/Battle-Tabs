# Battle Tabs

This game was inspired by [BattleTabs - Chrome Web Store](https://chrome.google.com/webstore/detail/battletabs/mjcklhnhfiepmofggcoegkmkokbljmjd)

It is a Python implementation of the old version of the game. 

## Installation

In order to run Battle Tabs, you must have Python installed. 

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies. The only one used is NumPy. 

```bash
pip install numpy
```

Then clone the repository. 

```bash
git clone https://github.com/NathanDai5287/Battle-Tabs.git
```

## Usage

cd into Battle Tabs. 
```bash
cd Battle-Tabs
```

Run `battletabs.py`
```bash
battletabs.py
```
or
```bash
python battletabs.py
```

## Rules
After you run `battletabs.py`, a 7 × 7 window will open. 

To make a guess, click on one of the squares. 

After you guess, you will know the Manhattan distance to the nearest ship. 

If you hit a ship, the square will turn red, and the number inside will be 0. 

There are 4 different ships: 2 × 2, 1 × 4, 1 × 3, and 1 × 1. They can be rotated in any direction. 

```bash
o o
o o
```

```bash
o o o o
```

```bash
o o o
```

```bash
o
```

Your score is the number of guesses it takes you to destroy all the ships. For reference, a "par" score would be 20. If it takes you less than 20 guesses, good job. If it takes more than 20, you're bad, or you got unlucky that round. You can tell yourself whatever you like. 

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update `testing.py` as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
