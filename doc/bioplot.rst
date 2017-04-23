Introduction to Bioplot
=======================

You will not be able to use this program or any of its parts to slay a dragon, that I'm sure of, and I do not guarantee
that it is fit for any other purpose at all, but I would appreciate if you would include a reference to this code and my name
in any publications you may write using its features or add a source reference to your code if you include some part(s)
of this code in yours. Especially if you plan to use part of the code please respect the :ref:`rst_license`.

bioplot.py is a program which can draw several plots that can be used
when evaluating the performance of a biometric system. It reads settings from the file 'bioplot.cfg'.
But using the -c option you can specify your own settings file (see :ref:`rst_settings`).
These settings may be used to determine the way information is shown in a plot, what directory plot files
are written to etc.

The plot types currently supported are: :ref:`rst_accuracy`, :ref:`rst_detplot`, :ref:`rst_eerplot`, :ref:`rst_histogram`,
:ref:`rst_matrixplot`, :ref:`rst_rankingplot`, :ref:`rst_rocplot`, :ref:`rst_tippetplot` and :ref:`rst_zooplot`.

Please read INSTALL.txt, this html documentation (note that the file 'manual.txt' is obsolete) and bioplot.cfg before you try to use
bioplot.py. You'll learn more of the program's potential than from its command line help message.

@Windows dudes and dudettes: I'm afraid you have to run the program by hand from a command line or build shortcuts
which not only start the program but also provide the command line options and parameters needed. You're on your
own here. I'm a linux/OSX command line junky anyway so I did not spend any time building a (windows) gui. But don't fret. All plots
are shown in an interactive window, you can click on that as much as you like. The interface allows you to zoom in,
click on a point to see the associated label, save the plot in a file etc. etc.

Usage
-----

What bioplot.py basically does is: read a data file and plot one or more interactive graphs.
You can run bioplot.py from the command line. The follow command will show help info for bioplot:
On OSX and linux run: ::

    python bioplot.py -h

On Ms Windows run: ::

    python.exe bioplot.py -h

This wil output the following information: ::

    usage: bioplot.py [-h] [-Z] [-A] [-D] [-E] [-T] [-M] [-O] [-R] [-C] [-H] [-k]
                      [-L LABELS [LABELS ...]] [-e EXPNAME]
                      [-i FILENAMES [FILENAMES ...]] [-t DATATYPE] [-d THRESHOLD]
                      [-c CONFIGFILENAME] [-l] [-s] [-q]

    bioplot.py [plot type] [<label1> <label2> <label3> ...] bioplot.py version
    This is bioplot.py version 1.2, Copyright (C) 2014: Jos Bouten
    This program comes with ABSOLUTELY NO WARRANTY; for details run
    `bioplot.py -l'. This is free software, and you are welcome to redistribute it
    under certain conditions; type `bioplot.py -l' for details. This program was
    written by Jos Bouten. You can contact me via josbouten at gmail dot com.

    optional arguments:
      -h, --help            show this help message and exit
      -Z, --zoo             show zoo plot
      -A, --accuracy        show accuracy plot
      -D, --det             show Det plot
      -E, --eer             show EER plot
      -T, --tippet          show Tippett plot
      -M, --matrix          show matrix plot
      -O, --roc             show roc plot
      -R, --ranking         show ranking plot
      -C, --histogramc      show cumulative histogram
      -H, --histogram       show histogram
      -k, --kernel          show kernel estimate in histogram
      -L LABELS [LABELS ...], --label LABELS [LABELS ...]
                            add labels to plot
      -e EXPNAME, --exp EXPNAME
                            name of experiment used in plot title, default = test
      -i FILENAMES [FILENAMES ...], --inputfile FILENAMES [FILENAMES ...]
                            filename of filenames of data file(s) or name of
                            database, default = input/testdata_A.txt
      -t DATATYPE, --type DATATYPE
                            type of data, default = type3, use 'database' if you
                            want to read data from a database.
      -d THRESHOLD, --threshold THRESHOLD
                            system threshold for ranking plot, default = 0.7
      -c CONFIGFILENAME, --config CONFIGFILENAME
                            use alternative config file
      -l, --license         show license
      -s, --settings        show settings only
      -q, --quiet           do not show settings

