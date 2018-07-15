# -*- coding: utf-8 -*-
import chardet
import configparser

class IndexModule:

    stop_words = set()

    config_path = ''
    config_encoding = ''

    def __init__(self,config_path,config_encoding):
        self.config_path = config_path
        self.config_encoding = config_encoding
        config = configparser.ConfigParser()
        config.read(config_path,config_encoding)
        # 读取停用词
        f = open(config['DEFAULT']['stop_words_path'])
        words = f.read()
        self.stop_words = set(words.split('\n'))
        

if __name__ == "__main__":
    im = IndexModule('../config.ini', 'utf-8')



