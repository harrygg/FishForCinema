import requests
import sqlite3
from time import sleep
from utils import *
from random import randint
import db

##############################
## SETTINGS
##############################
MAX_SCRAPPED_PAGES = 4000
MAX_TIMEOUT_BETWEEN_SCRAPS = 10
MIN_TIMEOUT_BETWEEN_SCRAPS = 5
MAX_ERRORS = 3

print "###################################"
print " Fish4Cinema scrapper by Harry_GG "
print "###################################"

id = db.get_last_id() + 1
max = id + MAX_SCRAPPED_PAGES
errors = 0

while(id < max and errors <= MAX_ERRORS):

  movie = scrap_page(id)
  id += 1

  if movie == None:
    errors += 1
    continue

  log("Adding movie to DB: %s " % movie.title)
  if db.add(movie):
    log("Success!")

  sleep_time = randint(MIN_TIMEOUT_BETWEEN_SCRAPS, MAX_TIMEOUT_BETWEEN_SCRAPS)
  log("Sleeping for %s seconds" % sleep_time)
  sleep(sleep_time)


log("Max scrabbed pages %s reached" % MAX_SCRAPPED_PAGES)
