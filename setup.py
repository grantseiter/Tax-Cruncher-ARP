import setuptools
import os

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="taxcrunch",
    version=os.environ.get("VERSION", "0.0.0"),
    author="Grant M. Seiter",
    author_email="seiterecon@gmail.com",
    description=(
        "Calculates federal tax liabilities from individual data under "
        "the American Rescue Plan (2021). Modified Version of Tax-Cruncher" 
        "developed and licensed by Peter Metz (email: pmetzdc@gmail.com)"
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pslmodels/Tax-Cruncher",
    packages=setuptools.find_packages(),
    install_requires=["paramtools"],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)