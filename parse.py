from parser import *
import os
import shutil
    
    
dossier = '/home/bouable/workspace/project/sfr/neufbox-evol/integration/testi/fusion/13.2.20/2014/4/3/'

pk_scenario = 1
pk_theme = 1
pk_test = 1
pk_campagne = 15 
pk_mesure = 1  

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
    if "theme" in fic_gen:
        pk_theme += 1
    if "test" in fic_gen:
        pk_test += 1
    if "mesure" in fic_gen:
        pk_mesure += 1

shutill.rmtree()
os.makedirs(fixture)
os.makedirs(fixture+'/principal')

print pk_campagne
print pk_theme
print pk_scenario
print pk_test
print pk_mesure
