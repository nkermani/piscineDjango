from chat.models import Room

rooms = ["General", "Gaming", "Random"]

for name in rooms:
    room, created = Room.objects.get_or_create(name=name)
    if created:
        print(f"Room '{name}' created.")
    else:
        print(f"Room '{name}' already exists.")
