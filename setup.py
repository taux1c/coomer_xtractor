from setuptools import setup

setup(
    name='coomer_xtractor',
    version='0.0.9',
    packages=['coomer_xtractor', 'coomer_xtractor.menus', 'coomer_xtractor.models', 'coomer_xtractor.actions',
              'coomer_xtractor.scrapers'],
    url='https://github.com/taux1c/coomer_xtractor/',
    license='MIT',
    author='Taux1c',
    author_email='taux1c.software@protonmail.com',
    description='A simple tool used to download content from coomer.su',
    entry_points={
        'console_scripts': [
            'coomer=coomer_xtractor.main:main'
        ]
    },
    install_requires=[
        "aiofiles~=23.2.1",
        "httpx~=0.25.2",
        "bs4~=0.0.1",
        "beautifulsoup4~=4.12.2",
        "SQLAlchemy~=2.0.23",
        "lxml"
    ],
    long_description="""Coomer Xtractor is a simple tool used to download content from coomer.su. The tool is freely available for use, and contributions from the community are welcomed and appreciated.""",

)
