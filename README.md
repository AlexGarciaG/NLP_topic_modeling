# NLP_topic_modelling

Topic modeling is an unsupervised machine learning technique that discovers relevant topics within a text. In this project will be investigate and implement various topic modeling techniques.

## Team Members
#### Fernanda Bueso Medina
#### Emiliano Etienne Iracheta
#### Alexis García Gutiérrez
#### Diego Garza Noriega
#### Gregorio González Franco

## Install
Download and install the following libraries:

```

pip install praw

pip install tweepy

pip install spacy

pip install facebook-sdk

pip install requests

pip install bertopic

pip install gensim

pip install wordcloud

pip install kaleido

pip install django

pip install django-crispy-forms

pip install django-widget-tweaks

```
## Topic_Modelling
The objective of the project is to use topic modelling techniques to find the most frequent topic that was generated throughout different posts of users in different online platforms (Reddit, Twitter, YouTube, Facebook). Two different techniques were applied: BERTopic and Latent Semantic Analysis/Indexing.

### The following steps will explain how to install the required library and requirements.
Firstly, posts collected must be processed to anonymize any sensitive information (people's names, geographic locations, email addresses and cell phone numbers), and any hyperlinks must be removed. This step was done with the help of the spaCy library.

### The following steps will explain how to use  NLP_topic_modelling.

#### BERTopic
The first topic modeling technique used was BERTopic. For this step the bertopic library was installed and used. BERTopic supports guided, (semi-) supervised, and dynamic topic modeling. The input received was the dataframe containing the different posts from a user over time. The output generated was the list of topic words most commonly found throughout the posts made by the user.

#### LSA/LSI
The second topic modeling technique chosen was Latent Semantic Analysis/Indexing. The library used in this step was gensim, a library specifically focused on topic modelling, document indexing and similarity retrieval with large corpora. The input received was the dataframe containing the different posts from a user over time. The output generated was the list of topic words most commonly found throughout the posts made by the user.
For more information about LSA technique a video explanation can be found in the following link: https://youtu.be/_muodj2Qv6k

### To know to how topic_modeling read topic_modeling.md

## Aditional Functionalities
In addition to twitter and reddit, information was also extracted from Facebook and YouTube. Also, a web page was designed.
