from dataclasses import dataclass 
import pkg_resources  # part of setuptools

@dataclass
class Version:
    version_nbr:str
    version_endpoint:str

version_1 = Version("v1.0", "/v1")
version_list = [version_1]

project_name = "{{ cookiecutter.project_name }}"

last_version = version_1

def get_versions():
    return version_list

def get_last_version():
    return last_version