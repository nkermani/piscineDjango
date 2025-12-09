from django.shortcuts import render, redirect
from django.http import HttpResponse
import psycopg2


def get_db_connection():
    return psycopg2.connect(
        dbname="djangotrain",
        user="djangouser",
        password="secretpassword",
        host="localhost",
        port="5432",
    )


def init(request):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        create_table_query = """
        CREATE TABLE IF NOT EXISTS ex06_movies (
            title VARCHAR(64) UNIQUE NOT NULL,
            episode_nb INTEGER PRIMARY KEY,
            opening_crawl TEXT,
            director VARCHAR(32) NOT NULL,
            producer VARCHAR(128) NOT NULL,
            release_date DATE NOT NULL,
            created TIMESTAMP DEFAULT NOW(),
            updated TIMESTAMP DEFAULT NOW()
        );
        """
        cursor.execute(create_table_query)

        create_function_query = """
        CREATE OR REPLACE FUNCTION update_changetimestamp_column()
        RETURNS TRIGGER AS $$
        BEGIN
        NEW.updated = now();
        NEW.created = OLD.created;
        RETURN NEW;
        END;
        $$ language 'plpgsql';
        """
        cursor.execute(create_function_query)

        # Drop trigger if exists to avoid error on re-run or use CREATE OR REPLACE if supported (triggers don't support OR REPLACE directly usually)
        # But the prompt says "create a table... if not exists" implied.
        # For trigger, we can check if it exists or just try to create it and catch error if it exists, or drop it first.
        # Postgres 9.4+ supports DROP TRIGGER IF EXISTS.

        cursor.execute(
            "DROP TRIGGER IF EXISTS update_films_changetimestamp ON ex06_movies;"
        )

        create_trigger_query = """
        CREATE TRIGGER update_films_changetimestamp BEFORE UPDATE
        ON ex06_movies FOR EACH ROW EXECUTE PROCEDURE
        update_changetimestamp_column();
        """
        cursor.execute(create_trigger_query)

        conn.commit()
        cursor.close()
        conn.close()
        return HttpResponse("OK")
    except Exception as e:
        return HttpResponse(f"Error: {e}")


def populate(request):
    data = [
        {
            "episode_nb": 1,
            "title": "The Phantom Menace",
            "director": "George Lucas",
            "producer": "Rick McCallum",
            "release_date": "1999-05-19",
        },
        {
            "episode_nb": 2,
            "title": "Attack of the Clones",
            "director": "George Lucas",
            "producer": "Rick McCallum",
            "release_date": "2002-05-16",
        },
        {
            "episode_nb": 3,
            "title": "Revenge of the Sith",
            "director": "George Lucas",
            "producer": "Rick McCallum",
            "release_date": "2005-05-19",
        },
        {
            "episode_nb": 4,
            "title": "A New Hope",
            "director": "George Lucas",
            "producer": "Gary Kurtz, Rick McCallum",
            "release_date": "1977-05-25",
        },
        {
            "episode_nb": 5,
            "title": "The Empire Strikes Back",
            "director": "Irvin Kershner",
            "producer": "Gary Kutz, Rick McCallum",
            "release_date": "1980-05-17",
        },
        {
            "episode_nb": 6,
            "title": "Return of the Jedi",
            "director": "Richard Marquand",
            "producer": "Howard G. Kazanjian, George Lucas, Rick McCallum",
            "release_date": "1983-05-25",
        },
        {
            "episode_nb": 7,
            "title": "The Force Awakens",
            "director": "J. J. Abrams",
            "producer": "Kathleen Kennedy, J. J. Abrams, Bryan Burk",
            "release_date": "2015-12-11",
        },
    ]

    results = []
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        for movie in data:
            try:
                # We rely on DEFAULT NOW() for created and updated
                cursor.execute(
                    """
                    INSERT INTO ex06_movies (episode_nb, title, director, producer, release_date)
                    VALUES (%s, %s, %s, %s, %s)
                """,
                    (
                        movie["episode_nb"],
                        movie["title"],
                        movie["director"],
                        movie["producer"],
                        movie["release_date"],
                    ),
                )
                conn.commit()
                results.append("OK")
            except Exception as e:
                conn.rollback()
                results.append(f"{movie['title']}: {e}")

        cursor.close()
        conn.close()
    except Exception as e:
        return HttpResponse(f"Database connection error: {e}")

    return HttpResponse("<br>".join(results))


def display(request):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ex06_movies")
        movies = cursor.fetchall()
        cursor.close()
        conn.close()

        if not movies:
            return HttpResponse("No data available")

        return render(request, "ex06/display.html", {"movies": movies})
    except Exception as e:
        return HttpResponse("No data available")


def update(request):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        if request.method == "POST":
            title_to_update = request.POST.get("movie")
            new_opening_crawl = request.POST.get("opening_crawl")
            if title_to_update:
                try:
                    cursor.execute(
                        """
                        UPDATE ex06_movies
                        SET opening_crawl = %s
                        WHERE title = %s
                    """,
                        (new_opening_crawl, title_to_update),
                    )
                    conn.commit()
                except Exception as e:
                    conn.rollback()

        cursor.execute("SELECT title FROM ex06_movies")
        movies = cursor.fetchall()
        cursor.close()
        conn.close()

        if not movies:
            return HttpResponse("No data available")

        return render(request, "ex06/update.html", {"movies": movies})

    except Exception as e:
        return HttpResponse("No data available")
