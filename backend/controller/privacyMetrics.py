# This file contains privacyMetric calculation

import whois
import datetime

# calculating privacy score
def calculatePrivacyScore(m_websiteInfo, m_userInfo):
    # initialise privacy score
    privacyScore = 0 
    factorsUsed = 0

    # score based on website's protocol ++++++++++++++++++++++
    if m_websiteInfo[9] == "http":
        factorsUsed += 1
        privacyScore = factorsUsed
    else:
        # 1. score based on location @@ implement ++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # adding user details location into userProfileLocation list
        userProfileLocation = []
        print("test1:", type(m_userInfo['userProfile']))
        userProfileLocation.append(m_userInfo['userProfile']['nationality'])
        for edu in m_userInfo['userProfile']['EducationDetails']:
            userProfileLocation.append(edu['Location'])
        for prof in m_userInfo['userProfile']['ProfessionalExpirenceDetails']:
            userProfileLocation.append(prof['Location'])
        
        print("userprofileLocationList: ", userProfileLocation)

        websiteDomainLocation = m_websiteInfo[8]
        if (websiteDomainLocation != None and m_userInfo['websitevisitedcountry'] != None and userProfileLocation is not None):
            print("location mataching : ", m_userInfo['websitevisitedcountry'], websiteDomainLocation)

            if m_userInfo['websitevisitedcountry'] in userProfileLocation:
                if m_userInfo['websitevisitedcountry'] == websiteDomainLocation:
                    factorsUsed += 1
                    privacyScore += 0
                elif m_userInfo['websitevisitedcountry'] in userProfileLocation:
                    factorsUsed += 1
                    privacyScore += 0.3
            elif m_userInfo['websitevisitedcountry'] != websiteDomainLocation:
                print("No connection between websitevisitedcountry")
                factorsUsed += 1
                privacyScore += 0.4
                
        # 2. score based on ranking @ but ranking changes daily in alexa but here rank stored is static +++++++++
        if m_websiteInfo[6] != None:
            factorsUsed += 1
            if float(m_websiteInfo[6]) > 100000:
                privacyScore += 1 # 100% privacy score
            elif float(m_websiteInfo[6]) > 75000 and float(m_websiteInfo[6]) < 100000:
                privacyScore += 0.9
            elif float(m_websiteInfo[6]) > 50000 and float(m_websiteInfo[6]) < 75000:
                privacyScore += 0.8
            elif float(m_websiteInfo[6]) > 25000 and float(m_websiteInfo[6]) < 50000:
                privacyScore += 0.7
            elif float(m_websiteInfo[6]) > 10000 and float(m_websiteInfo[6]) < 25000:
                privacyScore += 0.6
            elif float(m_websiteInfo[6]) > 7500 and float(m_websiteInfo[6]) < 10000:
                privacyScore += 0.5
            elif float(m_websiteInfo[6]) > 5000 and float(m_websiteInfo[6]) < 7500:
                privacyScore += 0.4
            elif float(m_websiteInfo[6]) > 3000 and float(m_websiteInfo[6]) < 5000:
                privacyScore += 0.3
            elif float(m_websiteInfo[6]) > 1000 and float(m_websiteInfo[6]) < 3000:
                privacyScore += 0.2
            elif float(m_websiteInfo[6]) > 500 and float(m_websiteInfo[6]) < 1000:
                privacyScore += 0.1

        # 3. score based on adult content ++++++++++++++++++++++++++++++++++++
        if m_websiteInfo[3] != None:
            factorsUsed += 1
            if m_websiteInfo[3] == 'yes':
                privacyScore += 1.0

        # 4. score based on website type @@TODO add more companyType +++++++++++++++++++++++++++
        
        if m_websiteInfo[4] != None:
            factorsUsed += 1
            # get website general type which is before / @@todo chaange this to some generatilation
            m_websiteInfo[4] = m_websiteInfo[4].split('/')[0] 

            if m_websiteInfo[4] == "Search Engines":
                privacyScore += 0.1
            elif m_websiteInfo[4] == "Shopping":
                privacyScore += 0.5
            elif m_websiteInfo[4] == "Social Networking":
                privacyScore += 0.7
            elif m_websiteInfo[4] == "Financial Services":
                privacyScore += 0.1
            elif m_websiteInfo[4] == "Banks":
                privacyScore += 0.1
            elif m_websiteInfo[4] == "Holding Companies":
                privacyScore += 0.2
            elif m_websiteInfo[4] == "Information Services":
                privacyScore += 0.8
            elif m_websiteInfo[4] == "Library Services":
                privacyScore += 0.8
            elif m_websiteInfo[4] == "Tools":
                privacyScore += 0.7
            elif m_websiteInfo[4] == "Chats":
                privacyScore += 0.7
            elif m_websiteInfo[4] == "Instructional Technology":
                privacyScore += 0.3
            elif m_websiteInfo[4] == "Open Source":
                privacyScore += 0.8
            elif m_websiteInfo[4] == "Resources":
                privacyScore += 0.8

        # 5. score based on website age ++++++++++++++++++++++++++++++++++++
        # calculate website's age
        if m_websiteInfo[7] != None:
            factorsUsed += 1
            websiteAge = datetime.datetime.now() - datetime.datetime.strptime(m_websiteInfo[7], '%Y-%m-%d %H:%M:%S') # 
            print("website Age: ", websiteAge)
            
            # assign privacy score
            if websiteAge <= datetime.timedelta(weeks=52):
                privacyScore += 0.8
        
        # 6. score based on user's visit count to the domain ++++++++++++++++++++++++++++++++++++
        if "domainVisitCount" in m_userInfo:
            factorsUsed += 1
            if m_userInfo["domainVisitCount"] == 0:
                privacyScore += 0.8
            elif m_userInfo["domainVisitCount"] <= 10:
                privacyScore += 0.6
            elif m_userInfo["domainVisitCount"] <= 15:
                privacyScore += 0.4
            elif m_userInfo["domainVisitCount"] <= 50:
                privacyScore += 0.2

    return ( privacyScore / factorsUsed) # only average is considered @@todo consider weighted average