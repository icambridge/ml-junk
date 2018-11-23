import praw
import re
import pandas



def get_ebay_url(string):
    matches = re.findall("https?:\/\/[a-z]+\.ebay\.[a-z]+/[^\s\]\)]+", string)
    if len(matches) == 0:
        return ""
    return matches[0]

def get_imgur_url(string):
    matches = re.findall("https?:\/\/i?.?imgur\.com/[^\s\]\)]+", string)
    if len(matches) == 0:
        return ""
    return matches[0]

reddit = praw.Reddit(client_id='fc4jAkTY3VhJ9Q', client_secret="lStY4VIk558nTqWLleUwbW9mgnk",
                     password='alittlebot', user_agent='HockeyBot/0.1',
                     username='hockey_hilights_bot')

urls = []
legits = []
post_urls = [
    "https://www.reddit.com/r/hockeyjerseys/comments/8noyr2/monthly_legit_check_thread_june_2018/",
    "https://www.reddit.com/r/hockeyjerseys/comments/9c0x8t/monthly_legit_check_thread_september_2018/",
    "https://www.reddit.com/r/hockeyjerseys/comments/93mfbf/monthly_legit_check_thread_august_2018/",
    "https://www.reddit.com/r/hockeyjerseys/comments/8v7gnw/monthly_legit_check_thread_july_2018/",
    "https://www.reddit.com/r/hockeyjerseys/comments/8g5s2m/monthly_legit_check_thread_may_2018/",
    "https://www.reddit.com/r/hockeyjerseys/comments/88w2kt/legit_check_thread_april_edition/",
    "https://www.reddit.com/r/hockeyjerseys/comments/81bsup/legit_check_thread_march_edition/",
    "https://www.reddit.com/r/hockeyjerseys/comments/7ugjvp/legit_check_thread_february_edition/",
    "https://www.reddit.com/r/hockeyjerseys/comments/7nonr3/legit_check_thread_january_edition/",
    "https://www.reddit.com/r/hockeyjerseys/comments/7h83r3/legit_check_thread_december_edition/"
]

for post_url in post_urls:
    print(post_url)
    post = reddit.submission(url=post_url)
    post.comments.replace_more(limit=None)
    count = 0
    for top_level_comment in post.comments:
        legit = -1
        for second_level_comment in top_level_comment.replies:
            print(second_level_comment.karma)

            foundLegit = re.findall("(legit|good|real)\.?",second_level_comment.body, re.IGNORECASE)
            if foundLegit:
                legit = 1
                break
            foundFake = re.findall("(fake|counterfeit)\.?",second_level_comment.body, re.IGNORECASE)
            if foundFake:
                legit = 0
                break

        if legit == -1:
            continue

        url = get_ebay_url(top_level_comment.body)
        if url != "":
            urls.append(url)
            legits.append(legit)
            count = count+1
            continue
        url = get_imgur_url(top_level_comment.body)
        if url != "":
            urls.append(url)
            legits.append(legit)
            count = count+1
            continue

df = pandas.DataFrame({"url": urls, "legit": legits})

df.to_csv("hockey_jerseys_raw.csv")
