from setuptools import find_packages, setup

setup(
    name="jerome_tutorial",
    packages=find_packages(exclude=["jerome_tutorial_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud"
    ],
    extras_require={"dev": ["dagit", "pytest"]},
)
