```
    ###########################################################################
    #                        Conformational Identifier                        #
    #                            ConfID 0.1.0 (2019)                          #
    #                                                                         #
    # Marcelo D Poleto, Bruno I Grisci, Marcio Dorn, Hugo Verli, ConfID: an   #
    # analytical method for conformational characterization of small          #
    # molecules using molecular dynamics trajectories, Bioinformatics, Volume #
    # X, Issue X, Day Month 2019, Pages XXXX-XXX, doi                         #
    #                                                                         #
    #                    http://sbcb.inf.ufrgs.br/confid                      #
    #                                                                         #
    #            In case of bugs or suggestions, please contact us:           #
    #                         marcelo.poleto@ufv.br                           #
    #                         bigrisci@inf.ufrgs.br                           #
    #                                                                         #
    # LGPL-3.0                                          BR512019001928-8 2019 #
    ###########################################################################
```

# Installation

## Install ***ConfID*** on Ubuntu using snapcraft (recommended)

### 1. Enable snapd

If you are using Ubuntu 16.04 LTS (Xenial Xerus) or later, including Ubuntu 18.04 LTS (Bionic Beaver), Ubuntu 18.10 (Cosmic Cuttlefish) and Ubuntu 19.04 (Disco Dingo), Snap should be already installed.

For versions of Ubuntu between 14.04 LTS (Trusty Tahr) and 15.10 (Wily Werewolf), as well as Ubuntu flavours that do not include snap by default, it can be installed from the Ubuntu Software Centre by searching for snapd, or from the command line:
```
$ sudo apt update
$ sudo apt install snapd
```
Either log out and back in again, or restart your system, to ensure snap’s paths are updated correctly.

### 2. Install ***ConfID***

To install ***ConfID***, simply use the following commands on your terminal:
```
$ sudo snap install confid
$ snap connect confid:removable-media
```
Confirm ***ConfID*** is installed by listing your installed snaps:
```
$ snap list
```
Then you can run ***ConfID*** by typing on your terminal:
```
$ confid input.inp config
```
## Install ***ConfID*** on other Linux distributions using snapcraft

To install ***ConfID*** in other Linux distributions (Fedora, Linux Mint, Kubuntu, Debian, etc.) please refer to the instructions at the bottom of the page: https://snapcraft.io/confid

## Install ***ConfID*** on macOS using the exec file (recommended)

You can run ***ConfID*** on your macOS machine by using the provided exec file.

### 1. Download the exec

Download the file [confid_0.1.0_macos](confid_0.1.0_macos) to your directory of choice: https://github.com/sbcblab/confid/blob/master/confid_0.1.0_macos

Rename it to ```confid``` for practicality.

### 2. Run ***ConfID***

To run, simply type on your terminal in the same directory of the downloaded exec:

```
$ ./confid -h
```

## Install ***ConfID*** on macOS using Snapcraft

Snapcraft 3 can be installed via Homebrew on Apple macOS Yosemite (or later), and then used to build ***ConfID*** within the macOS environment.

### 1. Prerequisites

Install the the Homebrew package manager: https://brew.sh/#install

Install Snapcraft and Multipass by opening 'Terminal' and entering the following:

```
$ brew install snapcraft
$ brew cask install multipass
```
### 2. Configure the virtual machine

Create a Linux virtual machine:
```
$ multipass launch -n testvm
```
Connect to the virtual machine:
```
$ multipass shell testvm
```

### 3. Install the snap

Install ***ConfID*** inside the virtual machine:

```
$ sudo snap install confid
$ snap connect confid:removable-media
```
Confirm ***ConfID*** is installed by listing your installed snaps:

```
$ snap list
```
Run ***ConfID*** inside the virtual machine:
```
$ confid -h
```
Exit the virtual machine:

```
$ exit
```

## Install ***ConfID*** from the source code

This is the best way to use ***ConfID*** as a developer if you wish to modify the source code yourself, or if you want to use ***ConfID*** on other operating systems.

### 1. Check for dependencies

To run ***ConfID*** you will need either Python 2.7 or Python 3.x installed in your machine.

***ConfID*** requires the following external libraries:

- graphviz (https://pypi.org/project/graphviz/)
- matplotlib (https://matplotlib.org/)
- numpy (https://numpy.org/)

If any of those are missing, you should install them before continuing. Before installing Graphviz for Python, make sure that the original software is installed (http://www.graphviz.org/download/). Before installing it, the following dependencies should be installed as well:
```
$ sudo apt install -y libgd-dev
$ sudo apt install -y fontconfig
$ sudo apt install -y libcairo2-dev
$ sudo apt install -y libpango1.0-dev
$ sudo apt install -y libgts-dev
```
### 2. Download ***ConfID***

Download all files from https://github.com/sbcblab/confid and save them to your directory of choice. If you have git installed you can do this by typing the following in your terminal:
```
$ git clone https://github.com/sbcblab/confid.git
```
Now you can run ***ConfID*** by typing the following command in your terminal:
```
$ python3 confID.py input.inp config
```
### 3. Aliasing ***ConfID*** (optional)

To run ***ConfID*** in any given directory without carrying a lot of files with you, we advise you to alias ***ConfID***. For this:

Copy the ```confid``` folder that was extracted before;

Move it to an installation folder of your choice;

Then, add the following line to the end of your ```~/.bashrc``` file:

```
alias confid='python3 /installation\_folder\_you\_chose/ConfID/confID.py'

(example: alias confid='python3 /home/user/Tools/ConfID/confID.py)
```

```
$ source ~/.bashrc
```
After this, you should be able to run ***ConfID*** in your terminal at any given directory by simple typing:
```
$ confid input.inp config
```
# Running ***ConfID***

To run ***ConfID*** open your terminal and type

### From Snapcraft
```
$ confid input.inp config
```
### From macOS exec
```
$ ./confid input.inp config
```
### From source (not aliased)
```
$ python3 confID.py input.inp config
```
### From source (aliased)
```
$ confid input.inp config
```

In which ```input.inp``` is a file containing in each line the paths to each dihedral file to serve as input, and ```config``` is an optional file containing the configuration of parameters for ***ConfID***.

To read the help section of ***ConfID*** you can also run 
```
$ confid -h
```