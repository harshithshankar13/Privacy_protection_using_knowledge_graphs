from SPARQLWrapper import SPARQLWrapper, JSON , POST, DIGEST
import datetime

# create sparql instance
sparql = SPARQLWrapper("http://localhost:9999/blazegraph/sparql")

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

    companyInfo = [subject_m]

    if subject_m != None and predicate_m == None and object_m == None:
        sparql.setQuery("""
            prefix pp: <http://pp.org/>
            select * where{
                GRAPH pp:company_information { pp:"""+ subject_m +""" ?p ?o .  }
            } 
        """)
        result = sparql.query().convert()
        
        for b in result['results']['bindings']:
            print( b['p']['value'], b['o']['value'])
            companyInfo.append(b['o']['value'])

    elif predicate_m != None and subject_m == None and object_m == None:
        sparql.setQuery("""
            prefix pp: <http://pp.org/>
            select * where{
                GRAPH pp:company_information { ?s pp:"""+ predicate_m +""" ?o .  }
            } 
        """)
        result = sparql.query().convert()
        
        for b in result['results']['bindings']:
            print(b['s']['value'], b['o']['value'])
            companyInfo.append(b['o']['value'])

    elif object_m != None and predicate_m == None and subject_m == None:
        sparql.setQuery("""
            prefix pp: <http://pp.org/>
            select * where{
                GRAPH pp:company_information { ?s ?p pp:"""+ object_m +""".   }
            } 
        """)
        result = sparql.query().convert()
        
        for b in result['results']['bindings']:
            print(b['s']['value'], b['p']['value'])
            companyInfo.append(b['o']['value'])

    elif object_m != None and subject_m != None and predicate_m == None:
        sparql.setQuery("""
            prefix pp: <http://pp.org/>
            select * where{
                GRAPH pp:company_information { pp:"""+ subject_m +""" ?p pp:"""+ object_m +""" .   }
            } 
        """)
        result = sparql.query().convert()
        
        for b in result['results']['bindings']:
            print(b['p']['value'])
            companyInfo.append(b['p']['value'])

    elif predicate_m != None and object_m != None and subject_m == None:
        sparql.setQuery("""
            prefix pp: <http://pp.org/>
            select * where{
                GRAPH pp:company_information { ?s pp:"""+ predicate_m +""" pp:"""+ object_m +""" .   }
            } 
        """)
        result = sparql.query().convert()
        
        for b in result['results']['bindings']:
            print(b['s']['value'])
            companyInfo.append(b['s']['value'])

    elif predicate_m != None and subject_m != None and object_m == None:
        sparql.setQuery("""
            prefix pp: <http://pp.org/>
            select * where{
                GRAPH pp:company_information { pp:"""+ subject_m +""" pp:"""+ predicate_m +""" ?o .  }
            } 
        """)
        result = sparql.query().convert()
        
        for b in result['results']['bindings']:
            print( b['o']['value'])
            companyInfo.append(b['o']['value'])
    
    return companyInfo

def select_all():
    sparql.setQuery("""
            prefix pp: <http://pp.org/>
            select * where{
                GRAPH pp:company_information { ?s ?p ?o.   }
            } 
        """)
    sparql.setReturnFormat(JSON)
    result = sparql.query().convert()
    
    for b in result['results']['bindings']:
        print(b['s']['value'], b['p']['value'], b['o']['value'])

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
            			  pp:rank \"""" + compInfo[6] +"""\"^^xsd:double ;
                          pp:onlineSince \"""" + str(datetime.datetime.strptime(compInfo[7], '%d-%b-%Y')) + """\"^^xsd:date .
            } 
            }   
            """)
    sparql.setReturnFormat(JSON)

    result = sparql.query()

    print("Information about company added.")

# add company location 
def addCompanyLocation(m_domain, m_location):
    sparql.setMethod('POST')

    sparql.setQuery("""
        prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        prefix xsd: <http://www.w3.org/2001/XMLSchema#>
        prefix pp: <http://pp.org/>

        INSERT DATA{
          GRAPH pp:company_information {
                    pp:""" + m_domain + """ pp:location <""" + m_location + """>.
            } 
            }   
            """)
    sparql.setReturnFormat(JSON)

    result = sparql.query()

    print("Information about company location is added.")


# add company website created date
def addCompanyCreatedDate(m_domain, m_date):
    sparql.setMethod('POST')

    sparql.setQuery("""
        prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        prefix xsd: <http://www.w3.org/2001/XMLSchema#>
        prefix pp: <http://pp.org/>

        INSERT DATA{
          GRAPH pp:company_information {
                    pp:""" + m_domain + """ pp:onlineSince <""" + m_date + """>.
            } 
            }   
            """)
    sparql.setReturnFormat(JSON)

    result = sparql.query()

    print("Information about website created date is added.")

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
    print("subject:" ,result["boolean"])
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
          GRAPH pp:company_information { pp:"""+subject +""" ?p ?o . } }
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

def getCompanyInfoInFormat(subject_m):
    sparql.setMethod('POST')
    
    sparql.setQuery("""
        prefix pp: <http://pp.org/>

        CONSTRUCT  {
           
              pp:""" + subject_m +""" pp:websiteTitle ?websiteTitle ;
            			  pp:websiteDescription ?websiteDescription ;
            			  pp:hasAdultContent ?AdultContent ;
            			  pp:websiteType ?websiteType;
                          pp:websiteMainActivity ?websiteMainActivity;
            			  pp:rank ?rank ;
                          pp:onlineSince ?onlineSince ;
                          pp:location ?location .
                          
           } 
  
    	WHERE
			{
              GRAPH pp:company_information {
            	optional { pp:""" + subject_m +""" pp:websiteTitle ?websiteTitle .}
                optional {pp:""" + subject_m +""" pp:websiteDescription ?websiteDescription . }
                optional {pp:""" + subject_m +""" pp:hasAdultContent ?AdultContent . }
                optional {pp:""" + subject_m +""" pp:websiteType ?websiteType . }
                optional {pp:""" + subject_m +""" pp:websiteMainActivity ?websiteMainActivity . }
                optional {pp:""" + subject_m +""" pp:rank ?rank . }
                optional {pp:""" + subject_m +""" pp:onlineSince ?onlineSince . }
                optional {pp:""" + subject_m +""" pp:location ?location . }
                
            }  }
            """)  

    sparql.setReturnFormat(JSON)
    result = sparql.query().convert()
    
    companyInfo = [subject_m,None, None, None, None, None, None, None, None]
    # print(result)
    for b in result['results']['bindings']:
        if b['predicate']['value'] == "http://pp.org/websiteTitle":
            companyInfo[1] = b['object']['value']
        elif b['predicate']['value'] == "http://pp.org/websiteDescription":
            companyInfo[2] = b['object']['value']
        elif b['predicate']['value'] == "http://pp.org/hasAdultContent":
            companyInfo[3] = b['object']['value']
        elif b['predicate']['value'] == "http://pp.org/websiteType":
            companyInfo[4] = b['object']['value']
        elif b['predicate']['value'] == "http://pp.org/websiteMainActivity":
            companyInfo[5] = b['object']['value']
        elif b['predicate']['value'] == "http://pp.org/rank":
            companyInfo[6] = b['object']['value']
        elif b['predicate']['value'] == "http://pp.org/onlineSince":
            companyInfo[7] = b['object']['value']
        elif b['predicate']['value'] == "http://pp.org/location":
            companyInfo[8] = b['object']['value']

    return companyInfo
