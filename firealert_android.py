import feedparser
import re
import math
import android
app = android.Android()

appTitle = "Fire Incidents"
appMsg = "Retreiving incident status"

app.dialogCreateSpinnerProgress(appTitle, appMsg)
app.dialogShow()


#check for proximity to home location using John Cook's code  (haversine function)
#see http://www.johndcook.com/python_longitude_latitude.html code free to use

def distance_on_unit_sphere(lat1, long1, lat2, long2):

    # Convert latitude and longitude to 
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0
        
    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
        
    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians
        
    # Compute spherical distance from spherical coordinates.
        
    # For two locations in spherical coordinates 
    # (1, theta, phi) and (1, theta, phi)
    # cosine( arc length ) = 
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length
    
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )*6371

    # Remember to multiply arc by the radius of the earth 
    # in your favorite set of units to get length.
    return arc

#download the rss feed
cfa=feedparser.parse('http://osom.cfa.vic.gov.au/public/osom/IN_COMING.rss')

#calculate the total number of incidents
tot_inc=len(cfa['entries'])

#set up some lists to store incident attribute data
lati=[]
longi=[]
placename=[]
typ=[]
status=[]
appliances=[]
prox=[]

#loop through incidents, extract data, clean and store in the appropriate lists.
for i in range(1,tot_inc):
	coord=str(cfa['entries'][i]['georss_point'])
	coord=str.split(coord)
	lati.append(float(coord[0]))
	longi.append(float(coord[1]))
	pname=cfa['entries'][i]['title']
	placename.append(pname.encode('ascii','ignore'))
	descrip=cfa['entries'][i]['description']
	descrip=re.sub('<[^>]*>', '', descrip)
	descrip=re.sub('\t\t', '', descrip)
	descrip=re.split('\n', descrip)
	tt=descrip[4].encode('ascii','ignore')
	typ.append(tt)
	status.append(descrip[5])
	appl = descrip[7].encode('ascii','ignore')
	appl=re.sub('Appliances: ','', appl)
	appl=int(appl.strip())
	appliances.append(appl)
	#compute distance from each incident to home location
	prox.append(distance_on_unit_sphere(lati[i-1], longi[i-1], -37.703047, 145.284524))

#calculate the number of proximities less than a threshold
thresh=35.0
num_close_inc = len([elem for elem in prox if elem < thresh])

#alternative approach make list of lists, and transpose using zip()
#outmat=[lati, longi, placename, typ, status, appliances, prox]	
#outmat=zip(*outmat)	#transposing columns and rows
#outmat=sorted(outmat, key=lambda outmat: outmat[7]) #sorting by proximity (ascending)

#get the list indices of the incidents within the threshold distance
index_close_inc = [index for index,value in enumerate(prox) if value < thresh]

#for android will need code to sound an alert/vibrate if incidents>0, then list incident details in an alter message.
#can run the script episodically using tasker to provide continual coverage.

app.vibrate()
appMsg = str(num_close_inc) + ' Incidents within ' + str(round(thresh, 0)) + 'km'
app.dialogCreateAlert(appMsg)
app.dialogSetPositiveButtonText('OK')
app.dialogShow()
resp = app.dialogGetResponse().result
app.dialogDismiss()
k=1
for j in index_close_inc:
	msg = 'Incident ' + str(k)
	k += 1
	app.dialogCreateAlert(msg)
	placestring=placename[j].strip()+', '
	placestring=placestring.title()
	typstring=typ[j].strip()
	typstring=typstring.title()
	statstring=status[j].strip()
	statstring=statstring.title()
	applstring='Appliances: ' + str(appliances[j])
	proxstring='Distance: ' + str(round(prox[j], 1)) +'km'
	app.dialogSetItems([placestring, proxstring, typstring, statstring, applstring])
	app.dialogSetPositiveButtonText('OK')
	app.dialogShow()
	resp = app.dialogGetResponse().result
	app.dialogDismiss()
app.makeToast("No more incidents")



