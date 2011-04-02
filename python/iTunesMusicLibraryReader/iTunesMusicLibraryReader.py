# -*- coding: utf-8 -*-

from xml.etree.cElementTree import iterparse
import base64, datetime, re, urllib

unmarshallers = {
  # collections
  "array": lambda x: [v.text for v in x],
  "dict": lambda x:
      dict((x[i].text, x[i+1].text) for i in range(0, len(x), 2)),
  "key": lambda x: x.text or "",
  # simple types
  "string": lambda x: x.text or "",
  "data": lambda x: base64.decodestring(x.text or ""),
  "date": lambda x: datetime.datetime(*map(int, re.findall("\d+", x.text))),
  "true": lambda x: True,
  "false": lambda x: False,
  "real": lambda x: float(x.text),
  "integer": lambda x: int(x.text),
}

def load(file):
  parser = iterparse(file)
  for action, elem in parser:
    unmarshal = unmarshallers.get(elem.tag)
    if unmarshal:
      data = unmarshal(elem)
      elem.clear()
      elem.text = data
    elif elem.tag != "plist":
      raise IOError("unknown plist type: %r" % elem.tag)
  return parser.root[0].text

# usage

itunes = load("iTunes Music Library.xml")

tracks = itunes["Tracks"]
tracks_keys = tracks.keys()
for i in tracks_keys:
  #FIXME: encode problem
  try:
    print i, tracks[i]["Artist"], "-", tracks[i]["Name"]
    print tracks[i]["Location"]
  except:
    pass

playlists = itunes["Playlists"]
for playlist in playlists:
  #FIXME: encode problem
  try:
    print "Playlist - ", playlist["Name"]
    for track_id in playlist["Playlist Items"]:
      print track_id["Track ID"],
  except:
    pass