CREATE INDEX ON :Chart(start);
CREATE CONSTRAINT ON (l:Label) ASSERT l.name IS UNIQUE;
CREATE CONSTRAINT ON (s:Song) ASSERT s.uri IS UNIQUE;
CREATE CONSTRAINT ON (a:Artist) ASSERT a.id IS UNIQUE;

CALL apoc.load.json("file://items.json")
YIELD value

MERGE (chart:Chart {
  start: date(datetime({epochmillis: apoc.date.parse(value.start, "ms", "dd MMMM yyyy")})),
  end: date(datetime({epochmillis: apoc.date.parse(value.end, "ms", "dd MMMM yyyy")}))
})
MERGE (label:Label {name: value.label})
MERGE (song:Song {uri: value.track_uri})
SET song.title = value.track_name,
    song.duration = CASE WHEN value.duration is null THEN null ELSE duration({milliseconds:value.duration}) END

MERGE (song)-[:LABEL]->(label)
MERGE (song)-[inChart:IN_CHART]->(chart)
SET inChart.position = value.position

FOREACH(artist IN value.artists |
  MERGE (a:Artist {id: artist.id})
  SET a.name = artist.name
  MERGE (song)-[:ARTIST]->(a)
);
