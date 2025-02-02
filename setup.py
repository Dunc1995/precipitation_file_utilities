from setuptools import setup

setup(
    # Application name:
    name="PrecipitationFileUtilities",

    # Version number (initial):
    version="0.1.0",

    # Application author details:
    author="Duncan Bailey",
    author_email="dpbailey1995@outlook.com",

    # Packages
    packages=["prefileutils"],

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="https://github.com/Dunc1995/jba_code_challenge",

    #
    license="LICENSE",
    description="MVP application for uploading precipitation data to a SQL database.",
    #long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[],

    entry_points={
    'console_scripts': [
        'prefileutils = prefileutils.__main__:main'
    ]
    }
)