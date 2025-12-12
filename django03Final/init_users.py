from django.contrib.auth.models import User


def create_test_user(username, password, is_superuser=False):
    if not User.objects.filter(username=username).exists():
        if is_superuser:
            User.objects.create_superuser(username, "", password)
            print(f"Superuser '{username}' created.")
        else:
            User.objects.create_user(username, "", password)
            print(f"User '{username}' created.")
    else:
        print(f"User '{username}' already exists.")


create_test_user("testuser", "password123")
create_test_user("admin", "admin123", is_superuser=True)
create_test_user("user1", "password123")
create_test_user("user2", "password123")
create_test_user("user3", "password123")
