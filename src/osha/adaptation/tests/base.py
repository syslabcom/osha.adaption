from zope import component

from Testing import ZopeTestCase as ztc

from Products.Archetypes.Schema.factory import instanceSchemaFactory
from Products.Five import zcml
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase import layer

SiteLayer = layer.PloneSite

ztc.installProduct('ATVocabularyManager')
ztc.installProduct('TextIndexNG3')
ztc.installProduct('CaseStudy')
ztc.installProduct('DataGridField')
ztc.installProduct('LinguaPlone')
ztc.installProduct('PressRoom')
ztc.installProduct('RALink')
ztc.installProduct('OSHATranslations')
ztc.installProduct('RichDocument')
ztc.installProduct('VocabularyPickerWidget')

class OshaAdaptationLayer(SiteLayer):

    @classmethod
    def setUp(cls):
        PRODUCTS = [
            'ATVocabularyManager',
            'TextIndexNG3',
            'CaseStudy',
            'DataGridField',
            'LinguaPlone',
            'PressRoom',
            'RALink',
            'OSHATranslations',
            'RichDocument',
            'VocabularyPickerWidget',
            'p4a.subtyper',
            'slc.treecategories',
            'osha.adaptation',
            ]

        ptc.setupPloneSite(products=PRODUCTS)

        import osha.adaptation
        zcml.load_config('configure.zcml', osha.adaptation)

        component.provideAdapter(instanceSchemaFactory)
        SiteLayer.setUp()


class OshaAdaptationTestCase(ptc.PloneTestCase):
    """We use this base class for all the tests in this package. If necessary,
    we can put common utility or setup code in here.
    """
    layer = OshaAdaptationLayer



