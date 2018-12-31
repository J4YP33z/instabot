#!/usr/bin/env python
# -*- coding: utf-8 -*-


import atexit
import itertools
import json
import random
import sys
import time
import requests


'''
daily limits:
follow - 800
like - 1400
comment - 250

hourly limits:
follow/unfollow - 60
likes - 350
comment - 60

0 = unfollow
1 = like and comment
'''


user_login = '***REMOVED***'
user_password = '***REMOVED***'
tag_list=[
#GoT
'emiliaclarke', 'kitharington', 'maisiewilliams', 'peterdinklage',
'lenaheadey', 'nataliedormer', 'sophieturner', 'nikolajcosterwaldau',
'catelynstark', 'daenerys', 'jonsnow', 'aryastark', 'tyrion', 'cersei',
'themountain', 'oberyn', 'gameofthrones', 'got', 'hbo', 'gameofthronespost',
'daenerystargaryen', 'hodor', 'got', 'stark', 'winteriscoming',
#LoL
'Gamer', 'Gaming', 'teemo', 'vayne',  'starwars', 'leagueoflegends', 'esports',
'worlds', 'twitch', 'riot', 'leagueoflegend', 'blitzcrank', 'jhin', 'lolvine',
'leagueoflegendsfanart', 'leagueoflegendsmemes', 'lol', 'leagueoflegendsi',
'riotgames', 'riotpls', 'khazix', 'leblanc', 'talon',
#SW
'theforceawakens', 'darthvader', 'yoda', 'hansolo', 'rogueone', 'stormtrooper',
'darkside', 'kyloren', 'starwarsfan', 'starwarsart',
#AC
'AssassinsCreedSyndicate', 'Ubisoft', 'PS4', 'PlayStation', 'PlayStation4',
'EzioAuditore', 'TheEzioCollection', 'Assassin', 'Auditore', 'Assassins',
'Collection', 'Firenze', 'Adventure', 'Cosplay', 'MichaelFassbender', 'Animus',
'ACSyndicate',
#Westworld
'AnthonyHopkins', 'Westworld', 'westworldhbo', 'robots', 'AI', 'robotics',
'tech', 'technology', 'science', 'robot', 'cowboy', 'Western', 'cowgirl',
'ArtificialIntelligence', 'MachineLearning', 'DeepLearning', 'evanrachelwood',
#Seasonal
'christmas', 'christmasgifts', 'christmastree', 'merrychristmas',
'christmasiscoming', 'christmas2016', 'cmachristmas',
#General
'love', 'instagood', 'photooftheday', 'tbt', 'beautiful', 'cute', 'me', 'happy',
'followme', 'fashion', 'selfie', 'picoftheday', 'like4likes', 'friends',
'instadaily', 'girl', 'fun', 'tagforlikes', 'smile', 'repost', 'igers',
#items
'coffee', 'tea', 'mug', 'sweater', 'hoodie']


url = 'https://www.instagram.com/'
url_tag = 'https://www.instagram.com/explore/tags/'
url_likes = 'https://www.instagram.com/web/likes/%s/like/'
url_unlike = 'https://www.instagram.com/web/likes/%s/unlike/'
url_comment = 'https://www.instagram.com/web/comments/%s/add/'
url_follow = 'https://www.instagram.com/web/friendships/%s/follow/'
url_unfollow = 'https://www.instagram.com/web/friendships/%s/unfollow/'
url_login = 'https://www.instagram.com/accounts/login/ajax/'
url_logout = 'https://www.instagram.com/accounts/logout/'
url_media_detail = 'https://www.instagram.com/p/%s/?__a=1'
url_user_detail = 'https://www.instagram.com/%s/?__a=1'


def requestData(source):
  r = s.get(source)
  text = r.text
  startingTxt = ('<script type="text/javascript">'
                 'window._sharedData = ')
  startingTxt_len = len(startingTxt)-1
  endingTxt = ';</script>'
  all_data_start = text.find(startingTxt)
  all_data_end = text.find(endingTxt, all_data_start + 1)
  json_str = text[(all_data_start + startingTxt_len + 1) : all_data_end]
  return json.loads(json_str)

def getMedia():
  all_data = requestData('https://www.instagram.com/#')
  return list(all_data['entry_data']['FeedPage'][0]['feed']['media']['nodes'])

def get_media_id_by_tag(tag):
  url_tag_ = '%s%s%s' % (url_tag, tag, '/')
  all_data = requestData(url_tag_)
  return list(all_data['entry_data']['TagPage'][0]['tag']['media']['nodes'])

def generate_comment():
  if (0 == random.randint(0,2)):
    c_list = list(itertools.product(
        ["this", "your"],
        ["post", "content"],
        ["is", "looks", "is really"],
        ["great", "super", "good", "very good", "cool", "GREAT", "magnificent",
        "magical", "very cool", "beautiful", "so beautiful", "lovely",
        "so lovely", "very lovely", "excellent", "amazing"],
        [".", "..", "...", "!", "!!", "!!!"]))
    res = " ".join(random.choice(c_list))
    for s, r in [("  ", " "), (" .", "."), (" !", "!")]:
        res = res.replace(s, r)
    return res.capitalize()
  else:
    return random.choice(['👍', '👍👍👍', '😍', '😍😍😍', '❤️',
                          '❤️❤️❤️', '💯',
                          '💯💯💯', '👏', '👏👏👏'])


random.seed()


mode = 0
if (len(sys.argv) == 2):
  mode = int(sys.argv[1])

