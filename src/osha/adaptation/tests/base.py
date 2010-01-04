from zope import component

from Testing import ZopeTestCase as ztc

from Products.Archetypes.Schema.factory import instanceSchemaFactory
from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase import layer

from plone import browserlayer

try:
    from osha.policy.interfaces import IOSHACommentsLayer
except ImportError:
    IOSHACommentsLayer = None

SiteLayer = layer.PloneSite

ztc.installProduct('ATVocabularyManager')
ztc.installProduct('TextIndexNG3')
ztc.installProduct('CaseStudy')
ztc.installProduct('DataGridField')
ztc.installProduct('LinguaPlone')
ztc.installProduct('PressRoom')
ztc.installProduct('RALink')
ztc.installProduct('RemoteProvider')
ztc.installProduct('OSHATranslations')
ztc.installProduct('OSHContentLink')
ztc.installProduct('RichDocument')
ztc.installProduct('VocabularyPickerWidget')
ztc.installProduct('PloneHelpCenter')

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
            'OSHContentLink',
            'OSHATranslations',
            'RichDocument',
            'RemoteProvider',
            'PloneHelpCenter',
            'VocabularyPickerWidget',
            'p4a.subtyper',
            'plone.app.blob',
            'slc.treecategories',
            'slc.seminarportal',
            'osha.adaptation',
            ]

        ptc.setupPloneSite(products=PRODUCTS)

        fiveconfigure.debug_mode = True
        import p4a.subtyper
        zcml.load_config('configure.zcml', p4a.subtyper)

        import osha.adaptation
        zcml.load_config('configure.zcml', osha.adaptation)
        fiveconfigure.debug_mode = False

        ztc.installPackage('slc.seminarportal');

        if IOSHACommentsLayer:
            browserlayer.utils.register_layer(IOSHACommentsLayer, name='osha.policy')

        component.provideAdapter(instanceSchemaFactory)
        SiteLayer.setUp()


class OshaAdaptationTestCase(ptc.PloneTestCase):
    """We use this base class for all the tests in this package. If necessary,
    we can put common utility or setup code in here.
    """
    layer = OshaAdaptationLayer



