INSTALL
=======

Ms Windows
----------
Follow the instructions found here: http://matplotlib.org/users/installing.html
I've tried anaconda 2.01 (32 bit version) on W7 but I've heard that it works
with the 64 bit version on W8 as well.
This will install python 2.7.7 and a load of python modules amongst which numpy, matplotlib, pyplot.
You will be able to run bioplot.py and do much more pythony things ;-)
If you get into trouble, talk to your local windows guru. Do not mail me! 

Copy bioplot.cfg_4_windows.txt to bioplot.cfg in the working directory (the directory where
bioplot.py is stored): ::

    copy bioplot.cfg_4_windows.txt bioplot.cfg

And change any settings in it relevant to your use case.
From here on, you're ready to go. Run the main program from a terminal: ::

    python.exe bioplot.py -h 

to find out how to use it.
Also look at bioplot.cfg to find out about additional options not available
via the command line interface. There are lots of them. Their values are shown on the
commandline whenever you run the program, unless you choose not to via the appropriate
option in bioplot.cfg

Linux
-----
You need to have python2.7.x installed. On most linux systems this is the case.
Then install matplotlib and some other modules using:

sudo apt-get install python-matplotlib python-numpy python-scipy

I tried it on Ubuntu 14.04 and it worked like a charm.
Next, copy bioplot.cfg_4_linux to bioplot.cfg: ::

    cp bioplot.cfg_4_linux bioplot.cfg

And change any settings in it relevant to your use case.

Then run the main program: ::

    ./bioplot.py -h 

to find out how to use it.
Also look at bioplot.cfg to find out about additional options not available
via the command line interface. There are lots of them.  Their values are shown on the
commandline whenever you run the program, unless you choose not to via the appropriate
option in bioplot.cfg

OSX
---
On OSX 10.9.5 run these commands: ::

    curl -O https://bootstrap.pypa.io/get-pip.py

    python get-pip.py

    pip2 install matplotlib

    sudo git clone https://github.com/josbouten/bioplot.git

Then change the owner of the bioplot directory to your user: ::

    sudo chown -R your-user-name:staff bioplot

Next, copy plot.cfg_4_osx to bioplot.cfg: ::

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
