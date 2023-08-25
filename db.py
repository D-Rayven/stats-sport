import psycopg2
import api

conn = psycopg2.connect(dbname="Suivi_sport", user="postgres", password="password", host="localhost", port="5432")

cur = conn.cursor()

def check_existence_table(conn, table: str) -> bool:
    """Fonction permettant de vérifier la présence d'une table dans la base de données

    Args:
        conn (psycopg2.extensions.connection): Connexion à la base de données
        table (str): Table recherchée

    Returns:
        bool: True si la table existe, False sinon
    """
    cur = conn.cursor()

    table_exists = f'''
    SELECT EXISTS (
        SELECT FROM pg_tables
        WHERE
            schemaname = 'public' AND
            tablename = '{table}'
    );   
'''
    cur.execute(table_exists)
    result = cur.fetchone()[0]
    return result

exist_seasons = check_existence_table(conn, "seasons")

if not exist_seasons:
    create_table = '''
        CREATE TABLE seasons (
            id INTEGER PRIMARY KEY,
            season INTEGER
        )
    '''
    cur.execute(create_table)

    seasons = api.get_seasons()

    for season in seasons:
        add_value = f'INSERT INTO seasons (season) VALUES ({season})'
        cur.execute(add_value)

exist_leagues = check_existence_table(conn, "leagues")

if not exist_leagues:
    create_table = '''
    CREATE TABLE leagues (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255)  
    )
    '''
    cur.execute(create_table)

    leagues = api.get_leagues()

    for league in leagues:
        if "'" in league:
            league = league.replace("'", "''")
        add_value = f"INSERT INTO leagues (name) VALUES ('{league}')"
        cur.execute(add_value)

conn.commit()
conn.close()