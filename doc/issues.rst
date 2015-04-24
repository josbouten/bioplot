Known Issues
============

data separation character
-------------------------
In data.py the following characters are used to group data: _#_
If they are in your data set, e.g. as part of a label or meta data value, either change your data set or change the characters in format.py and choose non ambiguous replacements.

matplotlib
----------
The software works well with matplotlib-1.3.1. With older versions (like 0.99.3) you may encounter that plt.show(block=True) leads to an error message. Either upgrade matplotlib or change the statement to::

    plt.show()

OSX
---
Labels in zoo plots on OSX will appear in black on a grey background.