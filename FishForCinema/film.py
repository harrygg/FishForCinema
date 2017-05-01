class Film():
  title = None
  titleOriginal = None
  year = 0
  plot = None
  length = 0
  image = None
  categories = []
  countries = []
  writers = []
  directors = []
  cast = []

  imdbId = None
  imdbRating = 0
  trailerId = None
  trailerPath = None

  def to_string(self):
    for k,v in vars(self).iteritems():
      if isinstance(v, list):
        v = ", ".join(v)          
      print "%s=%s" % (k, v.encode("utf-8"))
