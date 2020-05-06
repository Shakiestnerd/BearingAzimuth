===========================
Bearing / Azimuth Converter
===========================


.. image:: https://readthedocs.org/projects/bearing/badge/?version=latest
        :target: https://bearingazimuth.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

Simple application to convert between bearings and azimuth.  This application
came about when I found my simple CAD program did not accept bearings as input.
So, the best choice was to build a little converter so that values could be copied
to the clipboard and pasted into the CAD program.

* Free software: MIT license
* Documentation: https://bearingazimuth.readthedocs.io/en/latest/
* Github Repository: https://github.com/Shakiestnerd/BearingAzimuth


Features
--------

* Enter a bearing in the form N 45° 30' 00" E and have it converted to an azimuth (angle from north).
* Enter the azimuth angle and have the bearing automatically calculated.
* Copy the results to the clipboard
* Draw a sample angle on screen.
* User interface created with PySimpleGui

.. image:: _static/main.gif
        :align: center
        :alt: Bearing Screen

Credits
-------

Used the Anaconda distribution for development.

PySimpleGui is the name of my virtual environment.

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
