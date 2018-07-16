# -*- coding: utf-8 -*-

import jieba
import configparser
import sqlite3
from os import listdir
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#基于概率的BM25模型

class SearchEngine:

    stop_words = set()
    config_path = ''
    config_encoding = ''

    def __init__(self, config_path, config_encoding):
        self.config_path = config_path
        self.config_encoding = config_encoding
        config = configparser.ConfigParser()
        config.read(config_path, config_encoding)
        f = open(config['DEFAULT']['stop_words_path'])
        words = f.read()
        self.stop_words = set(words.split('\n'))
        self.conn = sqlite3.connect(config['DEFAULT']['db_path'])

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
            print("result:"+"/".join(seg_list))

    def fetch_from_db(self, term):
        c = self.conn.cursor()
        c.execute('SELECT * FROM postings WHERE term=?', (term,))
        return (c.fetchone())


if __name__ == "__main__":
    im = SearchEngine('../config.ini', 'utf-8')
    test = im.fetch_from_db(u'中国')
    print(test)
