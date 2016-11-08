Bioplot
=======

![bioplot of 2 data sets](https://github.com/josbouten/bioplot/blob/master/examples/showcase_zoo_plot.png "bioplot of 2 data sets")
bioplot.py is a program which can draw several plots that can be used
when evaluating the performance of a biometric system. 
The plot types currently supported are:
accuracy plot, cumulative score distribution plot, DET plot, EER plot, histogram, matrix plot,
ranking plot, roc plot, tippett plot and zoo plot.
The example picture shows a so called zoo plot.
 
Copyright (C) 2014, 2015, 2016 Jos Bouten ( josbouten at gmail dot com )

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

Read the rst or html documentation and the bioplot.cfg config file to find out what the program can do.
Also take a look at the screendumps in the examples directory.

Installation
============

Linux
-----
You need to have python3.5 installed. On most linux systems this is already the case.
First install git, matplotlib and some other modules using:

<code>$ sudo apt-get install python3-matplotlib python3-numpy python3-scipy git python3-sklearn</code>

Next, install bioplot using either git:

<code>$ git clone https://www.github.com/josbouten/bioplot.git</code>

(this will create a directory called 'bioplot')

or download the zip file from github and unzip it in a directory of choice.

Next, copy plot.cfg_4_linux to bioplot.cfg

Finally run the main program: 

<code>$ ./bioplot.py -h</code>

to find out how to use it.
Also look at bioplot.cfg to find out about additional options not available
via the command line interface. There are lots of them.  Their values are shown on the
command line whenever you run the program, unless you choose not to via the appropriate
option in bioplot.cfg. Finally, there is the html doc you might want to read ...

Ms Windows
----------
Follow the instructions found here: http://matplotlib.org/users/installing.html
Download anaconda 3-4.2.0 (32 bit version) on W7 32 bits or the 64 bits version accoring to your machine's architecture.
Anaconda will install python 3.5 and a load of python modules amongst which numpy, matplotlib, pyplot.
You will be able to run bioplot.py and do much more pythony things ;-)

Download the zip file from the github page and unzip its contents to a local directory.

Copy plot.cfg_4_windows.txt to bioplot.cfg in this local directory and run the main 
program from that directory to find out how to use it (and read the html doc).


<code>python3.5.exe bioplot.py -h</code>

Also look at bioplot.cfg to find out about additional options not available
via the command line interface. There are lots of them. Their values are shown on the
command line whenever you run the program, unless you choose not to via the appropriate
option in bioplot.cfg

OSX
---
On OSX 10.9.5 run these commands:

<code>$ curl -O https://bootstrap.pypa.io/get-pip.py</code>

<code>$ sudo python get-pip.py</code>

<code>$ sudo pip2 install matplotlib</code>

<code> $ sudo pip install scikit-learn </code>

<code>$ git clone https://github.com/josbouten/bioplot.git</code>

Then change the owner of the bioplot directory to your user:

<code>$ sudo chown -R your-user-name:staff bioplot</code>

Next, copy bioplot.cfg_4_osx to bioplot.cfg

From here on, you're ready to go.
Finally run the main program from a terminal from within the directory where you installed it: 

<code>$ ./bioplot.py -h</code>

to find out how to use it.
Also look at bioplot.cfg to find out about additional options not available
via the command line interface.  There are lots of them.  Their values are shown on the
command line whenever you run the program, unless you choose not to via the appropriate
option in bioplot.cfg. Finally, there is the html doc you might want to read ...
   
Note: in contrast to the example plots supplied labels in plots on OSX will appear in
black on a grey background.

Usage or Problems
-----------------
READ THE DOCS!

Windows users:

Copy and paste this line into internet explorer:

<code>file:///C:\Users\user name\bioplot\doc\\_build\html\index.html</code>

Make sure you change \<user name\> into the appropriate name.
You can also navigate to the html directory and double clicking on index.html.
Internet Explorer may indicate that some active X element or script was blocked.
This is caused by the search function in the bioplot docs. This function is perfectly 
harmless, and helpfull, so you can enable it without any risks.

OSX users:

Copy and paste this line:

<code>file:///Users/\<user name\>/bioplot/doc/\_build/html/index.html</code>

into whatever browser you use.

Make sure you change \<user name\> into the appropriate name.

Linux users:

Copy and paste this line:

<code>file:///home/users/\<user name\>/bioplot/doc/\_build/html/index.html</code>

into whatever browser you use.

Make sure you change \<user name\> into the appropriate name.

How to Update
=============

OSX
---
From bioplot v0.9.4 on you’ll need to install the python machine learning library scikit-learn:

<code> $ sudo pip install scikit-learn </code>

All versions
------------
Keep a copy of bioplot.cfg with your latest settings before updating anything.

Note: each version you download is self contained. You do not need anything from an existing version to run a new one.

If you want to only try the new version, download the latest zip file from the github page and unzip it to a new local
directory. If you want to replace the bioplot version with a new one download the latest zip file from the github page,
rename the old bioplot directory to bioplot.org and unzip the new version. Then copy your input and output files from
the input and output dir from the old version into the corresponding directory of the new one.

Merge your favourite settings in the saved version of bioplot.cfg with the new one. On osx or linux I would use diff or
vimdiff for this. As I’m not a windows user, if you are, you’re on your own.

From here on, you’re ready to go. Have a look at the changelog.txt file, the html docs, man pages and bioplot.cfg to
find out about new functions and settings and read the update section for possible extra update steps.

When running OSX or Windows do not forget to set either runningOSX or runningWindows in the [cfg] section in
bioplot.cfg. So in case of OSX use:

<code>[cfg]</code>

<code>runningOSX = True</code>

<code>runningWindows = False</code>

Or in case of a compatible MS Windows OS use:

<code>[cfg]</code>

<code>runningOSX = False</code>

<code>runningWindows = True</code>

Linux users set both to False. Do not forget to set your screen’s resolution in [cfg] using screenResolution (in this example it is set to 1600x1200).

<code>[cfg]</code>

<code>screenResolution = 1600x1200</code>
