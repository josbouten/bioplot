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

The plot types currently supported are: :ref:`rst_accuracy`, :ref:`rst_eerplot`, :ref:`rst_histogram`,
:ref:`rst_matrixplot`, :ref:`rst_rankingplot`, :ref:`rst_tippetplot` and :ref:`rst_zooplot`.

Please read INSTALL.txt, this html documentation (note that the file 'manual.txt' is obsolete) and bioplot.cfg before you try to use
bioplot.py. You'll learn more of the program's potential than from its command line help message.

@Windows dudes and dudettes: I'm afraid you have to run the program by hand from a command line or build shortcuts
which not only start the program but also provide the command line options and parameters needed. You're on your
own here. I'm a command line junky anyway so I did not spend any time building a gui. But don't fret. All plots
ares shown in an interactive window, you can click on that as much as you like. The interface allows you to zoom in,
click on a point to see the associated label, save the plot in a file etc. etc.

Usage
-----

What bioplot.py basically does is: read a data file and plot one or more interactive graphs.
You can run bioplot.py from the command line. The follow command will shows help info for bioplot:
On OSX and linux run: ::

    python bioplot.py -h

On Ms Windows run: ::

    python.exe bioplot.py -h

This wil output the following information: ::

    Usage: ./bioplot.py [options] [option <arg1>] [<label1> <label2> <label3> ...]
    bioplot.py version 0.9.4, Copyright (C) 2014, 2015 Jos Bouten
    bioplot.py comes with ABSOLUTELY NO WARRANTY; for details type `bioplot.py -l'.
    This is free software, and you are welcome to redistribute it
    under certain conditions; type `bioplot.py -l' for details.
    This program was written by Jos Bouten.
    You can contact me via josbouten at gmail dot com.

    Options:
      --version             show program's version number and exit
      -h, --help            show this help message and exit
      -Z, --zoo             show zoo plot
      -A, --accuracy        show accuracy plot
      -E, --eer             show EER plot
      -T, --tippet          show Tippett plot
      -M, --matrix          show matrix plot
      -R, --ranking         show ranking plot
      -C, --histogramc      show cumulative histogram
      -H, --histogram       show histogram
      -k, --kernel          show kernel estimate in histogram
      -e EXPNAME, --exp=EXPNAME
                            name of experiment used in plot title, default = test
      -i FILENAME, --inputfile=FILENAME
                            filename of data file, default = input/testdata_A.txt
      -t DATATYPE, --type=DATATYPE
                            type of data, default = type3, use 'database' if you
                            want to read data from a database.
      -d THRESHOLD, --threshold=THRESHOLD
                            system threshold for ranking plot, default = 0.7
      -c CONFIGFILENAME, --config=CONFIGFILENAME
                            use alternative config file
      -l, --license         show license
      -s, --settings        show settings only
      -q, --quiet           do not show settings
      -V                    show version info


Note: that you can use several options at the same time. The sequence is of no importance.

As you can see you need to choose what type of graph you want.

Bioplot can produce several plots in a row with just one invocation of the program. E.g. if you run: ::

    bioplot -Z -A -E -i some_input_data_file.txt

the program will produce a zoo plot, an accuracy plot and an EER plot one after the other.

The input data has to be in a specific format. Actually there are 2 types of format allowed. See 'Data Files' below.
All plots can be saved. This happens automagically as well, but you get more useful results if this happens under
your control.

If you do not provide an input file, the program uses input/testdata_A.txt.
By providing this default data file it is easy to test whether the program is installed correctly. You can try
the multi experiment capabilities of the program by choosing input/testdata_AB.txt or input/testdata_ABC.txt.

Auto store
----------
The program does a bit more than its command line arguments suggest.
You will notice this when you run it. It will for instance store all the
target and non target scores it distills from the data file you pass
to it and write them in text files (unless you set saveScores to False in bioplot.cfg).
For this to be usefull always add a name for the experiment you were running to the command line.
This name is used in the filenames bioplot produces. ::

    python bioplot.py -Z -e myFirstExperiment

You can use these file for further processing. The experiment name you specify is used as part
of the filename: <exp_name>_<meta_value>_non_target.txt, <exp_name>_<meta_value>_target.txt.
The <meta_value> is taken from the last column of data in the data files.

The files are stored in the directory specified by 'outputPath' in
bioplot.cfg in it's [cfg] section. The default will be 'output' in
the current directory. You can change this behaviour in bioplot.cfg via the following settings: ::

   [cfg]
   outputPath = my_own_data_dir/bioplot/output
   saveScores = True
   alwasySave = False

