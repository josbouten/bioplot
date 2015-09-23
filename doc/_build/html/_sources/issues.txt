Known Issues
============

Data separation character
-------------------------
In data.py the following characters are used to group data: _#_
If they are in your data set, e.g. as part of a label or meta data value, either change your data set or change the
definition of the separation characters in format.py and choose non ambiguous replacements.

Matplotlib on OSX and Ms Windows
--------------------------------
The software works well with matplotlib-1.3.1. Some matplotlib versions that are out there will show a plot on the
screen and then exit immediately. If you encounter this, let me know. This can be easily helped. Given that I encountered
this only with older versions of matplotlib I have not implemented any measures for it in the current version of bioplot.

There are some issues with labels in the zoo plots. See :ref:`rst_zooplot_labels`.
