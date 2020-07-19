'''
This file is the starting point of this flash server.

Apenx:
    @@ means todo

'''

from flask import Flask, request, jsonify, after_this_request, render_template
import tldextract   # to extract the domain name from url
import whois
import geocoder
import pycountry
from geopy.geocoders import Nominatim
import requests
import json
import time
from datetime import datetime

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

@app.route('/privacyMetric', methods=['GET', 'POST'])
def privacyMetric():
    
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    # variable initialise
    userInfo = {}

    # get domain name from url ======= 
    url = request.form.get("url")
    protocol = url.split(':')[0]
    urlInfo = tldextract.extract(url)
    domain = urlInfo.domain +'.' + urlInfo.suffix

    if protocol == "chrome-extension":
        return jsonify({'privacyScore': 0, 'reasonForPrivacyScore': "This webpage is completely safe."})

    print("protocol: ", protocol)

    # get data from request
    userInfo['domainVisitCount'] = int(request.form.get("domainVisitCount"))

    # get user profile
    userProfile = request.form.get("userProfile")
    userInfo['userProfile'] = json.loads(userProfile)
    print("UserProfile: ", request.form.get("userProfile"))

    # initialising privacyScore Variable
    privacyScore = 0

    # flags
    calledWhois = False

    if domain not in ['localhost.']:
        # get user location from userLocation ======
        userLocationLat = request.form.get("userLocationLat")
        userLocationLong = request.form.get("userLocationLong")
        print(userLocationLat)
        print(userLocationLong)

        g = geocoder.osm([userLocationLat, userLocationLong], method='reverse')
        while g == None:
            time.sleep(2)
            g = geocoder.osm([userLocationLat, userLocationLong], method='reverse')
        print(g.json['country'])
        userInfo['websitevisitedcountry'] = g.json['country']
        # check user's country is present in the dbpedia
        if dbpedia.IsInfoInDBPedia(userInfo['websitevisitedcountry']):
            userInfo['websitevisitedcountry']  = userInfo['websitevisitedcountry']

        print(domain)

        # check domain is present in the our graph
        objectIsPresent = blazegraph.checkForSubject(domain)
        comp_info_score = []

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
                print("websiteInfoFromWhoIs:@: ",websiteInfoFromWhoIs)
                calledWhois = True
                if isinstance(websiteInfoFromWhoIs.creation_date, list):
                    print("websiteDate1:")
                    comp_info[7] = datetime.strftime(websiteInfoFromWhoIs.creation_date[1], "%Y-%m-%d %H:%M:%S")
                else:
                    print("websiteDate2:")
                    comp_info[7] = datetime.strftime(websiteInfoFromWhoIs.creation_date, "%Y-%m-%d %H:%M:%S")
                    
            # to add create info into rdf.
            blazegraph.add_companyInfo(comp_info)

            # delete if NaN is present
            blazegraph.deleteNaN()
            
            # get complete URL and connect with DBPedia
            # check info is present in DBPedia
            comp_info[1] = comp_info[1].replace('/', '')
            comp_info[1] = comp_info[1].replace(' ', '_')
            isPresentInDBPedia = dbpedia.IsInfoInDBPedia(comp_info[1])  
            print("isPresentInDBPedia:", isPresentInDBPedia)
            
            if isPresentInDBPedia:
                print("same")
                # get company name 
                #companyTitle = blazegraph.getCompanyName(domain)
                blazegraph.sameAs(domain, comp_info[1])

                # get company location information from dbpedia
                companyLoc = dbpedia.getCompanyLocation(comp_info[1])
                
                if companyLoc != None:
                    # convert company location into country
                    geoLocator = Nominatim(user_agent="privacyProtection")
                    companyLocForGeoCoder = companyLoc.split('/')[-1]
                    location = geoLocator.geocode(companyLocForGeoCoder)
                    companyLoc = location.raw['display_name'].split(" ")[-1]
                    print("location country 222", companyLoc)
            
            if isPresentInDBPedia == False or companyLoc == None:
                # get website domain reg. location using whois
                if calledWhois == False:
                    # get expiration location using whois
                    websiteInfoFromWhoIs = whois.whois(domain)
                    
                # websiteDomainCity = websiteInfoFromWhoIs.city
                # if websiteDomainCity != None: 
                #     print("Company location in app @1@: ", websiteInfoFromWhoIs)
                #     companyLoc = websiteDomainCity.replace(" ", "_")
                # else:
                websiteDomainCountry = websiteInfoFromWhoIs.country
                companyLoc = pycountry.countries.get(alpha_2=websiteDomainCountry)
                if companyLoc == None:
                    companyLoc = "NaN"
                else:
                    companyLoc = companyLoc.name
                    companyLoc = companyLoc.replace(" ", "_")

            # get company information from dbpedia
            print("Company location in app @@: ", companyLoc)
            comp_info.append(companyLoc)
            blazegraph.addCompanyLocation(domain, comp_info[8])
            print("companyLoc: ", comp_info[8])

            # add website protocol info to calculate privacy score
            comp_info.append(protocol)
            comp_info_score = comp_info 
            # --------
        else:
            # get company information from our triple store
            comp_info = blazegraph.getCompanyInfoInFormat(subject_m=domain)
            print("Company's information: ",comp_info)
            comp_info.append(protocol)
            comp_info_score = comp_info

        # get privacy score based on company Info @@to-do send this data to the client
        privacyScore, reasonForPrivacyScore = privacyMetrics.calculatePrivacyScore(comp_info, userInfo)
        print("privacyScore :", privacyScore)
        print("reasonForPrivacyScore :", reasonForPrivacyScore)

    return jsonify({'privacyScore': privacyScore, 'reasonForPrivacyScore': reasonForPrivacyScore})

################################################################################################
@app.route('/getRDF', methods=['GET','POST'])
def getRDF():
    print("RDF")
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    res = blazegraph.select_all()
    return jsonify(res)


################################################################################################
@app.route('/userProfile', methods=['GET','POST'])
def getUserProfile():
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
        
    LinkedInAUTHCode = request.args.get('code')

    print(LinkedInAUTHCode)

    res = requests.post("https://www.linkedin.com/oauth/v2/accessToken?grant_type=authorization_code&code="+ LinkedInAUTHCode + "&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2FuserProfile&client_id=77mpeeyrvnkjaa&client_secret=loIraKqPvMjE9fOe",
        headers = {
                "content-type": "x-www-form-urlencoded"
        })
    

    if res.ok:
        print('Access_token', res.json())
        linkedInAccessToken = res.json()['access_token']
        linkedInAccessTokenExpiresIn = res.json()['expires_in'] # @@todo time + expiresIn
    else:
        print(res.json())

    res1 = requests.get("https://api.linkedin.com/v2/me",
        headers = {
                "Authorization": "Bearer " + linkedInAccessToken,
                "connection" : "Keep-Alive"
        })

    if res1.ok:
        print('Access_token', res1.json())
    else:
        print(res1.json())

    #return render_template('userProfile.html')
    return 'OK'

if __name__ == "__main__":  
    app.run(debug=True)