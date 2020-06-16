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
    
    # testing @@
    #print("Result &&& : ", res.text)

    # convert response xml into dict
    res_dict = xmltodict.parse(res.text)
    #res_json = json.dumps(res_dict)

    # call awis_json_parser
    #awis_json_parser_pp(res_dict)

    return awis_json_parser_pp(res_dict)

# custom function which takes all the releant information from the Alexa web information response json
def awis_json_parser_pp(awis_json_m):

    companyName = CompanyTitle = CompanyDescription = hasAdultContent = companyType = websiteMainActivity = websiteRank = 'NaN'

    # contains all the results
    Awis = awis_json_m.get('Awis') 
    if Awis != None:
        Results = Awis.get('Results')
        
        if Results != None:
            Result = Results.get('Result')
            if Result != None:
                Alexa = Result.get('Alexa')
                if Alexa != None:
                    ContentData = Alexa.get('ContentData')
                    if ContentData != None:
                        companyName = ContentData.get('DataUrl') or 'NaN'
                        hasAdultContent = ContentData.get('AdultContent') or 'NaN'
                        SiteData = ContentData.get('SiteData')
                        if SiteData != None:
                            CompanyTitle = SiteData.get('Title') or 'NaN'
                            CompanyDescription = SiteData.get('Description') or 'NaN'
                            websiteCreated = SiteData.get('OnlineSince') or 'NaN'
                            

                    CompanyCategory = Alexa.get('Related')
                    if CompanyCategory != None:
                        Categories = CompanyCategory.get('Categories') 
                        if Categories != None:
                            CategoryData = Categories.get('CategoryData')
                            if CategoryData != None:
                                if len(CategoryData) > 1:
                                    companyType = CategoryData[0].get('Title') or 'NaN'
                                    websiteMainActivity = CategoryData[1].get('Title') or 'NaN'
    

                    usageStats = Alexa.get('TrafficData')
                    if usageStats != None:
                        websiteRank = usageStats.get('Rank') or 'NaN'

    #@@todo use data - alexa gives the usage statistic using 3 months, 1 months, 7 days and 1 day of analysis

    return companyName, CompanyTitle, CompanyDescription, hasAdultContent, companyType, websiteMainActivity, websiteRank, websiteCreated