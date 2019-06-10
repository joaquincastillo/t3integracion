from t3.graphQL import queries
from django.shortcuts import render
import json


# Create your views here.


def index(request):

    ## NEW CODE

    client = queries.gql_client
    result = queries.get_all_films(client)
    films = json.loads(result)

    film_dict = {}
    for film in films["data"]["allFilms"]["edges"]:
        film_id = film["node"]["id"]
        title = film["node"]["title"]
        year = film["node"]["releaseDate"]
        director = film["node"]["director"]
        producer = film["node"]["producers"]
        episode = film["node"]["episodeID"]
        film_dict[episode] = {"title": title, "year": year, "director": director,
                              "producer": producer, "episode": episode,
                              "film_id": film_id, "url": "", "small_url": film_id}

    return render(request, 'principal_page.html', {'films': film_dict})


def show_film_page(request):

    # NEW CODE #

    # url_param = film_id
    url_param = request.GET.get("url_param")

    client = queries.gql_client
    result = queries.get_film(url_param, client)
    film = json.loads(result)

    film_data = {'id': film["data"]["film"]["id"],
                 'title': film["data"]["film"]["title"],
                 'opening_crawl': film["data"]["film"]["openingCrawl"],
                 'episode_id': film["data"]["film"]["episodeID"],
                 'director': film["data"]["film"]["director"],
                 'producer': film["data"]["film"]["producers"],
                 'release_date': film["data"]["film"]["releaseDate"]
                  }

    characters = {}
    for character in film["data"]["film"]["characterConnection"]["edges"]:
        name = character["node"]["name"]
        character_id = character["node"]["id"]

        characters[character_id] = name

    starships = {}
    for starship in film["data"]["film"]["starshipConnection"]["edges"]:
        name = starship["node"]["name"]
        starship_id = starship["node"]["id"]

        starships[starship_id] = name

    planets = {}
    for planet in film["data"]["film"]["planetConnection"]["edges"]:
        name = planet["node"]["name"]
        planetId = planet["node"]["id"]

        planets[planetId] = name

    return render(request, 'film_page.html', {"film": film_data, "characters": characters,
                                              "starships": starships, "planets": planets})

def show_character_page(request):

    # NEW CODE

    url_param = request.GET.get("url_param")

    client = queries.gql_client
    result = queries.get_character(url_param, client)
    character = json.loads(result)

    data = {'id': character["data"]["person"]["id"],
            'name': character["data"]["person"]["name"],
            'birth_year': character["data"]["person"]["birthYear"],
            'eye_color': character["data"]["person"]["eyeColor"],
            'gender': character["data"]["person"]["gender"],
            'hair_color': character["data"]["person"]["hairColor"],
            'height': character["data"]["person"]["height"],
            'mass': character["data"]["person"]["mass"],
            'skin_color': character["data"]["person"]["skinColor"]
            }

    homeworld_id = character["data"]["person"]["homeworld"]["id"]
    homeworld_name = character["data"]["person"]["homeworld"]["name"]
    homeworld_d = {homeworld_id: homeworld_name }

    films = {}
    for film in character["data"]["person"]["filmConnection"]["edges"]:
        title = film["node"]["title"]
        film_id = film["node"]["id"]

        films[film_id] = title

    starships = {}
    for starship in character["data"]["person"]["starshipConnection"]["edges"]:
        name = starship["node"]["name"]
        starship_id = starship["node"]["id"]

        starships[starship_id] = name

    return render(request, 'character_page.html', {"character": data,
                                                   "homeworld": homeworld_d,
                                                   "films": films,
                                                   "starships": starships})


def show_planet_page(request):

    # NEW CODE

    url_param = request.GET.get("url_param")

    client = queries.gql_client
    result = queries.get_planet(url_param, client)
    planet = json.loads(result)

    data = {'id': planet["data"]["planet"]["id"],
            'name': planet["data"]["planet"]["name"],
            'diameter': planet["data"]["planet"]["diameter"],
            'rotation_period': planet["data"]["planet"]["rotationPeriod"],
            'orbital_period': planet["data"]["planet"]["orbitalPeriod"],
            'gravity': planet["data"]["planet"]["gravity"],
            'population': planet["data"]["planet"]["population"],
            'climate': planet["data"]["planet"]["climates"],
            'terrain': planet["data"]["planet"]["terrains"],
            'surface_water': planet["data"]["planet"]["surfaceWater"]
            }


    films = {}
    for film in planet["data"]["planet"]["filmConnection"]["edges"]:
        title = film["node"]["title"]
        film_id = film["node"]["id"]
        films[film_id] = title

    residents = {}
    for resident in planet["data"]["planet"]["residentConnection"]["edges"]:
        name = resident["node"]["name"]
        resident_id = resident["node"]["id"]

        residents[resident_id] = name

    return render(request, 'planet_page.html', {"planet": data,
                                                "films": films,
                                                "residents": residents})


def show_starship_page(request):
    # NEW CODE #

    # url_param = starship_id
    url_param = request.GET.get("url_param")

    client = queries.gql_client
    result = queries.get_starship(url_param, client)
    starship = json.loads(result)

    data = {'id': starship["data"]["starship"]["id"],
            'name': starship["data"]["starship"]["name"],
            'model': starship["data"]["starship"]["model"],
            'manufacturer': starship["data"]["starship"]["manufacturers"],
            'cost_in_credits': starship["data"]["starship"]["costInCredits"],
            'length': starship["data"]["starship"]["length"],
            'max_atmosphering_speed': starship["data"]["starship"]["maxAtmospheringSpeed"],
            'crew': starship["data"]["starship"]['crew'],
            'passengers': starship["data"]["starship"]['passengers'],
            'cargo_capacity': starship["data"]["starship"]['cargoCapacity'],
            'consumables': starship["data"]["starship"]['consumables'],
            'hyperdrive_rating': starship["data"]["starship"]['hyperdriveRating'],
            'MGLT': starship["data"]["starship"]['MGLT'],
            'starship_class': starship["data"]["starship"]['starshipClass']
                 }

    pilots = {}
    for pilot in starship["data"]["starship"]["pilotConnection"]["edges"]:
        name = pilot["node"]["name"]
        pilot_id = pilot["node"]["id"]

        pilots[pilot_id] = name

    films = {}
    for film in starship["data"]["starship"]["filmConnection"]["edges"]:
        name = film["node"]["title"]
        starship_id = film["node"]["id"]

        films[starship_id] = name

    return render(request, 'starship_page.html', {"starship": data,
                                                  "pilots": pilots,
                                                  "films": films})


