INSTALL
=======

Ms Windows
----------
Follow the instructions found here: http://matplotlib.org/users/installing.html.
Download anaconda3-4.2.0 (32 bit version) on W7 32 bits or the 64 bits version according to your machine's architecture.
Anaconda will install python 3.5 and a load of python modules amongst which numpy, matplotlib, pyplot and scikit-learn. You will be able to run bioplot.py and do much more pythony things ;-)

Download the zip file from the github page and unzip its contents to a local directory.

Copy bioplot.cfg_4_windows.txt to bioplot.cfg in the working directory (the directory where
bioplot.py is stored): ::

    copy bioplot.cfg_4_windows.txt bioplot.cfg

And change any settings in it relevant to your use case.
From here on, you're ready to go. Run the main program from a terminal using: ::

    python3.exe bioplot.py -h 

to find out how to use it.
Also look at bioplot.cfg to find out about additional options not available
via the command line interface. There are lots of them. Their values are shown on the
command line whenever you run the program, unless you choose not to via the appropriate
option in bioplot.cfg

Set your screen's resolution in [cfg] using screenResolution (in this example it is set to 1600x1200). ::

    [cfg]
    screenResolution = 1600x1200

Update notifications
~~~~~~~~~~~~~~~~~~~~
Since there is no way for me to know who downloaded bioplot, other than the downloader telling me,
send me an email if you want to be notified of changes.

Linux
-----

Requirements
~~~~~~~~~~~~
From v0.9.9 on you need to have python3.5 installed. On most linux systems this is the case.
Then install matplotlib and some other modules using: ::

	sudo apt-get install python3-matplotlib python3-numpy python3-scipy

Next, copy bioplot.cfg_4_linux to bioplot.cfg (or make a link): ::

    cp bioplot.cfg_4_linux bioplot.cfg

And change any settings in it relevant to your use case.

Then run the main program using python 3: ::

    python3 ./bioplot.py -h

    or

    ./bioplot.py -h

to find out how to use it.
Also look at bioplot.cfg to find out about additional options not available
via the command line interface. There are lots of them.  Their values are shown on the
commandline whenever you run the program, unless you choose not to via the appropriate
option in bioplot.cfg

Set your screen's resolution in [cfg] using screenResolution (in this example it is set to 1600x1200). ::

    [cfg]
    screenResolution = 1600x1200

Man pages
~~~~~~~~~
If you want to include the bioplot doc as part of the  linux manual system, include  bioplot/doc/_build/man/bioplot.1 in your manpath.

Update notifications
~~~~~~~~~~~~~~~~~~~~
Since there is no way for me to know who downloaded bioplot, other than the downloader telling me,
send me an email if you want to be notified of changes.

OSX
---

Requirements
~~~~~~~~~~~~
You need to have python3.5 installed. 

On OSX 10.9.5 anf higher run these commands: ::

    curl -O https://bootstrap.pypa.io/get-pip.py

    python get-pip.py

You'll need to install the libraries matplotlib, numpy and scikit-learn: ::

    sudo pip3 install matplotlib
    sudo pip3 install numpy
    sudo pip3 install scikit-learn

An OSX Git installer is maintained and available for download at the Git website, at http://git-scm.com/download/mac.
Download it and install it by double clicking the dmg file. Then follow the instructions.
Next check out the source code of bioplot from the github repository: ::

    sudo git clone https://github.com/josbouten/bioplot.git

Then change the owner of the bioplot directory to your user: ::

    sudo chown -R your-user-name:staff bioplot

Next, copy plot.cfg_4_osx to bioplot.cfg (or make a link): ::

    cp plot.cfg_4_osx bioplot.cfg

And change any settings in it relevant to your use case.

From here on, you're ready to go. Run the main program from a terminal using python 3: ::

    python3 bioplot.py -h

    or

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

Set your screen's resolution in [cfg] using screenResolution: ::

    [cfg]
    screenResolution = 1600x1200


.. _rst_install_matplotlib:

Matplotlib backend
~~~~~~~~~~~~~~~~~~
You may need to set the matplotlib backend to TkAgg.
Create the file  /Users/<your user name>/.matplotlib/matplotlibrc and put the following line in: ::

	backend: TkAgg

Man pages
~~~~~~~~~
If you want to include the bioplot doc as part of the OSX manual system, include  bioplot/doc/_build/man/bioplot.1 in your manpath.

Update notifications
~~~~~~~~~~~~~~~~~~~~
Since there is no way for me to know who downloaded bioplot, other than the downloader telling me,
send me an email if you want to be notified of changes.
