import requests
import sqlite3
from time import sleep
from utils import *
from random import randint
import db

##############################
## SETTINGS
##############################
MAX_SCRAPPED_PAGES = 1000
MAX_TIMEOUT_BETWEEN_SCRAPS = 15
MIN_TIMEOUT_BETWEEN_SCRAPS = 5

print "###################################"
print " Fish4Cinema scrapper by Harry_GG "
print "###################################"

id = db.get_last_id() + 1
max = id + MAX_SCRAPPED_PAGES

while(id < max):
  movie = scrap_page(id)
  if movie:
    log("Adding movie to DB: %s " % movie.title)
    if db.add(movie):
      log("Success!")
    #log(movie.to_string())
    sleep_time = randint(MIN_TIMEOUT_BETWEEN_SCRAPS, MAX_TIMEOUT_BETWEEN_SCRAPS)
    log("Sleeping for %s seconds" % sleep_time)
    sleep(sleep_time)
  id += 1

log("Max scrabbed pages %s reached" % MAX_SCRAPPED_PAGES)