from parser import *
import os
import shutil
    
    
<<<<<<< HEAD
dossier = '/home/bouable/workspace/project/sfr/neufbox-evol/integration/testi/fusion/14.1.2/2014/4/12/'
=======
dossier = '/home/bouable/sfr-workspace/fusion/13.2.19/2014/3/6'
>>>>>>> bafbefa0a53bfdee823041dbf6a5ac328de01053

#TODO Get the last pk in database fo fill these initials values
pk_scenario = 1
pk_version = 2
pk_theme = 1
pk_test = 1
<<<<<<< HEAD
pk_campagne = 14 
pk_mesure = 8275 
pk_version = 3 
#
scenario_range = []
theme_range = []
test_range = []
campagne_range = []
mesure_range = []
=======
pk_campagne = 9 
pk_mesure = 2312  

tab_campagne = []
tab_scenario = []
tab_theme = []
tab_test = []
tab_mesure = []
>>>>>>> bafbefa0a53bfdee823041dbf6a5ac328de01053

for fic in os.listdir(dossier):
    fic = os.path.join(dossier,fic)
    f = WitbeLogFile(fic)
    res_campagne = f.serialize_campagne(pk_campagne)
    res_version = f.serialize_version(pk_version)
    if res_campagne == True:
        pk_campagne += 1
        tab_campagne.append(pk_campagne)
    res_scenario = f.serialize_scenario(pk_scenario)
    if res_scenario == True:
        pk_scenario += 1
<<<<<<< HEAD
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
=======
        tab_scenario.append(pk_scenario)
    res_theme = f.serialize_theme(pk_theme)
    if res_theme == True:
        pk_theme += 1
        tab_theme.append(pk_theme)
    res_test = f.serialize_test(pk_test)
    if res_test == True:
        pk_test += 1
        tab_test.append(pk_test)
    res_mesure = f.serialize_mesure(pk_mesure)
    if res_mesure == True:
        pk_mesure += 1 
        tab_mesure.append(pk_mesure)

print tab_campagne
print tab_scenario
print tab_theme
print tab_test
print tab_mesure


#shutill.rmtree()
#os.makedirs(fixture)
#os.makedirs(fixture+'/principal')
>>>>>>> bafbefa0a53bfdee823041dbf6a5ac328de01053
