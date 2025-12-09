from django.shortcuts import render
from django.http import HttpResponse
import psycopg2
import os

def get_db_connection():
    return psycopg2.connect(
        dbname="djangotrain",
        user="djangouser",
        password="secretpassword",
        host="localhost",
        port="5432"
    )

def init(request):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Create ex08_planets table
        create_planets_query = """
        CREATE TABLE IF NOT EXISTS ex08_planets (
            id SERIAL PRIMARY KEY,
            name VARCHAR(64) UNIQUE NOT NULL,
            climate VARCHAR,
            diameter INTEGER,
            orbital_period INTEGER,
            population BIGINT,
            rotation_period INTEGER,
            surface_water REAL,
            terrain VARCHAR(128)
        );
        """
        cursor.execute(create_planets_query)
        
        # Create ex08_people table
        create_people_query = """
        CREATE TABLE IF NOT EXISTS ex08_people (
            id SERIAL PRIMARY KEY,
            name VARCHAR(64) UNIQUE NOT NULL,
            birth_year VARCHAR(32),
            gender VARCHAR(32),
            eye_color VARCHAR(32),
            hair_color VARCHAR(32),
            height INTEGER,
            mass REAL,
            homeworld VARCHAR(64) REFERENCES ex08_planets(name)
        );
        """
        cursor.execute(create_people_query)
        
        conn.commit()
        cursor.close()
        conn.close()
        return HttpResponse("OK")
    except Exception as e:
        return HttpResponse(f"Error: {e}")

def populate(request):
    results = []
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        planets_path = os.path.join(base_dir, 'planets.csv')
        people_path = os.path.join(base_dir, 'people.csv')
        
        if not os.path.exists(planets_path):
             results.append(f"planets.csv not found at {planets_path}")
        else:
            # Populate planets
            try:
                with open(planets_path, 'r') as f:
                    cursor.copy_from(f, 'ex08_planets', sep='\t', null='NULL', columns=('name', 'climate', 'diameter', 'orbital_period', 'population', 'rotation_period', 'surface_water', 'terrain'))
                    conn.commit()
                    results.append("planets.csv: OK")
            except Exception as e:
                conn.rollback()
                results.append(f"planets.csv: {e}")

        if not os.path.exists(people_path):
             results.append(f"people.csv not found at {people_path}")
        else:
            # Populate people
            try:
                with open(people_path, 'r') as f:
                    cursor.copy_from(f, 'ex08_people', sep='\t', null='NULL', columns=('name', 'birth_year', 'gender', 'eye_color', 'hair_color', 'height', 'mass', 'homeworld'))
                    conn.commit()
                    results.append("people.csv: OK")
            except Exception as e:
                conn.rollback()
                results.append(f"people.csv: {e}")
            
        cursor.close()
        conn.close()
    except Exception as e:
        return HttpResponse(f"Database connection error: {e}")

    return HttpResponse("<br>".join(results))

def display(request):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
        SELECT p.name, p.homeworld, pl.climate
        FROM ex08_people p
        JOIN ex08_planets pl ON p.homeworld = pl.name
        WHERE pl.climate LIKE '%windy%'
        ORDER BY p.name ASC;
        """
        
        cursor.execute(query)
        people = cursor.fetchall()
        cursor.close()
        conn.close()
        
        if not people:
            return HttpResponse("No data available")
            
        return render(request, 'ex08/display.html', {'people': people})
    except Exception as e:
        return HttpResponse("No data available")
