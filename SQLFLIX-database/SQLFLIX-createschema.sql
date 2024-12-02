CREATE TABLE name (
    nconst TEXT PRIMARY KEY,
    primaryName TEXT,
    birthYear NUMERIC(4,0),
    deathYear NUMERIC(4,0),
    primaryProfession TEXT[],           -- Tableau pour les professions 
    knownForTitles TEXT[]         -- Tableau pour les titres associés
);


CREATE TABLE ratings (
    tconst TEXT PRIMARY KEY,
    averageRating NUMERIC(3,1),
    numVotes INTEGER
);

CREATE TABLE titlebasics (
    tconst TEXT PRIMARY KEY,
    titleType TEXT,
    primaryTitle TEXT,
    originalTitle TEXT,
    isAdult BOOLEAN,
    startYear NUMERIC(4,0),
    endYear NUMERIC(4,0),
    runtimeMinutes INTEGER,
    genres TEXT[] -- Tableau pour les genres
);

CREATE TABLE titleprincipal (
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
