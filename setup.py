'''import modules'''
from setuptools import setup, find_packages

VERSION = '0.2'
DESCRIPTION = 'Inventario para Pernos'
setup(
        name="Oiq-system",
        version=VERSION,
        author="1is7ac3",
        author_email="<isaac.qa13@gmail.com>",
        description=DESCRIPTION,
        packages=find_packages(),
        install_requires=[
            'mysql-connector-python'
        ],
)
