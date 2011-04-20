from setuptools import setup, find_packages
import os

version = "1.12"

setup(name="tno.euphorie",
      version=version,
      description="TNO specific extensions for Euphorie",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "changes.rst")).read(),
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python :: 2.6",
        ],
      keywords="Euphorie OIRA RIE",
      author="Wichert Akkerman",
      author_email="wichert@simplon.biz",
      url="http://instrumenten.rie.nl/",
      license="GPL",
      packages=find_packages(exclude=["ez_setup"]),
      namespace_packages=["tno"],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          "Euphorie >=2.6dev-r18059",
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
