# Workplace Violence Prediction API

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

---

## Description

This repository contains the source code for our groups Software Engineering project for Impact Intelligence.

---

## Development

To set up the development environment for this application, you must do a couple of things.

> [!TIP]
> Run the application with the environment variable `DJANGO_DEBUG` set to enable debug mode. The variable can be set
> to anything, as long as there is a value associated with it. Any non-null value will be parsed as truthy.

**1. Clone this repo**
> `git clone https://github.com/averybobbitt/workplace-violence-prediction-api.git`

**2. Initialize Python virtualenv**
> `python -m venv .venv`

**3. Install requirements**
> `pip install -r requirements.txt`

**4. Set up database connection**

_Windows (Powershell)_
> `Copy-Item "db-template.cnf" -Destination "db.cnf"`

_macOS / Unix (Bash)_
> `cp db-template.cnf db.cnf`

Then edit `db.cnf` and replace the placeholder values with your credentials.

> [!WARNING]
> If you are working in a shared database, you are finished at this point.
> Only continue with steps 5 and 6 if you are setting up a local development database.
> **DO NOT** run the final command on a database that is already set up.

**5. Apply migrations**
> `python manage.py migrate`

**6. Set up database admin user**
> `python manage.py createsuperuser --username admin --email admin@example.com`

After running these commands to get your environment set up, you should be good to go!

### Formatting

> [!IMPORTANT]
> Included in the pip requirements for this project is the `black` package. `black` is an opinionated formatter for
> Python, and is used in this project to enforce consistent code styles. **Make sure you are formatting your code before
committing to `master`!**

---

## Group Members

| Name           | Role            | Contact                                                           |
|----------------|-----------------|-------------------------------------------------------------------|
| Aiden Touhill  | *Product Owner* | [touhil76@students.rowan.edu](mailto:touhil76@students.rowan.edu) |
| Carter Profico | *Scrum Master*  | [profic93@students.rowan.edu](mailto:profic93@students.rowan.edu) |
| Avery Bobbitt  | *Developer*     | [bobbit82@rowan.edu](mailto:bobbit82@rowan.edu)                   |
| Joe DiPietro   | *Developer*     | [dipiet77@students.rowan.edu](mailto:dipiet77@students.rowan.edu) |
| Chris Duym     | *Developer*     | [duymch27@students.rowan.edu](mailto:duymch27@students.rowan.edu) |
| Anthony Ung    | *Developer*     | [ungant67@students.rowan.edu](mailto:ungant67@students.rowan.edu) |
