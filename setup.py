from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install
import subprocess

class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        develop.run(self)
        self.run_playwright_install()

    def run_playwright_install(self):
        """Run playwright install after setup in develop mode."""
        subprocess.check_call(["python3", "-m", "playwright.install"])

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        self.run_playwright_install()

    def run_playwright_install(self):
        """Run playwright install after setup."""
        subprocess.check_call(["python3", "-m", "playwright.install"])

setup(
    name='coomer_xtractor',
    version='2.0.1',
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
        "setuptools",  # Latest version
        "SQLAlchemy~=2.0.23",
        "playwright~=1.50.0",
        "Faker~=36.1.0",
        "cowsay~=6.1",
        "backoff~=2.2.1"
    ],
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },
    long_description="""Coomer Xtractor is a simple tool used to download content from coomer.su. The tool is freely available for use, and contributions from the community are welcomed and appreciated.""",
)
