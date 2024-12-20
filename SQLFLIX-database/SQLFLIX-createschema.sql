CREATE TABLE name (
    nconst TEXT PRIMARY KEY,
    primaryName TEXT,
    birthYear NUMERIC(4,0),
    deathYear NUMERIC(4,0),
    primaryProfession TEXT[],
    knownForTitles TEXT[]
);


CREATE TABLE ratings (
    tconst TEXT PRIMARY KEY,
    averageRating NUMERIC(3,1),
    numVotes INTEGER
);

CREATE TABLE basics (
    tconst TEXT PRIMARY KEY,
    titleType TEXT,
    primaryTitle TEXT,
    originalTitle TEXT,
    isAdult BOOLEAN,
    startYear NUMERIC(4,0),
    endYear NUMERIC(4,0),
    runtimeMinutes INTEGER,
    genres TEXT[]
);

CREATE TABLE principal (
    tconst TEXT,
    ordering INTEGER, 
    nconst TEXT, 
    category TEXT, 
    job TEXT, 
    characters TEXT
);

CREATE TABLE crew (
	tconst TEXT PRIMARY KEY,
	directors TEXT[],
	writers TEXT[]
);

CREATE TABLE episode (
    tconst TEXT PRIMARY KEY,
    parentTconst TEXT,
    seasonNumber INTEGER,
    episodeNumber INTEGER
);

CREATE TABLE akas (
    titleId TEXT,
    ordering INTEGER,
    title TEXT,
    region TEXT,
    language TEXT,
    types TEXT[],
    attributes TEXT[],
    isOriginalTitle BOOLEAN
);
