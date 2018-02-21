# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 09:09:30 2018

@author: Hakim.Abbes
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 11:50:05 2017

@author: Hakim.Abbes
"""
import pandas as pd
import re

class Post_forum:
    
    def __init__(self,textfile="",dictionary="",*forums):
        """This object is a text file with the template set for AMV France forum.
        It can be converted for posting to other forums.
        The dictionary is in a excel file and is read for columns from the excel you specify in *forums"""
        try:
            self.fo = open(textfile,encoding="utf-8")
        except: 
            print("Error while opening the text. Check path for the text file.")
        self.translation={}
        self.translation['AMVFrance'] = self.fo.readlines()
        self.dictionary = pd.read_excel(dictionary)
        self.forums = list(forums)

        
    def change_date(self,year=2018,month=6,day=3,numcontest=0,dayjapan=8):
        """This will change all dates but is really dependent on the input, so check if everything looks fine.
        This is designed for Japan Expo and will not work with other contests."""
        i = 0
        for line in self.translation['AMVFrance']:
            line = re.sub('20\d[0-3|5-9]', str(year), line, flags=re.IGNORECASE)
            line = re.sub('contest/\d*/','contest/'+str(numcontest)+'/',line)
            
            line = re.sub('\d+ +juin',str(day)+' juin',line, flags=re.IGNORECASE)
            line = re.sub('June +\d{1,2}','June '+str(day),line, flags=re.IGNORECASE)
            line = re.sub('\d{1,2} +de Junio',str(day)+' de Junio',line, flags=re.IGNORECASE)

            line = re.sub('\d+ +juillet',str(dayjapan)+' juillet',line, flags=re.IGNORECASE)
            line = re.sub('July +\d{1,2}','July '+str(dayjapan),line, flags=re.IGNORECASE)
            line = re.sub('\d{1,2} +de Julio',str(dayjapan)+' de Julio',line, flags=re.IGNORECASE)

            line = re.sub('samedi +\d{1,2}','samedi '+str(dayjapan-1),line, flags=re.IGNORECASE)
            line = re.sub('dimanche +\d{1,2}','dimanche '+str(dayjapan),line, flags=re.IGNORECASE)

            line = re.sub('Saturday +\d{1,2}','Saturday '+str(dayjapan-1),line, flags=re.IGNORECASE)
            line = re.sub('Sunday +\d{1,2}','Sunday '+str(dayjapan),line, flags=re.IGNORECASE)

            line = re.sub('sabado +\d{1,2}','sabado '+str(dayjapan-1),line, flags=re.IGNORECASE)
            line = re.sub('domingo +\d{1,2}','domingo '+str(dayjapan),line, flags=re.IGNORECASE)
            self.translation['AMVFrance'][i]=line
            i += 1
            
    def convert_balise(self):
        """Convert all texts for the forums chosen."""
        self.forum_dict = {}
        self.fixed_amvfrance = self.translation['AMVFrance']
        for forum in self.forums:
            self.translate = "".join(self.fixed_amvfrance)
            try:
                self.forum_dict[forum] = dict(zip(self.dictionary['AMVFrance'],self.dictionary[forum]))
            except: 
                print("The forum "+forum+" is not found in the excel dictionary, check the spelling.")
            for balise in self.forum_dict[forum]:
                try:
                    self.translate = self.translate.replace(balise,self.forum_dict[forum][balise])
                except:
                    self.translate = self.translate.replace(balise,"")
            self.translation[forum] = self.translate.split("\n")
                
    def reorganize(self,language='EN'):
        """Need to reorganize for non french speaking forums"""
        if language == 'EN':
            self.reorg={}
            for forum in self.forums:
                self.eng_span = [i for i, j in enumerate(self.translation[forum]) if str(j).lower().find("english") > -1 and str(j).lower().find("spanish") > -1]
                self.french_start = [i for i in range(len(self.translation[forum])) if len(self.translation[forum][i]) >= 100][0]
                self.french_end = [i for i in range(len(self.translation[forum])) if self.translation[forum][i].find("http://www.amv-france.com/img/logo-JE_2014.jpg")>-1][0]-1
                self.english_start = [i for i, j in enumerate(self.translation[forum]) if str(j).lower().find("english version") > -1][0]              
                self.english_end = [i for i, j in enumerate(self.translation[forum]) if str(j).lower().find("version espa") > -1][0]      

                self.title_part = self.translation[forum][0:self.eng_span[0]]
                self.eng_span_part = [self.translation[forum][i] for i in self.eng_span] 
                self.post_part = self.translation[forum][self.eng_span[0]+1:self.french_start]
                self.french_part = self.translation[forum][self.french_start:self.french_end]
                self.logo_part = self.translation[forum][self.french_end+1:self.eng_span[1]]
                self.english_part = self.translation[forum][self.eng_span[1]+1:self.english_end]
                try: 
                    self.english_part[1] = self.english_part[1][self.english_part[1].find('"]')+2:]
                except:
                    print(self.english_part[1])
                self.versionfr = '[spoil="Version française"]'.replace("[spoil=",self.forum_dict[forum]["[spoil="] if type(self.forum_dict[forum]["[spoil="])==str else "")
                self.endspoil = '[/spoil]'.replace("[/spoil]",self.forum_dict[forum]["[/spoil]"] if type(self.forum_dict[forum]["[/spoil]"])==str else "")
                self.french_part = [self.versionfr]+self.french_part+[self.endspoil]
                self.english_part = self.english_part[0:-2]
                self.spain_part = self.translation[forum][self.english_end-1:]

                self.title_part.append(self.eng_span_part[0].replace("English","French"))
                self.logo_part.append(self.eng_span_part[1].replace("English","French"))
                self.reorg[forum] = self.title_part+self.post_part+self.english_part+self.logo_part+self.french_part+self.spain_part
                
        else:
            print("Choose a proprer language.")

    def write_translate(self):
        """Write everything to the home directory."""
        for forum in self.forums:
            f = open("{}_FR.txt".format(forum),"w+",encoding="utf-8")
            f.write("\n".join(self.translation[forum]))
            f.close()
            f = open("{}_EN.txt".format(forum),"w+",encoding="utf-8")
            f.write("\n".join(self.reorg[forum]))
            f.close()
            

