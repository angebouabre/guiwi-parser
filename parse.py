from parser import *
import os
import shutil
from utils import *
from parsersettings import *
from datetime import date, timedelta

db = "/home/bouable/workspace/project/sfr/neufbox-evol/integration/testi/guiwi/witbe/ti.db"
user = "bouable"

tb_projet = "stbattack_projet"
tb_version = "stbattack_version"
tb_campagne = "stbattack_campagne"
tb_scenario = "stbattack_scenario"
tb_theme = "stbattack_theme"
tb_test = "stbattack_test"
tb_mesure = "stbattack_mesure"

pk = get_last_pk_sqlite

yest = date.today() - timedelta(days=1)
yest = yest.strftime("%m/%d").replace("0","")

yest = "4/29"

dossier = '/home/bouable/workspace/project/sfr/neufbox-evol/integration/testi/fusion/14.1.2/2014/%s' % yest

#TODO Get the last pk in database fo fill these initials values
pk_scenario = pk(db, tb_scenario) + 1
pk_version = pk(db, tb_version) + 1
pk_theme = pk(db, tb_theme) + 1
pk_test = pk(db, tb_test) + 1
pk_campagne = pk(db, tb_campagne) + 1 
pk_mesure = pk(db, tb_mesure) + 1 

for fic in os.listdir(dossier):
    fic = os.path.join(dossier,fic)
    f = WitbeLogFile(fic)
    res_campagne = f.serialize_campagne(pk_campagne)
    res_version = f.serialize_version(pk_version)
    if res_campagne == True:
        pk_campagne += 1
    res_scenario = f.serialize_scenario(pk_scenario)
    if res_scenario == True:
        pk_scenario += 1
    res_theme = f.serialize_theme(pk_theme)
    if res_theme == True:
        pk_theme += 1
    res_test = f.serialize_test(pk_test)
    if res_test == True:
        pk_test += 1
    res_mesure = f.serialize_mesure(pk_mesure)
    if res_mesure == True:
        pk_mesure += 1 
try:
    os.makedirs('fixture/todo')
except:
    pass
#shutill.rmtree()
#os.makedirs(fixture)
