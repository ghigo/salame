import gspread
import json
import logging
import os.path
import time

from oauth2client.client import SignedJwtAssertionCredentials

class Google_spreadsheet(object):
  """Log data in a table"""

  GDOCS_OAUTH_JSON = '/../raspberry-c1844d7c61a6.json'
  SLEEP_TIME = 30

  def __init__(self, spreadsheet_name):
    self.worksheet = None
    self.spreadsheet_name = spreadsheet_name

  def login_open_sheet(self, oauth_key_file, spreadsheet):
    """Connect to Google Docs spreadsheet and return the first worksheet."""

    try:
      file = open(os.path.dirname(__file__) + oauth_key_file)
      json_key = json.load(file)

      credentials = SignedJwtAssertionCredentials(json_key['client_email'],
                            json_key['private_key'],
                            ['https://spreadsheets.google.com/feeds'])
      gc = gspread.authorize(credentials)
      worksheet = gc.open(spreadsheet).sheet1
      return worksheet
    except:
      logging.error('Google_spreadsheet - Unable to login and get spreadsheet.')
      # print 'Unable to login and get spreadsheet. Check OAuth credentials, spreadsheet name, and make sure spreadsheet is shared to the client_email address in the OAuth .json file!'


  def log(self, row):
    """Add a new row to the spreadsheet"""

    if self.worksheet is None:
      self.worksheet = self.login_open_sheet(Google_spreadsheet.GDOCS_OAUTH_JSON, self.spreadsheet_name)

    try:
      # worksheet.append_row((datetime.datetime.now(), temp, humidity))
      self.worksheet.append_row(row)
      # self.worksheet.insert_row(row, self.worksheet.row_count)
    except:
      # Error appending data, most likely because credentials are stale.
      # Null out the worksheet so a login is performed at the top of the loop.
      logging.error('Google_spreadsheet - Append error, logging in again.')
      # print 'Append error, logging in again'
      self.worksheet = None
      time.sleep(Google_spreadsheet.SLEEP_TIME)

    logging.debug('Google_spreadsheet - wrote a row to %s', self.spreadsheet_name)
    # print 'Wrote a row to {0}'.format(self.spreadsheet_name)
