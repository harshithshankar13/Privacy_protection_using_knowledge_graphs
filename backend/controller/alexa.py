from flask import Blueprint, abort
import requests 
import xmltodict, json

alexa = Blueprint('alexa', __name__,
                        template_folder='templates')

def alexa(domain):
        
    # request alexa for company information
    #set header
    header = {'Authorization': "AWS4-HMAC-SHA256",
              'Credential':'<COGNITO_STS_ACCESS_KEY>/20190129/us-east-1/execute-api/aws4_request, SignedHeaders=host;x-amz-date, Signature=<GENERATED_AUTH_V4_SIGNATURE>Content-Type: application/xml',
              'X-Amz-Date': '20190129T043159Z',
              'x-api-key': 'R8rDWfkl5H6eh0LWnkbdzIn0l1XjO5x6kU2QsHy7',
              'x-amz-security-token': '<COGNITO_STS_SECURITY_TOKEN>'}
    
    # make get request
    res = requests.get('https://awis.api.alexa.com/api?Action=UrlInfo&ResponseGroup=SiteData,Rank,UsageStats,Categories,AdultContent&Url='+domain, headers=header)
    
    # convert response xml into json
    res_dict = xmltodict.parse(res.text)
    res_json = json.dumps(res_dict)

    return res_json


    