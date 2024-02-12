# Stream (Classic) Videos permission collector tool

This repository contains a script that retrieves permissions information for videos that uploaded on Stream (Classic), which will become EOS in April 15, 2024.  
[Migration Overview - Stream (Classic) to Stream (on SharePoint)](https://learn.microsoft.com/en-us/stream/streamnew/stream-classic-to-new-migration-overview)  

Although Microsoft says that it is not possible to retrieve read permissions granted to videos in Stream (Classic), Stream (Classic) can still be retrieved and displayed that information.  
In other words, if Microsoft publish the ways to get the permissions, we should be able to obtain the same information.

But unfortunately, Microsoft did not reveal the method until the end.  
So we hacked the communication on Stream Classic ourselves and found a method hidden by Microsoft.  

I don't know how many people will refer to the information on Stream (Classic), which will be EOS soon, but I hope it helps at least one person.

## How to Use

### Preparation

- Install Docker and Docker Compose
- Clone this repository to local
- Promote the user running the script to Stream Classic Administrator

### Get the access token and authority

1. Start your browser and open the DevTools
1. Go to the Network tab and start recording network logs
1. Access [Stream (Classic)](https://web.microsoftstream.com/)
1. Filter the traced network log by `video`, select the XHR record whose name starts with **videos?$top=** from the filter results, and get the request header information: `authority` and `Authorization`

### Run the script

1. Write the obtained authority and Authorization values to `python/web-variables.env`
1. Write the output directory values to `python/web-variables.env` if you need to change the directory
    1. `OUTPUT_DIR_ROLL_ASSIGNMENTS`: Directory to output permissions data for each video
    1. `OUTPUT_DIR_STREAM_GROUP`: Directory to output group members data for each StreamOnlyGroup
1. Enter the ID (GUID) of the video for which you want to obtain retrives permissions information in `python/sample/input/videos.csv` and save it.
1. move to path `python` directory, then run the following command: `docker compose up -d`
1. run the following command: `docker compose run app python3 get_video_permissions.py`

#### Notes

The bearer token used by Stream (Classic) internal API seems to expire in about an hour.  
If you want to obtain permissions information for a large number of videos, I recommend dividing the number of videos you want to obtain at one time into a maximum of 10,000, and then running the tool.  