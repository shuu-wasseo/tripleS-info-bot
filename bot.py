import tweepy
import logging
import time
import datetime

# Authenticate to Twitter
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

msgs = {
    "!nfts": """
    	debunking misconceptions about tripleS and NFTs: a thread
    	'The NFT itself is not a core value of our system. I started this project to have more participation from fans and more activity. As a voting tool, the NFT has a certain value and transparency because it cannot be manipulated. 
        We could vote via email, text or CD, but we’ve seen many manipulation scandals. With this technology, we have integrity in our votes. TripleS is a girl group with many decisions made by fan vote, not a girl group with NFTs.' ~ jaden jeong in an interview with NME
        additionally, polygon (the blockchain system that modhaus is running on) has pledged to become carbon negative by the end of 2022. https://polygon.technology/blog/polygon-is-going-carbon-negative-in-2022-with-a-20-million-pledge
        polygon has already reached carbon neutrality as of june 2022. https://www.prnewswire.com/ae/news-releases/polygon-network-reaches-first-sustainability-milestone-by-achieving-carbon-neutrality-301571777.html
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
        jaden jeong isn't the best person, but he wasn't as shit as you guys make him out to be. if you even knew how the k-pop industry works, you would know most of the things that jaden jeong allegedly did were obviously not true.
        read more here: https://www.reddit.com/r/LOONA/comments/nmm7ea/lets_lay_to_rest_this_false_narrative_that_jaden/
    """,
    "!voting": """
    	debunking misconceptions about the tripleS voting system: a thread
        tripleS' voting system is not like a survival system. so far, the only form of fan voting to decide members of a unit was in the form of 'grand gravity'. 
        the first grand gravity separated S1-S8 into 4 pairs. in each pair, one member would be in the unit AAA while the other would be in the unit KRE. each member at the time had a chance to debut in a unit. 
        this allows all members to get to debut in at least one unit, and does not leave any members being treated extremely unfairly (left out of unit activities / without a unit / etc.) as you can see from the tweet below, each member was placed in a unit.
https://twitter.com/triplescosmos/status/1574005796693839875
    """,
    "!salary": """
    	unlike most idols, tripleS members are paid like MODHAUS employees. according to MODHAUS staff in the AMA: "profits from Objekt will be shared with our artists, even before the cumulative BEP is made".
        source of AMA: https://unopnd.notion.site/AMA-Recap-f25d4c4893734e46b33d09c119ea2949
    """,
    "!guide": """
    	to learn more about tripleS, read varsha (@vibts713)'s guide here: https://docs.google.com/presentation/d/1rjc9o6Wm2NLOPuPdMVt0oCXIDIYobVMdVIUmNmcU2rc/edit?usp=sharing
       	for a shorter and less dense timeline, try shua (@kajetesantakalu, the bot's creator)'s timeline here: https://triples-timeline.carrd.co
        for even more information, join the discord server at https://discord.gg/triplescosmos!
    """,
    "!help": """
    	to learn how to use the bot, visit https://shuu-wasseo.github.io/tripleS-info-bot-docs/.
    """
}

id = 1608738653559488514

def log(info):
    logger.info(str(datetime.datetime.now()) + " " + info )

def create_client():
    client = tweepy.Client(
        # secrecy
    )
    log("client created")
    return client

def check_mentions(client, keywords, since_id):
    log("retrieving mentions")
    new_since_id = since_id
    ments = client.get_users_mentions(id, since_id=since_id).data
    if ments is not None:
        for tweet in ments:
            if any(keyword in tweet.text.lower() for keyword in keywords):
                new_since_id = max(tweet.id, new_since_id)
                for keyword in keywords:
                    if keyword in tweet.text.lower():
                        try:
                            tweets = [tweet.id]
                            text = [l.strip() for l in msgs[keyword].split("\n") if l.strip() != ""]
                            for t in text:
                                if t != "":
                                    newt = client.create_tweet(
                                        text=t,
                                        in_reply_to_tweet_id=tweets[-1],
                                        user_auth=True
                                    ).data
                                    tweets.append(newt["id"])
                            log(f"answering with keyword {keyword}, tweet id {tweet.id}")
                        except tweepy.errors.Forbidden:
                            return new_since_id + 1
    return new_since_id

def main():
    client = create_client()
    with open('readme.txt') as f:
        since_id = int(f.readlines()[0].strip())
    while True:
        since_id = check_mentions(client, list(msgs.keys()), since_id)
        log("waiting...")
        with open('readme.txt', 'w') as f:
            f.write(str(since_id))
        time.sleep(10)

if __name__ == "__main__":
    main()
