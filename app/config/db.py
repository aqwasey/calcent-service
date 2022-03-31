from pymysql.cursors import DictCursor
from pymongo import MongoClient
import pymysql
from dotenv import load_dotenv
import os

load_dotenv()


def demo():
    print(os.getenv("musr"))
    print(os.getenv("mpwd"))
    print(os.getenv("mport"))
    print(os.getenv("mser"))


def db():
    # connecting to mongo db server
    monc = MongoClient('127.0.0.1', 27017)
    # working database selected
    raw_db = monc['luvuyo-call-center']
    return raw_db


def mdo():
    conn = pymysql.connect(host='000.000.000.000', port=3306,
                           user='******', password='*******',
                           db='*******', charset='utf8')
    return conn
