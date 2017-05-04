# -*- coding: utf-8 -*-
import sys
reload(sys)  
sys.setdefaultencoding('utf8')

class Film():
  id = 0
  title = ""
  titleOriginal = ""
  plot = ""
  year = 0 
  length = 0
  image = ""
  categories = []
  countries = []
  writers = []
  directors = []
  cast = []

  imdbId = ""
  imdbRating = 0
  trailerId = 0
  trailerPath = ""
  parentalRating = ""
  
  def to_string(self):
    for k,v in vars(self).iteritems():
      if isinstance(v, list):
        v = ", ".join(v)          
      print "%s=%s" % (k, v.encode("utf-8"))

  def to_list(self):
    return (self.id, self.title.decode('utf8'), self.titleOriginal.decode('utf8'), 
            self.plot.decode('utf8'), self.year, self.length, self.image.decode('utf8'), 
            u", ".join(self.categories), u", ".join(self.countries), u", ".join(self.writers), 
            u", ".join(self.directors), u", ".join(self.cast), self.imdbId, self.imdbRating, 
            self.trailerPath.decode('utf8'), self.trailerId, self.parentalRating.decode('utf8'))