# -*- coding: utf-8 -*-

import jieba
import configparser
import sqlite3
import operator
from os import listdir
import sys
import math
reload(sys)
sys.setdefaultencoding('utf-8')

#基于概率的BM25模型

class SearchEngine:

    stop_words = set()

    config_path = ''
    config_encoding = ''

    N = 0
    B = 0
    N = 0
    AVG_L = 0

    def __init__(self, config_path, config_encoding):
        self.config_path = config_path
        self.config_encoding = config_encoding
        config = configparser.ConfigParser()
        config.read(config_path, config_encoding)
        f = open(config['DEFAULT']['stop_words_path'])
        words = f.read()
        self.stop_words = set(words.split('\n'))
        self.conn = sqlite3.connect(config['DEFAULT']['db_path'])
        self.K1 = float(config['DEFAULT']['k1'])
        self.B = float(config['DEFAULT']['b'])
        self.N = int(config['DEFAULT']['n'])
        self.AVG_L = float(config['DEFAULT']['avg_l'])

    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def clean_list(self, seg_list):
        cleaned_dict = {}
        n = 0
        for i in seg_list:
            i = i.strip().lower()
            if i != '' and not self.is_number(i) and i not in self.stop_words:
                n = n + 1
                if i in cleaned_dict:
                    cleaned_dict[i] = cleaned_dict[i] + 1
                else:
                    cleaned_dict[i] = 1
        return n, cleaned_dict

    def result_by_BM25(self,sentence):
        seg_list = jieba.lcut(sentence,cut_all=True)
        n, cleaned_dict = self.clean_list(seg_list)
        BM25_scores = {}
        for term in cleaned_dict.keys():
            r = self.fetch_from_db(term)
            if r is None:
                continue
            df = r[1] #df 文档频率
            x = float((self.N - df + 0.5)) / float((df + 0.5))
            w = math.log(x,2)
            docs = r[2].split('\n')
            for doc in docs:
                docid, date_time, tf, ld = doc.split('\t')
                docid = int(docid)
                tf = int(tf)   #词频
                ld = int(ld)   #文档长度
                s = (self.K1 * tf * w) / (tf + self.K1 * (1 - self.B + self.B * ld / self.AVG_L))
                print("---------")
                print(docid)
                print(df)
                print(tf)
                print(ld)
                print(s)
                print("---------")

    #从索引中取出包含单词的文章
    def fetch_from_db(self, term):
        c = self.conn.cursor()
        c.execute('SELECT * FROM postings WHERE term=?', (term,))
        return (c.fetchone())


if __name__ == "__main__":
    im = SearchEngine('../config.ini', 'utf-8')
    # test = im.result_by_BM25(u'广东实行生育登记制度')
    x = im.fetch_from_db(u'世界')
    print(x[1])
    print(x[2])
    # print(test[1])
    # print(test[2].split('\n'))
    #Minimum threshold value
    # for i in test:
    #     print(i)
    # print(test.decode('unicode-escape'))
