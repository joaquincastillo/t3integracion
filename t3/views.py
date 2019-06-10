from t3.graphQL import queries
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from urllib3 import PoolManager
import json
import certifi


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

    ## OLD CODE

    # url = "https://swapi.co/api/films/"
    # # return HttpResponse("Hello, world. You're at the t3 index.")
    # http = PoolManager(cert_reqs="CERT_REQUIRED", ca_certs=certifi.where())
    # r = http.request('GET', url)
    # print(r.status)
    #
    # # Decode UTF-8 bytes to Unicode, and convert single quotes
    # # to double quotes to make it valid JSON
    # my_json = r.data.decode('utf8')
    # print(my_json)
    # print('- ' * 20)
    #
    # # Load the JSON to a Python list & dump it back out as formatted JSON
    # films = json.loads(my_json)
    # # Para ver el json como string bonito
    # # json_films = json.dumps(films, indent=4, sort_keys=True)
    # # print(json_films)
    #
    # # --------- Requisito NAV 1 ---------- #
    # # Para la página principal
    # film_dict = {}
    # for film in films["results"]:
    #     title = film["title"]
    #     year = film["release_date"]
    #     director = film["director"]
    #     producer = film["producer"]
    #     episode = film["episode_id"]
    #     url = film["url"]
    #     pos = url.find("films")
    #     small_url = url[pos+6:len(url)-1]
    #     film_dict[episode] = {"title": title, "year": year, "director": director,
    #                           "producer": producer, "episode": episode, "url": url,
    #                           "small_url": small_url}

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


    # # OLD CODE
    # url_param = request.GET.get("url_param")
    # req_url = "https://swapi.co/api/planets/{}".format(url_param)
    # http = PoolManager(cert_reqs="CERT_REQUIRED", ca_certs=certifi.where())
    # r = http.request('GET', req_url)
    # my_json = r.data.decode('utf8')
    # planet = json.loads(my_json)
    #
    # # Buscando las peliculas donde apareció
    # films = {}
    # for film_url in planet["films"]:
    #     film_req = http.request('GET', film_url)
    #     film_json = film_req.data.decode('utf8')
    #     film = json.loads(film_json)
    #     film_name = film["title"]
    #     f_url = film["url"]
    #     pos = f_url.find("films")
    #     url_id = film["url"][pos + 6:len(film["url"]) - 1]
    #     films[url_id] = film_name
    #
    # # Buscando sus residentes
    # residents = {}
    # for people_url in planet["residents"]:
    #     people_req = http.request('GET', people_url)
    #     people_json = people_req.data.decode('utf8')
    #     people = json.loads(people_json)
    #     people_name = people["name"]
    #     p_url = people["url"]
    #     pos = p_url.find("people")
    #     url_id = people["url"][pos + 7:len(people["url"]) - 1]
    #     residents[url_id] = people_name

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

def show_search_page(request):
    acc = []
    search = request.GET.get("search")
    filtro = request.GET.get("filter")
    req_url = "https://swapi.co/api/{}/?search={}".format(filtro, search)
    http = PoolManager(cert_reqs="CERT_REQUIRED", ca_certs=certifi.where())
    r = http.request('GET', req_url)
    my_json = r.data.decode('utf8')
    results = json.loads(my_json)
    acc += results["results"]
    next_req = results["next"]

    while next_req is not None:  # This almost destroyed me
        res = http.request('GET', next_req)
        res_json = res.data.decode('utf8')
        results = json.loads(res_json)
        acc += results["results"]
        next_req = results["next"]

    results_size = len(acc)
    deliverable = {}
    for elem in acc:
        n = "name"
        if filtro=='films':
            n = "title"
            extra = 6
            pos = elem["url"].find("films")
        elif filtro=='people':
            extra = 7
            pos = elem["url"].find("people")
        elif filtro=='starships':
            extra = 10
            pos = elem["url"].find("starships")
        else: #if filtro=='planets':
            extra = 8
            pos = elem["url"].find("planets")
        name = elem[n]
        url_id = elem["url"][pos + extra:len(elem["url"]) - 1]
        deliverable[url_id] = name

    context = {"search": search, "filter": filtro, "results": deliverable, "size": results_size}
    return render(request, 'search_page.html', context)



