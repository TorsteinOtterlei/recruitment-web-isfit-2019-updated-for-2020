from django.core.management.base import BaseCommand
from django.utils import timezone
import random
from halo import Halo
# from hopcroftkarp import HopcroftKarp
from apps.accounts.models import User
from apps.applications.models import Application
from apps.jobs.models import Section, Gang, Position, Project
from django.core import management

# Settings:
USER_AMOUNT = 200
USER_PW = "Django123"
USERS_WITH_APPLICATION = 180
RANKING_AMOUNT = 180 # <= USERS_WITH_APPLICATION
DATES_RANGE = 70
DATES_SAMPLE = 40
USERS_WITH_DATES = 180

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
    def reset_db(self):
        management.call_command('reset_db')
        print()

    def migrate(self):
        print("Applying migrations")
        management.call_command('migrate')
        print()

    def createsu(self):
        spinner = Halo("Creating superuser")
        spinner.start()
        email = "admin@admin.com"
        pw = "admin"
        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(email=email, password=pw, first_name="Admin", last_name="Adminsen", phone_number=12345678)
            spinner.succeed("Creating superuser. email: {}, password: {}".format(email, pw))
        else:
            spinner.fail("Superuser already exists")

    def create_users(self):
        global USER_AMOUNT
        global USER_PW
        spinner = Halo(text="Creating users", color="magenta")
        spinner.start()
        kristian = User.objects.create_user(email="kris@test.no", first_name="Kristian", password=USER_PW)
        camilla = User.objects.create_user(email="camilla@test.no", first_name="Camilla", password=USER_PW)
        johan = User.objects.create_user(email="johan@test.no", first_name="Johan", password=USER_PW)
        peder = User.objects.create_user(email="peder@test.no", first_name="Peder", password=USER_PW)
        sofie = User.objects.create_user(email="sofie@test.no", first_name="Sofie", password=USER_PW)
        synnove = User.objects.create_user(email="synnove@test.no", first_name="Synnove", password=USER_PW)
        ola = User.objects.create_user(email="ola@test.no", first_name="Ola", password=USER_PW)
        mona = User.objects.create_user(email="mona@test.no", first_name="Mona", password=USER_PW)
        ellen = User.objects.create_user(email="ellen@test.no", first_name="Ellen", password=USER_PW)
        ragnhild = User.objects.create_user(email="ragnhild@test.no", first_name="Ragnhild", password=USER_PW)
        # Create simple users
        for i in range(USER_AMOUNT):
            User.objects.create_user(email="pers"+str(i)+"@test.no", first_name="Yolo"+str(i), last_name="Swag", password=USER_PW)
        spinner.succeed("Creating users. Over {} users generated. Password: {}".format(USER_AMOUNT, USER_PW))

    def create_sections(self):
        spinner = Halo("Creating sections")
        spinner.start()
        s1 = Section()
        s1.name = "Economy"
        s1.leader = User.objects.get(first_name='Camilla')
        s1.information = "Her hviler blandt annet IT"
        s1.save()

        s2 = Section()
        s2.name = "Culture"
        s2.leader = User.objects.get(first_name='Johan')
        s2.information = "Driver med kultur"
        s2.save()

        s3 = Section()
        s3.name = "Theme"
        s3.leader = User.objects.get(first_name='Peder')
        s3.information = "Driver med tema"
        s3.save()

        s4 = Section()
        s4.name = "Administration"
        s4.leader = User.objects.get(first_name='Ola')
        s4.information = "Driver med kultur"
        s4.save()

        spinner.succeed()
        # End of create_sections

    def create_gangs(self):
        spinner = Halo("Creating gangs")
        spinner.start()
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

        spinner.succeed()

        #"  ==  End of create_gangs()  ==  "

    def create_projects(self):
        spinner = Halo("Creating projects")
        spinner.start()
        # Economy
        p = Project()
        p.name = "Recruitment Web"
        p.leader = User.objects.get(first_name='Peder')
        p.gang = Gang.objects.get(name="IT")
        p.save()

        p = Project()
        p.name = "Web App"
        p.leader = User.objects.get(first_name='Sofie')
        p.gang = Gang.objects.get(name="IT")
        p.save()

        # Culture
        p = Project()
        p.name = "Economy Managing"
        p.leader = User.objects.get(first_name='Ola')
        p.gang = Gang.objects.get(name="Art")
        p.save()

        p = Project()
        p.name = "Communication Coordination"
        p.leader = User.objects.get(first_name='Johan')
        p.gang = Gang.objects.get(name="Ceremony")
        p.save()

        # Theme

        # Administration

        spinner.succeed()

        # End of create_projects

    def create_positions(self):
        spinner = Halo("Creating positions")
        spinner.start()
        # Economy
        users = list(User.objects.all())

        p = Position()
        p.title = "Web App Developer"
        p.gang = Gang.objects.get(name="IT")
        p.description = "dummy"
        p.interviewer = users.pop()
        p.save()

        p = Position()
        p.title = "App Developer"
        p.gang = Gang.objects.get(name="IT")
        p.description = "dummy"
        p.interviewer = users.pop()
        p.save()

        p = Position()
        p.title = "Participant Web Developer"
        p.gang = Gang.objects.get(name="IT")
        p.description = "dummy"
        p.interviewer = users.pop()
        p.save()

        p = Position()
        p.title = "Recruitment Web Developer"
        p.gang = Gang.objects.get(name="IT")
        p.description = "dummy"
        p.interviewer = users.pop()
        p.save()

        p = Position()
        p.title = "Internal Project Manager"
        p.gang = Gang.objects.get(name="Finance")
        p.description = "dummy2"
        p.interviewer = users.pop()
        p.save()

        # Culture
        p = Position()
        p.title = "Culture_position1"
        p.gang = Gang.objects.get(name="Art")
        p.description = "dummy"
        p.interviewer = users.pop()
        p.save()

        # Theme
        p = Position()
        p.title = "Theme_position1"
        p.gang = Gang.objects.get(name="Dialogue")
        p.description = "dummy"
        p.interviewer = users.pop()
        p.save()

        # Administration
        p = Position()
        p.title = "Administration_position1"
        p.gang = Gang.objects.get(name="Transport")
        p.description = "dummy"
        p.interviewer = users.pop()
        p.save()

        spinner.succeed()
        # End of create_positions

    def create_applications(self):
        spinner = Halo("Creating applications")
        spinner.start()

        global USERS_WITH_APPLICATION, DATES_RANGE, DATES_SAMPLE
        positions = list(Position.objects.all())
        users = list(User.objects.all())
        application_amount = min(USERS_WITH_APPLICATION, len(users))

        for i in range(application_amount): # Dependent on number of rankings available
            pos_sample = random.sample(positions, 3)
            Application.objects.create( applicant=users[i],
                                        text="dummy",
                                        first=pos_sample.pop(),
                                        second=pos_sample.pop(),
                                        third=pos_sample.pop(),
                                        dates=",".join(str(x) for x in sorted(random.sample(range(DATES_RANGE), DATES_SAMPLE))),
                                        interview_time=timezone.now()
                                        )
        spinner.succeed("Creating applications. Over {} applications generated".format(application_amount))
        # End of create_applications

    """
    def create_calendars(self):
        c = Calendar()
        gangleader = User.objects.filter(username="admin")
        c.gangleader = gangleader
        gangleader_dates = Dates.objects.filter(user=gangleader).dates_list()
        print(gangleader_dates)

        applications = list(Application.objects.filter(ranking.first=))





        # Genererer 200 søkere med 20 tilfeldige tider som passer for dem
        graph = {}
        for i in range(200):
            # key er navn fra 0 til 200
            # value er samplet fra grid over
            graph["pers"+str(i)] = random.sample(range(70), 20)

        # Bare tider som er tilgjengelig for begge gjengledere blir med videre.
        # Gjør dette ved å fjerne tider som egt passet for søker, men som
        # ikke passet for intervjuerne.
        for pers, times in graph.items():
            # Skriver over tidene til søkeren med de nye gunstige tidene
            times = [t for t in times if t in gjengleder1 and t in gjengleder2]
            # Erstatter de gamle tidspunktene med de nye
            graph[pers] = times

        # HopcroftKarp algoritmen matcher flest mulig søkere på kalenderen
        result = HopcroftKarp(graph).maximum_matching()
        # Ordner slik at person får tildelt ett tidspunkt
        fixed = [(pers, time) for pers, time in result.items() if type(pers) is not int]
        fixed2 = {pers: time for pers, time in result.items() if type(pers) is not int}
        # Vis resultat
        print("Result:")
        print(fixed2)
    """

    def handle(self, *args, **options):
        #self.flush()
        #self.reset_db()
        self.migrate()
        self.createsu()
        self.create_users()
        self.create_sections()
        self.create_gangs()
        self.create_projects()
        self.create_positions()
        self.create_applications()
        print("  ==  Dummydata inserted  ==  ")
        # End of handle
