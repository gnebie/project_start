
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

2. setup a virtual environement

```bash
python3 -m venv venv

source venv/bin/activate    
```

3. install requirements 

install project requirements: 

```bash
pip install -r requirements.txt
```

install dev requirements :

```bash
pip install -r requirements-dev.txt
```

4. run the project :

```bash
python cli.py
```



## Features <a name="Features"></a>

```bash
python cli.py --help
```

...


## Configuration <a name="Configuration"></a>


## Contributing <a name="Contributing"></a>

"If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcome."

## Links <a name="Links"></a>

[documentation](https:google.com)
[project page](https:google.com)

## Licensing <a name="Licensing"></a>

"The code in this project is licensed under MIT license."