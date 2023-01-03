import tweepy
import logging
import datetime
import pytz

utc=pytz.UTC

# Authenticate to Twitter
msgs = {
    "!nfts": """
    	debunking misconceptions about tripleS and NFTs: a thread
    	'The NFT itself is not a core value of our system. I started this project to have more participation from fans and more activity. As a voting tool, the NFT has a certain value and transparency because it cannot be manipulated. 
        We could vote via email, text or CD, but we’ve seen many manipulation scandals. With this technology, we have integrity in our votes. TripleS is a girl group with many decisions made by fan vote, not a girl group with NFTs.' ~ jaden jeong in an interview with NME
        read more here: https://twitter.com/gwnyoo/status/1587253190885605379?s=20&t=KfAttZgS-aFSylnKJ1ZfTg
        source of interview: https://www.nme.com/news/music/jaden-jeong-triples-acid-angel-from-asia-disband-controversy-interview-modhaus-nft-3363178
    """,
    "!disband": """
       	debunking misconceptions about tripleS and disbanding units: a thread
    	'We built this band with the intention of having many types of sub-unit and to make many different types of music, but with the fans’ participation and decisions. If someone is asking if AAA is disbanded, our answer is ‘half yes, half no’. 
        We can’t say that AAA is going to have another album come out, but we do have a fundamental principle that fans can decide our next steps. We can never say never.' ~ jaden jeong in an interview with NME
        read more here: https://twitter.com/gwnyoo/status/1587253190885605379?s=20&t=KfAttZgS-aFSylnKJ1ZfTg
        source of interview: https://www.nme.com/news/music/jaden-jeong-triples-acid-angel-from-asia-disband-controversy-interview-modhaus-nft-3363178
    """,
    "!jj": """
        jaden jeong isn't the best person, but god fucking dammit he wasn't as shit as you guys make him out to be. if you even knew how the k-pop industry works, you would know most of the things that jaden jeong allegedly did were obviously not true.
        read more here: https://www.reddit.com/r/LOONA/comments/nmm7ea/lets_lay_to_rest_this_false_narrative_that_jaden/
    """,
    "!voting": """
    	debunking misconceptions about the tripleS voting system: a thread
        tripleS' voting system is not like a survival system. so far, the only form of fan voting to decide members of a unit was in the form of 'grand gravity'. the first grand gravity separated S1-S8 into 4 pairs. 
        in each pair, one member would be in the unit AAA while the other would be in the unit KRE. each member at the time had a chance to debut in a unit. 
        this allows all members to get to debut in at least one unit, and does not leave any members being treated extremely unfairly (left out of unit activities / without a unit / etc.) as you can see from the tweet below, each member was placed in a unit.
https://twitter.com/triplescosmos/status/1574005796693839875
    """,
    "!salary": """
    	unlike most idols, tripleS members are paid like MODHAUS employees. according to MODHAUS staff in the AMA: "profits from Objekt will be shared with our artists, even before the cumulative BEP is made".
        source of AMA: https://unopnd.notion.site/AMA-Recap-f25d4c4893734e46b33d09c119ea2949
    """,
    "!guide": """
    	to learn more about tripleS, read varsha (@vibts713)'s guide here: https://docs.google.com/presentation/d/1rjc9o6Wm2NLOPuPdMVt0oCXIDIYobVMdVIUmNmcU2rc/edit?usp=sharing
        for even more information, join the discord server at https://discord.gg/triplescosmos!
    """,
    "!help": """
    	to learn how to use the bot, visit https://shuu-wasseo.github.io/tripleS-info-bot-docs/.
    """
}

id = 1608738653559488514

def create_client():
    client = tweepy.Client(
        consumer_key="zdlLN0kAr1D4dYbJyTyAzfGHg",
        consumer_secret="SLWQsQmiQ87jAMBtOCEE6TM5wGByRDk5cFJHXla00UFd1rpUDn",
        access_token="1608738653559488514-qOJxFiqg7wsjllTe3QHwpEwOp8g7gY",
        access_token_secret="Hh432CsX5yIFf8kOf8lJPkoggZ6z6ukKjuDw7suNVDTWZ",
        bearer_token="AAAAAAAAAAAAAAAAAAAAAI2pkwEAAAAAsCh6efOxZumxm%2FiCzrxG28cXAMI%3DBO4av3FvP1Qkn2opyQrkCrmXlNdAee9xLeIf6wAqWP7z2nNn9X",
    )
    return client

def check_mentions(client, keywords, start, end):
    stats = {
        "commands": {command: 0 for command in keywords},
        "users": {}
    }
    start = utc.localize(datetime.datetime.combine(start, datetime.time(0, 0)))
    end = utc.localize(datetime.datetime.combine(end, datetime.time(0, 0)))
    lastsid = 1
    while 1:
        brk = False
        ids = [t.id for t in client.get_users_mentions(id, start_time=start, since_id=lastsid, max_results=100).data if any(keyword in t.text for keyword in keywords)]
        if len(ids) == 0:
            break
        ments = client.get_tweets(ids, tweet_fields=["created_at", "author_id", "in_reply_to_user_id"]).data
        ol = lastsid
        if ments is not None:
            lastsid = ments[0].id
            for tweet in ments:
                dt = tweet.created_at
                if dt > start and dt < end and tweet.in_reply_to_user_id != None:
                    for k in keywords:
                        if k in tweet.text:
                            try:
                                stats["commands"][k] += 1
                            except:
                                pass
                    try:
                        stats["users"][client.get_user(id=tweet.author_id).data.username] += 1
                    except:
                        stats["users"][client.get_user(id=tweet.author_id).data.username] = 1
                elif dt > end:
                    brk = True
                    break
        if brk == True or ol == lastsid:
            break
    return stats

def main():
    stt = datetime.date(2023, 1, 1)
    end = datetime.date(2023, 1, 31)
    client = create_client()
    stats = check_mentions(client, list(msgs.keys()), stt, end)
    for x in stats:
        stats[x] = {k: v for k, v in sorted(stats[x].items(), key=lambda item: item[1], reverse=True)}
        for y in stats[x]:
            if y != "tripleSinfobot":
                print(y, stats[x][y])
        print()

if __name__ == "__main__":
    main()
