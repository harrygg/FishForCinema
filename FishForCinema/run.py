import requests
import sqlite3
from time import sleep
from bs4 import BeautifulSoup
from utils import *

##############################
## SETTINGS
##############################

print "###################################"
print " Starting scrapper "
print "###################################"

id = get_last_id()

while(id < 4):
  movie = None
  movie = scrap(id)
  if movie:
    print "Movie title: %s " % movie.title
    log(movie.to_string())
    sleep(5)
  id += 1