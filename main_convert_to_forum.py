# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 16:09:43 2018

@author: Hakim.Abbes
"""

import os
os.chdir("H:/Mes images/Graph/Amv France/convert_to_forum-master")
import convert_to_forum
Post_forum = convert_to_forum.Post_forum

Post = Post_forum('japan_expo2017_AMVFRANCE.txt','Forum_dict.xlsx','AMVFrance','Forumactif','Site','Org','Central','News')

Post.change_date(year=2018,day=3,dayjapan=8,numcontest=33)
#Post.translation['AMVFrance']

Post.convert_balise()

Post.reorganize()

Post.write_translate()