Note:
 - that you can use several options at the same time. The sequence is of no importance.
 - each time in this documentation you read 'python' as part of a command then on a windows platform use 'python.exe' (without the quotes).
 - On OSX and linux you need not specify the python interpreter at all. bioplot.py can be run using: ./bioplot.py

As you can tell from the list of options you need to choose what type of graph you want.
Bioplot can produce several plots in a row with just one invocation of the program. E.g. if you run: ::

    python bioplot.py -Z -A -E -i some_input_data_file.txt yet_another_input_file.txt

the program will produce a zoo plot, an accuracy plot and an EER plot one after the other.

The input data has to be in a specific format. Actually there are 2 types of format allowed. See :ref:`rst_data_files` below.
All plots can be saved. This happens automagically as well, as soon as you click on a plot and press a key, but depending
on the screen size you get more useful results if this happens under your control.

If you do not provide an input file, the program uses input/testdata_A.txt.
This makes it is easy to try the program. You can try the multi experiment capabilities
of the program by choosing input/testdata_AB.txt or input/testdata_ABC.txt.

Bioplot when run reads its config file (by default called 'bioplot.cfg') and uses the settings it finds in there.
If no config file exists it uses a set of default values. Have a look at the config file. The program has quite a lot
of settings you may want set to your own liking.

Auto store
----------
The program does a bit more than its command line arguments suggest.
You will notice this when you run it. It will for instance store all the
target and non target scores it distills from the data file you pass
to it and write them in text files (unless you set saveScores to False in bioplot.cfg).
For this to be usefull always add a name for the experiment you were running to the command line,
otherwise the prefix 'test' is used.

The experiment name is used in the titles of the plots and in the filenames bioplot produces. ::

    python bioplot.py -Z -e myFirstExperiment

You can use these file for further processing. The experiment name you specify is used as part
of the filename: <exp_name>_<meta_value>_non_target.txt, <exp_name>_<meta_value>_target.txt.
The <meta_value> is taken from the last column of data in the data files: ::

    myFirstExperiment_conditionA_target.txt
    myFirstExperiment_conditionA_non_target.txt

The files are stored in the directory specified by 'outputPath' in
bioplot.cfg in it's [cfg] section. The default path will be 'output' in
the current directory. You can change this behaviour in bioplot.cfg via the following settings: ::

   [cfg]
   outputPath = output
   saveScores = True
   alwasySave = False

If the output path does not exist, bioplot will try to create it. Note: this may require privileges to be set propperly.
If you run the program repeatedly using the same experiment name, the scores are not saved again, saving some processing
time, unless you add the following setting to the config file: ::

    [cfg]
    alwaysSave = True

The default value is False as it is expected that you will run bioplot several times with the same data (hoping this
will speed things up a bit). Note, that if you do not change the experiment name but do change the data, if alwaysSave = False,
the data extracted will not reflect the analysis of the (new) data file used. If you want to have new versions of these files,
you need to delete them before running bioplot.py again (or set alwaysSave to True).

If you choose to plot a zoo plot, the labels which fall within the doves, chameleons, worms and phantom quartiles
are saved in individual text files: <exp_name>_chameleons.txt, <exp_name>_doves.txt, <exp_name>_phantoms.txt and
<exp_name>_worms.txt. This automatically documents all outliers. ::

    myFirstExperiment_chameleons.txt
    myFirstExperiment_doves.txt
    myFirstExperiment_phantoms.txt
    myFirstExperiment_worms.txt

The content of output/myFirstExperiment_chameleons.txt looks like this: ::

    # label, metavalue, average_target_score, average_non_target_score, nr_of_target_scores, nr_of_non_target_scores, average_target_score_stdev, average_non_target_score_stdev
    116 conditionB -0.563504928571 -1.07438894059 14 202 -0.502857 1.25531696972
    1118 conditionA -0.264748666667 -1.07494067871 30 249 2.000000 -0.733892414191
    226 conditionB -0.555475 -1.06827121759 1 216 0.010000 -0.717001903115
    1066 conditionA -0.399073347826 -1.06514522689 23 238 1.985593 0.181852885922
    1066 conditionB -0.205634 -1.07308166403 12 253 2.000000 0.234369371589
    3146 conditionB -0.542155 -1.07573414493 2 207 -0.588718 -0.808330988919
    1096 conditionB -0.47514326087 -1.06535841905 23 210 2.000000 -0.964818041437
    1096 conditionA -0.3189693125 -1.06838052917 32 240 2.000000 -0.825256532013

