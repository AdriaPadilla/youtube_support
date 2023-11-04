if __name__ == "__main__":

    search_keywords = ["how to win money"]

    API_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXXXXx"
    youtube = build("youtube", "v3", developerKey=API_KEY)


    delta = timedelta(days=1)
    for q in search_keywords:
        loop = 0
        sub_loop = 0
        next_token = None
        print(f"Working on {q}")

        start_date = date(2019, 1, 1)
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


            get_video_details(q, loop, sub_loop, next_token, after, before, raw_folder, days)
