import pandas as pd
import json

# Function to escape single quotes for SQL compatibility
def escape_string(value):
    return value.replace("'", "''") if isinstance(value, str) else value

# Function to generate SQL INSERT statements
def generate_insert_statements(table_name, data_frame, column_mapping):
    insert_statements = []
    for _, row in data_frame.iterrows():
        values = []
        for col in column_mapping.values():
            value = row.get(col)
            if pd.isnull(value):
                values.append('NULL')
            elif isinstance(value, str):
                values.append(f"'{escape_string(value)}'")
            else:
                values.append(str(value))
        statement = f"INSERT INTO {table_name} ({', '.join(column_mapping.keys())}) VALUES ({', '.join(values)});"
        insert_statements.append(statement)
    return insert_statements

# File paths
movies_csv_path = 'tmdb_5000_movies.csv'
credits_csv_path = 'tmdb_5000_credits.csv'

# Load data
movies_df = pd.read_csv(movies_csv_path)
credits_df = pd.read_csv(credits_csv_path)

# Generate SQL for movies table
movies_columns = {
    'movie_id': 'movie_id',
    'title': 'title',
    'budget': 'budget',
    'homepage': 'homepage',
    'original_language': 'original_language',
    'original_title': 'original_title',
    'overview': 'overview',
    'popularity': 'popularity',
    'release_date': 'release_date',
    'revenue': 'revenue',
    'runtime': 'runtime',
    'status': 'status',
    'tagline': 'tagline',
    'vote_average': 'vote_average',
    'vote_count': 'vote_count'
}
movies_inserts = generate_insert_statements("movies", movies_df.rename(columns=movies_columns), movies_columns)

# Parse and generate SQL for movie_cast table
cast_columns = {
    'cast_id': 'cast_id',
    'movie_id': 'movie_id',
    'actor_id': 'id',
    'actor_name': 'name',
    'character_name': 'character',
    'credit_id': 'credit_id',
    'gender': 'gender',
    'display_order': 'order'
}
cast_data = []
for _, row in credits_df.iterrows():
    if pd.notna(row['cast']):
        cast_list = json.loads(row['cast'])
        for cast_member in cast_list:
            cast_member['movie_id'] = row['movie_id']
            cast_data.append(cast_member)
cast_df = pd.DataFrame(cast_data)
cast_inserts = generate_insert_statements("movie_cast", cast_df, cast_columns)

# Parse and generate SQL for crew table
crew_columns = {
    'crew_id': 'id',
    'movie_id': 'movie_id',
    'credit_id': 'credit_id',
    'department': 'department',
    'gender': 'gender',
    'melber_id': 'id',
    'job': 'job',
    'member_name': 'name'
}
crew_data = []
for _, row in credits_df.iterrows():
    if pd.notna(row['crew']):
        crew_list = json.loads(row['crew'])
        for crew_member in crew_list:
            crew_member['movie_id'] = row['movie_id']
            crew_data.append(crew_member)
crew_df = pd.DataFrame(crew_data)
crew_inserts = generate_insert_statements("crew", crew_df, crew_columns)

# Parse and generate SQL for genres table
genres_columns = {
    'genre_id': 'id',
    'name': 'name'
}
genres_data = []
movie_genres_data = []
for _, row in movies_df.iterrows():
    if pd.notna(row['genres']):
        genres_list = json.loads(row['genres'])
        for genre in genres_list:
            genres_data.append(genre)
            movie_genres_data.append({'movie_id': row['movie_id'], 'genre_id': genre['id']})
genres_df = pd.DataFrame(genres_data).drop_duplicates()
movie_genres_df = pd.DataFrame(movie_genres_data)
genres_inserts = generate_insert_statements("genres", genres_df, genres_columns)
movie_genres_inserts = generate_insert_statements("movie_genres", movie_genres_df, {'movie_id': 'movie_id', 'genre_id': 'genre_id'})

# Parse and generate SQL for spoken_languages table
spoken_languages_columns = {
    'language_code': 'iso_639_1',
    'name': 'name'
}
spoken_languages_data = []
movie_spoken_languages_data = []
for _, row in movies_df.iterrows():
    if pd.notna(row['spoken_languages']):
        languages_list = json.loads(row['spoken_languages'])
        for language in languages_list:
            spoken_languages_data.append(language)
            movie_spoken_languages_data.append({'movie_id': row['movie_id'], 'language_code': language['iso_639_1']})
spoken_languages_df = pd.DataFrame(spoken_languages_data).drop_duplicates()
movie_spoken_languages_df = pd.DataFrame(movie_spoken_languages_data)
spoken_languages_inserts = generate_insert_statements("spoken_languages", spoken_languages_df, spoken_languages_columns)
movie_spoken_languages_inserts = generate_insert_statements("movie_spoken_languages", movie_spoken_languages_df, {'movie_id': 'movie_id', 'language_code': 'language_code'})

# Parse and generate SQL for keywords table
keywords_columns = {
    'keyword_id': 'id',
    'name': 'name'
}
keywords_data = []
movie_keywords_data = []
for _, row in movies_df.iterrows():
    if pd.notna(row['keywords']):
        keywords_list = json.loads(row['keywords'])
        for keyword in keywords_list:
            keywords_data.append(keyword)
            movie_keywords_data.append({'movie_id': row['movie_id'], 'keyword_id': keyword['id']})
keywords_df = pd.DataFrame(keywords_data).drop_duplicates()
movie_keywords_df = pd.DataFrame(movie_keywords_data)
keywords_inserts = generate_insert_statements("keywords", keywords_df, keywords_columns)
movie_keywords_inserts = generate_insert_statements("movie_keywords", movie_keywords_df, {'movie_id': 'movie_id', 'keyword_id': 'keyword_id'})

# Write SQL to file
with open('SQLFLIX-data.sql', 'w') as f:
    f.write('\n'.join(
        movies_inserts +
        cast_inserts +
        crew_inserts +
        genres_inserts +
        movie_genres_inserts +
        spoken_languages_inserts +
        movie_spoken_languages_inserts +
        keywords_inserts +
        movie_keywords_inserts
    ))

print("SQL INSERT statements for all tables have been written to 'SQLFLIX-data.sql'.")
