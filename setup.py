from setuptools import setup
import os

#https://pythonhosted.org/an_example_pypi_project/setuptools.html
#https://python-poetry.org/docs/basic-usage/

project_name = "{{ cookiecutter.project_name }}"
git = "https://github.com/{{ cookiecutter.repo_name }}"

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

with open('requirements.txt') as f:
    required = f.read().splitlines()


setup(
    version="{{ cookiecutter.version }}",
    description="My description",
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    url=f"{git}/{project_name}",
    author="{{ cookiecutter.autor }}",
    author_email="{{ cookiecutter.email }}",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    packages=[f"{project_name}"],
    include_package_data=True,
    
    install_requires= [
        'importlib-metadata; python_version == "3.10"',
    ] + required,
    entry_points={"console_scripts": [f"{project_name}={project_name}.__main__:main"]},
)