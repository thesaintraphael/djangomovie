import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from requests.compat import quote_plus
from .models import Search
import json
import random

BASE_MOVIE_MAP_URL = 'https://www.movie-map.com/{}'
API_MOVIE_DATA_URL = 'http://www.omdbapi.com/?t={}&apikey=3f756fe6'


def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')
    Search.objects.create(search=search)
    final_url = BASE_MOVIE_MAP_URL.format(quote_plus(search.lower()))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, 'html.parser')
    titles = soup.find_all('a')
    if len(titles) >= 13:
        length = 13
    else:
        length = len(titles)
    final_postings = []

    for i in range(3, length):
        post_title = str(titles[i].text)
        post_title = post_title.replace(':', '')
        
        final_url = API_MOVIE_DATA_URL.format(quote_plus(post_title.lower()))
        response = requests.get(final_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        movie_dict = json.loads(soup.prettify())

        src = "https://cdn.wallpapersafari.com/30/17/H3okeM.jpg"

        final_postings.append((post_title, src, movie_dict))

    stuff_for_frontend = {
        'search': search,
        'final_postings': final_postings,
    }
    return render(request, 'new_search.html', stuff_for_frontend)


def random_movie(request):
    pics = ['12 Angry Men', '12 Years a Slave', '1917', '2001 A Space Odyssey', '3 Idiots', 'A Beautiful Mind', 'A Clockwork Orange', 'A Separation', 'A Silent Voice The Movie', 'Aladdin', 'Alien', 'Aliens', 'All About Eve', 'Amadeus', 'American Beauty', 'American History X', 'American Psycho', 'Amores Perros', 'Amélie', 'Anand', 'Andhadhun', 'Andrei Rublev', 'Apocalypse Now', 'Avengers Endgame', 'Avengers Infinity War', 'Avengers', 'Back to the Future', 'Barry Lyndon', 'Batman Begins', 'Before Sunrise', 'Before Sunset', 'Ben Hur', 'Bicycle Thieves', 'Blade Runner', 'BladeRunner', 'Braveheart', 'Capernaum', 'Casablanca', 'Casino', 'Catch Me If You Can', 'Children Of Heaven', 'Chinatown', 'Cinema Paradiso', 'Citizen Kane', 'City Lights', 'City Of God', 'Coco', 'Come and See', 'Cool Hand Luke', 'Dangal', 'Das Boot', 'Dead Poets Society', 'Dial M for Murder', 'Die Hard', 'Django Unchained', 'Donnie Darko', 'Double Indemnity', 'Downfall', 'Dr Strangelove or How I Learned to Stop Worrying and Love the Bomb', 'Drishyam', 'Eternal Sunshine of the Spotless Mind', 'Fargo', 'Fight Club', 'Finding Nemo', 'For a Few Dollars More', 'Ford v Ferrari', 'Forrest Gump', 'Full Metal Jacket', 'Gangs of Wasseypur', 'Gladiator', 'Gone Girl', 'Gone with the Wind', 'Good Will Hunting', 'Goodfellas', 'Gran Torino', 'Grave of the Fireflies', 'Green Book', "Hachi A Dog's Tale", 'Hacksaw Ridge', 'Hamilton', 'Harakiri', 'Harry Potter and the Deathly Hallows Part 2', 'Harry Potter', 'Heat', 'High and Low', 'Hotel Rwanda', 'How to Train Your Dragon', "Howl's Moving Castle", 'Hunt', 'Ikiru', 'In the Mood for Love', 'Incendies', 'Inception', 'Indiana Jones and the Last Crusade', 'Inglourious Basterds', 'Inside Out', 'Interstellar', 'Into the Wild', "It's a Wonderful Life", 'It Happened One Night', 'Jagten', 'Joker', 'Judgment at Nuremberg', 'Jurassic Park', 'Kill Bill Vol 1', 'Claus', 'Pulp Fiction', 'LA Confidential', 'Lawrence of Arabia', 'Life Is Beautiful', 'Life of Brian', 'Like Stars on Earth', 'Lock, Stock and Two Smoking Barrels', 'Logan', 'Léon The Professional', 'M', 'Mad Max Fury Road', 'Mary and Max', 'Memento', 'Memories of Murder', 'Metropolis', 'Million Dollar Baby', 'Modern Times', 'Monsters, Inc', "Monty Python's Life of Brian", 'Monty Python and the Holy Grail', 'Mr Smith Goes to Washington', 'My Father and My Son', 'My Neighbor Totoro', 'Network', 'No Country for Old Men', 'North by Northwest', 'Oldboy', 'Pianist', 'On the Waterfront', 'Once Upon a Time in America', 'Once Upon a Time in the West', "One Flew Over the Cuckoo's Nest", "Pan's Labyrinth", 'Parasite', 'Paris, Texas', 'Paths of Glory', 'Persona', 'Platoon', 'Portrait of a Lady on Fire', 'Princess Mononoke', 'Prisoners', 'Psycho', 'Pulp Fiction', 'Raging Bull', 'Raiders of the Lost Ark', 'Ran', 'Rang De Basanti', 'Rashomon', 'Rear Window', 'Requiem for a Dream', 'Reservoir Dogs', 'Rififi', 'Rocky', 'Room', 'Rush', 'Saving Private Ryan', 'Scarface', "Schindler's List", 'Se7en', 'Seven Samurai', 'Shawshank Redemption', 'Sherlock Jr', 'Shutter Island', "Singin' in the Rain", 'Snatch', 'Some Like It Hot', 'Spider Man Into the Spider Verse', 'Spider Man', 'Spirited Away', 'Spotlight', 'Stalker', 'Stand by Me', 'Star Wars Episode IV   A New Hope', 'Star Wars Episode V   The Empire Strikes Back', 'Star Wars Episode VI   Return of the Jedi', 'Star Wars', 'Sunset Blvd', 'Tangerines', 'Taxi Driver', 'Terminator 2 Judgment Day', 'Terminator', 'The 400 Blows', 'The Apartment', 'The Bandit', 'The Battle of Algiers', 'The Big Lebowski', 'The Bridge on the River Kwai', 'The Circus', 'The Dark Knight Rises', 'The Dark Knight', 'The Deer Hunter', 'The Departed', 'The Elephant Man', 'The General', 'The Godfather Part II', 'The Godfather', 'The Gold Rush', 'The Good, the Bad and the Ugly', 'The Grand Budapest Hotel', 'The Great Dictator', 'The Great Escape', 'The Green Mile', 'The Handmaiden', 'The Help', 'The Intouchables', 'The Invisible Guest', 'The Kid', 'The Lion King', 'The Lives of Others', 'The Lord of the Rings The Fellowship of the Ring', 'The Lord of the Rings The Return of the King', 'The Lord of the Rings The Two Towers', 'The Lord of the Rings', 'The Matrix', 'The Passion of Joan of Arc', 'The Pianist', 'The Prestige', 'The Princess Bride', 'The Secret in Their Eyes', 'The Seventh Seal', 'The Shining', 'The Silence of the Lambs', 'The Sixth Sense', 'The Sting', 'The Terminator', 'The Thing', 'The Third Man', 'The Treasure of the Sierra Madre', 'The Truman Show', 'The Usual Suspects', 'The Wages of Fear', 'The Wolf of Wall Street', 'There Will Be Blood', 'To Be or Not to Be', 'Tokyo Story', 'Toy Story 3', 'Toy Story', 'Trainspotting', 'Twelve Monkeys', 'Unforgiven', 'Up', 'V for Vendetta', 'Vertigo', 'Vikram Vedha', 'WALL E', 'Warrior', 'Whiplash', 'Wild Strawberries', 'Wild Tales', 'Witness for the Prosecution', 'Yojimbo', 'Your Name', '7even', 'The Book Thief']
    idx = random.randrange(0, len(pics))
    title = pics[idx]

    final_url = API_MOVIE_DATA_URL.format(quote_plus(title.lower()))
    response = requests.get(final_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    movie_dict = json.loads(soup.prettify())
    length = len(movie_dict)
    context = {
        'movie_title': title,
        'movie_dict': movie_dict,
        'length': length,
    }

    return render(request, 'generator.html', context)


def error_404(request, exception):
    data = {}
    return render(request, '404.html', data)


def error_405(request, exception):
    data = {}
    return render(request, '404.html', data)
