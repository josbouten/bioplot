INSTALL
=======

Ms Windows
----------
Follow the instructions found here: http://matplotlib.org/users/installing.html.
I've tried anaconda 2.01 (32 bit version) on W7 32 bits, and I've heard that it works on XP and with the 64 bit
version on W8 as well. Moreover I've tried anaconda 2.2.0.x with W10 (the preview) 64 bits, and it works as well.
So it seems you can choose whatever version of windows you like. Anaconda will install python 2.7.x and a load of
python modules amongst which numpy, matplotlib, pyplot.
You will be able to run bioplot.py and do much more pythony things ;-)

Download the zip file from the github page and unzip its contents to a local directory.

Copy bioplot.cfg_4_windows.txt to bioplot.cfg in the working directory (the directory where
bioplot.py is stored): ::

    copy bioplot.cfg_4_windows.txt bioplot.cfg

And change any settings in it relevant to your use case.
From here on, you're ready to go. Run the main program from a terminal: ::

    python.exe bioplot.py -h 

to find out how to use it.
Also look at bioplot.cfg to find out about additional options not available
via the command line interface. There are lots of them. Their values are shown on the
command line whenever you run the program, unless you choose not to via the appropriate
option in bioplot.cfg

Set your screen's resolution in [cfg] using screenResolution (in this example it is set to 1600x1200). ::

    [cfg]
    screenResolution = 1600x1200

Since there is no way for me to know who downloaded bioplot, other than the downloader telling me herself,
send me an email if you want to be kept in the loop with changes or updates.

Linux
-----
You need to have python2.7.x installed. On most linux systems this is the case.
Then install matplotlib (e.g. version 1.3.1 or higher) and some other modules using:

sudo apt-get install python-matplotlib python-numpy python-scipy

I tried it on Ubuntu 14.04 and it worked like a charm.
Next, copy bioplot.cfg_4_linux to bioplot.cfg (or make a link): ::

    cp bioplot.cfg_4_linux bioplot.cfg

And change any settings in it relevant to your use case.

Then run the main program: ::

    ./bioplot.py -h 

to find out how to use it.
Also look at bioplot.cfg to find out about additional options not available
via the command line interface. There are lots of them.  Their values are shown on the
commandline whenever you run the program, unless you choose not to via the appropriate
option in bioplot.cfg

Set your screen's resolution in [cfg] using screenResolution (in this example it is set to 1600x1200). ::

    [cfg]
    screenResolution = 1600x1200

Since there is no way for me to know who downloaded bioplot, other than the downloader telling me herself,
send me an email if you want to be kept in the loop with changes or updates.

OSX
---
On OSX 10.9.5 run these commands: ::

    curl -O https://bootstrap.pypa.io/get-pip.py

    python get-pip.py

    pip2 install matplotlib

    sudo git clone https://github.com/josbouten/bioplot.git

Then change the owner of the bioplot directory to your user: ::

    sudo chown -R your-user-name:staff bioplot

Next, copy plot.cfg_4_osx to bioplot.cfg (or make a link): ::

    cp plot.cfg_4_osx bioplot.cfg

And change any settings in it relevant to your use case.

From here on, you're ready to go. Run the main program from a terminal: ::

    ./bioplot.py -h 

to find out how to use it.
Also look at bioplot.cfg to find out about additional options not available
via the command line interface.  There are lots of them.  Their values are shown on the
commandline whenever you run the program, unless you choose not to via the appropriate
option in bioplot.cfg

Note: in contrast to the example plots supplied labels in plots on OSX will appear in
black on a grey background. In order to make labels readable the following flag should be set
in bioplot.cfg: ::

    [cfg] 
    runningOSX = True

Set your screen's resolution in [cfg] using screenResolution (in this example it is set to 1600x1200). ::

    [cfg]
    screenResolution = 1600x1200

Since there is no way for me to know who downloaded bioplot, other than the downloader telling me herself,
send me an email if you want to be kept in the loop with changes or updates.