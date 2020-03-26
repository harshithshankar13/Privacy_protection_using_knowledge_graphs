from flask import Flask, request, jsonify, after_this_request
import tldextract   # to extract the domain name from url

from controller.alexa import alexa

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

    # get domain information using alexa api
    com_info = alexa(domain)
    print("alexa: ", com_info)

    return jsonify(request.url)

if __name__ == "__main__":  
    app.run(debug=True)