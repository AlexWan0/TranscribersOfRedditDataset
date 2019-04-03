import urllib.request as request
import urllib
import json
import praw
import html
import re
import time
import csv
import os

REDDIT_CLIENT_ID = "CLIENT ID"
REDDIT_CLIENT_SECRET = "CLIENT SECRET"
REDDIT_USER_AGENT = "USERAGENT"
ALLOWED_IMAGE_EXTENSIONS = ["png", "jpg"]
OUTPUT_FILE_NAME = "data.csv"
DOWNLOAD_IMAGES = True
IMAGE_DIRECTORY = "images"

reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID, client_secret=REDDIT_CLIENT_SECRET, user_agent=REDDIT_USER_AGENT)

def get_posts(time_before=round(time.time())):
	res = request.urlopen("https://api.pushshift.io/reddit/search/submission/?subreddit=TranscribersOfReddit&limit=1000&sort=desc&before="+str(time_before)).read()

	data = json.loads(res)

	return data["data"]

posts = get_posts()

with open(OUTPUT_FILE_NAME, "w", encoding="utf-8") as output_file:
	csv_writer = csv.writer(output_file, lineterminator="\n")
	while len(posts) > 0:
		for p in posts:
			submission = reddit.submission(id=p["id"])
			#print(submission.link_flair_text)
			if submission.link_flair_text == "Completed!":
				print("Found:", submission.title)

				post_url = p["url"]
				image_post = reddit.submission(url=post_url)

				image_url = image_post.url

				image_post_id = image_post.id

				file_split = image_url.split(".")
				file_ext = file_split.pop()

				if file_ext in ALLOWED_IMAGE_EXTENSIONS:
					for comment in image_post.comments:
						#print(comment.body)
						if "image transcription" in comment.body.lower():
							if DOWNLOAD_IMAGES:
								try:
									request.urlretrieve(image_url, os.path.join(IMAGE_DIRECTORY, image_post_id+"."+file_ext))
								except urllib.error.HTTPError as err:
									print("Image not found, skipping...")
									break

							body_raw = comment.body

							body_clean = html.unescape(body_raw)
							body_clean = body_clean.strip()
							body_lines = body_clean.splitlines()
							body_clean = " ".join(body_lines[1:len(body_lines)-1])
							body_clean = re.sub(r"\[[^\[\]\(\)]{0,}\]\([^\[\]\(\)]{0,}\)", "", body_clean)
							body_clean = re.sub(r"[^\w: \.\[\]/'\"]", "", body_clean)
							body_clean = re.sub(r" {2,}", " ", body_clean)
							body_clean = body_clean.strip()

							#print(post_url, image_url)
							#print(body_raw, body_clean)

							csv_writer.writerows([[image_post_id, post_url, image_url, body_clean]])

							break
			
		oldest_time = min(posts, key=lambda x:x["created_utc"])["created_utc"]

		print("Scraping next oldest batch:", str(oldest_time))

		posts = get_posts(oldest_time)