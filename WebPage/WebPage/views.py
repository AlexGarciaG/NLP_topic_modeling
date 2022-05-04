from pydoc import render_doc
from django.http import HttpResponse
from django.shortcuts import render
import random
import matplotlib
from pandas import array
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np
from WebPage.topic_modeling import topic_modeling
from io import StringIO
import traceback

def inicio (request):
    return render(request, "inicio.html", {})
def twitter (request):
    return render(request, "twitter.html", {})
def reddit (request):
    return render(request, "reddit.html", {})
def facebook (request):
    return render(request, "facebook.html",{})
def youtube (request):
    return render(request, "youtube.html",{} )


def chose_topic (request):
    array = {}
    NLP_topic_modeling = topic_modeling()
    #get data
    if 'how_to_get_data' in request.GET.keys():
        
        
        try:
            if request.GET['how_to_get_data'] == '1':
                NLP_topic_modeling.get_tweets(request.GET['name'],request.GET['maxNumber'],request.GET['get_data_by'])
            elif request.GET['how_to_get_data'] == '2':
                NLP_topic_modeling.get_reddit(request.GET['name'])
            elif request.GET['how_to_get_data'] == '3':
                NLP_topic_modeling.get_facebook(request.GET['name'],request.GET['tokenF'])
            elif request.GET['how_to_get_data'] == '4':
                NLP_topic_modeling.get_videos(request.GET['name'],request.GET['maxNumber'])
        except:
            array['error'] = 'Error fail to get data'
            return render(request, "chose_topic.html", array)
    else:
        array['error'] = 'Error fail to get data'
        return render(request, "chose_topic.html", array)
    #clean data
    try:
        NLP_topic_modeling.cleanData()
    except:
        array['error'] = 'Error fail to clean data'
        return render(request, "chose_topic.html", array)
    #plot data
    try:
        if request.GET['topic_modeling'] == '1':
            array['plot']=NLP_topic_modeling.Bert_topic(request.GET['maxNumberTop']).to_html(full_html=False)
        elif request.GET['topic_modeling'] == '2':
            array['plot']=NLP_topic_modeling.Dynamic_Bert_topic(request.GET['maxNumberTop']).to_html(full_html=False)
        elif request.GET['topic_modeling'] == '3':
            imgdata = StringIO()
            fig1 = NLP_topic_modeling.LSA(request.GET['maxNumberTop']).gcf()
            fig1.savefig(imgdata, format='svg', transparent=True)
            imgdata.seek(0)
            data = imgdata.getvalue()
            array['MatPlot']=data
        

    except Exception as e:
        array['error'] = 'Error fail to plot data'
        return render(request, "chose_topic.html", array)
    return render(request, "chose_topic.html", array)