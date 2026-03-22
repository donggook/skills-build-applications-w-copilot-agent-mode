from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.db import connection

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Delete all data
        Leaderboard.objects.all().delete()
        Activity.objects.all().delete()
        User.objects.all().delete()
        Team.objects.all().delete()
        Workout.objects.all().delete()

        # Create teams
        marvel = Team.objects.create(name='Marvel', description='Marvel superheroes')
        dc = Team.objects.create(name='DC', description='DC superheroes')

        # Create users
        ironman = User.objects.create(email='ironman@marvel.com', username='Iron Man', team=marvel, is_superhero=True)
        captain = User.objects.create(email='captain@marvel.com', username='Captain America', team=marvel, is_superhero=True)
        batman = User.objects.create(email='batman@dc.com', username='Batman', team=dc, is_superhero=True)
        superman = User.objects.create(email='superman@dc.com', username='Superman', team=dc, is_superhero=True)

        # Create workouts
        pushups = Workout.objects.create(name='Pushups', description='Do 20 pushups', suggested_for='heroes')
        running = Workout.objects.create(name='Running', description='Run 5km', suggested_for='heroes')

        # Create activities
        Activity.objects.create(user=ironman, activity_type='pushups', duration=10, date='2024-01-01')
        Activity.objects.create(user=batman, activity_type='running', duration=30, date='2024-01-02')
        Activity.objects.create(user=superman, activity_type='pushups', duration=15, date='2024-01-03')
        Activity.objects.create(user=captain, activity_type='running', duration=25, date='2024-01-04')

        # Create leaderboard
        Leaderboard.objects.create(user=ironman, score=100)
        Leaderboard.objects.create(user=batman, score=90)
        Leaderboard.objects.create(user=superman, score=95)
        Leaderboard.objects.create(user=captain, score=85)

        # Ensure unique index on email
        with connection.cursor() as cursor:
            cursor.execute('db.users.createIndex({ "email": 1 }, { unique: true })')

        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data!'))
