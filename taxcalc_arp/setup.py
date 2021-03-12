import setuptools
import os

long_description = "placeholder"

setuptools.setup(
    name="taxcalc",
    version=os.environ.get("VERSION", "0.0.0"),
    author="Grant M. Seiter",
    author_email="seiterecon@gmail.com",
    description=(
        "Calculates federal tax liabilities from individual data under "
        "the American Rescue Plan (2021). Modified Version of Tax-Calculator" 
        "developed by open-source PSLModels"
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pslmodels/Tax-Calculator",
    packages=setuptools.find_packages(),
    install_requires=["paramtools"],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)