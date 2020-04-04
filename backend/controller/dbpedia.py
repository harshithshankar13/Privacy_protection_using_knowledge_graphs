import requests

def IsInfoInDBPedia(subject):
    url = 'https://dbpedia.org/sparql'

    query = """
        PREFIX res: <http://dbpedia.org/resource/>
        prefix dbo: <http://dbpedia.org/ontology/>

        ASK 
        where 
        {
            res:"""+ subject +""" ?p ?o.
        }
        """

    response = requests.get(url, params={'format':'json', 'query': query})
    isPresent = response.json()

    return isPresent['boolean']