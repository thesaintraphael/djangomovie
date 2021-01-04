import random
import requests
from bs4 import BeautifulSoup

# crawl IMDB Top 250 and randomly select a movie


def generate_movie():

    url = 'http://www.imdb.com/chart/top'
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    #   soup = BeautifulSoup(response.text, 'lxml') # faster

    # print(soup.prettify())

    movie_tags = soup.select('td.titleColumn')
    inner_movie_tags = soup.select('td.titleColumn a')
    rating_tags = soup.select('td.posterColumn span[name=ir]')
    img_tags = soup.find_all('img')

    def get_year(movie_tag):
        movie_split = movie_tag.text.split()
        year = movie_split[-1]  # last item
        return year

    years = [get_year(tag) for tag in movie_tags]
    actors_list = [tag['title'] for tag in inner_movie_tags]     # access attribute 'title'
    titles = [tag.text for tag in inner_movie_tags]
    ratings = [float(tag['data-value']) for tag in rating_tags]     # access attribute 'data-value'
    images = [str(img_tag).split('src="')[1].split('"')[0] for img_tag in img_tags]

    links = []
    for a in soup.find_all('a'):  # , href=True):
        links.append(a.get('href'))
    links = ['https://www.imdb.com' + a.strip() for a in links if a is not None and a.startswith('/title/tt')]

    top_250_links = []
    for c in links:
        if c not in top_250_links:
            top_250_links.append(c)

    n_movies = len(titles)
    idx = random.randrange(0, n_movies)
    rating = str(ratings[idx])[:3]

    movie_data = (titles[idx], years[idx], rating, actors_list[idx], images[idx], top_250_links[idx])
    return movie_data
