# Prerequisites for course 10 - Model serving


## Github repository

* Install [Git](https://git-scm.com/downloads)

* Open a shell (conda Prompt if you are on Windows, Terminal if you are on Mac)

* Clone the github repository, and go to the root of the repository:
```bash
git clone https://github.com/artefactory/french-box-office.git
cd french-box-office
```

## IDE
* Install an IDE, such as [Visual Studio Code](https://code.visualstudio.com/) (recommended) or PyCharm.
* Open it and open the folder of the repository (french-box-office)


## Create a virtual environment and download dependencies
* Make sure you installed Python with [Anaconda](https://www.anaconda.com/) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html)

* Open a shell (conda shell if you are on Windows)
* Create a new conda virtual environment

To do so, you have 2 alternatives:

**A - from the `environment.yml` file**
```bash
conda env create -f environment.yml -n french_box_office
```
It will install the packages. If it doesn't work, you can try manually with pip

**B - With pip *-not recommended-***
```bash
conda create --name french_box_office python=3.7 --no-default-packages
conda activate french_box_office
pip install -r requirements.txt
```

## Add this virtual environment to Jupyter kernels

```
conda activate french_box_office
conda install ipykernel
python -m ipykernel install --user --name=french_box_office_env
```
Now you can run ```jupyter notebook``` and the change kernel in `Menu > kernel > Change Kernel > french_box_office_env`

## Add the path of the repository to PYTHONPATH

Via conda, replace `[c:/replace/by/absolute/path/to/french-box-office]` by the absolute path to the repository. 
Should work for Mac or Windows if you have conda:
```bash
conda activate french_box_office
conda env config vars set PYTHONPATH="[c:/replace/by/absolute/path/to/french-box-office]:$PYTHONPATH"
```

Via Windows, check [this stackoverflow issue](https://stackoverflow.com/questions/7472436/add-a-directory-to-python-sys-path-so-that-its-included-each-time-i-use-python).

## Add the data and the model to the repository

* Create a folder `data` at the root of the repository, and copy-paste the data inside.

* Create a folder `models` if it doesn't already exist and copy-paste the .txt of the model inside.


## Create a TMDb account

Movie features are extracted via [The Movie Database API](https://developers.themoviedb.org/3/getting-started/introduction). 
Create an account on their website and export your **API key**.

These kind of credentials are considered as "secrets", so you don't want to share it with anyone. NEVER version it or write it down in your code. 
A good practice is to set an environment variable. 

In a terminal shell, run the following command

if you are on Windows:
```bash
set TMDB_API_KEY='your-key-here'
```

If you are on MacOS / linux
```bash
export TMDB_API_KEY='your-key-here'
```

Also, create a new file named `.env` at the root of the repository and write:
```bash
TMDB_API_KEY='your-key-here'
```