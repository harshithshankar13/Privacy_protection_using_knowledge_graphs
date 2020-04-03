from SPARQLWrapper import SPARQLWrapper, JSON , POST, DIGEST

def select_all():
    sparql = SPARQLWrapper("http://192.168.43.134:9999/blazegraph/sparql")
    sparql.setQuery("""
        prefix pp: <http://pp.org/>
        select * where{
            GRAPH pp:company_information { ?s ?p ?o ;   }
        } 
    """)
    sparql.setReturnFormat(JSON)

    result = sparql.query().convert()

    for b in result['results']['bindings']:
        print(b['s']['value'], b['p']['value'], b['o']['value'])

def update():
    sparql = SPARQLWrapper("http://192.168.43.134:9999/blazegraph/sparql")
    sparql.setMethod('POST')
    sparql.setQuery("""
    prefix pp: <http://pp.org/>
    prefix wiki: <https://en.wikipedia.org/wiki/>
        INSERT DATA{
          GRAPH pp:company_information {
            
        wiki:amazom 	pp:name    "amazom"   
        } 
    }
        
    """)

    sparql.setReturnFormat(JSON)
    print(sparql.isSparqlUpdateRequest())

    result = sparql.query()

    print(result)

    # for b in result['results']['bindings']:
    #     print(b['subject']['value'], b['predicate']['value'], b['object']['value'])

# check if the data already exist in our graph
def checkForObject(companyName):
    sparql = SPARQLWrapper("http://192.168.43.170:9999/blazegraph/sparql")
    sparql.setQuery("""
        prefix pp: <http://pp.org/>
        ASK {
            GRAPH pp:company_information { pp:""" + companyName +""" ?p ?o ;   }
        } 
    """)

    sparql.setReturnFormat(JSON)
    result = sparql.query().convert()

    print(result["boolean"])  
     
    return result["boolean"] 