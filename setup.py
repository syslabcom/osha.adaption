from setuptools import setup
import os

version = '0.1.14dev'

tests_require=[
            'zope.testing',
            'Products.TextIndexNG3',
            'Products.CaseStudy',
            'Products.RichDocument',
            'Products.RALink',
            'Products.RemoteProvider',
            'Products.PressRoom',
            'Products.PloneHelpCenter',
            'Products.OSHContentLink',
            'osha.whoswho',
            'plone.app.blob',
            'slc.seminarportal',
            ]

setup(
    name='osha.adaptation',
    version=version,
    description="OSHA specific adaptors, schemaextensions and subtypes",
    long_description=open("README.txt").read() + "\n" +
                    open(os.path.join("docs", "HISTORY.txt")).read() +"\n" +
                    open(os.path.join("docs", "TODO.txt")).read(),
    # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
    "Framework :: Plone",
    "Programming Language :: Python",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "License :: OSI Approved :: GNU General Public License (GPL)",
    "License :: OSI Approved :: European Union Public Licence 1.1 (EUPL 1.1)",
    ],
    keywords='plone osha',
    author='Syslab.com GmbH',
    author_email='info@syslab.com',
    url='http://syslab.com',
    license='GPL',
    packages=['osha', 'osha/adaptation'],
    package_dir = {'' : 'src'},
    namespace_packages=['osha'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'Products.ATCountryWidget',
        'archetypes.schemaextender',
        'Products.ATVocabularyManager',
        'Products.DataGridField',
        'Products.LinguaPlone',
        'Products.VocabularyPickerWidget',
        'p4a.subtyper',
        'slc.treecategories',
    ],
    tests_require=tests_require,
    extras_require=dict(tests=tests_require),
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
    setup_requires=["PasteScript"],
    paster_plugins = ["ZopeSkel"],
    )

