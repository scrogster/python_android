#!/usr/bin/env python
#python script to download and save a chunk of streaming audio from ABC Radio National. 
#For use in time-shifting the ABC news, so I can listen to it as an alarm on my phone, regardless of what time the alarm is set.
#Should work for any other radio stations, just change the URL defined in variable conn.

#copy to /mnt/sdcard/sl4a/scripts
#schedule download time using tasker, prior to desired waking time
#use the resulting mp3 as an alarm clock ringtone
#in the event of download failure, you'll just get yesterdays news.
import urllib

#file to save to
target = open('/mnt/ext_card/music/abc.mp3', "wb")
#target = open('abc.mp3', "wb")

#RADIO NATIONAL streaming url
conn = urllib.urlopen('http://shoutmedia.abc.net.au:10420/')
#approx number of minutes desired
mins=10
#chunk size to write to file
chunksize=1024*8
#number of chunks to write to get approximately correct recording duration
#approximate 630 kB per minute of audio
chunks=int(mins*650000/chunksize)
#keep buffering and writing the stream intermittently until the required number of seconds has elapsed.
#writes in 8kB chunks (could be changed depending on CPUspeed/RAM availability).
for i in range(1, chunks):
    target.write(conn.read(chunksize))
conn.close()





