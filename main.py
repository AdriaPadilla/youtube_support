from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
import time
import json
from datetime import date, timedelta


API_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXX" # YOUR API KEY
youtube = build("youtube", "v3", developerKey=API_KEY)

# DEFINE YOUR SEARCH QUERY IN search_keywords var
search_keywords = ["how to win money"]

def get_video_details(q, loop, sub_loop, next_token, after, before, query_folder, days):
    filename = f"{query_folder}/{loop}-{sub_loop}--{after}-{before}.json"
    if os.path.exists(filename):
            print("yet downloaded")
            pass
    else:
        yt_api_response = youtube.search().list(
            q=q,
            part="id",
            maxResults=50,
            order="date",
            type="video",
            safeSearch="none",
            videoDuration="any",
            regionCode="es",
            relevanceLanguage="es",
            pageToken=next_token,
            publishedAfter=after,
            publishedBefore=before,
            channelId="",

        ).execute()
        print(f"Query {loop}/{days} - {q} from {after} to {before} | VIDEOS in Query: {yt_api_response['pageInfo']['resultsPerPage']}")
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(yt_api_response, f, ensure_ascii=False, indent=4)

        try:
            next_token = yt_api_response["nextPageToken"]
            time.sleep(0.1)
            sub_loop = sub_loop + 1
            get_video_details(q, loop, sub_loop, next_token, after, before, query_folder, days)
        except KeyError:
            pass

if __name__ == "__main__":

    base_folder = "extracts"
    query_folder = f"{base_folder}/{search_keywords}"
    if not os.path.exists(query_folder):
        os.makedirs(query_folder)

    delta = timedelta(days=1)

    for q in search_keywords:
        loop = 0
        sub_loop = 0
        next_token = None
        print(f"Working on {q}")

        start_date = date(2023, 1, 1)
        end_date = date(2023, 10, 1)

        date_diff = end_date-start_date
        days = date_diff.days
        print(start_date, end_date)

        while start_date <= end_date:
            after = start_date.strftime("%Y-%m-%dT00:00:00Z")
            before = start_date + delta
            before = before.strftime("%Y-%m-%dT00:00:00Z")
            start_date += delta
            loop = loop + 1

            get_video_details(q, loop, sub_loop, next_token, after, before, query_folder, days)
