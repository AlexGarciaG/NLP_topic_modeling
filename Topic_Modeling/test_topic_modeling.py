from topic_modeling import topic_modeling
test_topic_modeling = topic_modeling()
#test_topic_modeling.get_tweets("USA",500,'2')
test_topic_modeling.get_reddit('V0IDN')
#access_token= 'EAAQkKTpRYoUBABS33mkybE83EJZAQK7SBace8RNXRPEhLWPZAsbklKuHzlMOGrPCfL88dUZAe22QLZBkOLAuZA1WJELdEw7kSBbuT5xZACBIVlrBgjntIQosIoVVDFUErkR0aGwpLSJhi9SXtitrNLcTV3cyQlLoOFmhpL88OlbF0lFZBG25tZAYncZA0QuZAf5mnue5i6aZCbUQH5wQwrnwQNMv4WrTkcd5GYlcFZBf1qCYZCswRK42vf9Bp'
#test_topic_modeling.get_facebook("5266027646789347",access_token)
#test_topic_modeling.get_videos('LinusTechTips',300)
#test_topic_modeling.cleanData()
a=(test_topic_modeling.Bert_topic(5))
#print(a)
#a.savefig('foo.png')
