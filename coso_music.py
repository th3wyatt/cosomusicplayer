import pafy
import vlc 
from mastodon import Mastodon
from time import sleep

user_name = 'USERNAME@EMAIL'
pw = 'PASSWORD'
app_name = 'cosomusicplayer'

def get_url(toot_content):
    content_list = toot_content.split("\"")
    url = None
    for item in content_list:
        if "https://www.youtube" in item or "https://youtu.be" in item or "https://youtube.com" in item:
            url = item

    return url

def play_url(toot_content):
    url = get_url(toot_content)
    if url != None:
        video = pafy.new(url)
        print("playing " + url)
        best = video.getbest()
        playurl = best.url

        video_instance = vlc.Instance()
        player = video_instance.media_player_new()
        media = video_instance.media_new(playurl)
        media.get_mrl()
        player.set_media(media)
        player.play()
        sleep(10)
        while player.is_playing():
            sleep(1)
        player.stop()

    else:
        print("no youtube url")

Mastodon.create_app(
     app_name,
     api_base_url = 'https://counter.social',
     to_file = app_name + '_clientcred.secret'
)

cosomusicplayer = Mastodon(
    client_id = app_name + '_clientcred.secret',
    api_base_url = 'https://counter.social'
)
cosomusicplayer.log_in(
    user_name,
    pw,
    to_file = app_name + '_usercred.secret'
)

#getting latest cosomusic post

coso_hashtag = cosomusicplayer.timeline_hashtag("CoSoMusic")

latest_tag = coso_hashtag[0].get("id")
print("current status id: " + str(latest_tag))

play_url(cosomusicplayer.status(latest_tag).get("content"))

while(True):
    coso_hashtag = cosomusicplayer.timeline_hashtag("CoSoMusic", since_id=latest_tag)
    
    if len(coso_hashtag) !=0:
        print("new post!")
        for item in coso_hashtag:
            play_url(item.get("content"))
            sleep(10)
        latest_tag = coso_hashtag[0].get("id")
        print("played all videos, sleeping for 300 seconds")
    else:
        print("no new videos, sleeping for 300 seconds")
        
    sleep(300)



