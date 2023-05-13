from setuptools import setup, find_namespace_packages

setup(
    name="clean_folder",
    version="3.0",
    description="Sorts your junk",
    author="Andrii Vlasiuk",
    packages=find_namespace_packages(),
    entry_points={"console_scripts": ["clean=clean_folder.clean:main"]},
)
