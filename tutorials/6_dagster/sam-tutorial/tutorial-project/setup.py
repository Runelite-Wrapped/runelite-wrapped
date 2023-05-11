from setuptools import find_packages, setup

setup(
    name="tutorial_project",
    packages=find_packages(exclude=["tutorial_project_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud"
    ],
    extras_require={"dev": ["dagit", "pytest"]},
)
