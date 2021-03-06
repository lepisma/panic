from setuptools import find_packages, setup

with open("README.rst") as readme_file:
    readme = readme_file.read()

project_url = "https://github.com/"
project_url += "lepisma/panic"

setup(
    name="panic",
    version="0.1.1",
    description="Notify (possible) memory leaks",
    long_description=readme,
    author="Abhinav Tushar",
    author_email="abhinav.tushar.vs@gmail.com",
    url=project_url,
    install_requires=["docopt", "psutil", "sh", "daemonize"],
    keywords="",
    packages=find_packages(),
    entry_points={
        "console_scripts":
        ["panic=panic:main"],
    },
    classifiers=(
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only"
    ))
