# -*- coding: utf-8 -*-
import re
import os
import shutil
import datetime
import requests
from film import *
import base64


### Clean last log
try: 
  shutil.copyfile("log.txt", "log.old.txt")
  os.remove("log.txt")
except: pass

host = base64.b64decode("aHR0cDovL3d3dy5jaW5lZmlzaC5iZw==")
url = host + "/movie.php?id=%s"


def scrap_page(id):
  film = Film()
  log("--------------------------------------------")
  log("Requesting url for scrapping: %s" % url % id)
  r = requests.get(url % id, headers={"User-agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"})
  log("Response code %s" % r.status_code)
  if r.status_code < 200 or r.status_code > 400:
    log("Exiting!", 2)
    return None

  html = r.text.encode('utf-8')

  ### ID
  film.id = id
  ### Title
  try:
    regex = re.compile("<title>(.+?)</title>")
    title_text = regex.findall(html)[0]
    needle = base64.b64decode("IC0g0YTQuNC70LzQuCwg0YLRgNC10LnQu9GK0YDQuCwg0YHQvdC40LzQutC4IC0gQ2luZWZpc2guYmc=")
    title_text = title_text.replace(needle, "")
    parts = title_text.split(",")
    l = len(parts)
    if l == 2:
      film.title = parts[0]
      titleOriginal = parts[1]
    elif l == 3:
      film.title = parts[0] + ", " + parts[1]
      titleOriginal = parts[2]
    elif l == 4:
      film.title = parts[0] + ", " + parts[1]
      titleOriginal = parts[2] + ", " + parts[3]
    else:
      film.title = title_text
      titleOriginal = title_text

    ### Title original
    try: film.titleOriginal = titleOriginal.lstrip().rstrip()
    except: 
      log("No original title found!", 1)
      
  except Exception, er:
    log("No title found on page! Exiting!", 2)
    log(html)
    return None

  ### Description
  try:
    regex = re.compile("<td valign=\"top\" class=\"page_film\">(?:<font size=\"\d*\">)*(.*?)(?:</font>)*</div>", re.DOTALL)
    film.plot = regex.findall(html)[0]
    film.plot = re.compile(r'<br\s*/>').sub(' ', film.plot)
    film.plot = re.compile(r'<[^>]+>').sub('', film.plot)
    #TODO clean html tags
  except:
    log("No plot extracted!", 1)
  
  ### Categories
  try: 
    regex = re.compile("genre_id=\d+['\"]+>(.+?)</a>")
    matches = regex.findall(html)
    film.categories = clean_html_list(matches)
  except:
    print log("No categories found!", 1)

  ### Length
  try: 
    regex = re.compile("/\s+(\d+?)\s+минути<br")
    film.length = int(regex.findall(html)[0])
  except:
    print log("No movie length found!", 1)

  ### Year
  try:
    regex = re.compile("movies\.php\?year=\d+['\"]+>(\d+?)</a>")
    film.year = int(regex.findall(html)[0])
  except:
    log("No year found!", 1)

  ### Country
  try:
    regex = re.compile("country_id=\d+[\"']+>(.*?)</a>")
    film.countries = regex.findall(html)
  except:
    log("No country found!", 1)

  ### Writers
  try:
    regex = re.compile("<b>Сценарист:</b>\n*\r*\s*(.+?)<br />")
    matches = regex.findall(html)[0].split(",")
    film.writers = clean_html_list(matches)    
  except:
    log("No writers found!", 1)

  ### Directors
  try:
    regex = re.compile("<b>Режисьор:</b>\n*\r*\s*(.+?)<br />")
    matches = regex.findall(html)[0].split(",")
    film.directors = clean_html_list(matches)
  except:
    log("No directors found!", 1)
    
  ### Cast
  try:
    regex = re.compile("<b>В\s+ролите:</b>\n*\r*\s*(.+?)<br />")
    matches = regex.findall(html)[0].split(", ")
    film.cast = clean_html_list(matches)
  except:
    log("No cast found!", 1)

  ### Image
  try:
    regex = re.compile("href=\"(.+?jpg)\".+?class=\"lightbox")
    film.image = host + regex.findall(html)[0]
  except:
    log("No image found!", 1)

  ### Trailer
  try:
    regex = re.compile("movie_trailers\.php\?id=(\d+?)\">")
    film.trailerId = int(regex.findall(html)[0])
  except:
    log("No trailer found!", 1)

  ### IMDB ID
  try:
    regex = re.compile("href=\"http://www\.imdb\.com/title/(tt\d+)")
    film.imdbId = regex.findall(html)[0]
  except:
    log("No IMDB id found!", 1)

  ### Parental rating
  try:
    regex = re.compile("Възрастова група:</b>\s*(?:&nbsp;)*(.+?)<")
    film.parentalRating = regex.findall(html)[0]
  except:
    log("No Parental rating found!", 1)

  return film


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
      levels: 0=Info, 1=Warning, 2=Error
  """
  
  #write to console
  formatted_msg = "%s | %s | %s" % (datetime.datetime.now(), LOGLEVEL[level], msg)
  if not "<!DOCTYPE" in str(msg):
    print formatted_msg
  
  #write to file
  with open("log.txt", "a") as w:
    w.write(formatted_msg + "\n")

LOGLEVEL = ["INFO", "WARNING", "ERROR"]
