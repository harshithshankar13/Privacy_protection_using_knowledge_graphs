'''
This file is the starting point of this flash server.

Apenx:
    @@ means todo

'''

from flask import Flask, request, jsonify, after_this_request, render_template
import tldextract   # to extract the domain name from url
import whois
import geocoder

import controller.alexa as alexa
import controller.blazeGraph as blazegraph
import controller.dbpedia as dbpedia
import controller.privacyMetrics as privacyMetrics

# from OpenSSL import SSL
# context = SSL.Context(SSL.PROTOCOL_TLSv1_2)
# context.use_privatekey_file('server.key')
# context.use_certificate_file('server.crt')

app = Flask(__name__)
#app.run('127.0.0.1', debug=True, port=5000, ssl_context=context)

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

    # get domain name from url ======= 
    url = request.args.get("url")
    urlInfo = tldextract.extract(url)
    domain = urlInfo.domain +'.' + urlInfo.suffix

    if domain in ['localhost']:
        # get user location from userLocation ======
        userLocationLat = request.args.get("userLocationLat")
        userLocationLong = request.args.get("userLocationLong")
        print(userLocationLat)
        print(userLocationLong)

        g = geocoder.osm([userLocationLat, userLocationLong], method='reverse')
        print(g.json['country'])
        userInfo = g.json['country']
        # check user's country is present in the dbpedia
        if dbpedia.IsInfoInDBPedia(userInfo):
            userInfo = 'http://dbpedia.org/resource/' + userInfo + '"'

        print(domain)

        # check domain is present in the our graph
        objectIsPresent = blazegraph.checkForSubject(domain)

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
                    print("websiteDate1:")
                    comp_info[7] = websiteInfoFromWhoIs.creation_date[1]
                else:
                    print("websiteDate2:")
                    comp_info[7] = websiteInfoFromWhoIs.creation_date
                    
            # to add create info into rdf.
            blazegraph.add_companyInfo(comp_info)

            # delete if NaN is present
            blazegraph.deleteNaN()
            
            # get complete URL and connect with DBPedia
            # check info is present in DBPedia
            isPresentInDBPedia = dbpedia.IsInfoInDBPedia(comp_info[1])  
            print("isPresentInDBPedia:", isPresentInDBPedia)
            
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
            comp_info.append(companyLoc)
            blazegraph.addCompanyLocation(domain, comp_info[8])
            print("companyLoc: ", comp_info[8])
            # --------
        else:
            # get company information from our triple store
            comp_info = blazegraph.getCompanyInfoInFormat(subject_m=domain)
            print("Company's information: ",comp_info)

        # get privacy score based on company Info @@to-do send this data to the client
        privacyScore = privacyMetrics.calculatePrivacyScore(comp_info, userInfo)
        print("privacyScore :", privacyScore)

        return jsonify({'privacyScore': privacyScore})

@app.route('/getRDF', methods=['GET','POST'])
def getRDF():
    print("RDF")
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    res = blazegraph.select_all()
    return jsonify(res)

@app.route('/userProfile', methods=['GET','POST'])
def getUserProfile():
    return render_template('userProfile.html')

if __name__ == "__main__":  
    app.run(debug=True)