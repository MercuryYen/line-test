#coding=utf-8
from flask import Flask, request, abort
import datetime
import time
import requests
from linebot import (
	LineBotApi, WebhookHandler
)
from linebot.exceptions import (
	InvalidSignatureError
)
from linebot.models import (
	MessageEvent, TextMessage, TextSendMessage,ImageSendMessage,
)
import random
app = Flask(__name__)

global test_cnt
client_id = '11adc840a89caab'
client_secret = 'f49f77227498f51711b49e94ae5e31aa889867e4'
test_cnt = 0
line_bot_api = LineBotApi('06oQSrqV6MLR0AnGN3hsRLPuHrGXkcU7i0r/MifC/bG6wV/6z6JAhLiYqzllsFO7/EyfgMAWLspZyMSlEcD97jjTIzwptJds8Wj/IV3SOmaHKCobZd/nVjYHyrVcN4JABfRa1LdKG1EOhszV2zC2owdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('24c72030e2a4c450662b587972270331')




#pixiv_client = ImgurClient(client_id, client_secret)
#authorization_url = pixiv_client.get_auth_url('pin')
#print(authorization_url)

# ... redirect user to `authorization_url`, obtain pin (or code or token) ...

#credentials = pixiv_client.authorize('afafec5058', 'pin')
#pixiv_client.set_user_auth(credentials['access_token'], credentials['refresh_token'])
#access_token = '0d6dcff17691dc7f7b8a3bcf5ee50206744f1f74'
#refresh_token = '7d5ff09a8b098421addd399d2d54c919bbaf18df'
#pixiv_client = ImgurClient(client_id, client_secret, access_token, refresh_token)
@app.route("/callback", methods=['POST'])
def callback():

	# get X-Line-Signature header value
	signature = request.headers['X-Line-Signature']

	# get request body as text
	body = request.get_data(as_text=True)
	app.logger.info("Request body: " + body)

	# handle webhook body
	try:
		handler.handle(body, signature)
	except InvalidSignatureError:
		abort(400)

	return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
	#groupID : C76178d58e6e2e0180b7cb82c060125cc
	#me: Uc242d41d19caa48431e682b73c08588e
	profile = line_bot_api.get_profile( "Uc242d41d19caa48431e682b73c08588e")
	print(profile)
	try:
		print(profile.displayName)
		print(1)
	except:
		try:
			print(profile['displayName'])
			print(2)
		except:
			print(3)
	if event.source.type == "user":
		if "/search" in event.message.text:
			message = event.message.text.replace("/search ","")
			search = message.replace(" ","%20").replace("/search","")
			all_search = search.split("%20")
			for ii in range(0,len(all_search)):
				if "100000" ==all_search[ii] or "50000" ==all_search[ii] or "10000" ==all_search[ii] or "5000" ==all_search[ii] or"1000" ==all_search[ii] or "500"==all_search[ii]:
					all_search[ii] = all_search[ii]+"users入り"            
			
			all_id = list()
			search = ""
			for ii in all_search:
				search+=ii+"%20"
			search = search[:-3]
			print(search)
			for page in range(0,11):
				print(page)
				get = requests.get("https://www.pixiv.net/search.php?word="+search+"&order=date_d&mode=safe&p="+str(page),verify = False)
				get.encoding = 'unicode'
				if '_p0_master1200.jpg' not in get.text:
					break
				else:
					pre=0
					while pre != -1:
						pos = get.text.find('_p0_master1200.jpg',pre)
						photo_id = get.text[pos-8:pos]
						if photo_id not in all_id:
							all_id.append(photo_id)
						pre = get.text.find("_p0_master1200.jpg",pre+10)
			if len(all_id) != 0:
				K = random.randint(0,len(all_id)-1)
				choose = all_id[K]
				page = requests.get("https://www.pixiv.net/member_illust.php?mode=medium&illust_id="+choose,verify = False).text

				possible = page[page.find("_p0_master1200.jpg")-100:page.find("_p0_master1200.jpg")+18]

				temp2 = page.find("comment-list")
				temp = page.find("tag_area")
				temp = page.find("tags-container",temp)
				text = page[temp:temp2]
				tags = "tags:\n  "
				temp = 0
				success = 0
				while temp!=7:
					temp = text.find("tag-value")+8
					if temp == 7:
						break
					text = text[temp:]
					tags+=text[3:text.find("</a>")]+"\n  "
					success = 1



				if success == 0:
					print("special")
					temp = page.find("for (var k in arg) {")
					temp2 = page.find("storableTags")
					print(temp)
					print(temp2)
					text = page[temp:temp2]
					#print(text)
					tags = "tags:\n  "
					while temp!=7:
						temp = text.find("\"tag\"")+3
						if temp == 2:
							break
						text = text[temp:]
						tags+=text[4:text.find("locked")-3]+"\n  "
					tags = tags.encode().decode("unicode_escape")
				print(event.source.user_id)
				#line_bot_api.push_message(event.source.user_id, ImageSendMessage(original_content_url=more_big,preview_image_url=preview))
				line_bot_api.push_message(event.source.user_id, TextSendMessage(text="https://www.pixiv.net/member_illust.php?mode=medium&illust_id="+choose+"\n"+tags))
		elif "/random" in event.message.text:
			now_time = time.localtime(time.time())
			max_num = (now_time.tm_year-2008)*365+now_time.tm_hour*30+now_time.tm_mday-601
			ran = random.randint(1,int(max_num))
			page = requests.get("https://www.pixivision.net/zh-tw/a/"+str(ran),verify = False)
			#page = requests.get("https://www.pixiv.net/showcase/a/3425/index.php?lang=zh_tw",verify = False)
			page.encoding = 'unicode'
			page = page.text
			while 'お探しのページが見つかりませんでした' in page:
				ran = random.randint(1,int(max_num))
				print("https://www.pixivision.net/zh-tw/a/"+str(ran))
				page = requests.get("https://www.pixivision.net/zh-tw/a/"+str(ran)+"",verify = False)
				page.encoding = 'unicode'
				page = page.text
			line_bot_api.push_message(event.source.user_id, TextSendMessage(text="https://www.pixivision.net/zh-tw/a/"+str(ran)))
		elif "/encode " in event.message.text:
			key = random.randint(1,2048)
			need = list(event.message.text[8:])
			
			for sss in range(0,len(need)-1):
				need[sss] = chr(ord(need[sss])+key)
			need.insert(0,chr(key))
			need = "".join(need)	
			line_bot_api.push_message(event.source.user_id, TextSendMessage(text=need))
		elif "/decode " in event.message.text:
			key = ord(event.message.text[8])
			need = list(event.message.text[9:])
			
			for sss in range(0,len(need)-1):
				need[sss] = chr(ord(need[sss])-key)
			need = "".join(need)	
			line_bot_api.push_message(event.source.user_id, TextSendMessage(text=need))
	else:
		if "/search" in event.message.text:
			message = event.message.text.replace("/search ","")
			search = message.replace(" ","%20").replace("/search","")
			all_search = search.split("%20")
			for ii in range(0,len(all_search)):
				if "100000" ==all_search[ii] or "50000" ==all_search[ii] or "10000" ==all_search[ii] or "5000" ==all_search[ii] or"1000" ==all_search[ii] or "500"==all_search[ii]:
					all_search[ii] = all_search[ii]+"users入り"            
			
			all_id = list()
			search = ""
			for ii in all_search:
				search+=ii+"%20"
			search = search[:-3]
			print(search)
			for page in range(0,11):
				print(page)
				get = requests.get("https://www.pixiv.net/search.php?word="+search+"&order=date_d&mode=safe&p="+str(page),verify = False)
				get.encoding = 'unicode'
				if '_p0_master1200.jpg' not in get.text:
					break
				else:
					pre=0
					while pre != -1:
						pos = get.text.find('_p0_master1200.jpg',pre)
						photo_id = get.text[pos-8:pos]
						if photo_id not in all_id:
							all_id.append(photo_id)
						pre = get.text.find("_p0_master1200.jpg",pre+10)
			if len(all_id) != 0:
				K = random.randint(0,len(all_id)-1)
				choose = all_id[K]
				page = requests.get("https://www.pixiv.net/member_illust.php?mode=medium&illust_id="+choose,verify = False).text

				possible = page[page.find("_p0_master1200.jpg")-100:page.find("_p0_master1200.jpg")+18]

				temp2 = page.find("comment-list")
				temp = page.find("tag_area")
				temp = page.find("tags-container",temp)
				text = page[temp:temp2]
				tags = "tags:\n  "
				temp = 0
				success = 0
				while temp!=7:
					temp = text.find("tag-value")+8
					if temp == 7:
						break
					text = text[temp:]
					tags+=text[3:text.find("</a>")]+"\n  "
					success = 1



				if success == 0:
					print("special")
					temp = page.find("for (var k in arg) {")
					temp2 = page.find("storableTags")
					print(temp)
					print(temp2)
					text = page[temp:temp2]
					#print(text)
					tags = "tags:\n  "
					while temp!=7:
						temp = text.find("\"tag\"")+3
						if temp == 2:
							break
						text = text[temp:]
						tags+=text[4:text.find("locked")-3]+"\n  "
					tags = tags.encode().decode("unicode_escape")
				line_bot_api.push_message(event.source.group_id, TextSendMessage(text="https://www.pixiv.net/member_illust.php?mode=medium&illust_id="+choose+"\n"+tags))

		elif "/random" in event.message.text:
			now_time = time.localtime(time.time())
			max_num = (now_time.tm_year-2008)*365+now_time.tm_hour*30+now_time.tm_mday-601
			ran = random.randint(1,int(max_num))
			page = requests.get("https://www.pixivision.net/zh-tw/a/"+str(ran),verify = False)
			#page = requests.get("https://www.pixiv.net/showcase/a/3425/index.php?lang=zh_tw",verify = False)
			page.encoding = 'unicode'
			page = page.text
			while 'お探しのページが見つかりませんでした' in page:
				ran = random.randint(1,int(max_num))
				print("https://www.pixivision.net/zh-tw/a/"+str(ran))
				page = requests.get("https://www.pixivision.net/zh-tw/a/"+str(ran)+"",verify = False)
				page.encoding = 'unicode'
				page = page.text
			line_bot_api.push_message(event.source.group_id, TextSendMessage(text="https://www.pixivision.net/zh-tw/a/"+str(ran)))
		elif "/encode " in event.message.text:
			key = random.randint(1,2048)
			need = list(event.message.text[8:])
			
			for sss in range(0,len(need)-1):
				need[sss] = chr(ord(need[sss])+key+sss)
			need.insert(0,chr(key))
			need = "".join(need)	
			line_bot_api.push_message(event.source.group_id, TextSendMessage(text=need))
		elif "/decode " in event.message.text:
			key = ord(event.message.text[8])
			need = list(event.message.text[9:])
			
			for sss in range(0,len(need)-1):
				need[sss] = chr(ord(need[sss])-key-sss)
			need = "".join(need)	
			line_bot_api.push_message(event.source.group_id, TextSendMessage(text=need))

if __name__ == "__main__":
	app.run()