from setuptools import find_packages
from setuptools import setup

import os


version = "9.0.1"

setup(
    name="tno.euphorie",
    version=version,
    description="TNO specific extensions for Euphorie",
    long_description=open("README.rst").read()
    + "\n"
    + open(os.path.join("docs", "changes.rst")).read(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 5.2",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Natural Language :: Dutch",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2 :: Only",
        "Programming Language :: Python :: 2.7",
        "Topic :: Internet :: WWW/HTTP",
    ],
    keywords="Euphorie OIRA RIE",
    author="Wichert Akkerman and Syslab.com",
    author_email="info@syslab.com",
    url="http://readthedocs.org/docs/tnoeuphorie/en/latest/",
    license="GPL",
    packages=find_packages("src"),
    namespace_packages=["tno"],
    include_package_data=True,
    package_dir={"": "src"},
    zip_safe=False,
    install_requires=[
        "Euphorie >=12.0.0",
        "NuPlone >=2.0.0",
        "Pillow",
        "alembic",
        "Products.statusmessages",
        "htmllaundry",
        "plone.autoform",
        "plone.tiles",
        "requests",
        "setuptools",
        "zope.publisher",
        "plone.api",
    ],
    tests_require=[
        "Euphorie [tests]",
    ],
    extras_require={
        "tests": ["Euphorie [tests]"],
    },
)
