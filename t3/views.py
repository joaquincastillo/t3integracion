from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from urllib3 import PoolManager
import json
import certifi
from import './graphQL/queries' import get_film


# Create your views here.


def index(request):
    url = "https://swapi.co/api/films/"
    # return HttpResponse("Hello, world. You're at the t3 index.")
    http = PoolManager(cert_reqs="CERT_REQUIRED", ca_certs=certifi.where())
    r = http.request('GET', url)
    print(r.status)

    # Decode UTF-8 bytes to Unicode, and convert single quotes
    # to double quotes to make it valid JSON
    my_json = r.data.decode('utf8')
    print(my_json)
    print('- ' * 20)

    # Load the JSON to a Python list & dump it back out as formatted JSON
    films = json.loads(my_json)
    # Para ver el json como string bonito
    # json_films = json.dumps(films, indent=4, sort_keys=True)
    # print(json_films)

    # --------- Requisito NAV 1 ---------- #
    # Para la página principal
    film_dict = {}
    for film in films["results"]:
        title = film["title"]
        year = film["release_date"]
        director = film["director"]
        producer = film["producer"]
        episode = film["episode_id"]
        url = film["url"]
        pos = url.find("films")
        small_url = url[pos+6:len(url)-1]
        film_dict[episode] = {"title": title, "year": year, "director": director,
                              "producer": producer, "episode": episode, "url": url,
                              "small_url": small_url}

    client = Client()
    get_film(client)

    return render(request, 'principal_page.html', {'films': film_dict})


def show_film_page(request):
    # NEW CODE #

    client = GraphQLClient('http://graphql-swapi.parseapp.com/')
    result = client.execute('''
    {
    allFilms {
        films {
        title
        }
    }
    }
    ''')
    print(result)



    # OLD CODE # 
    url_param = request.GET.get("url_param")
    req_url = "https://swapi.co/api/films/{}".format(url_param)

    # return HttpResponse("Hello, world. You're at the t3 index.")
    http = PoolManager(cert_reqs="CERT_REQUIRED", ca_certs=certifi.where())
    r = http.request('GET', req_url)
    my_json = r.data.decode('utf8')
    film = json.loads(my_json)

    # Obteniendo info de los personajes
    characters = {}
    for character_url in film["characters"]:
        char_req = http.request('GET', character_url)
        char_json = char_req.data.decode('utf8')
        character = json.loads(char_json)
        char_name = character["name"]
        char_url = character["url"]
        pos = char_url.find("people")
        url_id = character["url"][pos+7:len(character["url"])-1]
        characters[url_id] = char_name

    # Obteniendo info de las starships
    starships = {}
    for ship_url in film["starships"]:
        ship_req = http.request('GET', ship_url)
        ship_json = ship_req.data.decode('utf8')
        ship = json.loads(ship_json)
        ship_name = ship["name"]
        s_url = ship["url"]
        pos = s_url.find("starships")
        url_id = ship["url"][pos + 10:len(ship["url"]) - 1]
        starships[url_id] = ship_name

    # Obteniendo info de los planetas
    planets = {}
    for planet_url in film["planets"]:
        planet_req = http.request('GET', planet_url)
        planet_json = planet_req.data.decode('utf8')
        planet = json.loads(planet_json)
        planet_name = planet["name"]
        p_url = planet["url"]
        pos = p_url.find("planets")
        url_id = planet["url"][pos + 8:len(planet["url"]) - 1]
        planets[url_id] = planet_name

    return render(request, 'film_page.html', {"film": film, "characters": characters,
                                              "starships": starships, "planets": planets})

