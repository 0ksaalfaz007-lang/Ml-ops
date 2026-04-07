from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

    setup(
        name="mlops_project",
        version="0.1",
        author="faiz",
        packages=find_packages(),
        install_requires=requirements,
    )