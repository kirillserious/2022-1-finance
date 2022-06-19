# Before the beginning
Install required dependencies
```sh
sudo pacman -S tk # for Arch, or if you use Debian
# sudo apt-get install -y python3-tk
python3 -m pip install -r requirements.txt
git clone git@github.com:doctormee/robust-fpm-cmc-msu-edu-2021
```

# Project
The project contains several entry points to the program that build various graphs and a report that can be found in the `report` folder.

Main entry points:
```sh
# Plot of the dependence of the premium on the initial prices
python3 depends_on_start.py
# Plot of the dependence of the premium on the volatility
python3 depends_on_volatility.py
# Plot of the dependence of the premium on the strike
python3 depends_on_strike.py
# Plot of the dependence of the premium on the constraint
python3 depends_on_constraint.py
```