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

TVDB_API_URL = 'http://thetvdb.com/api/'

import ConfigParser
import httplib2
import os
import smtplib
import sys
import xml.etree.ElementTree as ElementTree

scriptLocation = os.path.dirname(os.path.realpath(__file__))

configFile = scriptLocation + '/notify.ini'
Config = ConfigParser.ConfigParser()
Config.read(configFile)

TVDB_API_KEY = Config.get('TVDB', 'tvdb_api_key')

MAIL_SERVER = Config.get('Mail', 'mail_server')
MAIL_PORT = Config.get('Mail', 'mail_port')
MAIL_ACCOUNT = Config.get('Mail', 'mail_account')
MAIL_PASSWORD = Config.get('Mail', 'mail_password')

MAIL_TO = Config.get('Notification', 'mail_to')
MAIL_FROM = Config.get('Notification', 'mail_from')

seriesId = sys.argv[3]
season = sys.argv[4]
episode = sys.argv[5]

dataUrl = TVDB_API_URL + TVDB_API_KEY + '/series/' + seriesId

h = httplib2.Http(scriptLocation + '/.cache')
(resp, content) = h.request(dataUrl, "GET")

root = ElementTree.fromstring(content)
seriesName = root.find('./Series/SeriesName').text

sender = MAIL_FROM
recipient = MAIL_TO
subject = 'New episode of ' + seriesName
body = 'A new episode of ' + seriesName + ' is available (Season ' + season + ', episode ' + episode + ')'

headers = ["From: " + sender,
           "Subject: " + subject,
           "To: " + recipient,
           "MIME-Version: 1.0",
           "Content-Type: text/html"]
headers = "\r\n".join(headers)

session = smtplib.SMTP(MAIL_SERVER, MAIL_PORT)
session.ehlo()
session.starttls()
session.login(MAIL_ACCOUNT, MAIL_PASSWORD)
session.sendmail(sender, recipient, headers + "\r\n\r\n" + body)
session.quit()