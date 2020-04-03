'''
This file is the starting point of this flash server.

Apenx:
    @@ means todo

'''

from flask import Flask, request, jsonify, after_this_request
import tldextract   # to extract the domain name from url

import controller.alexa as alexa
import controller.blazeGraph as blazegraph

app = Flask(__name__)

@app.route('/')
def index():
    return "privary matters"

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

    #@@ get complete URL 
    #@@ check domain is present in the our graph
    objectIsPresent = blazegraph.checkForObject(domain)

    # get domain information using alexa api
    if objectIsPresent == False:
        # com_info = alexa(domain)
        print(alexa.alexa(domain))
        # print("alexa: ", com_info)

        #@@ if not, add info to that graph
        #@@ to add create info into rdf.


    return jsonify(request.url)

if __name__ == "__main__":  
    app.run(debug=True)






