import scrapy
import uuid
from urllib.parse import urljoin


class JpboxSpider(scrapy.Spider):
    name = 'jpbox'
    allowed_domains = ['jpbox-office.com']
    base_url = 'http://jpbox-office.com'

    def __init__(self, start_year:int=2015, end_year:int=2020, **kwargs):
        self.start_year = int(start_year)
        self.end_year = int(end_year)
        super().__init__(**kwargs)

    def start_requests(self):

        # Compute years range
        years = range(self.start_year, self.end_year+1)

        # Crawl for each one
        for year in years:
            self.log(f'Getting data for year {year}...')
            start_url = f'http://jpbox-office.com/charts_france.php?view=&filtre=datefr&limite=0&infla=0&variable={year}&tri=champ0&order=DESC&limit5=0'
            yield scrapy.Request(url=start_url, callback=self.parse, meta={'year': year})

    def parse(self, response):
        
        # Extract ranked rows
        year = response.meta['year']
        rows = response.xpath('//table[@class="tablesmall tablesmall5"]/tr')

        # Parse rows
        for row in rows:

            # Mind the extra whitespace in tags
            rank = row.xpath('td[@class="col_poster_compteur "]/div/text()').get()
            title = row.xpath('td[@class="col_poster_titre "]/h3/a/text()').get()
            sales = row.xpath('td[@class="col_poster_contenu_majeur "]/text()').get()

            if rank and title and sales:
                self.log(f'Found a new movie!')
                yield {
                    'id': str(uuid.uuid4()),
                    'year': year,
                    'rank': rank.strip(),
                    'title': title.strip(),
                    'sales': sales.strip()
                }

        # Get pagination choices at the page bottom 
        pagination_options = response.xpath('//div[@class="pagination"]/a')

        for option in pagination_options:
            # Get text and hyperlink
            text = option.xpath('text()').get()
            hyperlink = option.xpath('@href').get()

            # If has next page
            if text == '>': 

                # Go to next page
                self.log(f'Going to next page...')
                next_page = urljoin(self.base_url, hyperlink)
                yield scrapy.Request(next_page, callback=self.parse, meta={'year': year})

