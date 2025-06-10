import feedparser

FEED_URL = "https://news.ycombinator.com/rss"


def main():
    feed = feedparser.parse(FEED_URL)
    for entry in feed.entries[:10]:
        print(entry.title)


if __name__ == "__main__":
    main()
