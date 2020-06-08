# This file contains privacyMetric calculation

import whois
import datetime

# calculating privacy score
def calculatePrivacyScore(m_websiteInfo):
    # initialise privacy score
    privacyScore = 0 

    # 1. score based on location @@ implement ++++++++++++++++++++++++++++++++++++++++++++++++++++++
    websiteDomainLocation = m_websiteInfo[8]
    # @@to-do get user location and compare

    # 2. score based on ranking @ but ranking changes daily in alexa but here rank stored is static +++++++++
    if m_websiteInfo[6] > 100000:
        privacyScore += 1 # 100% privacy score
    elif m_websiteInfo[6] > 75000 and m_websiteInfo[6] < 100000:
        privacyScore += 0.9
    elif m_websiteInfo[6] > 50000 and m_websiteInfo[6] < 75000:
        privacyScore += 0.8
    elif m_websiteInfo[6] > 25000 and m_websiteInfo[6] < 50000:
        privacyScore += 0.7
    elif m_websiteInfo[6] > 10000 and m_websiteInfo[6] < 25000:
        privacyScore += 0.6
    elif m_websiteInfo[6] > 7500 and m_websiteInfo[6] < 10000:
        privacyScore += 0.5
    elif m_websiteInfo[6] > 5000 and m_websiteInfo[6] < 7500:
        privacyScore += 0.4
    elif m_websiteInfo[6] > 3000 and m_websiteInfo[6] < 5000:
        privacyScore += 0.3
    elif m_websiteInfo[6] > 1000 and m_websiteInfo[6] < 3000:
        privacyScore += 0.2
    elif m_websiteInfo[6] > 500 and m_websiteInfo[6] < 1000:
        privacyScore += 0.1

    # 3. score based on adult content ++++++++++++++++++++++++++++++++++++
    if m_websiteInfo[3] == 'yes':
        privacyScore += 1.0

    # 4. score based on website type @@TODO add more companyType +++++++++++++++++++++++++++
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

    # 5. score based on website age ++++++++++++++++++++++++++++++++++++
    # calculate website's age
    websiteAge = datetime.datetime.now() - m_websiteInfo[7]
    # assign privacy score
    if websiteAge <= datetime.timedelta(weeks=52):
        privacyScore += 0.8
    
    return privacyScore