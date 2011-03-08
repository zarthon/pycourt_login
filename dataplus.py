from pycourt_login import models
import datetime
import random,string,re,cgi

def getUniqueId(length=12):
    allowedChars = "abcdefghijklmnopqrstuvwzyzABCDEFGHIJKLMNOPQRSTUVWZYZ0123456789"
    word = ""
    for i in range(0,length):
        word = word+ allowedChars[random.randint(0,0xffffff)%len(allowedChars)]
    return word

def dictGetval(dic,key,otherwise=None):
    try:
        result = dic[key]
    except:
        return otherwise
    return result

def returnIfExists(query_set):
    if query_set.count()>0:
        return query_set[0]
