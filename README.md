# Channel Checker
 
A python script to check some of the streaming channels.

v1 - just checks the number of segments

## Notes

This script needs two additional files:

channels.txt
urls,py

## channels.txt

Is a CSV that contains a lit of channel name and their associated channel IDs, i.e.

Channel One, 0001
Channel Two, 0002

## urls.py

Is a variable file that constructs the URLs to query. Format is:

url_prefix="http://url_start"
url_body="url_middle"
url_suffix="url_end"

--