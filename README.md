# Foodgram
![example workflow](https://github.com/supermegacoolgirlwowyes/foodgram-project-react/actions/workflows/main.yml/badge.svg)

Foodgram service is made for people who are passionate about food. View recipes from all over the world or create your owns, follow the authors you like, make a list of your favorite recipes or download a shopping list in just few clicks.

### Foodgram and Foodgram API

The project is available at www.irinabalerina.tk
Current version of Foodgram API is available at www.irinabalerina.tk/api

### Getting Started

These instructions will get you a copy of the project up and running on your production server.

### Prerequisites

Make sure your system is ready for running the project. Check if you have Git installed locally and Docker with Docker-compose both: locally and on your server:
```
git version
```
```
docker --version
docker-compose --version
```
If not, follow this link for [git](https://github.com/git-guides/install-git) installation manual. Or these ones to install [docker](https://docs.docker.com/get-docker) and [docker-compose](https://docs.docker.com/compose/install/).

You may want to customize the project at some point in the future. 
To be able to do so, fork from the [GitHub Original Repository](https://github.com/Supermegacoolgirlwowyes/foodgram-project-react.git) first.

Navigate to the working directory on your local machine and clone the project from the forked version. 

```
git clone https://github.com/<your_github_name>/foodgram-project-react.git
```

### Deploying

Locally make a copy of the included **.env.template** and name it **.env**. 

```
cp .env.template .env
```
Declare your own environment variables in **.env** and save changes.

Create the following structure on your server:
```
foodgram
    docs
        openapi-schema.yml
        redoc.html
    frontend
        build
    infra dir
        .env
        docker-cpompose.yml
        nginx.conf
    static
        admin
        css
        js
        media
        rest_farmework
```

You are now set up to run the containers. Log in to your server, go to the **infra** directory and run the following command:


```
sudo docker-compose up -d
```
This command will pull up the Project, Postgres Database and Nginx images from Docker Hub and run the containers. It will also start Frontend contaier, which will do it's job end stop with Exit code 0. The '-d' flag will make them run in a detached mode and will let you keep working in the same tab.

Deploying project for the first time you will need to apply migrations and collect static files manually. Then create a superuser and load initial data if needed. You can either go with included **data/recipes.json** and **users.json** files or create your own.

```
sudo docker-compose exec backend python manage.py collectstatic --noinput
sudo docker-compose exec backend python manage.py migrate
sudo docker-compose exec backend python manage.py createsuperuser
sudo docker-compose exec backend python manage.py loaddata data/<file_name>.json
```

Now your project is running at **<your_ip_address>** and **<your_domain_address>**.

Django admin interface is available at **<your_address>/admin**. Foodgram documentation is available at **<your_address>/api/docs/**.

### Updating

This project is ready for Continuous Integration.

Create new workflow in you GitHub Repository. Copy code from included **foodgram_workflow.yml** file to the newly created **main.yml**. Set up environment variables from this workflow using GitHub secrets *(Settings > Secrets)*.

Whenever you need to implement your updates to the project, push them to the master branch. The workflow will automatically run the tests, create new Docker image, upload it to the DockerHub and Deploy your project. If the workflow runs successfully, you will receive a confirmation message on Telegram. Sweet :)

## Built With
* [Django](https://www.djangoproject.com) - Python web framework
* [Django REST](https://www.django-rest-framework.org) -  a toolkit for building Web APIs
* [Djoser](https://djoser.readthedocs.io/) - authentication system for Django projects
* [Docker](https://www.docker.com) - containerization platform
* [GitHub](https://github.com) - cloud-based version control service
* [Gunicorn](https://gunicorn.org) - Python WSGI HTTP Server
* [Nginx](https://nginx.org/en/) - HTTP and reverse proxy server
* [PostgreSQL](https://www.postgresql.org) - object-relational database system
* [React](https://reactjs.org) - a JavaScript library for building user interfaces 

## Authors

* **Irina Balerina** - *Backend, Dockerizing, Project Infrastructure, Continuous Integration* - [Supermegacoolgirlwowyes](https://github.com/Supermegacoolgirlwowyes)
* **Yandex Praktikum** - *Frontend* [Yandex Praktikum](https://github.com/yandex-praktikum/)

## License

This product is real. Everything is real.