print(time.strftime("%d/%m/%Y"), time.strftime("%I:%M:%S"))

media_on_feed = []
media_by_tag = []
user_agent = ("Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36")
accept_language = 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4'
s = requests.Session()
s.cookies.update({'sessionid': '', 'mid': '', 'ig_pr': '1', 'ig_vw': '1920',
                  'csrftoken': '', 's_network': '', 'ds_user_id': ''})
login_post = {'username': user_login, 'password': user_password}
s.headers.update({'Accept-Encoding': 'gzip, deflate',
                  'Accept-Language': accept_language,
                  'Connection': 'keep-alive',
                  'Content-Length': '0',
                  'Host': 'www.instagram.com',
                  'Origin': 'https://www.instagram.com',
                  'Referer': 'https://www.instagram.com/',
                  'User-Agent': user_agent,
                  'X-Instagram-AJAX': '1',
                  'X-Requested-With': 'XMLHttpRequest'})
r = s.get(url)
s.headers.update({'X-CSRFToken': r.cookies['csrftoken']})
time.sleep(2)
login = s.post(url_login, data=login_post, allow_redirects=True)
s.headers.update({'X-CSRFToken': login.cookies['csrftoken']})
csrftoken = login.cookies['csrftoken']
time.sleep(2)

if login.status_code == 200:
  r = s.get('https://www.instagram.com/')
  finder = r.text.find(user_login)
  if finder != -1:
    print('Log in success')
  else:
    print('Log in error! Check your login data!')
    sys.exit()
else:
  print('Log in error! Connection error!')
  sys.exit()

timeStart = time.time()
like_counter = 0
comments_counter = 0

mode_changer = 0
limit = 2000

while(1):
  if (mode_changer >= limit): # run unfollow for every 50 likes
    mode_changer = 0
    unfollow_counter = -1
    while(len(getMedia()) > 0 and unfollow_counter != 0):
      print('getting feed...')
      time.sleep(5)
      unfollow_counter = 0
      media_on_feed = getMedia() # get recent media
      for i in range(0, len(media_on_feed)):
        current_user=media_on_feed[i]["owner"]["username"]
        current_id=media_on_feed[i]["owner"]["id"]
        url_user = 'https://www.instagram.com/%s/'%(current_user)
        all_data = requestData(url_user) # get user info
        user_info = list(all_data['entry_data']['ProfilePage'])
        follower = user_info[0]['user']['followed_by']['count']
        follow_viewer = user_info[0]['user']['follows_viewer']
        has_requested_viewer = user_info[0]['user']['has_requested_viewer']
        if (follower > 100000 or (follow_viewer or has_requested_viewer)):
          print("ignoring %s" % current_user)
          continue # ignore if user is follower or big account
        url_unfollow_ = url_unfollow % (current_id)
        unfollow = s.post(url_unfollow_)
        if unfollow.status_code == 200: # unfollow success
          unfollow_counter += 1
          print("Unfollow: %s #%i." % (current_id, unfollow_counter))
          time.sleep(random.randint(4, 6))
        else: # unfollow failed
          print('failed: %s' % current_id)

  if (time.time() - timeStart > 3600): # sleep 5 minutes per hour
    print("sleeping for 5 minutes...")
    time.sleep(300)
    timeStart = time.time()
    
  current_tag = random.choice(tag_list)
  # finding media to like
  media_by_tag = get_media_id_by_tag(current_tag)
  print("Liking %s..." % current_tag)
  for i in range(0, random.randint(1, len(media_by_tag))):
    if (media_by_tag[i]['likes']['count'] > 299): # don't like popular stuff
      continue
    url_likes_ = url_likes % (media_by_tag[i]['id'])
    like = s.post(url_likes_)
    if like.status_code == 200: # like success
      like_counter += 1
      mode_changer += 1
      print("Like: %s #%i." % (media_by_tag[i]['id'], like_counter))
    else:
      print("like failed.")
    time.sleep(random.randint(12, 15)) # sleep after liking
    if (random.randint(0, 5) == 0): # one comment for every 6 likes
      comment_post = {'comment_text': generate_comment()}
      url_comment_ = url_comment % (media_by_tag[i]['id'])
      comment = s.post(url_comment_, data=comment_post)
      if comment.status_code == 200:
        comments_counter += 1
        print("Comment: %s #%i." % (media_by_tag[i]['id'], comments_counter))
      else:
        print(comment.status_code)
      time.sleep(random.randint(8, 16)) # sleep after commenting
    if (mode_changer >= limit):
      break

'''
def check_exisiting_comment(self, media_code):
  url_check = self.url_media_detail % (media_code)
  check_comment = self.s.get(url_check)
  all_data = json.loads(check_comment.text)
  if all_data['media']['owner']['id'] == self.user_id:
          self.write_log("Keep calm - It's your own media ;)")
          # Del media to don't loop on it
          del self.media_by_tag[0]
          return True
  comment_list = list(all_data['media']['comments']['nodes'])
  for d in comment_list:
      if d['user']['id'] == self.user_id:
          self.write_log("Keep calm - Media already commented ;)")
          # Del media to don't loop on it
          del self.media_by_tag[0]
          return True
  return False
  
def get_user_id_by_login(self, user_name):
  url_info= self.url_user_info % (user_name)
  info = self.s.get(url_info)
  all_data = json.loads(info.text)
  id_user = all_data['user']['id']
  return id_user  
'''
