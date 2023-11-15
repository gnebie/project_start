from dataclasses import dataclass 
import pkg_resources  # part of setuptools

@dataclass
class Version:
    version_nbr:str
    version_endpoint:str

version_1 = Version("v1.0", "/v1")

version_list = [
    version_1
]

project_name = "{{ cookiecutter.project_name }}"

version = pkg_resources.require("MyProject")[0].version
last_version = version

def versions():
    return version_list

def version():
    return last_version