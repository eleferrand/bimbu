# bimbu
This is the main scripts for Syllables spotting
# Installation
After having cloned the project run:

```bash
make install
```
This will download and install allosaurus which is the main tool used for terms spotting and download the model in Kunwinjku

# On Windows
Python 3.6 is needed
Install pip. pip is used to install python librairies
then you can install the main dependencies:
```bash
py -m pip install praatio
py -mpip install pydub
py -m pip install auditok
```
After that you need to clone Allosaurus project:
```bash
git clone https://github.com/xinjli/allosaurus.git
```
Once done, before the proper installation, go on allosaurus/allosaurus/bin/download_model.py and replace on line 20 the content of url variable by https://github.com/eleferrand/bimbu/blob/main/big_kun.tar.gz
you can then go on the main allosaurus folder and run
```bash
python setup.py install
```
and run the following command to unpack the model
```bash
python -m allosaurus.bin.download_model
```
To generate the syllable for a given audio file, run
```bash
python transcribe.py <path to your audio>
```
this will generate a json file with inside the syllable spotted for the given audio file
If the audio is two long, it will automatically be broken down into smaller units into the folder splits
