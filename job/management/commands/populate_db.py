from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from job.models import Section, Gang, Position, Project, Ranking, Application
from django.utils import timezone
import random
from hopcroftkarp import HopcroftKarp

class Command(BaseCommand):
    args = '<foo bar ...>'
    help = """No options or args needed.
    Run this command to fill the database with dummydata:
    OBS: It will flush the database first
    Superuser
    Users
    Sections
    Gangs
    Positions
    Projects
    Ranks
    Applications
    """

    def flush(self):
        User.objects.all().delete()
        Section.objects.all().delete()
        Gang.objects.all().delete()
        Position.objects.all().delete()
        Project.objects.all().delete()
        Ranking.objects.all().delete()
        Application.objects.all().delete()

    def createsu(self):
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@admin.com", "admin")

    def create_users(self):
        pw = "django123"
        kristian = User.objects.create_user(username="kris", email="test6@test.no", first_name="kristian", password=pw)
        camilla = User.objects.create_user(username="cami", email="test1@test.no", first_name="camilla", password=pw)
        johan = User.objects.create_user(username="joha", email="test2@test.no", first_name="johan", password=pw)
        peder = User.objects.create_user(username="pede", email="test3@test.no", first_name="peder", password=pw)
        sofie = User.objects.create_user(username="sofi", email="test5@test.no", first_name="sofie", password=pw)
        synnove = User.objects.create_user(username="synn", email="test5@test.no", first_name="synnove", password=pw)
        ola = User.objects.create_user(username="ola", email="test4@test.no", first_name="ola", password=pw)
        mona = User.objects.create_user(username="mona", email="test4@test.no", first_name="mona", password=pw)
        ellen = User.objects.create_user(username="elle", email="test4@test.no", first_name="ellen", password=pw)
        ragnhild = User.objects.create_user(username="ragn", email="test4@test.no", first_name="ragnhild", password=pw)
        # Create 200 simple users
        for i in range(200):
            User.objects.create_user(username="p"+str(i), email="pers"+str(i)+"@test.no", first_name="pers"+str(i), password=pw)
        print("Over 200 users generated")

    def create_sections(self):
        s1 = Section()
        s1.name = "Economy"
        s1.leader = User.objects.get(first_name='camilla')
        s1.information = "Her hviler blandt annet IT"
        s1.save()

        s2 = Section()
        s2.name = "Culture"
        s2.leader = User.objects.get(first_name='johan')
        s2.information = "Driver med kultur"
        s2.save()

        s3 = Section()
        s3.name = "Theme"
        s3.leader = User.objects.get(first_name='peder')
        s3.information = "Driver med tema"
        s3.save()

        s4 = Section()
        s4.name = "Administration"
        s4.leader = User.objects.get(first_name='ola')
        s4.information = "Driver med kultur"
        s4.save()

        print("Sections added")

        # End of create_sections

    def create_gangs(self):
        # Economy
        g = Gang()
        g.name = "Accounting"
        g.section = Section.objects.get(name="Economy")
        g.save()

        g = Gang()
        g.name = "Finance"
        g.section = Section.objects.get(name="Economy")
        g.save()

        g = Gang()
        g.name = "IT"
        g.section = Section.objects.get(name="Economy")
        g.save()

        # Culture
        g = Gang()
        g.name = "Art"
        g.section = Section.objects.get(name="Culture")
        g.save()

        g = Gang()
        g.name = "Ceremony"
        g.section = Section.objects.get(name="Culture")
        g.save()

        # Theme
        g = Gang()
        g.name = "Dialogue"
        g.section = Section.objects.get(name="Theme")
        g.save()

        g = Gang()
        g.name = "Research"
        g.section = Section.objects.get(name="Theme")
        g.save()

        # Administration
        g = Gang()
        g.name = "Secretariat"
        g.section = Section.objects.get(name="Administration")
        g.save()

        g = Gang()
        g.name = "Transport"
        g.section = Section.objects.get(name="Administration")
        g.save()

        print("Gangs added")

        #"  ==  End of create_gangs()  ==  "

    def create_projects(self):
        # Economy
        p = Project()
        p.name = "Recruitment Web"
        p.leader = User.objects.get(username="pede")
        p.gang = Gang.objects.get(name="IT")
        p.save()

        p = Project()
        p.name = "Web App"
        p.leader = User.objects.get(username="sofi")
        p.gang = Gang.objects.get(name="IT")
        p.save()

        # Culture
        p = Project()
        p.name = "Economy Managing"
        p.leader = User.objects.get(username="ola")
        p.gang = Gang.objects.get(name="Art")
        p.save()

        p = Project()
        p.name = "Communication Coordination"
        p.leader = User.objects.get(username="joha")
        p.gang = Gang.objects.get(name="Ceremony")
        p.save()

        # Theme

        # Administration

        print("Projects added")

        # End of create_projects

    def create_positions(self):
        # Economy
        p = Position()
        p.title = "Web App Developer"
        p.gang = Gang.objects.get(name="IT")
        p.description = "dummy"
        p.email = "dummy@dummy.com"
        p.name_of_interviewer = "dummy"
        p.phone_number = 12345678
        p.save()

        p = Position()
        p.title = "App Developer"
        p.gang = Gang.objects.get(name="IT")
        p.description = "dummy"
        p.email = "dummy@dummy.com"
        p.name_of_interviewer = "dummy"
        p.phone_number = 12345678
        p.save()

        p = Position()
        p.title = "Participant Web Developer"
        p.gang = Gang.objects.get(name="IT")
        p.description = "dummy"
        p.email = "dummy@dummy.com"
        p.name_of_interviewer = "dummy"
        p.phone_number = 12345678
        p.save()

        p = Position()
        p.title = "Recruitment Web Developer"
        p.gang = Gang.objects.get(name="IT")
        p.description = "dummy"
        p.email = "dummy@dummy.com"
        p.name_of_interviewer = "Peder"
        p.phone_number = 12345678
        p.save()

        p = Position()
        p.title = "Internal Project Manager"
        p.gang = Gang.objects.get(name="Finance")
        p.description = "dummy2"
        p.email = "dummy2@dummy.com"
        p.name_of_interviewer = "dummy2"
        p.phone_number = 12345678
        p.save()

        # Culture
        p = Position()
        p.title = "Culture_position1"
        p.gang = Gang.objects.get(name="Art")
        p.description = "dummy"
        p.email = "dummy@dummy.com"
        p.name_of_interviewer = "dummy"
        p.phone_number = 12345678
        p.save()

        # Theme
        p = Position()
        p.title = "Theme_position1"
        p.gang = Gang.objects.get(name="Dialogue")
        p.description = "dummy"
        p.email = "dummy@dummy.com"
        p.name_of_interviewer = "dummy"
        p.phone_number = 12345678
        p.save()

        # Administration
        p = Position()
        p.title = "Administration_position1"
        p.gang = Gang.objects.get(name="Transport")
        p.description = "dummy"
        p.email = "dummy@dummy.com"
        p.name_of_interviewer = "dummy"
        p.phone_number = 12345678
        p.save()

        print("Positions added")

        # End of create_positions

    def create_rankings(self):
        r = Ranking()
        r.first = Position.objects.get(title="Web App Developer")
        r.save()

        r = Ranking()
        r.first = Position.objects.get(title="Recruitment Web Developer")
        r.second = Position.objects.get(title="Theme_position1")
        r.save()

        all_positions = list(Position.objects.all())
        for i in range(180):
            r = Ranking()
            pos = random.sample(all_positions, 3) # Three unique positions
            r.first = pos.pop()
            r.second = pos.pop()
            r.third = pos.pop()
            r.save()

        print("Over 180 rankings generated")

        # End of create_rankings

    def create_applications(self):
        rankings = list(Ranking.objects.all())
        users = list(User.objects.all())
        for i in range(180): # Dependent on number of rankings available
            a = Application()
            a.ranking = rankings[i]
            a.applicant = users[i]
            a.text = "dummy"
            a.phone_number = 12345678
            a.interview_time = timezone.now()
            a.dates = ",".join(str(x) for x in random.sample(range(70), 40))
            print(a.dates)
            a.save()

        print("Over 180 applications generated")

        # End of create_applications


    def handle(self, *args, **options):
        self.flush()
        print("Flushed current database")
        self.createsu()
        print("This will take some time...")
        self.create_users()
        self.create_sections()
        self.create_gangs()
        self.create_projects()
        self.create_positions()
        self.create_rankings()
        self.create_applications()
        print("  ==  Dummydata inserted  ==  ")
        # End of handle
