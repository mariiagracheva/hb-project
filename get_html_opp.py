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
# ====== default version ======================
# def get_list_of_ids(file, key):
#     f = open(file)
#     id_list = []
#     for line in f:
#         cur_len = len(json.loads(line)[key])
#         for i in range(cur_len):
#             # print type(json.loads(line)['organizations'][i]['id'])
#             cur_id = json.loads(line)[key][i]['id']
#             # print cur_id
#             id_list.append(cur_id)
#     print 'id_list created', len(id_list)
#     return id_list

def get_list_of_ids(file):
    lst_opp = []
    for line in open(file):
        lst_opp.append(line.rstrip())
    return lst_opp


# already done, download html, extact
def get_og_data(document):
    soup = BeautifulSoup(document.text, 'html.parser')

    og_data = {}
    try:
        og_data['opp_time'] = soup.find("span", class_="left").text.strip()
    except:
        pass
    # try:
    #     og_data['opp_type'] = soup.find("meta", property="og:title")['content']
    # except:
    #     pass
    # try:
    #     og_data['cause'] = soup.find("meta", property="og:type")['content']
    # except:
    #     pass
    # try:
    #     og_data['description'] = soup.find("meta", property="og:description")['content']
    # except:
    #     pass
    # try:
    #     og_data['title'] = soup.find("meta", property="og:title")['content']
    # except:
    #     pass
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
    # try:
    #    og_data['country'] = soup.find("meta", property="og:country-name")['content']
    # except:
    #     pass
    return json.dumps(og_data)



def get_and_save_og(id):
    filename = str(id) + ".json"
    # ask why it's not working
    # here = os.path.dirname(os.path.realpath(__file__))
    # here = os.path.abspath(os.path.dirname(sys.argv[1]))
    
    # =======================================================================
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!! CHANGE SUBDIR!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # =======================================================================
    here = '/home/vagrant/src/hb-project/tmp'
    subdir = 'opp_html'
    try:
        os.makedirs(subdir)
    except:
        pass
    filepath = os.path.join(here, subdir, filename)
    outfile = open(filepath, 'w')
    url = 'https://www.volunteermatch.org/search/opp{}.jsp'.format(id)

    document = requests.get(url)
    if url == document.url:
        og_data = get_og_data(document)
    else:
        og_data = "no longer available"

    outfile.write(og_data)
    outfile.close()


opportunities_ids = get_list_of_ids('tmp/opp_ids.txt')

# opportunities_ids = [2592295]


# ================= loop through list of id's, create url
# ================= fetch it and save needed part of html like json
for id in opportunities_ids:
    print id
    # time.sleep(1)
    get_and_save_og(id)
    print "saved {}".format(id)
