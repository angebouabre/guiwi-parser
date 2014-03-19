from parser import *
    
    
dossier = '/home/bouable/workspace/project/sfr/neufbox-evol/integration/testi/fusion/13.2.20/2014/3/19/'

pk_mesure = 1
pk_scenario = 1
pk_theme = 1
pk_test = 1
pk_mesure =1

for fic in os.listdir(dossier):
    fic = os.path.join(dossier,fic)
    
    for fic_gen in os.listdir("/home/bouable/workspace/project/sfr/neufbox-evol/integration/testi/guiwi-parser/fixture"):
        if "scenario" in fic_gen:
            pk_scenario += 1
        if "theme" in fic_gen:
            pk_theme += 1
        if "test" in fic_gen:
            pk_test += 1
        if "mesure" in fic_gen:
            pk_mesure += 1
    
    f=WitbeLogFile(fic, pk_mesure, pk_scenario, pk_test, pk_theme)
