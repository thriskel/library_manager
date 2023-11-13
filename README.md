# Library Manager
REST API Project to emulate a library management system where you can perform CRUD operations on the object representation of books, authors, clients and their interaction with each other.

# Requirements
To be able to run Library Manager you need the following dependencies:
1. [Docker](https://www.docker.com/get-started/)

# Installation
To install Library Manager you need to clone this repository, you can do so using the following command:
```
git clone https://github.com/thriskel/library_manager.git
```
Navigate to the base of the project and execute docker compose:
```
cd library_manager/
```
Build and run the docker compose:
```
docker compose build

docker compose up
```
Done, the services should now be ready to be used.

# API documentation
Once the project is built, you can access the swagger documentation in the root endpoint e.g:
>http://localhost:8000/

# Authentication
There are endpoints available to register a new user and handle token retreiving, refreshing, revoking operations, each documented in the swagger schema.