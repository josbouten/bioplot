UPDATE
======

Any OS
------
Keep a copy of bioplot.cfg with your latest settings before updating anything.

If you want to only try the new version, download the latest zip file from the github page and unzip it to a new local directory.
If you want to replace the bioplot version with a new one download the latest zip file from the github page and unzip its contents to the directory bioplot is in.

Merge your favourite settings in the saved version of bioplot.cfg with the new one.

From here on, you're ready to go. 
Look at the docs and bioplot.cfg to find out about new functions and settings.

When running OSX or Windows do not forget to set either runningOSX or runningWindows in the [cfg] section in bioplot.cfg. So in case of OSX use: ::

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

