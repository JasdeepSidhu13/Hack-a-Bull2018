
import json
import pandas as pd
import matplotlib.pyplot as plt
import re


def word_in_text(word, text):
    word = word.lower()
    text = text.lower()
    match = re.search(word, text)
    if match:
        return True
    return False


def extract_link(text):
    regex = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
    match = re.search(regex, text)
    if match:
        return match.group()
    return ''


def main():
    # Reading Tweets
    print('Reading Tweets\n')
    tweets_data_path = 'twitter_data2.txt'

    tweets_data = []
    tweets_file = open(tweets_data_path, "r")
    for line in tweets_file:
        try:
            tweet = json.loads(line)
            tweets_data.append(tweet)
        except:
            continue


            # Structuring Tweets
    print('Structuring Tweets\n')
    tweets = pd.DataFrame()
    tweets['text'] = list([tweet['text'] for tweet in tweets_data])
    tweets['lang'] = list([tweet['lang'] for tweet in tweets_data])
    tweets['country'] = list([tweet['place']['country'] if tweet['place'] != None else None for tweet in tweets_data])


    # Analyzing Tweets by Language
    print('Analyzing tweets by language\n')
    tweets_by_lang = tweets['lang'].value_counts()
    fig, ax = plt.subplots()
    ax.tick_params(axis='x', labelsize=10)
    ax.tick_params(axis='y', labelsize=10)
    ax.set_xlabel('Languages', fontsize=10)
    ax.set_ylabel('Number of tweets', fontsize=10)
    ax.set_title('Top 5 languages', fontsize=10, fontweight='bold')
    tweets_by_lang[:5].plot(ax=ax, kind='bar', color='red')
    plt.savefig('tweet_by_lang', format='png')


    # Analyzing Tweets by Country
    print('Analyzing tweets by country\n')
    tweets_by_country = tweets['country'].value_counts()
    fig, ax = plt.subplots()
    ax.tick_params(axis='x', labelsize=10)
    ax.tick_params(axis='y', labelsize=10)
    ax.set_xlabel('Countries', fontsize=10)
    ax.set_ylabel('Number of tweets', fontsize=10)
    ax.set_title('Top 5 countries', fontsize=10, fontweight='bold')
    tweets_by_country[:5].plot(ax=ax, kind='bar', color='blue')
    plt.savefig('tweet_by_country', format='png')


    # Adding programming languages columns to the tweets DataFrame
    print('Adding programming languages tags to the data\n')
    tweets['earthquake'] = tweets['text'].apply(lambda tweet: word_in_text('earthquake', tweet))
    tweets['hurricane'] = tweets['text'].apply(lambda tweet: word_in_text('hurricane', tweet))
    tweets['floods'] = tweets['text'].apply(lambda tweet: word_in_text('floods', tweet))


    # Analyzing Tweets by programming language: First attempt
    print('Analyzing tweets by active disasters: First attempt\n')
    prg_langs = ['earthquake', 'hurricane', 'floods']
    tweets_by_prg_lang = [tweets['earthquake'].value_counts()[True], tweets['hurricane'].value_counts()[True],
                          tweets['floods'].value_counts()[True]]
    x_pos = list(range(len(prg_langs)))
    width = 0.8
    fig, ax = plt.subplots()
    plt.bar(x_pos, tweets_by_prg_lang, width, alpha=1, color='g')
    ax.set_ylabel('Number of tweets', fontsize=10)
    ax.set_title('Ranking: earthquake vs. hurricane vs. floods (Raw data)', fontsize=10, fontweight='bold')
    ax.set_xticks([p + 0.4 * width for p in x_pos])
    ax.set_xticklabels(prg_langs)
    plt.grid()
    plt.savefig('tweet_by_diaster_freq.', format='png')


    # Targeting relevant tweets
    print('Targeting relevant tweets\n')
    tweets['crisis'] = tweets['text'].apply(lambda tweet: word_in_text('crisis', tweet))
    tweets['danger'] = tweets['text'].apply(lambda tweet: word_in_text('danger', tweet))
    tweets['emergency'] = tweets['text'].apply(
        lambda tweet: word_in_text('programming', tweet) or word_in_text('emergency', tweet))


    # Analyzing Tweets by programming language: Second attempt
    print('Analyzing tweets by disaster analysis: First attempt\n')

    import IPython
    IPython.embed()

    def get_value_counts(tweets, language):
         try:
             return tweets[tweets['relevant'] == True][language].value_counts()[True]
         except KeyError:
             return 0

    tweets_by_prg_lang = [get_value_counts(tweets, 'earthquake'),
                          get_value_counts(tweets, 'hurricane'),
                          get_value_counts(tweets, 'floods')]
    x_pos = list(range(len(prg_langs)))
    width = 0.8
    fig, ax = plt.subplots()
    plt.bar(x_pos, tweets_by_prg_lang, width, alpha=1, color='g')
    ax.set_ylabel('Number of tweets', fontsize=10)
    ax.set_title('Ranking: earthquake vs. hurricane vs. floods (Relevant data)', fontsize=10, fontweight='bold')
    ax.set_xticks([p + 0.4 * width for p in x_pos])
    ax.set_xticklabels(prg_langs)
    plt.grid()
    plt.savefig('tweet_by_disaster_analysis', format='png')


    # Extracting Links
    tweets['link'] = tweets['text'].apply(lambda tweet: extract_link(tweet))
    tweets_relevant = tweets[tweets['relevant'] == True]
    tweets_relevant_with_link = tweets_relevant[tweets_relevant['link'] != '']

    print('\nBelow are some Python links that we extracted\n')
    print(tweets_relevant_with_link[tweets_relevant_with_link['earthquake'] == True]['link'].head())



if __name__ == '__main__':
    main()