# Utopia For Reddit

[![Build Status](https://travis-ci.com/NicklasTegner/UtopiaForReddit.svg?branch=master)](https://travis-ci.com/NicklasTegner/UtopiaForReddit)

# NOTE: UTOPIA IS STILL VERY MUCH IN ALPHA. RUN AT YOUR OWN RISK. MANY FEATURES AREN'T CODED YET, AND SOME FEATURES MAY NOT WORK AS EXCPECTED!!!

### What is this
UtopiaForReddit (also just Utopia) is a reddit client for the blind and visually impaired, running on Windows and MacOS.


### Installation

If you're looking for binary distributions of Utopia, please go to [the releases page](https://github.com/NicklasTegner/UtopiaForReddit/releases) and pick the latest stable version (beta and alpha's at your own risk).


#### Installation from source:

To install Utopia from source, do the following:

    # install poetry (the tool we use to manage dependencies) from pip or from their bootstrap installer (pip will be used in this example).
    pip install poetry
    # clone the GitHub repository and change into it.
    git clone https://github.com/NicklasTegner/UtopiaForReddit.git
    cd UtopiaForReddit
    # next, install all the required dependencies.
    poetry install
    # next, change into the src directory, and run the main file.
    cd src
    poetry run python UtopiaForReddit.py


### Contributing

Want to help out, please open an issue discussing the problem/bug/feature, before submitting a pull request.
If you want to tackle an issue, please let everyone know, by commenting on the issue, that you're working on it.


### License
    UtopiaForReddit is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    UtopiaForReddit is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with UtopiaForReddit.  If not, see <https://raw.githubusercontent.com/NicklasTegner/UtopiaForReddit/master/LICENSE>.
