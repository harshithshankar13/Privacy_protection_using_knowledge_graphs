# Personal data privacy protection using knowledge graph

In this information era, data is considered as the new oil of the 21st
century. Data is misused by organizations or countries for economic
or political gain. The potential damage due to personal data privacy
breach can be controlled at a political, social, and technological level.
This research aims to provide a technical solution to evaluate and
warn the user of a potential data breach via a software plugin which
uses semantic web technologies and knowledge graphs.

This project aims to build a software that analyses the privacy risk of
visiting and entering data into the website by considering the user's
relationship with the organization and user-entered data into the web-
site. This software generates a data sensitivity metric of the data
entered and a privacy risk score associated with the website. Based
on the sensitivity metric/privacy risk score, the user will be warned
about the potential privacy risk via a software plugin in their web
browser.

The user's relationship with the organization is analysed based on
two sources, one is from the organisation's knowledge graph and an-
other is from the user profile. The organisation's knowledge graph has
knowledge about its website's category, web traffic rate, website's age,
presence of adult content and its physical presence. The user profile
has information such as nationality, date of birth, education details,
professional experience details and user's browsing history. Among
all these data, connection with respect to their physical location and
their history impact the most, and additionally website's web traffic,
website's age and website's category are major factors to be used to
assess the privacy risk to the user.

The code in this repository has two folders

* Plugin: This folder has a Google chrome extension software code which is
written in the JavaScript programming language. (client)

* Backend: This folder has ask-based backend software code which is written in the python programming language. (Server)

To test the approach and the developed framework, testing is done by 7 participants. 
Folder "Survey_feedback" has data files which consist of privacy risk score feedback by
the participants.
