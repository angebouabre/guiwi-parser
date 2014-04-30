#!/usr/bin/python
#-*-coding:utf-8-*-

import os, sys
import sqlite3
import psycopg2
from datetime import datetime
from parsersettings import LOG_DIR

def write_logs(msg):
    """ Write msg in the logs file """
    if not os.path.isdir(LOG_DIR):
        os.makedirs(LOG_DIR)
    log_file = os.path.join(LOG_DIR,'logs')
    log_file = open(log_file,'a')
    now = datetime.now()
    log_time = now.strftime('%b %d %Y %X')
    log_file.write("%s\t\t%s\n" %(log_time, msg))
    log_file.close()
    return True

def get_daily_wrs_results(raw_wrs):
    """ Recursive enter in version, then year, then month, then day. Using it in folder which contains the global version tests results"""
    wrs_folders=[]
    try:
        for version_folder in os.listdir(raw_wrs):
            version_folder = os.path.join(raw_wrs,version_folder)
    except OSError as e:
        write_logs("Fixture Failed,\t%s:%s\tCheck RAW_RESULTS_DIR in setting." %(e.strerror, raw_wrs)) 
        sys.exit()
    else:
        for year_folder in os.listdir(version_folder):
            year_folder = os.path.join(raw_wrs,version_folder,year_folder)
            for month_folder in os.listdir(year_folder):
                month_folder = os.path.join(raw_wrs,version_folder,year_folder,month_folder)
                for day_folder in os.listdir(month_folder):
                    day_folder = os.path.join(raw_wrs,version_folder,year_folder,month_folder,day_folder)
                    wrs_folders.append(day_folder)
    return wrs_folders

def get_last_pk_sqlite(db, table):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    query = "select id from %s order by id" %table
    c.execute(query)
    val = c.fetchall()
    val = val[-1][0]
    return val


def get_last_pk_pg(db, user, table):
    connection = "dbname=%s user=%s" %(db, user)
    conn = psycopg2.connect(connection)
    c = conn.cursor()
    query = "select id from %s order by id" %table
    c.execute(query)
    val = c.fetchall()
    val = val[-1][0]
    return val
