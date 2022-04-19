class topic_modeling:
    def __init__(self):
        #Accounts
            #Facebook
        self.facebookPasword = None
        self.facebookPasword = None
    def scrapData (self,socialMedia=None,user=None):
        """
            scrapData (socialMedia="Facebook",user="Cookies")
        """
        if (socialMedia is None):
            raise Exception("Error: socialMedia is missing")
        if (user is None):
            raise Exception("Error: user is missing")
        result = 0   
        #Check social media to scrapp
        if   (socialMedia == "Reddit"):
            result = self.__redditScrappData(user)
        elif (socialMedia == "Twitter"):
            result = self.__twitterScrappData(user)
        elif  (socialMedia == "Facebook"):
            result = self.__facebookScrappData(user)
        else:
            raise Exception("Error: "+str(socialMedia)+" is not a valid value for socialMedia")
        self.__cleanData()

    def __redditScrappData(self,user=None):
        pass
    def __twitterScrappData(self,user=None):
        pass
    def __facebookScrappData(self,user=None):
        pass
    def __cleanData(self):
        pass
    def topicModeling(self,technic = None, type = None):
        if (technic is None):
            raise Exception("Error: technic is missing")
        if (type is None):
            raise Exception("Error: technic is missing")
        if   (technic == "Bertopic"):
            result = self.__bertopicTopicModeling()
        elif (technic == "Other"):
            result = self.__otherTopicModeling()
        else:
            raise Exception("Error: "+str(technic)+" is not a valid value for technic")
        self.__topicModelPlot()

    def __bertopicTopicModeling(self):
        pass
    def __otherTopicModeling(self):
        pass
    def __topicModelPlot(self):
        pass