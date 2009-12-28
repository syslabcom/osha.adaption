from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='osha.adaptation',
      version=version,
      description="OSHA specific adaptors, schemaextensions and subtypes",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='plone osha',
      author='Syslab.com GmbH',
      author_email='info@syslab.com',
      url='http://syslab.com',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      package_dir = {'' : 'src'},
      namespace_packages=['osha'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
            'setuptools',
            'Products.ATVocabularyManager',
            'Products.OSHATranslations',
            'slc.treecategories',
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=["PasteScript"],
      paster_plugins = ["ZopeSkel"],
      )
