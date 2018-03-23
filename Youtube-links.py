import urllib.request
import json
import csv 
all_links={}#store are the videoids and related videos
def get_all_video_in_channel(channel_id):            #returns a list with all the links on a channel
    api_key = 'AIzaSyCrF_IsqWkWcMG3rlxOVCWs87Re7_xlU7A' #youtube api key

    base_video_url = 'https://www.youtube.com/watch?v='
    base_search_url = 'https://www.googleapis.com/youtube/v3/search?'

    first_url = base_search_url+'key={}&channelId={}&part=snippet,id&order=date&maxResults=25'.format(api_key, channel_id)

    video_links = []
    url = first_url
    while True:
        inp = urllib.request.urlopen(url)
        resp = json.load(inp)

        for i in resp['items']:
            if i['id']['kind'] == "youtube#video":
                video_links.append(base_video_url + i['id']['videoId'])

        try:
            next_page_token = resp['nextPageToken']
            url = first_url + '&pageToken={}'.format(next_page_token)
        except:
            break
    return video_links
def get_all_related_videos(videolink):          #Get related videos for a given link
    api_key = 'AIzaSyCrF_IsqWkWcMG3rlxOVCWs87Re7_xlU7A'# youtube api key
    i=videolink.find("v=")
    vid=videolink[(i+2):]
    print(vid)
    base_video_url = 'https://www.youtube.com/watch?v='
    base_search_url = 'https://www.googleapis.com/youtube/v3/search?'
    first_url = 'https://www.googleapis.com/youtube/v3/search?part=snippet&relatedToVideoId={}&type=video&key={}'.format(vid,api_key)
    video_links = []
    url = first_url
    it=1
    while it<4:
        inp = urllib.request.urlopen(url)
        resp = json.load(inp)
        for i in resp['items']:
            if i['id']['kind'] == "youtube#video":
                video_links.append(base_video_url + i['id']['videoId'])
        try:
            next_page_token = resp['nextPageToken']
            url = first_url + '&pageToken={}'.format(next_page_token)
        except:
            break
        it+=1
    all_links[vid]=video_links
    return video_links



cid=input("Input the channel ID  :  ") #input channel ID
name=input("Enter the name of the csv file to store result  :  ") #input name of the output csv file.
listv=get_all_video_in_channel(cid) #list with all the video links for a channel id
for i in listv:
    listr=get_all_related_videos(i) # input related videos for video
with open(name+".csv",'w')as file:  #store channel links in csv
    fieldnames=['Videos']
    writer=csv.DictWriter(file,fieldnames=fieldnames)
    writer.writeheader()
    for i in listv:    
        writer.writerow({'Videos':i})
with open(name+"Related.csv",'w') as file: #store related links according to video ids
    writer = csv.writer(file)
    writer.writerow(all_links.keys())
    writer.writerows(zip(*all_links.values()))