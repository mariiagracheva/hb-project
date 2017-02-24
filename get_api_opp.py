# 
# Getting data through VolunteerMatch API.
# organizations.json - all data about opportunities in SF
# 
# 
import random
import base64
import hashlib
import json
import requests
import os
from datetime import datetime

nonce = hashlib.sha1().hexdigest()
created = datetime.now().strftime("%Y-%m-%dT%H:%M:%S-0800")

Username="mariiagracheva"
Key="0b889c96111465444d53e3b71d5caba3"
PasswordDigest = base64.b64encode(hashlib.sha256((nonce+created+Key).encode('utf-8')).digest())
url = "https://www.volunteermatch.org/api/call"
ongoing = False
# # ======================== get oppotrunities ===================================
# outfile = open('tmp/opportunities.json', 'w')
# for i in range(1,40):
#     print i
#     query_params = {
#      "location" : "San Francisco",
#      "numberOfResults":20,
#      "pageNumber":i,
#      "fieldsToDisplay":[
#         'allowGroupInvitations',
#         'allowGroupReservation',
#         'availability',
#         'beneficiary categoryIds',
#         'contact',
#         'created',
#         'currentPage',
#         'description',
#         'greatFor',
#         'hasWaitList',
#         'id',
#         'imageUrl',
#         'location',
#         'minimumAge',
#         'numReferred',
#         'parentOrg',
#         'plaintextDescription',
#         'plaintextRequirements',
#         'plaintextSkillsNeeded',
#         'referralFields',
#         'requirements',
#         'requirementsMap',
#         'requiresAddress',
#         'resultsSize',
#         'skillsList',
#         'skillsNeeded',
#         'spacesAvailable',
#         'status',
#         'tags',
#         'title',
#         'trackedHours',
#         'type',
#         'updated',
#         'virtual',
#         'vmUrl',
#         'volunteersNeeded',
#         'name']
#     }

#     action_param = "searchOpportunities"

#     params = {"action": action_param, "query": json.dumps(query_params)}

#     custom_headers = {
#         "Authorization": 'WSSE profile="UsernameToken"',
#         "X-WSSE": u'UsernameToken Username="{}", \
#                 PasswordDigest="{}", \
#                 Nonce="{}", \
#                 Created="{}"'.format(Username, PasswordDigest, nonce, created)
#     }


#     r = requests.get(url, params=params, headers=custom_headers)
#     line = json.dumps(r.json())
#     outfile.write(line+'\n')

# outfile.close()





# ======================== get organizations ===================================
outfile = open('tmp/organizations.json', 'w')
for i in range(1,100):
    # with open('orgs.json', 'a') as outfile:

    query_params = {
     "location" : "San Francisco",
     "numberOfResults":20,
     "pageNumber":i,
     "fieldsToDisplay":['id',
    'name',
    'url',
    'location',
    'description',
    'plaintextDescription',
    'mission',
    'plaintextMission',
    'imageUrl',
    'created',
    'updated',
    'numReviews',
    'avgRating',
    'contact',
    'categoryIds',
    'vmUrl',
    'type',
    'ein',
    'classification']
    }

    action_param = "searchOrganizations"

    params = {"action": action_param, "query": json.dumps(query_params)}

    custom_headers = {
        "Authorization": 'WSSE profile="UsernameToken"',
        "X-WSSE": u'UsernameToken Username="{}", \
                PasswordDigest="{}", \
                Nonce="{}", \
                Created="{}"'.format(Username, PasswordDigest, nonce, created)
    }


    r = requests.get(url, params=params, headers=custom_headers)

    # with open('orgs.json', 'a') as outfile:
    #     json.dumps(r.json(), outfile)

    line = json.dumps(r.json())

    outfile.write(line+'\n')

outfile.close()

