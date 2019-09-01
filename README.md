# DolfinInterpreter
Build off KineticAnalysis, Tech Dev's most utilized project for automated data reporting of assay devlopment
  * GUI interface layer at DolfinReading.py
  * CLI interface layer at dolfin_handler_cli.py
  * UI definition at DolfinInterpreter.ui
  * dolfinParser Class layer for parsing dolfin results file
  * graphicalInterpretation Class layer for graphing results
  * Function Layer not necessary for Object Oriented Programming in KineticAssayTools

# Requirements
* Verbose error logging on GUI
* Automated GUI identification of labels, reducing the need to go into files themselves
* User can name labels whatever they want
* User can name files whatever they want in whatever location they prefer
* User can analyze this at their desk and on their own computer easily
* User downloads file from FINDER Manager and analyzes at their desk
* Minimal IT help needed due to stable releases
* Tested at every layer in batch scripts and python assert testing

# Key Differentiation from Kinetic Reading
  * GUI layer inputs simplified because of single input file
  * Input file is a dolfin csv output
  

## Versioning
Versions are tagged in git using the "Semantic Versioning 2.0" standard beginning with 0.1.0.
For details, please refer to: [http://semver.org/spec/v2.0.0.html](http://semver.org/spec/v2.0.0.html)

Version is manually updated using a text source file, but also provided automatically at build time by git itself, using it's `git describe` command.

## Summary
A version is of the form MAJOR.MINOR.PATCH, where each gets incremented for the following:

 * MAJOR, for incompatible API changes
 * MINOR, for functionality added in a backwards-compatible manner
 * PATCH, for backwards-compatible bug fixes

 The MAJOR patch will be zero for initial dev.

## Branching Model
Development is intended to follow the Git Flow branching model.

For details, please refer to: [http://nvie.com/posts/a-successful-git-branching-model/](http://nvie.com/posts/a-successful-git-branching-model/)

In summary, development takes place in feature branches (named anything except master, develop, release-\*, or hotfix-\*), then moved into release branches (release-\*), then tagged when released, and merged back into development and master branches.  For our purposes, build artifacts (elf, bin, hex, map files) are included in the release branches so that the build output is available once tagged.

## Install Anaconda 5.2.0 (64 bit), python 2.7.14
https://www.anaconda.com/download/
backports-functools-lru-cache 1.5                   pypi_0    pypi
backports_abc             0.5                        py_0
blas                      1.0                         mkl
bokeh                     0.13.0                   py27_0
ca-certificates           2019.1.23                     0
certifi                   2019.3.9                 py27_0
cycler                    0.10.0                   pypi_0    pypi
freetype                  2.9.1                h4d385ea_1
futures                   3.2.0                    py27_0
icc_rt                    2019.0.0             h0cc432a_1
icu                       58.2                 h2aa20d9_1
intel-openmp              2019.3                      203
jinja2                    2.10.1                   py27_0
jpeg                      9b                   ha175dff_2
kiwisolver                1.1.0                    pypi_0    pypi
libpng                    1.6.37               h7a46e7a_0
libtiff                   4.0.10               h1c3b264_2
logging                   0.4.9.6                  pypi_0    pypi
markupsafe                1.1.1            py27h0c8e037_0
matplotlib                2.2.4                    pypi_0    pypi
mkl                       2019.3                      203
mkl_fft                   1.0.12           py27h44c1dab_0
numpy                     1.16.3           py27h5fc8d92_0
numpy-base                1.16.3           py27hb1d0314_0
olefile                   0.46                     py27_0
openssl                   1.0.2r               h0c8e037_0
packaging                 19.0                     py27_0
pandas                    0.24.2                   pypi_0    pypi
pillow                    6.0.0                    pypi_0    pypi
pip                       19.1.1                   py27_0
pyparsing                 2.4.0                      py_0
pyqt                      5.6.0            py27h6e61f57_6
python                    2.7.16               hcb6e200_0
python-dateutil           2.8.0                    py27_0
pytz                      2019.1                   pypi_0    pypi
pyyaml                    5.1              py27h0c8e037_0
qt                        5.6.2            vc9hc26998b_12
scikit-learn              0.20.3                   pypi_0    pypi
scipy                     1.2.1                    pypi_0    pypi
selenium                  3.141.0                  pypi_0    pypi
setuptools                41.0.1                   py27_0
singledispatch            3.4.0.3          py27h3f9d112_0
sip                       4.18.1           py27hc56fc5f_2
six                       1.12.0                   py27_0
sklearn                   0.0                      pypi_0    pypi
sqlite                    3.28.0               h0c8e037_0
tk                        8.6.8                h0c8e037_0
tornado                   5.1.1            py27h0c8e037_0
urllib3                   1.25.3                   pypi_0    pypi
vc                        9                    h7299396_1
vs2008_runtime            9.00.30729.1         hfaea7d5_1
wheel                     0.33.4                   py27_0
wincertstore              0.2              py27hf04cefb_0
xlsxwriter                1.1.8                    pypi_0    pypi
xz                        5.2.4                h3cc03e0_4
yaml                      0.1.7                h3e6d941_2
zlib                      1.2.11               h3cc03e0_3
zstd                      1.3.7                h1b0e4d7_0