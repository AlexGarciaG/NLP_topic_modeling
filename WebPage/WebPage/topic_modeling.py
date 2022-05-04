import datetime
import pandas as pd
import numpy as np
import tweepy
import praw
import spacy
from spacy import displacy
# importing the model en_core_web_sm of English for vocabluary, syntax & entities
import en_core_web_sm
#Word tokenization
from spacy.lang.en import English
from gensim.parsing.preprocessing import remove_stopwords, strip_punctuation,preprocess_string, strip_short, stem_text
from googleapiclient.discovery import build
import facebook
from bertopic import BERTopic
from gensim import corpora
from gensim.models import LsiModel
from gensim.models.coherencemodel import CoherenceModel
from matplotlib import pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import matplotlib.colors as mcolors

class topic_modeling:
    def __init__(self):
        self.posts = []
        #Twitter
        consumer_key_twitter = ""
        consumer_secret_twitter = ""
        access_key_twitter = ""
        access_secret_twitter = ""
        auth = tweepy.OAuthHandler(consumer_key_twitter, consumer_secret_twitter)
        auth.set_access_token(access_key_twitter, access_secret_twitter)
        
        self.apiTwitter = tweepy.API(auth,wait_on_rate_limit=True)
        #Reddit
        client_id_reddit=""
        client_secret_reddit=""
        password_reddit=""
        user_agent_reddit=""
        username_reddit=""
        self.reddit = praw.Reddit(
            client_id=client_id_reddit,
            client_secret=client_secret_reddit,
            password=password_reddit,
            user_agent=user_agent_reddit,
            username=username_reddit,
        )
        #YouTube
        api_key = ''
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        #Clean data
        # Load English tokenizer, tagger, parser, NER and word vectors
        self.nlp = English()

        # load en_core_web_sm of English for vocabluary, syntax & entities
        self.nlp = en_core_web_sm.load()
        self.topic_model = BERTopic()
    def get_tweets(self,name,num_tweets = 100,option='2'):
        if option=='1':
            data=[]
            tweets = self.apiTwitter.user_timeline(screen_name=name,tweet_mode='extended',count=num_tweets)
            for tweet in tweets:
                comentData=tweet.full_text
                comentDate=(tweet.created_at)
                data.append([comentData,comentDate]) 
            self.posts = pd.DataFrame(data,columns = ['date','text']) 
        elif option == '2':
            places = self.apiTwitter.search_geo(query=name,granularity='country',max_results=int(num_tweets)) #Select the country
            if places:
                place_id = places[0].id
            # Define the search term and the date_since date as variables
            search_words = "(#politics OR politics) -filter:retweets place:%s " % place_id
            # Collect tweets
            tweets = tweepy.Cursor(self.apiTwitter.search_tweets,
                        q=search_words,
                        lang="en").items(int(num_tweets))
            self.posts = pd.DataFrame()
            # Put tweets in a DataFrame, it takes time to recover the tweets
            for tweet in tweets:
                if tweet.place is not None:        
                    self.posts = self.posts.append({
                        'date':tweet.created_at,
                        'text':tweet.text
                        },ignore_index=True) 


    def get_reddit(self,user):
        redditUser = self.reddit.redditor(user)
        #Get user comments
        comments = redditUser.comments.new(limit=None)
        #Create a list of the data
        data=[]
        for comment in comments:
            comentData=comment.body
            comentDate=datetime.datetime.fromtimestamp(comment.created_utc)
            data.append([comentDate,comentData]) 
        #Create a data frame and save it as a csv
        self.posts = pd.DataFrame(data,columns = ['date','text'])

    def get_facebook(self,id,token):
        graph = facebook.GraphAPI(access_token=token, version = 3.1)
        html = "/"+id+"/posts?"
        events = graph.request(html)
        data=[]
        for p in events['data']:
            if p.get('message') is not None :
                comentData=p['message']
                comentDate=p['created_time']
                data.append([comentDate,comentData]) 
        self.posts  = pd.DataFrame(data,columns = [ 'date','text'])

    def get_videos (self,chanal,maxNResults):
        request = self.youtube.channels().list(
                part='contentDetails',
                forUsername=chanal
            )
        response = request.execute()
        id= (response['items'][0]['id'])
        request = self.youtube.search().list(
                part="snippet",
                channelId=id,
                type='video',
                order='date',
                maxResults=maxNResults
            )
        response = request.execute()
        data=[]
        for video in response['items']:
            comentData=video['snippet']['title']
            comentDate=video['snippet']['publishedAt']
            data.append([comentDate,comentData]) 
        self.posts = pd.DataFrame(data,columns = ['date','text'])
        
    def __eliminate_info(self,text):
        if type(text) == pd._libs.tslibs.nattype.NaTType:
            return text
        else:
            #  "nlp" Objects used to create documents with linguistic annotations.
            doc = self.nlp(text)
            # Create list of word tokens
            token_list = []
            for token in doc:
                token_list.append(token.text)
                entities=[(i, i.label_, i.label) for i in doc.ents]
                filt_doc = (" ".join([ent.text for ent in doc if not ent.ent_type_]))
                my_doc = self.nlp(filt_doc)
                #print(filt_doc)
                #s = ' '.join(my_doc) 
                return my_doc.text
    
    def cleanData(self):
        for index, row in self.posts.iterrows():
            self.posts.at[index,'text']=self.__eliminate_info(row['text'])

    def Bert_topic(self,numbeTopTopics):
        
        self.topics, self.probs = self.topic_model.fit_transform(self.posts['text'])
        numbeTopTopics=min(int(numbeTopTopics),len(self.topic_model.get_topic_info()))
        return self.topic_model.visualize_topics(topics = range(0,numbeTopTopics))
        
        

    def Dynamic_Bert_topic(self,numbeTopTopics):
        
        self.topics, self.probs = self.topic_model.fit_transform(self.posts['text'])
        numbeTopTopics=min(int(numbeTopTopics),len(self.topic_model.get_topic_info()))
        self.topics_over_time = self.topic_model.topics_over_time(self.posts['text'], self.topics, self.posts['date'], nr_bins = 20)
        return self.topic_model.visualize_topics_over_time(self.topics_over_time, topics=range(0,numbeTopTopics))
    
        
        

    def LSA (self,number_of_topics=2):
        corpus=self.posts['text'].apply(lambda x: self.__lsapreprocess(x))
        dictionary = corpora.Dictionary(corpus)
        # convert corpus into a bag of words
        bow = [dictionary.doc2bow(text) for text in corpus]
        # generate LDA model
        model = LsiModel(bow, number_of_topics, id2word=dictionary)

        cols = [color for name, color in mcolors.TABLEAU_COLORS.items()]  # more colors: 'mcolors.XKCD_COLORS'

        cloud = WordCloud(stopwords=3,
                        background_color='white',
                        width=2500,
                        height=1800,
                        #max_words=10,
                        colormap='tab10',
                        color_func=lambda *args, **kwargs: cols[i],
                        prefer_horizontal=1.0)

        topics = model.show_topics(formatted=False)

        fig, axes = plt.subplots(1, 2
        , figsize=(10,10), sharex=True, sharey=True)

        for i, ax in enumerate(axes.flatten()):
            fig.add_subplot(ax)
            topic_words = dict(topics[i][1])
            cloud.generate_from_frequencies(topic_words, max_font_size=300)
            plt.gca().imshow(cloud)
            plt.gca().set_title('Topic ' + str(i), fontdict=dict(size=16))
            plt.gca().axis('off')


        plt.subplots_adjust(wspace=0, hspace=0)
        plt.axis('off')
        plt.margins(x=0, y=0)
        plt.tight_layout()
        return plt
    def __lsapreprocess(self,text):
        CUSTOM_FILTERS = [lambda x: x.lower(), 
                                    remove_stopwords, 
                                    strip_punctuation, 
                                    strip_short, 
                                    stem_text]
        text = preprocess_string(text, CUSTOM_FILTERS)
        
        return text        