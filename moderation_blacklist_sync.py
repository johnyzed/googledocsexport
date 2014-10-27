import gdata.service
import gdata.spreadsheet
import gdata.spreadsheet.service
import gdata.spreadsheet.text_db
import logging
import socket
import moderation_blacklist_sync_conf as configuration
 
gd_client = gdata.spreadsheet.service.SpreadsheetsService()
 
# Set the email to your Google account email
gd_client.email = configuration.username 
 
# Set the password to your Google account password. Please note that if you have 
# enabled the 2-steps authentication in Google you will have to generate a 
# password for this script.
gd_client.password = configuration.passwd
 
try:                    
    gd_client.ProgrammaticLogin()
except socket.sslerror, e:
    logging.error('Spreadsheet socket.sslerror: ' + str(e))
 
# key: is the "key" value that you see in the url bar of the browser once you 
# open a Google Docs spreadsheet
key = configuration.key 
 
# This is the worksheet ID: the default name of the first sheet is "od6"
wksht_id = 'od6'
 
try:
    feed = gd_client.GetListFeed(key, wksht_id)
except gdata.service.RequestError, e:
    logging.error('Spreadsheet gdata.service.RequestError: ' + str(e))
except socket.sslerror, e:
    logging.error('Spreadsheet socket.sslerror: ' + str(e))

output_file=open(configuration.lookup_path,'w')
for key in configuration.field_list:
    if key == configuration.field_list[-1]:
        word=key
    else:
        word=key+','
    output_file.write(word)
output_file.write("\n")
output_file.close()

output_file=open(configuration.lookup_path,'a')
for row in feed.entry:
    for key in configuration.field_list:
        if key == configuration.field_list[-1]:
            if (key in configuration.field_star):
                word="*"+row.custom[key].text+"*"
            else:
                word=row.custom[key].text
            print "%s" % (word)
        else :
            if (key in configuration.field_star):
                word="*"+row.custom[key].text+"*,"
            else:
                word=row.custom[key].text+","
            print "%s" % (word),
        output_file.write(word)
    output_file.write("\n")
output_file.close()

