import pandas as pd
import numpy as np
import os.path
import requests
import io
from requests import get
from bs4 import BeautifulSoup
from time import sleep
from random import randint
from time import time
from warnings import warn 
warn("Warning Simulation")
from IPython.core.display import clear_output

def acquire_imdb():
    '''
    Checks if csv exists; if yes, reads csv. If no, reads url
    scrapes data from imdb into a list, converts list into a dataframe,
    and writes to csv. Returns dataframe.
    '''
    if os.path.isfile('movie_ratings.csv'):
        movies = pd.read_csv('movie_ratings.csv')
    else:
        # empty lists that we will convert to a df @ the end
        names = []
        years = []
        imdb_ratings = []
        metascores = []
        votes = []

        # Preparing the monitoring of the loop
        start_time = time()
        requests = 0

        # setting up the url's we want to scrape
        pages = [str(i) for i in range(1,5)]
        years_url = [str(i) for i in range(2000,2020)]


        # For every year in the interval 2000-2020
        for year_url in years_url:
    
            # For every page in the interval 1-4
            for page in pages:
        
                # make a get request
                response = get('https://www.imdb.com/search/title/?release_date=' + year_url 
                + '&sort=num_votes,desc&page=' + page)
        
                # Pause the loop
                sleep(randint(8,15))
        
              # Monitor the requests
                requests += 1
                sleep(randint(1,3))
                current_time = time()
                elapsed_time = current_time - start_time
                print('Request: {}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
                clear_output(wait = True)
        
                # Throw a warning for non-200 status codes
                if response.status_code != 200:
                    warn("Number of requests was greater than expected.")
                    break
            
                # Parse the content of the request with Beautiful Soup
                page_html = BeautifulSoup(response.text, 'html.parser')
        
                # Select all 50 movie containers from a single parse
                mv_containers = page_html.find_all('div', class_ = 'lister-item mode-advanced')
        
                # For every movie of these 50
                for container in mv_containers:
                    # If movie has a metascore, then
                    if container.find('div', class_ = 'ratings-metascore') is not None:
                
                        # Scrape the name
                        name = container.h3.a.text
                        names.append(name)
                
                        # Scrape the year
                        year = container.h3.find('span', class_ = 'lister-item-year').text
                        years.append(year)
                
                        # Scrape the IMDB rating
                        imdb = float(container.strong.text)
                        imdb_ratings.append(imdb)
                
                        # Scrape the metascore
                        meta = container.find('span', class_ = 'metascore').text
                        metascores.append(int(meta))
                
                        # Scrape the number of votes from IMDB
                        vote = container.find('span', attrs = {'name':'nv'})['data-value']
                        votes.append(int(vote))
        
        movies = pd.DataFrame({
            'movie':names,
            'year':years,
            'imdb_rating':imdb_ratings,
            'metascore':metascores,
            'votes':votes})
        movies.loc[:, 'year'] = movies['year'].str[-5:-1].astype(int)   
        # importing to csv
        movies.to_csv('movie_ratings.csv')        
        return movies
