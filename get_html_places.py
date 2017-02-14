import requests
import re
import string
import json
import os
import time
import math
from bs4 import BeautifulSoup
import sys

# gets .json file, return list of id's by key = 'id'
def get_list_of_ids(file, key):
    f = open(file)
    id_list = []
    for line in f:
        cur_len = len(json.loads(line)[key])
        for i in range(cur_len):
            # print type(json.loads(line)['organizations'][i]['id'])
            cur_id = json.loads(line)[key][i]['id']
            # print cur_id
            id_list.append(cur_id)
    print 'id_list created', len(id_list)
    return id_list


# already done, download html, extact
def get_og_data(document):
    soup = BeautifulSoup(document.text, 'html.parser')
    
    og_data = {}
    try:
        og_data['description'] = soup.find("meta", property="og:description")['content']
    except:
        pass
    try:
        og_data['title'] = soup.find("meta", property="og:title")['content']
    except:
        pass
    try:
        og_data['latitude'] = soup.find("meta", property="og:latitude")['content']
    except:
        pass
    try:
        og_data['longitude'] = soup.find("meta", property="og:longitude")['content']
    except:
        pass
    try:
        og_data['street-address'] = soup.find("span", class_="street-address").text.strip()
    except:
        pass
    try:
        og_data['street-address2'] = soup.find("span", class_="street-address2").text.strip()
    except:
        pass
    try:
        og_data['city'] = soup.find("span", class_="locality").text.strip()
    except:
        pass
    try:
        og_data['state'] = soup.find("span", class_="region").text.strip()
    except:
        pass
    try:
        og_data['zip_code'] = soup.find("span", class_="postal-code").text.strip()
    except:
        pass
    try:
        og_data['country'] = soup.find("meta", property="og:country-name")['content']
    except:
        pass

    return json.dumps(og_data)



def get_and_save_og(id):
    filename = str(id) + ".json"
    # ask why it's not working
    # here = os.path.dirname(os.path.realpath(__file__))
    # here = os.path.abspath(os.path.dirname(sys.argv[1]))
    here = '/home/vagrant/src/project'
    # =======================================================================
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!! CHANGE SUBDIR!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # =======================================================================
    here = '/home/vagrant/src/project'
    subdir = "org_json"
    try:
        os.makedirs(subdir)
    except:
        pass
    filepath = os.path.join(here, subdir, filename)
    outfile = open(filepath, 'w')
    url = 'https://www.volunteermatch.org/search/org{}.jsp'.format(id)

    document = requests.get(url)
    if url == document.url:
        og_data = get_og_data(document)
    else:
        og_data = "no longer available"

    outfile.write(og_data)
    outfile.close()


organizations_ids = get_list_of_ids('organizations.json', 'organizations')

# organizations_ids = [100592]


# ================= loop through list of id's, create url
# ================= fetch it and save needed part of html like json
for id in organizations_ids:
    print id
    # time.sleep(1)
    get_and_save_og(id)
    print "saved {}".format(id)
