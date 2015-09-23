Tools
=====

.. _rst_anonymize:

anonymize.py
------------
This script will convert a bioplot data file into an anonymized data file by replacing all relevant elements by a hash value.
That should make it hard for anyone to decode it. In case you want to exchange data with anyone, you can thus
preserve the anonymity of the subjects. You can e.g. use this script if you want to send me a data set in case you have
problems processing it. Use it like so: ::

     python anonymize.py input_file output_file

Example: ::

    python anonymize.py example_data.txt example_data_anonymized.txt

If you now look at the contents of the files (only the first few lines are shown), you will see that all elements except
the score, truth value and meta data label have been replaced by hash values: ::

    ==> input/example_data.txt <==
    114846 0000000005146119b 114854 bla -1.3412277399322274 FALSE 60s_2x30s
    114847 0000000005146119b 114854 bla -2.2384162803080474 FALSE 60s_2x30s
    114848 0000000005146119b 114854 bla -0.22776277505632123 FALSE 60s_2x30s
    114849 0000000005146119b 114854 bla -0.42766955655065264 FALSE 60s_2x30s
    114850 0000000005146119b 114854 bla -2.838987423178022 FALSE 60s_2x30s

    ==> input/example_data_anonymized.txt <==
    d068898f905ec982135fadb46e1fe2db5c4e227b4b2deb97ad3b1064b92b7c04 a7f2c50142fe068f12f8fb530559069cf5ae8ce254ef92bfc1530f6162d8be09 f0b9eb4dd3befe3018195f76384bcd4d33e79f520319968b87d7babf40b1d21f 4df3c3f68fcc83b27e9d42c90431a72499f17875c81a599b566c9889b9696703 -1.3412277399322274 FALSE 60s_2x30s
    3b6ca0f6c6d06ea87807b87a6fba612206381c0d96a844f988fc71d1d6e8528c a7f2c50142fe068f12f8fb530559069cf5ae8ce254ef92bfc1530f6162d8be09 f0b9eb4dd3befe3018195f76384bcd4d33e79f520319968b87d7babf40b1d21f 4df3c3f68fcc83b27e9d42c90431a72499f17875c81a599b566c9889b9696703 -2.2384162803080474 FALSE 60s_2x30s
    bb663b5dedca2fac332f3c7aa53155f3e7e038fe02faefbb85d8315616f603cd a7f2c50142fe068f12f8fb530559069cf5ae8ce254ef92bfc1530f6162d8be09 f0b9eb4dd3befe3018195f76384bcd4d33e79f520319968b87d7babf40b1d21f 4df3c3f68fcc83b27e9d42c90431a72499f17875c81a599b566c9889b9696703 -0.22776277505632123 FALSE 60s_2x30s
    8ef620b7e211385969b72d04b9ad7d760cf0f7e5f4b19ad32b85dd046c110f70 a7f2c50142fe068f12f8fb530559069cf5ae8ce254ef92bfc1530f6162d8be09 f0b9eb4dd3befe3018195f76384bcd4d33e79f520319968b87d7babf40b1d21f 4df3c3f68fcc83b27e9d42c90431a72499f17875c81a599b566c9889b9696703 -0.42766955655065264 FALSE 60s_2x30s
    4bb2c3af939742181003c57fc21c06fe2236c06d365963b2c7ceacc3df3e6e0c a7f2c50142fe068f12f8fb530559069cf5ae8ce254ef92bfc1530f6162d8be09 f0b9eb4dd3befe3018195f76384bcd4d33e79f520319968b87d7babf40b1d21f 4df3c3f68fcc83b27e9d42c90431a72499f17875c81a599b566c9889b9696703 -2.838987423178022 FALSE 60s_2x30s

For anonymization the sha256 hash function is used. For most purposes this should be adequaat.

bv2bioplot.py
-------------
Convert a bv results data file to a data file for bioplot.
Example of usage: ::

    python bv2bioplot.py  -i inputfile -o outputfile

sretools2bioplot.py
-------------------
Convert a sretools type input data file to a data file for bioplot.

Sretools consist of utilities witten in R which accept several columns of data.
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
