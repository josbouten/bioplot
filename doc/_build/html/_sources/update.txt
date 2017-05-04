UPDATE
======

------------
All versions
------------
Keep a copy of bioplot.cfg with your latest settings before updating anything.

Note: each version you download is self contained. You do not need anything from an existing version to run a new one.

If you want to only try the new version, download the latest zip file from the github page and unzip it to a new local directory.
If you want to replace the bioplot version with a new one download the latest zip file from the github page, rename the
old bioplot directory to bioplot.org and unzip the new version. Then copy your input and output files from the input and
output dir from the old version into the corresponding directory of the new one.

Merge your favourite settings in the saved version of bioplot.cfg with the new one. On osx or linux I would use diff or vimdiff for this.
As I'm not a windows user, if you are, you're on your own.

From here on, you're ready to go.
Have a look at the changelog.txt file, the man pages, the html docs and bioplot.cfg to find out about new functions and
settings and read the update section for possible extra update steps.

When running OSX or Windows do not forget to set either runningOSX or runningWindows in the [cfg] section in bioplot.cfg.
So in case of OSX use: ::

    [cfg]
    runningOSX = True
    runningWindows = False

Or in case of a compatible MS Windows OS use: ::

    [cfg]
    runningOSX = False
    runningWindows = True

Linux users set both to False.
Do not forget to set your screen's resolution in [cfg] using screenResolution (in this example it is set to 1600x1200). ::

    [cfg]
    screenResolution = 1600x1200


bioplot will run on python3.x only.

v0.9.9
------
Because of the transition of the code base to python3.5 you need to start bioplot.py with python3.5
Bioplot should run with any version of python equal to or higher than 3.0.
If on your system you have both versions, make sure to use the right one. This can be enforced by
explicitely prepending it to the command like so (assume you run the command from the command line
in the bioplot code directory): ::

	On Ms Windows (after installing anaconda3)
	python.exe ./bioplot.py -h

	On OSX
	python3 ./bioplot.py -h

	On linux
	python3 ./bioplot.py -h

If you are experiencing problems with matplotlib you may need get an error message when it is imported. You may see something like this: ::

  File "/Users/jos/projects/bioplot/utils.py", line 30, in <module>
    import matplotlib.pyplot as plt
  File "/Users/jos/anaconda/lib/python3.5/site-packages/matplotlib/pyplot.py", line 114, in <module>
    _backend_mod, new_figure_manager, draw_if_interactive, _show = pylab_setup()
  File "/Users/jos/anaconda/lib/python3.5/site-packages/matplotlib/backends/__init__.py", line 32, in pylab_setup
    globals(),locals(),[backend_name],0)
  File "/Users/jos/anaconda/lib/python3.5/site-packages/matplotlib/backends/backend_macosx.py", line 24, in <module>
    from matplotlib.backends import _macosx

  RuntimeError: Python is not installed as a framework. The Mac OS X backend will 
  not be able to function correctly if Python is not installed as a framework. 
  See the Python documentation for more information on installing Python as a 
  framework on Mac OS X. Please either reinstall Python as a framework, or try 
  one of the other backends. If you are Working with Matplotlib in a virtual 
  enviroment see 'Working with Matplotlib in Virtual environments' in the Matplotlib 
  FAQ

To remedy this set the plotting backend in /Users/<your user name>/.matplotlib/matplotlibrc. 
If the file does not exist, make it and put the following content in it: ::

	backend: TkAgg

------
v0.9.4
------

OSX
---
From bioplot v0.9.4 on you'll need to install the python machine learning library scikit-learn: ::

    sudo pip install scikit-learn

