
# {{ cookiecutter.project_name }}

Project simple description

## Table of Contents
1. [Quickstart](#Quickstart)
2. [Installation](#Installation)
    1. [Prerequisites](#Prerequisites)
    1. [Run localy](#RunLocaly)
3. [Features](#Features)
4. [Configuration](#Configuration)
5. [Contributing](#Contributing)
6. [Links](#Links)
7. [Licensing](#Licensing)


## Quickstart  <a name="Quickstart"></a>

...

## Installation <a name="Installation"></a>

see [https://github.com/jehna/readme-best-practices/blob/master/README-default.md](https://github.com/jehna/readme-best-practices/blob/master/README-default.md)
...
### Prerequisites<a name="Prerequisites"></a>
- Python 3.10 or higher

### Run localy <a name="RunLocaly"></a>
1. Clone the repository:

```bash
git clone https://github.com/{{ cookiecutter.repo_name }}/{{ cookiecutter.project_name }}.git

cd {{ cookiecutter.project_name }}
```

2. setup the environement

```bash
make init
```

3. run the project (local test) :

```bash
make local-run
```

4. deploy the project (docker test) :

```bash
make local-run
```


## Features <a name="Features"></a>

```bash
```

...



## Configuration <a name="Configuration"></a>


Simple docker to create a temp database
```bash 
docker run --name my_postgres -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres
DATABASE_URL = "postgresql+asyncpg://postgres:mysecretpassword@localhost/mydatabase"

# relancer le docker
docker start my_postgres

# faire une bdd 
docker exec -it my_postgres psql -U postgres
CREATE DATABASE mydatabase;

docker run -p 1080:80 \
    -e "PGADMIN_DEFAULT_EMAIL=user@domain.com" \
    -e "PGADMIN_DEFAULT_PASSWORD=SuperSecret" \
    --name pgadmin \
    dpage/pgadmin4

# Host name/address : docker inspect -f "\{\{range .NetworkSettings.Networks\}\}\{\{.IPAddress\}\}\{\{end\}\}" my_postgres
# docker rm -f pgadmin
```

Faire des certificats auto signes
```bash

openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout key.pem -out cert.pem
```

Test de l'application en local
```bash
 curl https://localhost:8000/api/version --insecure 
```

```bash
find ./app/api/models  -maxdepth 1 -type f -exec bash -c 'echo "Nom du fichier : $1"; cat "$1" ; echo ""; echo ""' _ {} \; | xclip -selection clipboard
```


### Swagger 

```
https://localhost:8000/docs
```

Create an 
```
npm install @tanstack/react-query -g
npm install @openapitools/openapi-generator-cli -g

openapi-generator-cli generate -i path/to/swagger.yaml -g typescript-react-query -o path/to/output
```


## Contributing <a name="Contributing"></a>

"If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcome."

## Links <a name="Links"></a>

[documentation](https:google.com)
[project page](https:google.com)

## Licensing <a name="Licensing"></a>

"The code in this project is licensed under MIT license."


## License Private <a name="Licensing Private"></a>

This project is subject to a private license. Use of this software is strictly prohibited without explicit and written permission from [Your Name or Organization Name]. For more details, please refer to the [LICENSE](./LICENSE) file.

To obtain permission to use this software, please contact [Your Email Address or Contact Information].