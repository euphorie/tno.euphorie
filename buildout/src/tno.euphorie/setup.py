from setuptools import setup, find_packages
import os

version = "1.10.1"

setup(name="tno.euphorie",
      version=version,
      description="TNO specific extensions for Euphorie",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords="Euphorie OIRAT RIE",
      author="Wichert Akkerman",
      author_email="wichert@simplon.biz",
      url="http://instrumenten.rie.nl/",
      license="GPL",
      packages=find_packages(exclude=["ez_setup"]),
      namespace_packages=["tno"],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          "Euphorie >=2.4dev-r17930",
          "plone.browserlayer",
          "five.grok",
          "plone.directives.form",
          "plone.namedfile",
          "setuptools",
          "z3c.form",
          "zope.i18nmessageid",
          "z3c.appconfig",
      ],
      tests_require = [
          "Euphorie [tests]",
      ],
      extras_require = {
        "tests" : [ "Euphorie [tests]",
                  ],
      },
      )
