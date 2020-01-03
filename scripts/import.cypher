call apoc.load.json("file://items.json") YIELD value
WITH value, value.spotify.tracks.items[0] AS track

MERGE (chart:Chart {
  start: date(datetime({epochmillis: apoc.date.parse(value.start, "ms", "dd MMMM yyyy")})),
  end: date(datetime({epochmillis: apoc.date.parse(value.end, "ms", "dd MMMM yyyy")}))
})
MERGE (label:Label {name: value.label})
MERGE (song:Song {uri: value.track_uri})
SET song.title = value.track_name,
    song.duration = CASE WHEN track.duration_ms is null THEN null ELSE duration({milliseconds:track.duration_ms}) END

MERGE (song)-[:LABEL]->(label)
MERGE (song)-[inChart:IN_CHART]->(chart)
SET inChart.position = value.position

FOREACH(artist IN track.artists |
  MERGE (a:Artist {id: artist.id})
  SET a.name = artist.name
  MERGE (song)-[:ARTIST]->(a)
);
