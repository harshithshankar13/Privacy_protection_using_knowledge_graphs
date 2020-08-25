# This file contains privacyMetric calculation

import whois
import tldextract 
import datetime

# calculating privacy score
def calculatePrivacyScore(m_websiteInfo, m_userInfo):
    # initialise privacy score
    privacyScore = 0 
    factorsUsed = 0
    reasons = "<br>"

    # user profile white list urls
    userProfileWhiteListURLs = []
    if 'EducationDetails' in m_userInfo['userProfile']:
        for edu in m_userInfo['userProfile']['EducationDetails']:
            userProfileWhiteListURLs.append(edu['InstituteURL'])
    if 'ProfessionalExpirenceDetails' in m_userInfo['userProfile']:
        for prof in m_userInfo['userProfile']['ProfessionalExpirenceDetails']:
            userProfileWhiteListURLs.append(prof['CompanyURL'])
    #++++++++++++++++++++++++++++

    # score based on website's protocol ++++++++++++++++++++++
    if m_websiteInfo[9] == "http":
        factorsUsed += 1
        privacyScore = 1
        reasons += "This website doesn't use secure protocol (Used protocol is http)."
    else:
        # 1. score based on location @@ implement ++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # adding user details location into userProfileLocation list
        userProfileLocation = []
        print("test1:", type(m_userInfo['userProfile']))
        if 'nationality' in m_userInfo['userProfile']:
            userProfileLocation.append(m_userInfo['userProfile']['nationality'])
        if 'EducationDetails' in m_userInfo['userProfile']:
            for edu in m_userInfo['userProfile']['EducationDetails']:
                userProfileLocation.append(edu['Location'])
        if 'ProfessionalExpirenceDetails' in m_userInfo['userProfile']:
            for prof in m_userInfo['userProfile']['ProfessionalExpirenceDetails']:
                userProfileLocation.append(prof['Location'])
        
        print("userprofileLocationList: ", userProfileLocation)

        # take only location for comparsion
        
        if (m_websiteInfo[8] != None and m_userInfo['websitevisitedcountry'] != None and userProfileLocation is not None):
            websiteDomainLocation = m_websiteInfo[8].split('/')[-1]
            if websiteDomainLocation =="NaN" :
                factorsUsed += 1
                privacyScore += 0.8
                reasons += "Not enough information about company's physical presence."
                reasons += "<br>"
                print("location mataching : ", m_userInfo['websitevisitedcountry'], websiteDomainLocation)
            elif m_userInfo['websitevisitedcountry'] == websiteDomainLocation:
                if websiteDomainLocation in userProfileLocation:
                    factorsUsed += 1
                    privacyScore += 0
                    reasons += "There is a match in user's browsering location and company's location"
                else:
                    factorsUsed += 1
                    privacyScore += 0.4
                    reasons += "There is a connection between user profile location and website but no collection between user's browsering location and company's location"
            else:
                if websiteDomainLocation in userProfileLocation:
                    factorsUsed += 1
                    privacyScore += 0.2
                    reasons += "Match in user's profile location and company's location but mismatch with user's browsing location"
                else:
                    factorsUsed += 1
                    privacyScore += 0.8
                    reasons += "There is no connection between user's and company's location"
            reasons += "<br>"
        else:
            factorsUsed += 1
            privacyScore += 0.8
            reasons += "Not enough information about company's physical presence."
            reasons += "<br>"
                
        # 2. score based on ranking @ but ranking changes daily in alexa but here rank stored is static +++++++++
        if m_websiteInfo[6] != None:
            factorsUsed += 1
            if float(m_websiteInfo[6]) > 100000:
                privacyScore += 1 # 100% privacy score
                reasons += "This website's traffic is very low"
            elif float(m_websiteInfo[6]) > 75000 and float(m_websiteInfo[6]) < 100000:
                privacyScore += 0.9
                reasons += "This website's traffic is very low"
            elif float(m_websiteInfo[6]) > 50000 and float(m_websiteInfo[6]) < 75000:
                privacyScore += 0.8
                reasons += "This website's traffic is very low"
            elif float(m_websiteInfo[6]) > 25000 and float(m_websiteInfo[6]) < 50000:
                privacyScore += 0.7
                reasons += "This website's traffic is very low"
            elif float(m_websiteInfo[6]) > 10000 and float(m_websiteInfo[6]) < 25000:
                privacyScore += 0.6
                reasons += "This website's traffic is low"
            elif float(m_websiteInfo[6]) > 7500 and float(m_websiteInfo[6]) < 10000:
                privacyScore += 0.5
                reasons += "This website's traffic is good"
            elif float(m_websiteInfo[6]) > 5000 and float(m_websiteInfo[6]) < 7500:
                privacyScore += 0.4
                reasons += "This website's traffic is very good"
            elif float(m_websiteInfo[6]) > 3000 and float(m_websiteInfo[6]) < 5000:
                privacyScore += 0.3
                reasons += "This website's traffic is high"
            elif float(m_websiteInfo[6]) > 1000 and float(m_websiteInfo[6]) < 3000:
                privacyScore += 0.2
                reasons += "This website's traffic is very high"
            elif float(m_websiteInfo[6]) > 500 and float(m_websiteInfo[6]) < 1000:
                privacyScore += 0.1
                reasons += "This website's traffic is sky-high"
            elif float(m_websiteInfo[6]) < 500:
                privacyScore += 0
                reasons += "This website's traffic is sky-high"
            reasons += "<br>"

        # 3. score based on adult content ++++++++++++++++++++++++++++++++++++
        if m_websiteInfo[3] != None:
            factorsUsed += 1
            #userAge = datetime.datetime.now() - datetime.datetime.strptime(m_userInfo['userProfile']['DOB'], '%Y-%m-%d')
            #print("Age:: ", userAge)
            if m_websiteInfo[3] == 'yes':
                if 'DOB' in m_userInfo['userProfile']:
                    if m_userInfo['userProfile']['DOB'] != None:
                        userAge = datetime.datetime.now() - m_userInfo['userProfile']['DOB']
                        if userAge <= datetime.timedelta(weeks=936):
                            privacyScore += 1.0
                            reasons += "This website may have an adult content and you are under 18 years."
                        else:
                            privacyScore += 0.8
                            reasons += "This website may have an adult content but you are over 18 years."
                    else:
                        privacyScore += 1.0
                        reasons += "This website may have an adult content."
            else:
                privacyScore += 0.0
                reasons += "This website doesn't contain an adult content"
            reasons += "<br>"

        # 4. score based on website type @@TODO add more companyType +++++++++++++++++++++++++++
        
        if m_websiteInfo[4] != None:
            factorsUsed += 1
            # get website general type which is before / @@todo chaange this to some generalisation
            m_websiteInfo[4] = m_websiteInfo[4].split('/')[0] 
            reasons += "This website belongs to " + m_websiteInfo[4] + " type."

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
                privacyScore += 0.5
            elif m_websiteInfo[4] == "Open Source":
                privacyScore += 0.8
            elif m_websiteInfo[4] == "Resources":
                privacyScore += 0.8
            elif m_websiteInfo[4] == "Employment":
                privacyScore += 0.5
            elif m_websiteInfo[4] == "Online Communities":
                privacyScore += 0.7
            elif m_websiteInfo[4] == "Video":
                privacyScore += 0.7
            elif m_websiteInfo[4] == "work":
                privacyScore += 0.5
        else:
            factorsUsed += 1
            privacyScore += 0.8
        reasons += "<br>"
            

        # 5. score based on website age ++++++++++++++++++++++++++++++++++++
        # calculate website's age
        if m_websiteInfo[7] != None:
            factorsUsed += 1
            websiteAge = datetime.datetime.now() - datetime.datetime.strptime(m_websiteInfo[7], '%Y-%m-%d %H:%M:%S') # 
            print("website Age: ", websiteAge)
            
            # assign privacy score
            if websiteAge <= datetime.timedelta(weeks=52): # 1 year = 52 weeks
                privacyScore += 0.8
                reasons += "This website's age is less than a year."
            else:
                privacyScore += 0.0
                reasons += "This website's age is more than a year."
            reasons += "<br>"

        # 6. score based on user's visit count to the domain ++++++++++++++++++++++++++++++++++++
        if "domainVisitCount" in m_userInfo:
            print("privacy score before domain visit: ", m_userInfo["domainVisitCount"] )
            factorsUsed += 1
            domainVisitCount = str(m_userInfo['domainVisitCount'])
            if m_userInfo["domainVisitCount"] == 0:
                privacyScore += 0.8
                reasons += "You visited this website " + domainVisitCount + " times in recent 3 months."
            elif m_userInfo["domainVisitCount"] <= 10:
                privacyScore += 0.6
                reasons += "You visited this website " + domainVisitCount + " times in recent 3 months."
            elif m_userInfo["domainVisitCount"] <= 15:
                privacyScore += 0.4
                reasons += "You visited this website " + domainVisitCount + " times in recent 3 months."
            elif m_userInfo["domainVisitCount"] <= 50:
                privacyScore += 0.2
                reasons += "You visited this website " + domainVisitCount + " times in recent 3 months."
            else:
                privacyScore += 0.0
                reasons += "You visited this website " + domainVisitCount + " times in recent 3 months."

            print("privacy score after domain visit: ", privacyScore)
            reasons += "<br>"

        
        # 7. score based on user History Website Type ++++++++++++++++++++++++++++++++++++
        if 'userHistoryWebsiteTypes' in m_userInfo['userProfile']:
            factorsUsed += 1
            if m_websiteInfo[4] == None:
                m_websiteInfo[4] = "others"
            if m_websiteInfo[4] in m_userInfo['userProfile']['userHistoryWebsiteTypes']:
                userHistoryWebsiteTypeFrequency = m_userInfo['userProfile']['userHistoryWebsiteTypes'][m_websiteInfo[4]]
        
                userHistoryWebsiteTypeFrequencyStr = str(userHistoryWebsiteTypeFrequency)
                
                if userHistoryWebsiteTypeFrequency == 0:
                    privacyScore += 0.8
                    reasons += "You visited this website type " + userHistoryWebsiteTypeFrequencyStr + " times in recent 3 months."
                elif userHistoryWebsiteTypeFrequency <= 10:
                    privacyScore += 0.6
                    reasons += "You visited this website type " + userHistoryWebsiteTypeFrequencyStr + " times in recent 3 months."
                elif userHistoryWebsiteTypeFrequency <= 15:
                    privacyScore += 0.4
                    reasons += "You visited this website type " + userHistoryWebsiteTypeFrequencyStr + " times in recent 3 months."
                elif userHistoryWebsiteTypeFrequency <= 50:
                    privacyScore += 0.2
                    reasons += "You visited this website type " + userHistoryWebsiteTypeFrequencyStr + " times in recent 3 months."
                else:
                    privacyScore += 0.0
                    reasons += "You visited this website type " + userHistoryWebsiteTypeFrequencyStr + " times in recent 3 months."

        print("privacy score after domain visit: ", privacyScore)
        reasons += "<br>"

        # calculate final privacy score
        finalPrivacyScore =  privacyScore / factorsUsed

        # 8. score based on user's white listed URL list ++++++++++++++++++++++++++++++++++++
        # get domain by removing www. in userProfileWhiteListURLs
        if m_websiteInfo[4] != None:
            if 'Trusted_' + m_websiteInfo[4] in m_userInfo['userProfile']:
                for domain in m_userInfo['userProfile']['Trusted_' + m_websiteInfo[4]]:
                    userProfileWhiteListURLs.append(domain)
        else:
            if 'Trusted_others' in m_userInfo['userProfile']:
                for domain in m_userInfo['userProfile']['Trusted_others']:
                    userProfileWhiteListURLs.append(domain)

        userProfileWhiteListDomains = []
        print("userProfileWhiteListURLs: ", userProfileWhiteListURLs)
        for url in userProfileWhiteListURLs:
            urlInfo = tldextract.extract(url)
            domainList = urlInfo.domain + "." + urlInfo.suffix
            userProfileWhiteListDomains.append(domainList )

        print("userProfileWhiteListDomains: ", userProfileWhiteListDomains)
        
        if m_websiteInfo[0] in userProfileWhiteListDomains:
            privacyScore = privacyScore/2
            reasons += "You are using a website that you trust. <br>"

    return finalPrivacyScore, reasons # only average is considered @@todo consider weighted average