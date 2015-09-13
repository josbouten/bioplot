Tools
=====

bv2bioplot.py
-------------

Convert a bv results data file to a data file for bioplot.
Example of usage: ::

    python bv2bioplot.py  -i inputfile -o outputfile

sretools2bioplot.py
-------------------
Convert a sretools type input data file to a data file for bioplot.

Sre tools consist of utilities witten in R which accepts several columns of data.
This script is an example which you can use to use that same data as input for bioplot.

Example of input: ::

    Tspid,Tfrid,Mspid,Mfrid,score,target
    114849,0000000005712904a,114849,0000000005713112b,5.368496418,TRUE
    114849,0000000005712904a,114853,0000000005281055b,1.67685461,FALSE
    114849,0000000005712904a,114853,0000000005288357b,1.363172889,FALSE
    114849,0000000005712904a,114854,0000000005133202a,-0.024709666,FALSE

Example of usage: ::

    python sretools2bioplot.py -i inputfile -o outputfile

vocalise2bioplot.py
-------------------

Convert a vocalise data file to a data file for bioplot.

Example of usage: ::

    python vocalise2bioplot.py -i inputfile -o outputfile
