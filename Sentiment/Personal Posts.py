import os
import json
import facebook
import requests

if __name__ == "__main__":
	token = os.environ.get("TEMP_TOKEN")
	
	graph = facebook.GraphAPI(token)
	all_fields=[
	'message',
	'created_time',
	'description',
	'caption',
	'place'
	'status_type'
	'Comments',
	'likes']
	all_fields=','.json(all_fields)
	profile = graph.get_object('me', 'posts')

	while True:
		try:
			with open(my_posts.json,'a') as fb:
				for post in posts['data']:
					fb.write(json.dumps(post)+"\n")
				posts = requests.get(posts['paging']['next']).json()
		except KeyError:
#No pages left, break loop
			break