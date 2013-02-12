#python for android script to 
#1. download Melbourne Water pumping restrictions from melb water website,
#2. parse relevant data into usable text
#3. output data to an android message box

#import required modules
import mechanize
import HTMLParser
from BeautifulSoup import BeautifulSoup
import android
app = android.Android()

appTitle = "Pumping"
appMsg = "Retreiving pumping status"

app.dialogCreateSpinnerProgress(appTitle, appMsg)
app.dialogShow()

BASE_URL = "http://www.melbournewater.com.au/content/rivers_and_creeks/waterway_diverters/yarra_upper.asp"
br = mechanize.Browser()
data = br.open(BASE_URL).get_data()
soup = BeautifulSoup(data)
table=soup.find("table",title="Table showing current waterway diversion status")
for row in table.findAll('tr')[1:]:
    col = row.findAll('td')
    restrict = col[1]
    ban = col[2].string
    flow = col[3].string
    avflow = col[4].string
    date = col[5].string
#Function to strip html tags from table cells (allows for episodic coloring/bolding of cell contents when bans apply!)
def stripper(data):
   data = str(data)
   count = data.count('<')
   while count:
       start = data.find('<')
       end = data.find('>')
       rem = data[start:end+1]
       data = data.replace(rem,'',1)
       count-=1
   out = data
   return out
#apply the stripper function to current restriction and ban statuses, and format strings
restrict = 'Status?  ' + stripper(restrict)
ban = 'Banned?  ' + stripper(ban)
flow = 'Flow:  ' + flow + ' ML/d'
avflow = 'Av. Flow:  ' + avflow + ' ML/d'

#output to message box
app.vibrate()

appMsg = "Pumping status today:"
app.dialogCreateAlert(appMsg)
app.dialogSetItems([restrict, ban, flow, avflow])
app.dialogSetPositiveButtonText('OK')
app.dialogShow()
resp = app.dialogGetResponse().result
app.vibrate()
app.makeToast("Done!")







