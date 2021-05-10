# Copyright (C) 2020 Artefact
# licence-information@artefact.com

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import scrapy
from typing import Optional
from urllib.parse import urljoin, urlparse, parse_qs


class JpboxSpider(scrapy.Spider):
    name = 'jpbox'
    allowed_domains = ['jpbox-office.com']
    base_url = 'http://jpbox-office.com'
    field_renames = {
        'Premier jour': "first_day_sales", 
        'Premier week-end': "first_weekend_sales", 
        'Première semaine': "first_week_sales", 
        '1ère séance': "first_screening_sales", 
        'Combinaison max.': 'max_theaters_used'
    }

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
        '''
        Parse the french ranking page (ex: http://jpbox-office.com/charts_france.php?view=&filtre=datefr&limite=0&infla=0&variable=2019&tri=champ0&order=DESC&limit5=0)
        '''
        
        # Extract ranked rows
        year = response.meta['year']
        rows = response.xpath('//table[@class="tablesmall tablesmall5"]/tr')

        # Parse rows
        for row in rows:

            # Mind the extra whitespace in tags
            rank = row.xpath('td[@class="col_poster_compteur "]/div/text()').get()
            sales = row.xpath('td[@class="col_poster_contenu_majeur "]/text()').get()
            title = row.xpath('td[@class="col_poster_titre "]/h3/a/text()').get()
            movie_page_url = row.xpath('td[@class="col_poster_titre "]/h3/a/@href').get()

            if rank and title and sales and movie_page_url:

                self.log(f'Found a new movie!')

                # Extract further information from movie url
                movie_page_url = urljoin(self.base_url, '/'+movie_page_url) # Adding a custom sep before join
                jpbox_id = self.extract_data_from_url(movie_page_url, 'id')
                movie_card = {
                    'year': year,
                    'rank': rank.strip(),
                    'title': title.strip(),
                    'total_sales': self.parse_number(sales.strip()),
                    'id': jpbox_id
                }

                # If the movie has its own webpage, go extract further info, else return
                if movie_page_url:
                    yield scrapy.Request(
                        url=movie_page_url, 
                        callback=self.parse_movie_page, 
                        meta={'movie_card': movie_card})
                else:
                    yield movie_card

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

    def extract_data_from_url(self, url: str, field: str) -> str:
        '''
        Extract data which is embeded into an url with an associated field, 
        e.g.: 
            http://jpbox-office.com/v9_avenir.php?fixe=1&view=2&date=2019-07-17 

        Parameters
        ----------
        url: str
            The url
        field: str
            A field embeded into the url (date, id, ...)

        Returns
        -------
        extracted_data: str
            the first element associated with field
        '''
        parsed = urlparse(url)
        data = parse_qs(parsed.query)[field]
        if len(data)>0:
            return data[0]

    def parse_number(self, number_as_str: str) -> Optional[int]:
        '''
        Try to cast a french int stored as string into int

        Parameters
        ----------
        number_as_str: str
            Value you'd like to cast into Int

        Returns
        -------
        value: Optional[int]
            Int if cast was successful
        '''
        value = number_as_str.replace(' ', '')
        try:
            value = int(value)
        except ValueError:
            value = None
        return value

    def parse_movie_page(self, response):
        '''
        Parse a movie card page (ex: http://jpbox-office.com/fichfilm.php?id=17528&view=2)
        '''

        # Extract ranked rows
        movie_card = response.meta['movie_card']

        # Date of release
        link_with_release_date = response.xpath('//div[@class="bloc_infos_center tablesmall1b"]/p/a/@href').get()
        release_date_url = urljoin(self.base_url, '/'+link_with_release_date) # Adding a custom sep before join
        movie_card['release_date'] = self.extract_data_from_url(release_date_url, 'date')

        # Sales
        rows = response.xpath('//table[@class="tablesmall tablesmall2"]/tr')
        for row in rows:

            # Decompose rows
            field = row.xpath('td[@class="col_poster_titre"]//text()').get()
            value = row.xpath('td[@class="col_poster_contenu_majeur"]/text()').get()

            # Add to results
            if field in self.field_renames.keys():
                
                # Clean value and try casting it as int
                value = self.parse_number(value)

                # Save result
                movie_card[self.field_renames[field]] = value

        yield movie_card