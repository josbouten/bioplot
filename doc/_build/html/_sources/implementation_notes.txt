Implementation notes
====================

histogram.py
------------

When drawing a histogram lots of warnings like this one may be seen on the screen: ::

    /usr/lib/pymodules/python2.7/matplotlib/cbook.py:1711: DeprecationWarning: using a non-integer number instead of an
    integer will result in an error in the future
    result = np.zeros(new_shape, a.dtype)

To suppress warnings like this a filter was added in histogram.py to filter out this specific warning using: ::

    import warnings
    warnings.filterwarnings("ignore", category=DeprecationWarning)

cllr.py
-------

When computing minimum Cllr values warnings are suppressed when computing log values. ::

    # disable runtime warnings for a short time since log(0) will raise a warning.
    old_warn_setup = np.seterr(divide='ignore')

The minCllr function computes the 'minimum cost of log likelihood ratio' measure as given in IDIAP's BOB code "measure/calibration.py".
Have a look here http://idiap.github.io/bob/ and at this: ::

    @inproceedings{bob2012, author = {A. Anjos AND L. El Shafey AND R. Wallace AND M. G\\"unther AND C. McCool AND S. Marcel}, title = {Bob: a free signal processing and machine learning toolbox for researchers}, year = {2012}, month = oct, booktitle = {20th ACM Conference on Multimedia Systems (ACMMM), Nara, Japan}, publisher = {ACM Press}, url = {http://publications.idiap.ch/downloads/papers/2012/Anjos_Bob_ACMMM12.pdf},}

However no use is made of BOB's pavx function as it would require linking c++ code. Instead sklearn's isotonic
regression function is used which is equivalent.


documentation
-------------

The man pages and html documentation was made using sphinx v1.3.1 combined with the bootstrap theme,
see https://github.com/ryan-roemer/sphinx-bootstrap-theme. You can find them in the bioplot directory under
doc/_build/man/bioplot.1 and doc/_build/html/index.html.