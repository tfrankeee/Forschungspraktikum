# QTI Learning App

## Setup

## 📦 Prerequisites

Before starting, please install:

- **Docker Desktop**  
  https://www.docker.com/products/docker-desktop/

- **DBeaver** (for database access)  
  https://dbeaver.io/download/

You do **not** need to install PostgreSQL locally.  
All services run inside Docker containers.


## 1. Clone the repository

```bash
git clone <repo-url>
cd <repo-folder>
```

## 2. Start Docker Container
Inside the project root folder (where docker-compose.yml is located):
```bash
docker compose up --build
```

Docker will start:

* the PostgreSQL database container

* the FastAPI backend container

* the Vue.js frontend container

### Access points:

* Backend API: http://localhost:8000/docs

* Frontend app: http://localhost:8080

## PostgreSQL connection settings (DBeaver)

Open DBeaver → New Connection → PostgreSQL

Fill in the following:
* host: ```localhost```
* Port: ```5432```
* Database: ```myapp```
* Username: ```myapp_user```
* password: ```'the password'```

##

## Questions
You can see the sample questions under public/qti/. 
You can add your own questions and tests (QTI 3.0!) to this directory.
Make sure to add the path to your tests to the constant `filenames` aswell:

```js
async function bootstrap() {
  // Dateinamen angeben, die unter public/qti/tests liegen
  const filenames = [
    'test1.xml',
    'test2.xml',
    'cloud_computing_test.xml'
    // ..alle anderen QTI-XMLs
  ]
```
