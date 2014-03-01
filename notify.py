#!/usr/bin/python
#
# Send a Sickbeard post processing email notification.
#
# This is designed to be called by Sickbeard as an additional post-processing 
# script (see https://code.google.com/p/sickbeard/wiki/AdvancedSettings).
# 
# It takes 6 parameters (although it only uses 3-5):
#  1. Final full path to the episode file
#  2. Original name of the episode file
#  3. Show tvdb id
#  4. Season number
#  5. Episode number
#  6. Episode air date
#
# You will need to initialise the following variable:
#  1. TVDB_API_KEY - A valid TVDB API key
#  2. MAIL_SERVER - An SMTP mail server (currently set for GMail)
#  3. MAIL_PORT - SMTP mail server port (currently set for GMail)
#  4. MAIL_ACCOUNT - SMTP mail account name
#  5. MAIL_PASSWORD - SMTP mail account password
#  6. MAIL_TO - Mail recepient
#  7. MAIL_FROM - Mail from address
#
# Note that this script makes no allowance for concurrent invocations.

import ConfigParser
import httplib2
import os
import smtplib
import sys
import time
import xml.etree.ElementTree as ElementTree

SCRIPT_LOCATION = os.path.dirname(os.path.realpath(__file__))


def last_run_millis():
    last_run_file = SCRIPT_LOCATION + '/lastrun.dat'

    if os.path.isfile(last_run_file):
        f = open(last_run_file, 'r+')
        last_run = float(f.readline())
        f.seek(0)
        f.truncate()
    else:
        last_run = 0
        f = open(last_run_file, 'w')

    now = time.time()
    f.write('{}'.format(now))
    f.close()

    return last_run


def file_changed_millis(path):
    return os.path.getmtime(path)


def parse_config():
    config_file = SCRIPT_LOCATION + '/notify.ini'
    config = ConfigParser.ConfigParser()
    config.read(config_file)
    return config


def series_name(config, id):

    api_url = 'http://thetvdb.com/api/'
    api_key = config.get('TVDB', 'tvdb_api_key')

    url = api_url + api_key + '/series/' + id

    h = httplib2.Http(SCRIPT_LOCATION + '/.cache')
    (resp, content) = h.request(url, "GET")

    root = ElementTree.fromstring(content)
    return root.find('./Series/SeriesName').text


def notify(config, series, season, episode):

    mail_server = config.get('Mail', 'mail_server')
    mail_port = config.get('Mail', 'mail_port')
    mail_account = config.get('Mail', 'mail_account')
    mail_password = config.get('Mail', 'mail_password')

    mail_to = config.get('Notification', 'mail_to')
    mail_from = config.get('Notification', 'mail_from')

    subject = 'New episode of ' + series
    body = 'A new episode of ' + seriesName + ' is available (Season ' + season + ', episode ' + episode + ')'

    headers = ["From: " + mail_from,
               "Subject: " + subject,
               "To: " + mail_to,
               "MIME-Version: 1.0",
               "Content-Type: text/html"]
    headers = "\r\n".join(headers)

    session = smtplib.SMTP(mail_server, mail_port)
    session.ehlo()
    session.starttls()
    session.login(mail_account, mail_password)
    session.sendmail(mail_from, mail_to, headers + "\r\n\r\n" + body)
    session.quit()


last_run = last_run_millis()
file_changed = file_changed_millis(sys.argv[1])
if file_changed < last_run:
    sys.exit()

config = parse_config()

series_id = sys.argv[3]
season_num = sys.argv[4]
episode_num = sys.argv[5]

seriesName = series_name(config, series_id)

notify(config, seriesName, season_num, episode_num)