def show_character_page(request):
    url_param = request.GET.get("url_param")
    req_url = "https://swapi.co/api/people/{}".format(url_param)
    http = PoolManager(cert_reqs="CERT_REQUIRED", ca_certs=certifi.where())
    r = http.request('GET', req_url)
    my_json = r.data.decode('utf8')
    character = json.loads(my_json)

    # Buscando su planeta de nacimiento
    homeworld_d = {}
    homeworld_url = character["homeworld"]
    homeworld_req = http.request('GET', homeworld_url)
    homeworld_json = homeworld_req.data.decode('utf8')
    homeworld = json.loads(homeworld_json)
    homeworld_name = homeworld["name"]
    h_url = homeworld["url"]
    pos = h_url.find("planets")
    url_id = homeworld["url"][pos + 8: len(homeworld["url"]) - 1]
    homeworld_d[url_id] = homeworld_name

    #Buscando las peliculas donde apareció
    films = {}
    for film_url in character["films"]:
        film_req = http.request('GET', film_url)
        film_json = film_req.data.decode('utf8')
        film = json.loads(film_json)
        film_name = film["title"]
        f_url = film["url"]
        pos = f_url.find("films")
        url_id = film["url"][pos + 6:len(film["url"]) - 1]
        films[url_id] = film_name

    #Buscando las starships que piloteo
    starships = {}
    for starship_url in character["starships"]:
        starship_req = http.request('GET', starship_url)
        starship_json = starship_req.data.decode('utf8')
        starship = json.loads(starship_json)
        starship_name = starship["name"]
        s_url = starship["url"]
        pos = s_url.find("starships")
        url_id = starship["url"][pos + 10:len(starship["url"]) - 1]
        starships[url_id] = starship_name

    return render(request, 'character_page.html', {"character": character,
                                                   "homeworld": homeworld_d,
                                                   "films": films,
                                                   "starships": starships})


def show_planet_page(request):
    url_param = request.GET.get("url_param")
    req_url = "https://swapi.co/api/planets/{}".format(url_param)
    http = PoolManager(cert_reqs="CERT_REQUIRED", ca_certs=certifi.where())
    r = http.request('GET', req_url)
    my_json = r.data.decode('utf8')
    planet = json.loads(my_json)

    # Buscando las peliculas donde apareció
    films = {}
    for film_url in planet["films"]:
        film_req = http.request('GET', film_url)
        film_json = film_req.data.decode('utf8')
        film = json.loads(film_json)
        film_name = film["title"]
        f_url = film["url"]
        pos = f_url.find("films")
        url_id = film["url"][pos + 6:len(film["url"]) - 1]
        films[url_id] = film_name

    # Buscando sus residentes
    residents = {}
    for people_url in planet["residents"]:
        people_req = http.request('GET', people_url)
        people_json = people_req.data.decode('utf8')
        people = json.loads(people_json)
        people_name = people["name"]
        p_url = people["url"]
        pos = p_url.find("people")
        url_id = people["url"][pos + 7:len(people["url"]) - 1]
        residents[url_id] = people_name

    return render(request, 'planet_page.html', {"planet": planet,
                                                "films": films,
                                                "residents": residents})


def show_starship_page(request):
    url_param = request.GET.get("url_param")
    req_url = "https://swapi.co/api/starships/{}".format(url_param)
    http = PoolManager(cert_reqs="CERT_REQUIRED", ca_certs=certifi.where())
    r = http.request('GET', req_url)
    my_json = r.data.decode('utf8')
    starship = json.loads(my_json)

    #Buscando sus pilotos
    pilots = {}
    for people_url in starship["pilots"]:
        people_req = http.request('GET', people_url)
        people_json = people_req.data.decode('utf8')
        people = json.loads(people_json)
        people_name = people["name"]
        p_url = people["url"]
        pos = p_url.find("people")
        url_id = people["url"][pos + 7:len(people["url"]) - 1]
        pilots[url_id] = people_name

    # Buscando las peliculas donde apareció
    films = {}
    for film_url in starship["films"]:
        film_req = http.request('GET', film_url)
        film_json = film_req.data.decode('utf8')
        film = json.loads(film_json)
        film_name = film["title"]
        f_url = film["url"]
        pos = f_url.find("films")
        url_id = film["url"][pos + 6:len(film["url"]) - 1]
        films[url_id] = film_name

    return render(request, 'starship_page.html', {"starship": starship,
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



