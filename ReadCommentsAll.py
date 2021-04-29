# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 21:25:48 2021

@author: nitis
"""

from psaw import PushshiftAPI
import datetime
import requests
import json
import codecs
from pathlib import Path
import sys
import time

class ReadCommentsAll():
    def __init__(self,subreddit_name,limit):
        print("API parameters:",subreddit_name,limit)
        
        ranges = [(1,1,2019,1,2,2019),(1,2,2019,1,3,2019),(1,3,2019,1,4,2019),(1,4,2019,1,5,2019),(1,5,2019,1,6,2019),(1,6,2019,1,7,2019),(1,7,2019,1,8,2019),(1,8,2019,1,9,2019),(1,9,2019,1,10,2019),(1,10,2019,1,11,2019),(1,11,2019,1,12,2019),(1,12,2019,1,1,2020),(1,1,2020,1,2,2020),(1,2,2020,1,3,2020),(1,3,2020,1,4,2020),(1,4,2020,1,5,2020),(1,5,2020,1,6,2020),(1,6,2020,1,7,2020),(1,7,2020,1,8,2020),(1,8,2020,1,9,2020),(1,9,2020,1,10,2020),(1,10,2020,1,11,2020),(1,11,2020,1,12,2020),(1,12,2020,1,1,2021),(1,1,2021,1,2,2021),(1,2,2021,1,3,2021),(1,3,2021,1,4,2021)]
        
        for d1,m1,y1,d2,m2,y2 in ranges:
            posted_after   = int(datetime.datetime(y1, m1, d1).timestamp())
            posted_before  = int(datetime.datetime(y2, m2, d2).timestamp())
            
            self.api            = PushshiftAPI()
            self.comBatchNo     = 0
            self.outputPath     = './{0}/{1}/'.format(subreddit_name, posted_after)
            
            Path(self.outputPath).mkdir(parents=True, exist_ok=True)
            
            self.getComments(subreddit_name,
                    None,
                    ['created_utc','score','selftext','title','upvote_ratio','body'],
                    posted_after,
                    posted_before,
                    limit
                    )
    
    def saveData(self, items:list):
        fileId      = 0
        filePath    = ''
        
        self.comBatchNo += 1
        fileId      = self.comBatchNo
        filePath    = self.outputPath
        
        filePath += 'file'+str(fileId)
        
        print("{0} - {1} - {2}".format(time.time(), len(items), filePath))
        
        data = ''
        
        for item in items:
            data += item + '\n'
        
        with codecs.open(filePath, 'w', encoding = 'utf-8-sig') as file:
            file.write(data)
        
        data = None
    
    def getComments(self, subreddit_name:str, query:str, fields:list, after:int, before:int, limit=1000, sortOrder='desc', sortType='score'):
        try:
            query       = self.api.search_comments(subreddit=subreddit_name, after=after, before=before, limit=limit, filter = fields)
            submissions = list()
            
            for element in query:
                submissions.append(json.dumps(element.d_))
                if len(submissions) == 1000:
                    self.saveData(submissions.copy())
                    submissions = list()
            
            if len(submissions) > 0:
                self.saveData(submissions.copy())
                submissions = list()
        except:
            print("Unexpected error:", sys.exc_info())
        
        print("Done!!!")

if __name__ == "__main__":
    print(f"Arguments count: {len(sys.argv)}")
    ReadCommentsAll(str(sys.argv[1]),int(sys.argv[2]))