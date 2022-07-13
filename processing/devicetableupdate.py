from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

import json, os
from datetime import date, datetime, timedelta
import pytz
from pymongo import MongoClient


#connect to mongodb
mongoconnection = MongoClient(
    'mongodb://admin:jrg123@10.10.95.42/?authMechanism=DEFAULT&authSource=admin'
)

db = mongoconnection.dashboardDb
timezone = pytz.timezone("America/New_York")

#get previous month
def monthdelta(date, delta):
    m, y = (date.month+delta) % 12, date.year + ((date.month)+delta-1) // 12
    if not m: m = 12
    d = min(date.day, [31,
        29 if y%4==0 and (not y%100==0 or y%400 == 0) else 28,
        31,30,31,30,31,31,30,31,30,31][m-1])
    return date.replace(day=d,month=m, year=y)

    timezone = pytz.timezone("America/New_York")


reports = db.readings
devices = db.devices

# Set datetime for 1 month ago
end = datetime.now()
end = timezone.localize(end)
onemonthago = (monthdelta(end, -1))

#Repeat for last 24 hours
onedayago = end - timedelta(hours = 24)

#Pull messages from twilio API for the last handful
#"TWILIO_SID":"AC891972f21eee99d4ed3d325d7528bb53",
#"TWILIO_TOKEN":"7785a4fc12c49736eacfdd769d6291d5"
account_sid = 'AC891972f21eee99d4ed3d325d7528bb53'
auth_token = '7785a4fc12c49736eacfdd769d6291d5'
voltage=0
reportedlist = []
client = Client(account_sid, auth_token)
messages = client.messages.list(limit=20, to='+17623204402')
reportedlist.append([messages[0].body.split("JRG")[1].split("@")[0],messages[0].date_sent])
for record in messages:
    if (record.date_sent > onedayago):
        append = True
        bodyunit = record.body.split("JRG")[1].split("@")[0]

        for unit in reportedlist:
            # print("Comparing Unit" + bodyunit + " with stored " + unit)
            if bodyunit == unit:
                #match found set flag
                #don't append flag
                # print("Match Found with " + bodyunit)
                append = False
        if (append == True):
            reportedlist.append([bodyunit,record.date_sent])
            print ("Checking " + str(bodyunit))
            thing = devices.find_one({"Device Name": "JRG-" + str(int(bodyunit))})
            # make sure date is newer
            thing['Last Reported'] = timezone.localize(thing['Last Reported'])

            if (record.date_sent > thing['Last Reported']):
                voltage = float(record.body.split("Battery ")[1].split("V,")[0])
                print(str(voltage))
                #push the update
                print("Updating Device: " + bodyunit + "with current update date:" + str(thing['Last Reported']) + " with new date: " + str(record.date_sent))
                devices.update_one({"Device Name": "JRG-" + str(int(bodyunit))},  {"$set": {"Last Reported": record.date_sent, "Voltage": voltage}})

#        print(len(reportedlist))


#devicelist = list(devices.find())