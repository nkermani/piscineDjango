from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Movies


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
    for movie_data in data:
        try:
            Movies.objects.create(**movie_data)
            results.append("OK")
        except Exception as e:
            results.append(f"Error: {e}")

    return HttpResponse("<br>".join(results))


def display(request):
    movies = Movies.objects.all()
    if not movies:
        return HttpResponse("No data available")
    return render(request, "ex07/display.html", {"movies": movies})


def update(request):
    if request.method == "POST":
        title_to_update = request.POST.get("movie")
        new_opening_crawl = request.POST.get("opening_crawl")
        if title_to_update:
            try:
                movie = Movies.objects.get(title=title_to_update)
                movie.opening_crawl = new_opening_crawl
                movie.save()
            except Movies.DoesNotExist:
                pass

    movies = Movies.objects.all()
    if not movies:
        return HttpResponse("No data available")

    return render(request, "ex07/update.html", {"movies": movies})
