import os
import django
import sys

# Add the project directory to the sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "d06.settings")
django.setup()

from django.contrib.auth import get_user_model
from tips.models import Tip

User = get_user_model()


def create_users():
    # Create main users
    users_data = {
        "newbie": "password123",
        "intermediate": "password123",
        "expert": "password123",
    }

    created_users = {}
    for username, password in users_data.items():
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, password=password)
            print(f"Created user: {username}")
            created_users[username] = user
        else:
            print(f"User {username} already exists")
            created_users[username] = User.objects.get(username=username)

    # Create voters
    voters = []
    for i in range(1, 7):
        username = f"voter{i}"
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, password="password123")
            voters.append(user)
        else:
            voters.append(User.objects.get(username=username))

    return created_users, voters


def setup_reputation(users, voters):
    # Setup Intermediate (Target: 15 rep)
    intermediate = users["intermediate"]
    # Check if tip already exists to avoid duplicates on re-run
    if not Tip.objects.filter(
        author=intermediate, content="This is a tip by intermediate user."
    ).exists():
        tip_int = Tip.objects.create(
            content="This is a tip by intermediate user.", author=intermediate
        )
        # 3 upvotes = 15 points
        for i in range(3):
            tip_int.upvotes.add(voters[i])

    print(
        f"Intermediate user reputation should be 15. Current: {intermediate.reputation}"
    )

    # Setup Expert (Target: 30 rep)
    expert = users["expert"]
    if not Tip.objects.filter(
        author=expert, content="This is a tip by expert user."
    ).exists():
        tip_exp = Tip.objects.create(
            content="This is a tip by expert user.", author=expert
        )
        # 6 upvotes = 30 points
        for i in range(6):
            tip_exp.upvotes.add(voters[i])

    print(f"Expert user reputation should be 30. Current: {expert.reputation}")


if __name__ == "__main__":
    print("Starting population script...")
    users, voters = create_users()
    setup_reputation(users, voters)
    print("Done!")
    print("-" * 30)
    print("Credentials (username / password):")
    print("newbie / password123 (Rep: 0)")
    print("intermediate / password123 (Rep: 15)")
    print("expert / password123 (Rep: 30)")
    print("-" * 30)
