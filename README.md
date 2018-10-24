# ISFIT 2019 Recruitment-Web

This is the application used by ISFIT 2019 to recieve and manage the applications from volunteers who wants to work in the festival.

## Getting Started

These instructions will make a copy of the project running on your local machine, to be used for development and testing purposes.

### Prerequisites

The things you need to install and run this project.

- Python - Version 3.4, 3.5, and 3.6. [Installation](https://www.python.org/downloads/)
- Pipenv [Installation](https://pipenv.readthedocs.io/en/latest/)

### Installing

- Clone the repository into your own project folder:
  ```sh
  git clone https://github.com/isfit/recruitment-web-isfit-2019.git
  ```
  
- Move into the project folder and make a virtual enviroment (here we use pipenv):
  ```sh
  cd recruitment-web-isfit-2019
  pipenv install
  ```
  Pipenv will automatically create a virtual enviroment and install the packages listed in requirements.txt.
  
- After you have installed all the requirements, its time to generate the database:
  ```
  python manage.py migrate
  ```

- Run the web application locally:
  ```
  python manage.py runserver
  ```
  
## Built With

* [Django](https://www.djangoproject.com/) - Web Framework.

## Authors

* **Peder Dueled** - *Head of Recruitmentweb* - [Pederduel](https://github.com/pederduel)
* **Emil Telstad** - *Developer* - [Emilte](https://github.com/emilte)
* **Peder Grundvold** - *Developer* - [PederBG](https://github.com/pederbg)
