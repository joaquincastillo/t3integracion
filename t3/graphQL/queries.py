from gql import gql, Client

# 1. Todas las películas

allFilms = '''{
    allFilms(first: 9) {
        edges {
            node {
                ...filmFragment
            }
        }
    }
}

fragment filmFragment on Film {
    id // ///// Clave para redirigirlo a la info del film
   	episodeID
   	title
    releaseDate
    director
    producers

}'''
# —————————————————————————————————

# 2 y 3. Pelicula X. Sin vehículos ni especies.
# OJO con el id. The Phantom Menace es id "ZmlsbXM6NA==" por ejemplo.


def get_film(client):
    query = gql('''
        query FetchFilm($filmId: String!) {
            film(id: $filmId) {
                id
                episodeID
                title
                openingCrawl
                director
                producers
                releaseDate
                starshipConnection {edges {node {...starshipFragment}}}
                characterConnection {edges {node {...characterFragment}}}
                planetConnection {edges {node {...planetFragment}}}
            }

            fragment starshipFragment on Starship {
                id
                name
                model
                costInCredits
            }
            fragment characterFragment on Person {
                name
                id
                species {name}
            }

            fragment planetFragment on Planet {
                name
                id
            }
        }
    ''')

    params = {
        'filmId': 'ZmlsbXM6NA==',
    }

    result = client.execute(query, variable_values=params)

    print(result)



