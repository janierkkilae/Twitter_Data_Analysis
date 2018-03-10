## Note: the code as a whole should work if using the "Export Data" .csv from https://analytics.twitter.com
# Function takes as input a .csv and renders a report.
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re
from datetime import datetime
import collections

def twitter_report(csv):
    df = pd.read_csv(csv)
    # get and print topscores
    df2 = df.sort_values('engagements', ascending=False)
    print('Top 5 tweets by engagements:')
    print(df2[['Tweet text', 'engagements']].head(5))
    df2 = df.sort_values('impressions', ascending=False)
    print()
    print('Top 5 tweets by impressions:')
    print(df2[['Tweet text', 'impressions']].head(5))
    print()
    print('On average a tweet gets:')
    print('    ', df['impressions'].mean(), ' impressions')
    print('    ', df['engagements'].mean(), ' engagements')
    print('    ', df['retweets'].mean(), ' retweets')
    print('    ', df['likes'].mean(), ' likes')
    print('    ', df['replies'].mean(), ' replies')
    print('    ', df['url clicks'].mean(), ' link clicks')
    print('    ', df['user profile clicks'].mean(), ' profile clicks')

    # has visual
    df_novisual = df[df['media engagements'] == 0]
    df_visual = df[df['media engagements'] != 0]
    print()
    print('Should you add a visual to your tweets?')
    print('Impressions without a visual:', df_novisual['impressions'].mean())
    print('Impressions with a visual:', df_visual['impressions'].mean())

    # define times
    df['yyyy'] = df['time'].str[0:13]
    df['year'] = df['time'].str[0:4]
    df['month'] = df['time'].str[5:7]
    df['day'] = df['time'].str[8:10]
    df['hour'] = df['time'].str[11:13]
    df['yyyy'] = df['yyyy'].astype(str)
    df['yyyy'] = pd.to_datetime(df['yyyy'], yearfirst=True)
    df['weekday'] = df['yyyy'].dt.weekday

    # Performance metrics
        # How many tweets were posted?
    def stat_metric(date_item):
        df_new = df.groupby(df[date_item]).count()
        plt.plot(df_new['impressions'])
        plt.ylabel('Tweets posted')
        plt.xlabel(date_item)
        plt.title('When do you tweet?')
        plt.show()

        # At what time do tweets perform better?
    def performance_metric(date_item):
        df_impressions_temp = df.groupby(df[date_item]).count()
        df_impressions = df_impressions_temp['Tweet id']
        df_impressions_temp2 = df.groupby(df[date_item]).sum()
        df_new = df_impressions_temp2.join(df_impressions, how='left', lsuffix='_left', rsuffix='_right')
        df_new['imp_per_tweet'] = df_new['impressions']/df_new['Tweet id_right']
        plt.plot(df_new['imp_per_tweet'])
        plt.ylabel('Impression per tweet')
        plt.xlabel(date_item)
        plt.title('When do tweets perform best?')
        plt.show()

    def length_metric():
        df['text_length'] = df['Tweet text'].str.len()
        df2 = df[['text_length', 'impressions', 'engagements']]
        plt.scatter(df2['text_length'], df2['impressions'])
        plt.ylabel('Impressions')
        plt.xlabel('Characters (incl. visual)')
        plt.title('Do longer tweets perform better?')
        plt.show()
        print('Correlation between length, impressions and engagements (R^2):')
        print(df2.corr(method='pearson', min_periods=1))

    # counts top 100 used hashtags
    def hashtag_analyser():
        strings = []
        for a, tweet_content in  df['Tweet text'].astype(str).iteritems():
            pat = re.compile(r"#(\w+)")
            hashtag=pat.findall(tweet_content)
            strings.append(hashtag)
        hashtags = []
        for lists in strings:
            for single_hashtag in lists:
                hashtags.append(single_hashtag.lower())
        # this code is from https://stackoverflow.com/questions/2290962/python-how-to-get-sorted-count-of-items-in-a-list
        def leaders(xs, top=100):
            counts = collections.defaultdict(int)
            for x in xs:
                counts[x] += 1
            return sorted(counts.items(), reverse=True, key=lambda tup: tup[1])[:top]
        print('most used hashtags:', leaders(hashtags))

    # launcher for all functions
    stat_metric('year')
    stat_metric('month')
    stat_metric('weekday')
    stat_metric('hour')
    performance_metric('year')
    performance_metric('month')
    performance_metric('weekday')
    performance_metric('hour')
    length_metric()
    hashtag_analyser()

# # Define here your .csv path (use the formatting provided by Twitter Analytics)
csv = 'example.csv'
twitter_report(csv)