If you run the program again using the same experiment
name, the scores are not saved again, saving some processing time, unless you add the following setting to the config file: ::

    [cfg]
    alwaysSave = True

The default value is False as it is expected that you will run bioplot several times with the same data (hoping this
will speed things up a bit). Note, that if you do not change the experiment name but do change the data, if alwasySave = False,
the data extracts will not reflect the analysis of the (new) data file used. If you want to have new versions of these files,
you need to delete them before running bioplot.py again.

Next, if you choose to plot a zoo plot, the labels which fall within the doves, chameleons, worms and phantom quartiles
are saved in individual text files: <exp_name>_chameleons.txt, <exp_name>_doves.txt, <exp_name>_phantoms.txt and
<exp_name>_worms.txt. This automatically documents all outliers.

The labels with a standard deviation for their target scores or their non target scores bigger than the unit standard
deviation are stored in a file <exp name>_limited.txt together with the violating score (have a look at the
:ref:`rst_zooplot` page for a general understanding of how the plot is made). The files will show the label name
followed by target/non target designation followed by the std dev for that label.

This example shows the chameleons found for the experiment 'testdata_A' in the file output/testdata_A_chameleons.txt: ::

    # label, metavalue, average_target_score, average_non_target_score, nr_of_target_scores, nr_of_non_target_scores, average_target_score_stdev, average_non_target_score_stdev
    1066 conditionA -0.399073347826 -1.06514522689 23 238 1.985593 0.181852885922
    1096 conditionA -0.3189693125 -1.06838052917 32 240 2.930263 -0.825256532013
    1118 conditionA -0.264748666667 -1.07494067871 30 249 2.395363 -0.733892414191

This example show the standard deviations that were limited to a maximum value of 6 * unit std dev for another experiment: ::

  cat output/condition_A_limited.txt

  1096 target std dev: 6.01978718893
  335 non target std dev: 6.71906032808

Note that you can switch limiting on or off via setting limitStdDevs = False in bioplot.cfg section [zoo].

Save plots
----------
Any plot you produce will be saved to disk as a png-file soon as you click on the plot (to het the window focus) and press a key.
Again the experiment name is used as part of the plot name. Note, it is important to maximise the plot's window to
get a proper layout of all elements in the plot! If you maximise the plot and press 's', you will be presented with a menu which
will allow you to save the plot anywhere you choose to. If you press a different key, the plot will be saved locally in
the directory specified by outputPath. This happens any time you press a key except l, k, g, s, f:

Note: l, k, g, s and f are predefined keys of the gui.
With them you can: ::

  g: toggle grid on / off
  k: toggle between lin horizontal scale and log horizontal scale
  l: toggle between lin vertical scale and log vertical scale
  s: open save menu
  f: toggle between standard size and full screen

Any other key will make that the file is saved in its current dimensions.
To get a nice plot it is wise to maximise and then press any key. Then close the window.

Data files
----------
The command line allows to specify a filename and a type. The default type is 'type3' which corresponds to a text file
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

field 2: string: name of data file containing biometric features or raw data originating from the subject denoted by field 1 used for making a test model. In the example you see a wav-file, but this can be any string identifying a file or feature set.

field 3: string: label identifying a subject (test data).

field 4: string: name of data file containing biometric features or raw data originating from the subject denoted by field 3 used for training the reference model. In the example you see a wav-file, but this can be any string identifying a file or feature set.

field 5: string: floating point value: score of trial.

field 6: boolean: ground truth.

field 7: meta data value for the experiment.

Field 7 can be used to contrast scores of experiments in most plots.
So if you have 2 experiments where you change one variable, when doing a cross
identification test, the meta value can be used to group the experiment's scores.

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

  python ./bioplot.py -i database -t type1 -e 'data taken from db' -Z

You will have to adapt the query in the function _readFromDatabase and the function
_decodeType1Results in data.py to your own needs.

There are several data files (of type3) which are meant as examples to play around
with: input/testdata_A.txt, input/testdata_B.txt, input/testdata_C.txt and input/testdata_ABC.txt

Example: ::

  python ./bioplot.py -e "condition A" -i testdata_A.txt -Z

If you experience any difficulties reading your data file, we can either discuss this
via email or you can send it to me ( josbouten at gmail dot com ) so that I can have a look at it.
Please consider anonimizing the data before you send it to me by mail! Have a look at
anonimize.py and adapt it to your needs.


Bugs and feature requests
-------------------------
If you have any questions or feature requests (no guarantees!) or find any bugs,
you can contact me at josbouten at gmail dot com.