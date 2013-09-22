#python for android script to 
#1. download Melbourne Water pumping restrictions from melb water website,
#2. parse relevant data into usable text
#3. output data to an android message box

#import required modules
import mechanize
import HTMLParser
from BeautifulSoup import BeautifulSoup
import re
import android
app = android.Android()

appTitle = "Pumping"
appMsg = "Retreiving pumping status"

app.dialogCreateSpinnerProgress(appTitle, appMsg)
app.dialogShow()

try:            
	BASE_URL = "http://www.melbournewater.com.au/waterdata/waterwaydiversionstatus/Pages/Yarra-River-Upper.aspx"
	br = mechanize.Browser()
	data = br.open(BASE_URL).get_data()
	soup = BeautifulSoup(data)
	table=soup.find("table",id="ctl00_m_g_a76a034b_68d1_4fca_8b53_c7d6e0cc6fc5_ctl00_grdDivertersSummary" )	
	rows = table.findAll('tr')
	dat=str(rows[1])
except:
	app.makeToast("Unable to retrieve data")
	die("Unable to retrieve data")

def remove_html_tags(data):
	p = re.compile(r'<.*?>')
	return p.split(data)

a=remove_html_tags(dat)
risk=a[3]
restrict=a[7]
ban=a[11]
flow=a[14]
avflow=a[16]
dddate=a[18]


restrict = 'Restricted?  ' + restrict
ban = 'Banned?  ' + ban
risk = 'Risk?    ' + risk
flow = 'Flow:  ' + flow + ' ML/d'
avflow = 'Av. Flow:  ' + avflow + ' ML/d'

print(restrict)
print(ban)
print(risk)
print(flow)
print(avflow)

##output to message box
##this code borrow extensively from the Linux journal article http://www.linuxjournal.com/article/10940?page=0,2 by Paul Barry

appMsg = "Pumping status today:"
app.dialogCreateAlert(appMsg)
app.dialogSetItems([restrict, ban, risk, flow, avflow])
app.dialogSetPositiveButtonText('OK')
app.dialogShow()
resp = app.dialogGetResponse().result
app.vibrate()
#app.makeToast("Done!")







