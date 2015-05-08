Known Issues
============

data separation character
-------------------------
In data.py the following characters are used to group data: _#_
If they are in your data set, e.g. as part of a label or meta data value, either change your data set or change the characters in format.py and choose non ambiguous replacements.

matplotlib in OSX and Ms Windows
--------------------------------
The software works well with matplotlib-1.3.1. With older versions (like 0.99.3) you may encounter that plt.show(block=True) leads to an error message in boutenzoo.py at line 168. Either upgrade matplotlib or change the statement to::

    plt.show()

The Labels by default show black text on a yellow background. The yellow background may be too large for the text on Ms Windows platforms when using matplotlib 1.4.3 however. If so, set cfg.runningWindows to True, this will change the yellow background into a grey one and make the background fit the text in size.

Labels in zoo plots on OSX will appear in black on a grey background. Set runningOSX to True, this will change the yellow background into a grey one and make the background fit the text in size.
