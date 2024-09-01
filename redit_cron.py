# Import Necessary Libraries
import logging
import time
from reddit_creds import *
import nltk
from nltk import tokenize
import itertools
import re
from database_connect import *
from joblib import Parallel, delayed
import socket
import sys
import pandas as pd
import datetime
from tqdm import tqdm
import praw
import os
os.chdir('/root/Desktop/scrapping_full/cron')
sys.path.insert(0, '/root/Desktop/scrapping_full/cron')
pool = Parallel(n_jobs=-1, pre_dispatch='all')
s = socket.socket()
s.settimeout(60)
nltk.download('punkt')
global connection, cursor
logging.getLogger("selenium").setLevel(logging.ERROR)

# create the reddit praw object,
reddit = praw.Reddit(client_id=ID,
                     client_secret=SECRET,
                     password=PASSWORD,
                     user_agent=AGENT,
                     username=USER, check_for_async=False)

start_time = time.time()
date = datetime.datetime.now().strftime(
    "%Y-%m-%d %H:%M:%S")  # -datetime.timedelta(days=6))
# now we will Create and configure logger
logging.basicConfig(
    filename=f"logs/redit_update_{date}.log", format='%(asctime)s %(message)s', filemode='w')

# Let us Create an object
logger = logging.getLogger()

# Now we are going to Set the threshold of logger to ERROR
logger.setLevel(logging.ERROR)

# to get the print statement in the log
print = logging.error

# EDITED PART
# updating brand table with redit mentions count

# Updating data into brand_table
def save_brand_redit(connection, cursor, redit, brand_name):
    data_tuple = (redit, brand_name, brand_name)
    cursor.execute("UPDATE brand_table SET ReditMentions= %s where BrandName= %s and Timestamp=(select c.cTime from(select             max(Timestamp) as cTime from brand_table where  BrandName=%s) as c)", data_tuple)
    connection.commit()


# accessing database and master table and getting shopify brands only
query = """SELECT BrandName, BrandSite, ShopifySite FROM master_table WHERE ShopifySite LIKE '%.%'"""
brands_categroy = shopify_master_only(query)

stime = time.time()
logger.error(f"Redit mention scrapping started")
print('#### Getting Redit mentions ####')
try:
    connection, cursor = master_db_login()
    for i in tqdm(range(int(len(brands_categroy)/3), int(2*len(brands_categroy)/3))):

        mentions = []
        name = brands_categroy['BrandName'][i]
        print(name)
        try:
            for submission in reddit.subreddit("all").search('#'+name, sort="comments", limit=None):
                # [^\x00-\x7F]+ to remove non ascii characters
                text = re.sub(
                    r'[^\x00-\x7F]+', ' ', submission.selftext.encode("ascii", "ignore").decode())
                text_list = tokenize.sent_tokenize(text)
                for text in text_list:
                    if re.search(fr'\b{name.lower()}\b', text.lower(), flags=re.IGNORECASE):
                        mentions.append(text)
            length = len(mentions)
            # finding repeated redit sentences
            if len(mentions) > 0:
                df2_redit = pd.read_sql_query(
                    f"""select * from redit_mentions where BrandName="{name}" """, connection)
                previous = ' '.join(list(itertools.chain.from_iterable(
                    df2_redit['ReditMentionsText'].values.tolist())))
                # [^\w\s] to remove non digit characters
                previous = re.sub(r'[^\w\s]', '', previous)
                mentions = json.dumps([x for x in mentions if (
                    (len(re.findall(re.sub(r'[^\w\s]', '', x), previous)) == 0) & (len(str(x)) > 10))])
            if len(mentions) == 0:
                mentions = 'NULL'

            sqlite_insert_with_param = """INSERT IGNORE INTO brand_table
                              (Timestamp,BrandName,ReditMentions) 
                              VALUES (%s,%s,%s);"""

            data_tuple = (date, name, length)
            cursor.execute(sqlite_insert_with_param, data_tuple)
            sqlite_insert_with_param = """INSERT IGNORE INTO redit_mentions 
                                  (Timestamp,BrandName,ReditMentionsText,ReditMentions) 
                                  VALUES (%s,%s,%s,%s);"""
            data_tuple = (date, name.replace("'", "\\'"), mentions, length)
            cursor.execute(sqlite_insert_with_param, data_tuple)
            connection.commit()
        except Exception as e:
            print(f'skipping {name}')
            print(e)
            continue
#         break
    connection.close()

except Exception as e:
    print(e)
feed_time = time.time()

logger.error(f"Redit mention scrapping end, time taken {feed_time - stime}")
