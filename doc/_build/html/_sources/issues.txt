Known Issues
============

Data separation character
-------------------------
In data.py the following characters are used to group data: _#_
If they are in your data set, e.g. as part of a label or meta data value, either change your data set or change the
characters in format.py and choose non ambiguous replacements.

Matplotlib on OSX and Ms Windows
--------------------------------
The software works well with matplotlib-1.3.1. Some matplotlib versions that are out there will show a plot on the
 screen and then exit immediately. If you encounter this, let me know. This can be easily helped. Given that I encountered
 this only with older versions of matplotlib I have not implemented any measures for it in the current version of bioplot.

The Labels by default show black text on a yellow background. The yellow background may be too large for the text on
Ms Windows platforms when using matplotlib 1.4.3 however. If so, set cfg.runningWindows to True, this will change the
yellow background into a grey one and make the background fit the text in size.

Labels in zoo plots on OSX will appear in black on a grey background. Set runningOSX to True, this will change the
yellow background into a grey one and make the background fit the text in size.

Implementation notes
--------------------
When drawing a histogram lots of warnings like this one may be seen on the screen: ::

    /usr/lib/pymodules/python2.7/matplotlib/cbook.py:1711: DeprecationWarning: using a non-integer number instead of an
    integer will result in an error in the future
    result = np.zeros(new_shape, a.dtype)

To suppress warnings like this a filter was added in histogram.py to filter out this specific warning using: ::

    import warnings
    warnings.filterwarnings("ignore", category=DeprecationWarning)
