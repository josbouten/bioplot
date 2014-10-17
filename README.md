=======
Bioplot
=======

![bioplot of 2 data sets](https://github.com/josbouten/bioplot/blob/master/examples/A_and_B_zoo_plot.png "bioplot of 2 data sets")
bioplot.py is a program which can draw several plots that can be used
when evaluating the performance of a biometric system. The example
picture shows a so called zoo plot.
 
Copyright (C) 2014 Jos Bouten ( josbouten@gmail.com )

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

Read the manual.txt document to find out what the program can do.
Also take a look at the screendumps in the examples directory.

Installation
============

Ms Windows
----------
Follow the instructions found here: http://matplotlib.org/users/installing.html
I've tried anaconda 2.01 (32 bit version) on W7 but I've heard that it works
with the 64 bit version on W8 as well.
This will install python 2.7.7 and a load of python modules amongst which numpy, matplotlib, pyplot.
You will be able to run bioplot.py and do much more pythony things ;-)
If you get into trouble, talk to your local windows guru. Do not mail me! 

Copy plot.cfg_4_windows.txt to bioplot.cfg in the working directory (the directory where
bioplot.py is stored) and run the main program from that directory to find out how to use it.

<code> python.exe bioplot.py -h</code>

Also look at bioplot.cfg to find out about additional options not available
via the command line interface. There are lots of them. Their values are shown on the
commandline whenever you run the program, unless you choose not to via the appropriate
option in bioplot.cfg

Linux
-----
You need to have python2.7.x installed. On most linux systems this is the case.
Then install matplotlib and some other modules using:

<code> $ sudo apt-get install python-matplotlib python-numpy python-scipy</code>

I tried it on Ubuntu 14.04 and it worked like a charm.
Next, copy plot.cfg_4_linux to bioplot.cfg
Then run the main program: 

<code> $ ./bioplot.py -h</code>

to find out how to use it.
Also look at bioplot.cfg to find out about additional options not available
via the command line interface. There are lots of them.  Their values are shown on the
commandline whenever you run the program, unless you choose not to via the appropriate
option in bioplot.cfg

OSX
---
On OSX 10.9.5 run these commands:

<code> $ curl -O https://bootstrap.pypa.io/get-pip.py</code>

<code>$ python get-pip.py</code>

<code>$ pip2 install matplotlib</code>

<code>$ sudo git clone https://github.com/josbouten/bioplot.git</code>

Then change the owner of the bioplot directory to your user:

<code> $ sudo chown -R your-user-name:staff bioplot</code>

Next, copy plot.cfg_4_osx to bioplot.cfg

From here on, you're ready to go.
Run the main program from a terminal from within the directory where you installed it: 

<code> $ ./bioplot.py -h</code>

to find out how to use it.
Also look at bioplot.cfg to find out about additional options not available
via the command line interface.  There are lots of them.  Their values are shown on the
commandline whenever you run the program, unless you choose not to via the appropriate
option in bioplot.cfg

Note: in contrast to the example plots supplied labels in plots on OSX will appear in
black on a grey background.

Usage
-----
See manual.txt
