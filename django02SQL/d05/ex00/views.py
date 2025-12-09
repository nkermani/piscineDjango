from django.shortcuts import render
from django.http import HttpResponse
import psycopg2


def init(request):
    try:
        conn = psycopg2.connect(
            dbname="djangotrain",
            user="djangouser",
            password="secretpassword",
            host="localhost",
            port="5432",
        )
        cursor = conn.cursor()

        create_table_query = """
        CREATE TABLE IF NOT EXISTS ex00_movies (
            title VARCHAR(64) UNIQUE NOT NULL,
            episode_nb INTEGER PRIMARY KEY,
            opening_crawl TEXT,
            director VARCHAR(32) NOT NULL,
            producer VARCHAR(128) NOT NULL,
            release_date DATE NOT NULL
        );
        """

        cursor.execute(create_table_query)
        conn.commit()
        cursor.close()
        conn.close()
        return HttpResponse("OK")
    except Exception as e:
        return HttpResponse(f"Error: {e}")
