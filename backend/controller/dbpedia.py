import requests

def IsInfoInDBPedia(subject):
    url = 'https://dbpedia.org/sparql'

    query = """
        PREFIX dbr: <http://dbpedia.org/resource/>
        prefix dbo: <http://dbpedia.org/ontology/>

        ASK 
        where 
        {
            dbr:"""+ subject +""" ?p ?o.
        }
        """

    response = requests.get(url, params={'format':'json', 'query': query})
    isPresent = response.json()

    return isPresent['boolean']


def getInfoFromDBPedia(subject):
    print("test-Subject: ", subject)
    url = 'https://dbpedia.org/sparql'

    query = """
        PREFIX res: <http://dbpedia.org/resource/>
        prefix dbo: <http://dbpedia.org/ontology/>

        select *
        where{
            res:""" + subject + """ ?p ?o.
        }
        """

    response = requests.get(url, params={'format':'json', 'query': query})
    companyInfo = response.json()

    return companyInfo

def getCompanyLocation(subject):
    url = 'https://dbpedia.org/sparql'

    query = """
        PREFIX res: <http://dbpedia.org/resource/>
        prefix dbo: <http://dbpedia.org/ontology/>

        select distinct *
        where{
         optional{res:""" +subject + """ dbo:location ?o. }
         optional{res:""" +subject + """ dbo:locationCity ?o}
        }
        """

    response = requests.get(url, params={'format':'json', 'query': query})
    companyLocation = response.json()

    companyLocation = companyLocation['results']['bindings'][0]['o']['value']

    return companyLocation

def getLatLong(m_location):
    url = 'https://dbpedia.org/sparql'

    query = """
        PREFIX res: <http://dbpedia.org/resource/>
        prefix dbo: <http://dbpedia.org/ontology/>
        PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>

        select *
        where{ """ + m_location +""" a dbo:Place ; geo:lat ?lat ; geo:long ?long .
        }
        """

    response = requests.get(url, params={'format':'json', 'query': query})
    companyLatLong = response.json()

    return companyLatLong