The labels with a normalized standard deviation for their target scores or their non target scores bigger than a maximum standard
deviation are stored in a file <exp name>_limited.txt together with the violating score (have a look at the
:ref:`rst_zooplot` page for a general understanding of how the plot is made).

Assuming these settings: ::

    [zoo]
    limitStdDevs = True
    maxStdDev = 2.0
    minStdDev = 0.01

the following command will produce the file 'myFirstExperiment_limited.txt' where the standard deviations are limited to a maximum value of 2 * unit std dev: ::

    python bioplot.py -Z -i input/testdata_AB.txt -e myFirstExperiment


This will result into the following content in output/myFirstExperiment_limited.txt (shown partially): ::

    # label, metavalue, average_target_score, average_non_target_score, nr_of_target_scores, nr_of_non_target_scores, average_target_score_stdev, average_non_target_score_stdev
    223 conditionA -0.6239485 -1.0987091784 2 213 -0.294772 2.0
    1129 conditionB -0.481959666667 -1.09234021145 12 227 2.000000 -0.487198065101
    57 conditionB -1.08974608333 -1.07881886634 12 202 -0.719556 -2.0
    609 conditionB -0.614352277778 -1.07410090099 18 202 -0.482100 2.0
    1130 conditionB -0.0728461428571 -1.11323731633 21 196 2.000000 0.0208211034315
    223 conditionB -0.59144 -1.14699159184 1 196 0.010000 2.0
    1112 conditionA -0.416871 -1.103248548 34 250 2.000000 1.17620375038
    1116 conditionA -0.4189825625 -1.1624667598 32 204 1.920131 2.0
    335 conditionA -0.3849315 -1.15242778855 2 227 -0.545516 2.0
    1123 conditionB -0.323721045455 -1.07929185124 22 242 2.000000 -0.212778963187
    1115 conditionA -0.491315227273 -1.14706272124 22 226 2.000000 1.42789578734
    1131 conditionA -0.3203315 -1.09662913636 34 220 2.000000 0.0194105127029

Note that the default setting for maxStdDev = 6.0 * unit std dev.

Save plots
----------
Any plot you produce will be saved to disk as a png-file in the output directory as soon as you click on the plot
(to get the window focus) and press a key. The experiment name is used as part of the plot name. Note, it is important to maximise the plot's window to
get a proper layout of all elements in the plot! If you press 's', you will be presented with a menu which
will allow you to save the plot anywhere you choose to. If you press a different key, the plot will be saved locally in
the directory specified by outputPath. This happens any time you press a key!

Note: the keys l, k, g, s and f are predefined keys of the gui. They provide additional functions.
With them you can: ::

  g: toggle grid on / off
  k: toggle between linear horizontal scale and logaritmic horizontal scale
  l: toggle between linear vertical scale and logaritmic vertical scale
  s: open save menu
  f: toggle between standard size and full screen

Any key will make that the file is saved in its window's dimensions.
To get a nice plot it is wise to maximise the window and then press a key. Then close the window.

Note that using l and k may lead to warnings if e.g. the scores contain negative values (the log is only defined for numbers >= 0).

.. _rst_data_files:

Data files
----------
The command line allows to specify a filename or a list of filenames and a type. The default type is 'type3' which corresponds to a text file
with 7 fields. You need not specify type3 as it is a default. This data type allows you to specify scores of
experiments where multiple files are used to make a model whether this is a training model or a test model.
Note, if you do not provide an input file, the program uses input/testdata_A.txt.

The data file should contain data in a format like this example: ::

    803742 17133729a.wav 803593 16842970b.wav 2.108616847991943 FALSE META_VAL1
    148407 47968376b.wav 898232 08087650a.wav 0.336018745422363 FALSE META_VAL3
    179408 34192626a.wav 803721 16749939b.wav 1.263523664188385 FALSE META_VAL2
    803442 48588750a.wav 803442 15560933b.wav 4.423274517059326 TRUE  META_VAL2

