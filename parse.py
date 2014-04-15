from parser import *
import os
import shutil
    
    
dossier = '/home/bouable/workspace/project/sfr/neufbox-evol/integration/testi/fusion/14.1.2/2014/4/12/'

#TODO Get the last pk in database fo fill these initials values
pk_scenario = 1
pk_theme = 1
pk_test = 1
pk_campagne = 14 
pk_mesure = 8275 
pk_version = 3 
#
scenario_range = []
theme_range = []
test_range = []
campagne_range = []
mesure_range = []

for fic in os.listdir(dossier):
    fic = os.path.join(dossier,fic)
    f = WitbeLogFile(fic)
    f.serialize_scenario(pk_scenario)
    f.serialize_theme(pk_theme)
    f.serialize_test(pk_test)
    f.serialize_mesure(pk_mesure)
    
fixture = "/home/bouable/workspace/project/sfr/neufbox-evol/integration/testi/guiwi-parser/fixture"

for fic_gen in os.listdir(fixture):
    
    if "scenario" in fic_gen:
        pk_scenario += 1
        scenario_range.append(pk_scenario)
    if "theme" in fic_gen:
        pk_theme += 1
        theme_range.append(pk_theme)
    if "test" in fic_gen:
        pk_test += 1
        test_range.append(pk_test)

shutil.rmtree(fixture)
os.makedirs(fixture)
os.makedirs(fixture+'/todo')

print mesure_range
for fic in os.listdir(dossier):
    fic = os.path.join(dossier,fic)
    f = WitbeLogFile(fic)
    f.serialize_scenario(pk_scenario)
    f.serialize_theme(pk_theme)
    f.serialize_test(pk_test)
    f.serialize_version(pk_version)
    f.serialize_campagne(pk_campagne)
    f.serialize_mesure(pk_mesure)
    pk_mesure += 1
