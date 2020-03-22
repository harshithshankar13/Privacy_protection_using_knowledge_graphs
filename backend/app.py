from flask import Flask, request, jsonify, after_this_request

app = Flask(__name__)

@app.route('/')
def index():
    return "privary matters"

@app.route('/getUrl', methods=["POST","GET"])
def getUrl():
    if request.method == "POST":
        url = request.form["url"]
        return f"<h1>{request.url}<h1>"
    else:
        return f"<h1>{request.url}<h1>"

@app.route('/hello', methods=['GET'])
def hello():
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    jsonResp = {'jack': 4098, 'sape': 4139}
    
    print(request.args.get("url"))

    return jsonify(request.url)

if __name__ == "__main__":  
    app.run(debug=True)