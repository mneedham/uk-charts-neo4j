MATCH (song:Song)-[inChart:IN_CHART {position: 1}]->(chart),
      (song)-[:ARTIST]->(artist)
WITH song, collect(artist) AS artists, inChart, chart ORDER BY chart.start
RETURN song.title,
       [artist in artists | artist.name] AS artists,
       apoc.date.format(song.duration.milliseconds, 'ms', 'mm:ss') AS duration,
       count(*) AS count,
       collect(toString(chart.end)) AS weeks
ORDER By count DESC;

MATCH (song:Song)-[inChart:IN_CHART {position: 1}]->(chart),
      (song)-[:ARTIST]->(artist)
WITH artist, song, count(*) AS weeks
RETURN artist.name,
       apoc.map.fromPairs(collect([song.title, weeks])) AS songs,
       count(*) AS count,
       sum(weeks) AS weeks
ORDER BY weeks DESC;

MATCH (label:Label)<-[:LABEL]-()-[inChart:IN_CHART]->(:Chart {end: date("2019-12-26")})
RETURN label.name, min(inChart.position) AS bestPosition, count(*), collect(inChart.position)
ORDER BY bestPosition;

MATCH (song:Song)-[inChart:IN_CHART]->(:Chart {end: date("2019-12-26")})
RETURN song.name, apoc.date.format(song.duration.milliseconds, 'ms', 'mm:ss'), inChart.position
ORDER BY inChart.position;
