from django.shortcuts import render
from .models import People
from .forms import SearchForm


def search(request):
    results = []
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            min_date = form.cleaned_data["min_release_date"]
            max_date = form.cleaned_data["max_release_date"]
            diameter = form.cleaned_data["planet_diameter"]
            gender = form.cleaned_data["gender"]

            people = People.objects.filter(
                gender=gender,
                homeworld__diameter__gte=diameter,
                movies__release_date__range=(min_date, max_date),
            ).distinct()

            for person in people:
                matching_movies = person.movies.filter(
                    release_date__range=(min_date, max_date)
                )
                for movie in matching_movies:
                    results.append(
                        {
                            "person_name": person.name,
                            "gender": person.gender,
                            "movie_title": movie.title,
                            "homeworld_name": person.homeworld.name,
                            "homeworld_diameter": person.homeworld.diameter,
                        }
                    )

            if not results:
                results = "Nothing corresponding to your research"

    else:
        form = SearchForm()

    return render(request, "ex10/search.html", {"form": form, "results": results})
