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
    blazegraph.baseRules()
    return "privary matters :) \n The basic rules are set in your RDF Triple store."

@app.route('/privacyMetric', methods=['GET'])
def privacyMetric():
    
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
        isPresentInDBPedia = dbpedia.IsInfoInDBPedia(comp_info[1])  
        print("isPresentInDBPedia:", isPresentInDBPedia)
    else:
        # get company information from our triple store
        blazegraph.select(subject_m=domain)

    if isPresentInDBPedia:
        print("same")
        # get company name 
        companyTitle = blazegraph.getCompanyName(domain)
        
        blazegraph.sameAs(domain, companyTitle)

    return jsonify(request.url)

@app.route('/getRDF', methods=['GET','POST'])
def getRDF():
    print("RDF")
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    res = blazegraph.select_all()
    return jsonify(res)

if __name__ == "__main__":  
    app.run(debug=True)






