from django.shortcuts import render
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
        CREATE TABLE IF NOT EXISTS ex04_movies (
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
                cursor.execute(
                    """
                    INSERT INTO ex04_movies (episode_nb, title, director, producer, release_date)
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
        cursor.execute("SELECT * FROM ex04_movies")
        movies = cursor.fetchall()
        cursor.close()
        conn.close()

        if not movies:
            return HttpResponse("No data available")

        return render(request, "ex04/display.html", {"movies": movies})
    except Exception as e:
        return HttpResponse("No data available")


def remove(request):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        if request.method == "POST":
            title_to_remove = request.POST.get("movie")
            if title_to_remove:
                try:
                    cursor.execute(
                        "DELETE FROM ex04_movies WHERE title = %s", (title_to_remove,)
                    )
                    conn.commit()
                except Exception as e:
                    conn.rollback()
                    # Handle error if needed, but for now just proceed to re-render

        cursor.execute("SELECT title FROM ex04_movies")
        movies = cursor.fetchall()
        cursor.close()
        conn.close()

        if not movies:
            return HttpResponse("No data available")

        return render(request, "ex04/remove.html", {"movies": movies})

    except Exception as e:
        return HttpResponse("No data available")
