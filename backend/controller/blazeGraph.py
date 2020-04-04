from SPARQLWrapper import SPARQLWrapper, JSON , POST, DIGEST

# create sparql instance
sparql = SPARQLWrapper("http://192.168.43.134:9999/blazegraph/sparql")

# @@ add basic owl such as company is class 
def baseRules():
    sparql.setQuery("""
        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        prefix owl: <http://www.w3.org/2002/07/owl#>
        prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        prefix xsd: <http://www.w3.org/2001/XMLSchema#>

		prefix wiki: <https://en.wikipedia.org/wiki/>
        prefix pp: <http://pp.org/>

        INSERT DATA{
          GRAPH pp:company_information {
            pp:no rdf:type wiki:Boolean_data_type.
            pp:yes rdf:type wiki:Boolean_data_type.
            
            pp:company  rdf:type rdfs:Class.
            
            pp:name rdf:type rdf:Property .
            pp:websiteTitle rdf:type rdf:Property .
            pp:websiteDescription rdf:type rdf:Property .
            pp:hasAdultContent rdf:type rdf:Property .
            pp:rank rdf:type rdf:Property .
            pp:websiteType rdf:type rdf:Property .
            
            pp:websiteTitle rdfs:domain pp:company.
            pp:websiteDescription rdfs:domain pp:company.
            pp:hasAdultContent rdfs:domain pp:company.
            pp:websiteType rdfs:domain pp:company.
            pp:name rdfs:domain pp:company.
            pp:rank rdfs:domain pp:company.
            
            pp:rank rdfs:range xsd:double.
            } 
            }   
    """)

    sparql.setReturnFormat(JSON)
    result = sparql.query().convert()

    print(result)  
     
    return result

def select(subject_m=None, predicate_m=None, object_m=None):
    sparql.setReturnFormat(JSON)

    if subject_m != None and predicate_m == None and object_m == None:
        sparql.setQuery("""
            prefix pp: <http://pp.org/>
            select * where{
                GRAPH pp:company_information { pp:"""+ subject_m +""" ?p ?o ;   }
            } 
        """)
        result = sparql.query().convert()
        
        for b in result['results']['bindings']:
            print( b['p']['value'], b['o']['value'])

    elif predicate_m != None and subject_m == None and object_m == None:
        sparql.setQuery("""
            prefix pp: <http://pp.org/>
            select * where{
                GRAPH pp:company_information { ?s pp:"""+ predicate_m +""" ?o ;   }
            } 
        """)
        result = sparql.query().convert()
        
        for b in result['results']['bindings']:
            print(b['s']['value'], b['o']['value'])

    elif object_m != None and predicate_m == None and subject_m == None:
        sparql.setQuery("""
            prefix pp: <http://pp.org/>
            select * where{
                GRAPH pp:company_information { ?s ?p pp:"""+ object_m +""" ;   }
            } 
        """)
        result = sparql.query().convert()
        
        for b in result['results']['bindings']:
            print(b['s']['value'], b['p']['value'])

    elif object_m != None and subject_m != None and predicate_m == None:
        sparql.setQuery("""
            prefix pp: <http://pp.org/>
            select * where{
                GRAPH pp:company_information { pp:"""+ subject_m +""" ?p pp:"""+ object_m +""" ;   }
            } 
        """)
        result = sparql.query().convert()
        
        for b in result['results']['bindings']:
            print(b['p']['value'])

    elif predicate_m != None and object_m != None and subject_m == None:
        sparql.setQuery("""
            prefix pp: <http://pp.org/>
            select * where{
                GRAPH pp:company_information { ?s pp:"""+ predicate_m +""" pp:"""+ object_m +""" ;   }
            } 
        """)
        result = sparql.query().convert()
        
        for b in result['results']['bindings']:
            print(b['s']['value'])

    elif predicate_m != None and subject_m != None and object_m == None:
        sparql.setQuery("""
            prefix pp: <http://pp.org/>
            select * where{
                GRAPH pp:company_information { pp:"""+ subject_m +""" pp:"""+ predicate_m +""" ?o ;   }
            } 
        """)
        result = sparql.query().convert()
        
        for b in result['results']['bindings']:
            print( b['o']['value'])
    
    return result

def add_companyInfo(compInfo):
    sparql.setMethod('POST')
    print(compInfo)
    sparql.setQuery("""
        prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        prefix xsd: <http://www.w3.org/2001/XMLSchema#>
        prefix pp: <http://pp.org/>

        INSERT DATA{
          GRAPH pp:company_information {
                    pp:""" + compInfo[0] + """ rdf:type pp:company;
            			  pp:websiteTitle \"""" + compInfo[1] +"""\";
            			  pp:websiteDescription \"""" + compInfo[2] +"""\";
            			  pp:hasAdultContent pp:""" + compInfo[3] +""";
            			  pp:websiteType \""""+ compInfo[4] +"""\";
                          pp:websiteMainActivity \""""+ compInfo[5] +"""\";
            			  pp:rank \"""" + compInfo[6] +"""\"^^xsd:double .
            } 
            }   
            """)
    sparql.setReturnFormat(JSON)

    result = sparql.query()

    print("Information about company added.")

# check if the data already exist in our graph
def checkForSubject(companyName):
    sparql.setQuery("""
        prefix pp: <http://pp.org/>
        ASK {
            GRAPH pp:company_information { pp:""" + companyName +""" ?p ?o .  }
        } 
    """)

    sparql.setReturnFormat(JSON)
    result = sparql.query().convert()
     
    return result["boolean"] 
    

# define to add info abour sameAs
def sameAs(bg_title, dbp_title):
    sparql.setMethod('POST')
    
    sparql.setQuery("""
        prefix owl: <http://www.w3.org/2002/07/owl#>

        prefix pp: <http://pp.org/>
		prefix res: <http://dbpedia.org/resource/>

        INSERT DATA{
          GRAPH pp:company_information {
			pp:"""+ bg_title +""" owl:sameAs  res:""" + dbp_title + """.
            } 
            }   
            """)

    sparql.setReturnFormat(JSON)

    result = sparql.query()

    print("SameAs data updated")   

def getCompanyName(domain):
    sparql.setMethod('POST')
    
    sparql.setQuery("""
        prefix pp: <http://pp.org/>
        select ?title where{
            GRAPH pp:company_information { pp:""" + domain +""" pp:websiteTitle ?title ;   }
        }    
            """)

    sparql.setReturnFormat(JSON)

    result = sparql.query().convert()

    return result['results']['bindings'][0]['title']['value']

def deleteUsingSub(subject):
    sparql.setMethod('POST')
    
    sparql.setQuery("""
        prefix pp: <http://pp.org/>

        DELETE {
          GRAPH pp:company_information { pp:netflix.com ?p ?o . } }
			where
			{
			pp:"""+ subject +""" ?p ?o .
            }    
            """)

    sparql.setReturnFormat(JSON)

    result = sparql.query()

    return True

def deleteNaN():
    sparql.setMethod('POST')
    
    sparql.setQuery("""
        prefix pp: <http://pp.org/>

        DELETE {
          GRAPH pp:company_information { ?s ?p 'NaN'. } }
			where
			{
			?s ?p 'NaN'.
            }    
            """)

    sparql.setReturnFormat(JSON)

    result = sparql.query().convert()

    return True