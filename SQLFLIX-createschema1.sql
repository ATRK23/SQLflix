CREATE TABLE movies (
    movie_id INT PRIMARY KEY,        -- Identifiant unique du film
    title VARCHAR(255),              -- Titre du film
    budget BIGINT,                    -- Budget du film
    homepage VARCHAR(2083),           -- URL de la page officielle
    original_language CHAR(2),        -- Langue d'origine (code ISO)
    original_title VARCHAR(255),      -- Titre original
    overview TEXT,                    -- Synopsis du film
    popularity FLOAT,                 -- Popularité du film
    release_date DATE,                -- Date de sortie
    revenue BIGINT,                   -- Revenus générés
    runtime FLOAT,                    -- Durée en minutes
    status VARCHAR(50),               -- Statut du film
    tagline VARCHAR(255),             -- Slogan ou phrase d'accroche
    vote_average FLOAT,               -- Moyenne des votes
    vote_count INT                    -- Nombre total de votes


);

CREATE TABLE movie_cast (
    cast_id INTEGER NOT NULL,
    movie_id INTEGER NOT NULL,
    actor_id INTEGER NOT NULL,
    actor_name TEXT,
    character_name TEXT,
    credit_id TEXT,
    gender SMALLINT,
    display_order INTEGER,
    PRIMARY KEY (cast_id, movie_id),  -- Clé primaire composée
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id) ON DELETE CASCADE
);


CREATE TABLE crew (
    crew_id INTEGER NOT NULL,
    movie_id INTEGER NOT NULL,
    credit_id TEXT,
    department TEXT,
    gender SMALLINT,
    melber_id INTEGER NOT NULL,
    job TEXT,
    member_name TEXT,
    PRIMARY KEY (crew_id, movie_id),  -- Clé primaire composée
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id) ON DELETE CASCADE
);


CREATE TABLE genres (
    genre_id INT PRIMARY KEY,         -- Identifiant unique du genre
    name VARCHAR(100) NOT NULL        -- Nom du genre (exemple : "Action")
);

CREATE TABLE movie_genres (
    movie_id INT,                     -- Référence au film
    genre_id INT,                     -- Référence au genre
    PRIMARY KEY (movie_id, genre_id),
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id) ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES genres(genre_id) ON DELETE CASCADE
);

CREATE TABLE production_companies (
    company_id INT PRIMARY KEY,       -- Identifiant unique de la société
    name VARCHAR(255) NOT NULL        -- Nom de la société
);

CREATE TABLE movie_production_companies (
    movie_id INT,                     -- Référence au film
    company_id INT,                   -- Référence à la société
    PRIMARY KEY (movie_id, company_id),
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id) ON DELETE CASCADE,
    FOREIGN KEY (company_id) REFERENCES production_companies(company_id) ON DELETE CASCADE
);

CREATE TABLE production_countries (
    country_code CHAR(2) PRIMARY KEY, -- Code ISO du pays
    name VARCHAR(100) NOT NULL        -- Nom du pays
);

CREATE TABLE movie_production_countries (
    movie_id INT,                     -- Référence au film
    country_code CHAR(2),             -- Référence au pays
    PRIMARY KEY (movie_id, country_code),
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id) ON DELETE CASCADE,
    FOREIGN KEY (country_code) REFERENCES production_countries(country_code) ON DELETE CASCADE
);

CREATE TABLE spoken_languages (
    language_code CHAR(2) PRIMARY KEY, -- Code ISO de la langue
    name VARCHAR(100) NOT NULL         -- Nom de la langue
);

CREATE TABLE movie_spoken_languages (
    movie_id INT,                      -- Référence au film
    language_code CHAR(2),             -- Référence à la langue
    PRIMARY KEY (movie_id, language_code),
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id) ON DELETE CASCADE,
    FOREIGN KEY (language_code) REFERENCES spoken_languages(language_code) ON DELETE CASCADE
);

CREATE TABLE keywords (
    keyword_id INT PRIMARY KEY,       -- Identifiant unique du mot-clé
    name VARCHAR(255) NOT NULL        -- Nom du mot-clé
);

CREATE TABLE movie_keywords (
    movie_id INT,                     -- Référence au film
    keyword_id INT,                   -- Référence au mot-clé
    PRIMARY KEY (movie_id, keyword_id),
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id) ON DELETE CASCADE,
    FOREIGN KEY (keyword_id) REFERENCES keywords(keyword_id) ON DELETE CASCADE
);
