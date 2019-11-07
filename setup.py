from setuptools import setup, find_packages
import os

version = '8.1.3'

setup(name="tno.euphorie",
      version=version,
      description="TNO specific extensions for Euphorie",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "changes.rst")).read(),
      classifiers=[
          "Framework :: Plone",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Natural Language :: Dutch",
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 2 :: Only",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
          "Topic :: Internet :: WWW/HTTP",
        ],
      keywords="Euphorie OIRA RIE",
      author="Wichert Akkerman",
      author_email="wichert@simplon.biz",
      url="http://readthedocs.org/docs/tnoeuphorie/en/latest/",
      license="GPL",
      packages=find_packages("src"),
      namespace_packages=["tno"],
      include_package_data=True,
      package_dir={"": "src"},
      zip_safe=False,
      install_requires=[
          'Euphorie >=11.0.0',
          'NuPlone >=1.6.1',
          'Pillow',
          # We seem to have a persisten utility that prevents running upgrade
          # steps. The following package is therefore added for providing the
          # required interface.
          'alembic',
          'collective.js.jqueryui',
          "collective.indexing",
          "plone.browserlayer",
          "five.grok",
          "plone.directives.form",
          "plone.namedfile",
          "setuptools",
          "z3c.form",
          "zope.i18nmessageid",
          "z3c.appconfig",
          "osa",
      ],
      tests_require=[
          "Euphorie [tests]",
      ],
      extras_require={
          "tests": ["Euphorie [tests]"],
      },
      )
