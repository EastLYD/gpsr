#!/usr/bin/env python

import rospy
import string
import nltk
from std_msgs.msg import String
from nltk.corpus import wordnet

class GPSR:
  def __init__(self):
    self.speech = rospy.Subscriber('voice_recog', String, self.NLP)
    self.token = []
    self.token_tag = []
    self.room_list = ["kitchen","bedroom","living_room"]
    self.object_list = ["chips","senbei","pringles","peanuts","chocolate","manju","mints","noodles","apple","paprika","watermelon","sushi","tea","beer","coke","sake","shampoo","soap","cloth","sponge","bowl","tray","plate"]

    #food, plant, koyu, sponge, shampoo, soap, cleansing agent, instrumentality.n.03
    # senbei -> cracker
    # pringles -> chips
    # manju -> cake
    # sake -> sake.n.02


  def NLP(self, message):
    hypernyms = self.WordNet(message.data, self.room_list + self.object_list)

    room = wordnet.synsets("room")[0]
    plant = wordnet.synsets("plant")[0]
    food = wordnet.synsets("food")[0]
    cleansing_agent = wordnet.synsets("cleansing_agent")[0]
    instrumentality = wordnet.synset("instrumentality.n.03")
    object_candidates = [room, plant, food, cleansing_agent, instrumentality]
    candidates_list = ["room", "plant", "food", "cleansing_agent", "instrumentality"]

    print hypernyms

    for hyp in hypernyms:
      if hyp.lemma_names()[0] is "sake":
        hyp = wordnet.synset("sake.n.02")
      

      max_similarity = [0, -1] # value, argmax

      for i in range(len(object_candidates)):
        if max_similarity[0] < hyp.path_similarity(object_candidates[i]):
          max_similarity = [hyp.path_similarity(object_candidates[i]), i]

      if max_similarity[0] > 0.1:
        #candidate found
        print "%s find : %s, likelifood : %f" % (candidates_list[max_similarity[1]], hyp, max_similarity[0])

  def WordNet(self,string, parameter_list):
    kitchen = []

    for i in range(len(parameter_list)):
      index = string.find(parameter_list[i])
      if index != -1:

        len_words = len(parameter_list[i])
        
        if  parameter_list[i] is "senbei":
          string = string.replace("senbei",wordnet.synsets("cracker")[0].lemma_names()[0])
          len_words = len("cracker")

        elif parameter_list[i] is "pringles":
          string = string.replace("pringles", wordnet.synsets("chips")[0].lemma_names()[0])
          len_words = len("french_fries")

        elif parameter_list[i] is "manju":
          string = string.replace("manju", wordnet.synsets("cake")[0].lemma_names()[0])
          len_words = len("cake")


        print "".join(string[index:index + len_words])

        kitchen.append(wordnet.synsets("".join(string[index:index + len_words]))[0])
      
    if len(kitchen) == 0:
      kitchen.append(wordnet.synset("hello.n.01"))
      print "can't find specified word", string

    return kitchen

if __name__ == "__main__":
    rospy.init_node("NLP")
    gpsr = GPSR()
    rospy.spin()
