'''
This file is the starting point of this flash server.

Apenx:
    @@ means todo

'''

from flask import Flask, request, jsonify, after_this_request
import tldextract   # to extract the domain name from url

import controller.alexa as alexa
import controller.blazeGraph as blazegraph
import controller.dbpedia as dbpedia

app = Flask(__name__)

@app.route('/')
def index():
    return "privary matters"

@app.route('/privacyMetric', methods=['GET'])
def privacyMetric():
    blazegraph.baseRules()

    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    # get domain name from url
    url = request.args.get("url")
    urlInfo = tldextract.extract(url)
    domain = urlInfo.domain +'.' + urlInfo.suffix
    print(domain)

    # check domain is present in the our graph
    objectIsPresent = blazegraph.checkForSubject(domain)

    # if not present, add info to that graph
    isPresentInDBPedia = False
    # get domain information using alexa api
    if objectIsPresent == False:
        comp_info = alexa.alexa(domain)
        
        # to add create info into rdf.
        blazegraph.add_companyInfo(comp_info)

        # delete if NaN is present
        blazegraph.deleteNaN()

        # get complete URL and connect with DBPedia
        # check info is present in DBPedia
        isPresentInDBPedia = dbpedia.IsInfoInDBPedia(comp_info[0])  
    else:
        # get company information from our triple store
        blazegraph.select(subject_m=domain, predicate_m = 'hasAdultContent')

    if isPresentInDBPedia:
        # get company name 
        companyTitle = blazegraph.getCompanyName(domain)
        #companyNameInDBPedia = "http://dbpedia.org/page/" + "Google"#comp_info
        
        blazegraph.sameAs(domain, companyTitle)

    return jsonify(request.url)

if __name__ == "__main__":  
    app.run(debug=True)






