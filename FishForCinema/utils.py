# -*- coding: utf-8 -*-
import re
import os
import sys
import datetime
import requests
from film import *
import base64

reload(sys)  
sys.setdefaultencoding('utf8')

### Clean last log
try: os.remove("log.txt")
except: pass

host = base64.b64decode("aHR0cDovL3d3dy5jaW5lZmlzaC5iZw==")
url = host + "/movie.php?id=%s"
#soup = BeautifulSoup(r.text)


def scrap(id):  
  film = Film()
  log("requesting url: %s" % url % id)
  r = requests.get(url % id)
  log("response code %s" % r.status_code)
  html = r.text.encode('utf-8')

  ### Title
  try:
    regex = re.compile("<title>(.+?)</title>")
    t = regex.findall(html)[0]
    t = t.replace(" - филми, трейлъри, снимки - Cinefish.bg", "")
    film.title = t.split(",")[0]
    log("Movie title: %s" % film.title)
    
    ### Title original
    try: film.titleOriginal = t.split(",")[1]
    except: 
      log("Original title not found on page!")
      
  except Exception, er:
    log("Title not found on page! Exiting!")
    log(html)
    return None

  ### Description
  try:
    regex = re.compile("<td valign=\"top\" class=\"page_film\">(?:<font size=\"\d*\">)*(.*?)(?:</font>)*</div>", re.DOTALL)
    film.plot = regex.findall(html)[0]
    film.plot = re.compile(r'<br\s*/>').sub(' ', film.plot)
    film.plot = re.compile(r'<[^>]+>').sub('', film.plot)
    #TODO clean html tags
  except Exception, er:
    print log("No plot extracted!")
    log(html)
  
  ### Categories
  try: 
    regex = re.compile("genre_id=\d+['\"]+>(.+?)</a>")
    matches = regex.findall(html)
    film.categories = clean_html_list(matches)
  except:
    print log("No categories found!")

  ### Length
  try: 
    regex = re.compile("/\s+(\d+?)\s+минути<br")
    film.length = regex.findall(html)[0]
  except:
    print log("No movie length found!")

  ### Year
  try:
    regex = re.compile("movies\.php\?year=\d+['\"]+>(\d+?)</a>")
    film.year = regex.findall(html)[0]
  except:
    log("No year found!")

  ### Country
  try:
    regex = re.compile("country_id=\d+[\"']+>(.*?)</a>")
    film.countries = regex.findall(html)
  except:
    log("No country found!")

  ### Writers
  try:
    regex = re.compile("<b>Сценарист:</b>\n*\r*\s*(.+?)<br />")
    matches = regex.findall(html)[0].split(",")
    film.writers = clean_html_list(matches)    
  except:
    log("No writers found!")

  ### Directors
  try:
    regex = re.compile("<b>Режисьор:</b>\n*\r*\s*(.+?)<br />")
    matches = regex.findall(html)[0].split(",")
    film.directors = clean_html_list(matches)
  except:
    log("No directors found!")
    
  ### Cast
  try:
    regex = re.compile("<b>В\s+ролите:</b>\n*\r*\s*(.+?)<br />")
    matches = regex.findall(html)[0].split(", ")
    film.cast = clean_html_list(matches)
  except:
    log("No cast found!")

  ### Image
  try:
    regex = re.compile("href=\"(.+?jpg)\".+?class=\"lightbox")
    film.image = host + regex.findall(html)[0]
  except:
    log("No image found!")

  ### Trailer
  try:
    regex = re.compile("movie_trailers\.php\?id=(\d+?)\">")
    film.trailerId = regex.findall(html)[0]
  except:
    log("No trailer found!")

  ### IMDB ID
  try:
    regex = re.compile("href=\"http://www\.imdb\.com/title/(tt\d+)")
    film.imdbId = regex.findall(html)[0]
  except:
    log("No IMDB id found!")

  return film

def get_last_id():
  return 4

def clean_href(entry):
  try:
    regex = re.compile("<a[^>]*>(.*?)</a>")
    cleaned = regex.findall(entry)[0].lstrip().rstrip()
    return cleaned
  except: 
    return entry

def clean_html_list(entries):
  results = []
  for entry in entries:
    results.append(clean_href(entry))
  return results

def log(msg, level=0, debug=True):
  """ Logs messages to console and log.txt
      levels: 1=Errors only, 2=Info, 3=Debug
  """
  
  #write to console
  formatted_msg = "%s | %s | %s" % (datetime.datetime.now(), LOGLEVEL[level], msg)
  if not "<!DOCTYPE" in str(msg):
    print formatted_msg
  
  #write to file
  with open("log.txt", "a") as w:
    w.write(formatted_msg + "\n")

LOGLEVEL = ["INFO", "ERROR"]
