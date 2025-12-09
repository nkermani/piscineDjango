from django.shortcuts import render


def index(request):
    shades = []
    steps = 50
    step_size = 255 / (steps - 1)

    for i in range(steps):
        val = int(i * step_size)
        shades.append(
            {
                "noir": f"rgb({val}, {val}, {val})",
                "rouge": f"rgb({val}, 0, 0)",
                "bleu": f"rgb(0, 0, {val})",
                "vert": f"rgb(0, {val}, 0)",
            }
        )

    return render(request, "ex03/index.html", {"shades": shades})
