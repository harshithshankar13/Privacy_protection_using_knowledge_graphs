'''
This file is the starting point of this flash server.

Apenx:
    @@ means todo

'''

from flask import Flask, request, jsonify, after_this_request
import tldextract   # to extract the domain name from url
import whois

import controller.alexa as alexa
import controller.blazeGraph as blazegraph
import controller.dbpedia as dbpedia
import controller.privacyMetrics as privacyMetrics

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

    # @@forTesting
    objectIsPresent = False

    # if not present, add info to that graph
    isPresentInDBPedia = False
    # get domain information using alexa api
    if objectIsPresent == False:
        comp_info = alexa.alexa(domain)
        
        comp_info = list(comp_info)
        # check if the website creation date is present
        if comp_info[7] == 'NaN':
            # get expiration date using whois
            websiteInfoFromWhoIs = whois.whois(domain)
            if isinstance(websiteInfoFromWhoIs.creation_date, list):
                comp_info[7] = websiteInfoFromWhoIs.creation_date[1]
            else:
                comp_info[7] = websiteInfoFromWhoIs.creation_date
                
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

        # get company location information from dbpedia
        companyLoc = dbpedia.getCompanyLocation(companyTitle)
    else:
        # get website domain reg. location using whois
        websiteDomainCountry = websiteInfoFromWhoIs.country
        websiteDomainState = websiteInfoFromWhoIs.state
        companyLoc = websiteDomainState + ", " + websiteDomainCountry

    # get company information from dbpedia
    comp_info[8] = companyLoc
    blazegraph.addCompanyLocation(domain, comp_info[8])
    print("companyLoc: ", comp_info[8])
    # --------

    # get privacy score based on company Info @@to-do send this data to the client
    privacyScore = privacyMetrics.calculatePrivacyScore(comp_info)

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