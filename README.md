# french-box-office

Predicting French movies success

## Install and Set up

Set-up once and for all a dedicated conda environment:

```bash
conda create -y -n french_box_office python=3.7
conda activate french_box_office
```

Install then the requirements:

```bash
pip install -r requirements.txt
```


## Usage

### Crawling

French box-office statistics are gently crawled from the website [jpbox-office](http://jpbox-office.com) using [`scrapy`](https://scrapy.org/). You can refresh this data by typing the following commands:

```bash
cd lib/crawling/boxoffice
scrapy crawl jpbox -a start_year=2000 -a end_year=2020 -o ../../../data/french-box-office-23nov2020.json
```
