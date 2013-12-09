#!/usr/bin/python
#-*-coding:utf-8-*-

import os
from datetime import datetime

def write_logs(logs, msg):
    """ Write msg in the logs file """
    logs = open(logs,'a')
    now = datetime.now()
    error_time = now.strftime('%b %d %Y %X')
    logs.write("%s\t\t%s\n" %(error_time, msg))
    logs.close()
    return True

def get_daily_wrs_results(raw_wrs):
    """ Recursive enter in version, then year, then month, then day. Using it in folder which contains the global version tests results"""
    wrs_folders=[]
    for version_folder in os.listdir(raw_wrs):
        version_folder = os.path.join(raw_wrs,version_folder)
        for year_folder in os.listdir(version_folder):
            year_folder = os.path.join(raw_wrs,version_folder,year_folder)
            for month_folder in os.listdir(year_folder):
                month_folder = os.path.join(raw_wrs,version_folder,year_folder,month_folder)
                for day_folder in os.listdir(month_folder):
                    day_folder = os.path.join(raw_wrs,version_folder,year_folder,month_folder,day_folder)
                    wrs_folders.append(day_folder)
    return wrs_folders
