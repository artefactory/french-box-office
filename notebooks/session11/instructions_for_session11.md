# Prerequisites for course 11 - Model serving


## Github repository

* Install [Git](https://git-scm.com/downloads)

* Open a shell (conda shell if you are on Windows)

* Clone the github repository, and go to the root of the repository:
```bash
git clone git@github.com:artefactory/french-box-office.git
cd french-box-office
```

## IDE
* Install [Visual Studio Code](https://code.visualstudio.com/)
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

## Create a TMDb account

Movie features are extracted via [The Movie Database API](https://developers.themoviedb.org/3/getting-started/introduction). 
Create an account on their website and export your **API key**.

These kind of credentials are considered as "secrets", so you don't want to share it with anyone. NEVER version it or write it down in your code. 
A good practice is to set an environment variable. 

In a terminal shell, run the following command

```bash
export TMDB_API_KEY='your-key-here'
```