Separation by comma's is also accepted.
This can be mixed as in: ::

    803742,17133729a.wav,803593,16842970b.wav,2.108616847991943,FALSE,META_VAL1
    148407,47968376b.wav,898232,08087650a.wav,0.336018745422363,FALSE,META_VAL3
    179408 34192626a.wav 803721 16749939b.wav 1.263523664188385 FALSE META_VAL2
    803442,48588750a.wav,803442,15560933b.wav,4.423274517059326,TRUE, META_VAL2

field 1: string: label identifying a subject (training data).

field 2: string: name of data file containing biometric features or raw data originating from the subject denoted by field 1 used for making a test/evaluation model. In the example you see a wav-file, but this can be any string identifying a file or feature set.

field 3: string: label identifying a subject (test/evaluation data).

field 4: string: name of data file containing biometric features or raw data originating from the subject denoted by field 3 used for training the reference model. In the example you see a wav-file, but this can be any string identifying a file or feature set.

field 5: string: floating point value: score of trial.

field 6: boolean: ground truth.

field 7: meta data value for the experiment.

Field 7 can be used to contrast scores of experiments in most plots.
So if you have 2 experiments where you change one variable, when doing a cross
identification test, the meta value can be used to group the experiment's scores.

Let's have a look at an example data line: ::

    803742 17133729a.wav 803593 16842970b.wav 2.108616847991943 FALSE META_VAL1

This line describes the result of a speaker verification experiment in which was used: ::
 
 - as training audio samples from the file 17133729a.wav
 - the label 803742 to identify the speaker in the training audio
 - the label 803593 to identify the speaker in the test/evaluation/disputed utterance
 - as evaluation audio samples from the file 16842970b.wav
 - the tag FALSE to denote that the training speaker is not the test/eval speaker
 - META_VAL1 as a label to identify the conditions of the experiment (e.g. this is an experiment 
   with training duration X seconds and test duration Y seconds, you may have various 
   variables and use other meta labels to identify those).

The result of the verification experiment was a score of 2.108616847991943.

If you have done experiments where the training model was made from several audio files, then
in field 4 use some symbolic name.

Note: bioplot.py uses the filenames in the data file only as symbols, the sample data in 
the files is not used in any way.

E.g. you run an experiment with gender as the main variable and you collect scores of male
to male and female to female comparisons. You need to set the meta value for each score
accordingly. The meta value field allows bioplot to distinguish
between the two conditions and it will in essence plot 2 plots in one overview.
If the same label occurs on more than one occasion in the score list with different meta
values, then the points in a zoo plot with corresponding labels are interconnected
(see interconnectMetaValues setting in bioplot.cfg under [zoo]) . This makes it easy
to see what the effect of an individual label is when changing the experiment's condition.

Field 7 must be present. If you don't want to contrast experiments, then give all lines
the same meta value. Any string of characters (excluding white space) will do except
the special characters mentioned below under 'Known Issues'.

File type 'type2' is deprecated as of august 2015.

File 'type1' is a database based data format and meant as an example on how to use bioplot in combination with a
database of scores. Specify 'database' as filename on the command line.

Example: ::

  python bioplot.py -i database -t type1 -e 'data taken from db' -Z

You will have to adapt the query in the function _readFromDatabase and the function
_decodeType1Results in data.py to your own needs.

There are several data files (of type3) which are meant as examples to play around
with: input/testdata_A.txt, input/testdata_B.txt, input/testdata_C.txt and input/testdata_ABC.txt

Example: ::

  python bioplot.py -e "condition A" -i input/testdata_A.txt -Z 
  python bioplot.py -e "condition A and B" -i input/testdata_A.txt input/testdata_B.txt -Z


If you experience any difficulties reading your data file, we can either discuss this
via email or you can send the data it to me ( josbouten at gmail dot com ) so that I can have a look at it.
Please consider anonymizing the data before you send it to me by mail! Have a look at
:ref:`rst_anonymize`.

Note: bioplot.py does not allow as input data a text file and a database at the same time.

Data exchange
-------------
bioplot formatted text files from linux, OSX and MS Windows platforms should be interchangeable without problems.

Data anonymity
--------------
If you want to anonymize your data e.g. in case you want to exchange data file with somebody, have a look at :ref:`rst_anonymize`.

Bugs and feature requests
-------------------------
If you have any questions or feature requests (no guarantees!) or find any bugs,
you can contact me at josbouten at gmail dot com.
