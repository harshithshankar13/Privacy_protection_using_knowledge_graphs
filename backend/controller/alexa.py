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
    
    # convert response xml into dict
    res_dict = xmltodict.parse(res.text)
    #res_json = json.dumps(res_dict)

    # call awis_json_parser
    #awis_json_parser_pp(res_dict)

    return awis_json_parser_pp(res_dict)

# custom function which takes all the releant information from the Alexa web information response json
def awis_json_parser_pp(awis_json_m):

    # contains all the results
    results = awis_json_m['Awis']['Results']
    
    ContentData = results['Result']['Alexa']['ContentData']
    companyName = ContentData['DataUrl']
    CompanyTitle = ContentData['SiteData']['Title']
    CompanyDescription = ContentData['SiteData']['Description']
    hasAdultContent = ContentData['AdultContent']

    CompanyCategory = results['Result']['Alexa']['Related']
    companyType = CompanyCategory['Categories']['CategoryData'][0]['Title']
    companyLocation = CompanyCategory['Categories']['CategoryData'][1]['Title']

    usageStats = results['Result']['Alexa']['TrafficData']
    websiteRank = usageStats['Rank']

    #@@todo use data - alexa gives the usage statistic using 3 months, 1 months, 7 days and 1 day of analysis

    print(companyName, CompanyTitle, CompanyDescription, hasAdultContent, companyLocation, companyType, websiteRank)

    return companyName, CompanyTitle, CompanyDescription, hasAdultContent, companyLocation, companyType, websiteRank