from graphqlclient import GraphQLClient

# 1. Todas las películas

gql_client = GraphQLClient('https://swapi-graphql-integracion-t3.herokuapp.com/')


def get_all_films(client):

    query = '''
    {
        allFilms(first: 9) {
            edges {
                node {
                    ...filmFragment
                }
            }
        }
    }
    
    fragment filmFragment on Film {
        id
        episodeID
        title
        releaseDate
        director
        producers
    
    }'''

    print(query)
    result = client.execute(query)
    print(result)
    return result


def get_film(filmId, client):


    query = '''
    {
        film(id: "%s" ) {
            id
            episodeID
            title
            openingCrawl
            director
            producers
            releaseDate
            starshipConnection { edges { node { ...starshipFragment }}}
            characterConnection { edges { node { ...characterFragment }}}
            planetConnection { edges { node { ...planetFragment }}}
        }
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
      species { name }
    }
    
    fragment planetFragment on Planet {
      name
      id
    }''' % filmId

    print(query)

    result = client.execute(query)

    print(result)
    return result


def get_character(characterId, client):

    query = '''
    {
        person(id: "%s"){
            id
            name
            birthYear
            eyeColor
            gender
            hairColor
            height
            mass
            skinColor
            homeworld {
              name
              id
            }
            species { name }
            filmConnection { edges { node { ...filmFragment }}}
            starshipConnection { edges { node { ...starshipFragment }}}
        }
    }

    fragment starshipFragment on Starship {
        id
        name
    }
    
    fragment filmFragment on Film {
        id
        title
    }
    ''' % characterId

    print(query)
    result = client.execute(query)
    print(result)
    return result

def get_starship(starshipId, client):

    query = '''
    {
        starship(id: "%s"){
            id
            name
            model
            manufacturers
            costInCredits
            length
            maxAtmospheringSpeed
            crew
            passengers
            cargoCapacity
            consumables
            hyperdriveRating
            MGLT
            starshipClass
            pilotConnection { edges { node { ...characterFragment }}}
            filmConnection { edges { node { ...filmFragment }}}
        }
    }

    fragment characterFragment on Person {
      id
      name
    }
    
    fragment filmFragment on Film {
      id
      title
    }
    ''' % starshipId

    print(query)
    result = client.execute(query)
    print(result)
    return result

def get_planet(planetId, client):

    query = '''
    {
        planet(id: "xxx") {
            id
            name
            diameter
            rotationPeriod
            orbitalPeriod
            gravity
            population
            climates
            terrains
            surfaceWater
            residentConnection { edges { node { ...characterFragment } }}
            filmConnection { edges { node { ...filmFragment }}}
        }
    }
        
    fragment characterFragment on Person {
        id
        name
    }
    
    fragment filmFragment on Film {
        id
        title
    }
    ''' % planetId

    print(query)

    result = client.execute(query)

    print(result)
    return result





