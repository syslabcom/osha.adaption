from zope import component

from Testing import ZopeTestCase as ztc

from Products.Archetypes.Schema.factory import instanceSchemaFactory
from Products.Five import fiveconfigure
from Products.Five import zcml
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase import layer

from plone import browserlayer
from osha.policy.interfaces import IOSHACommentsLayer
     
SiteLayer = layer.PloneSite

ztc.installProduct('Relations')
ztc.installProduct('ATReferenceBrowserWidget')
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
            'ATCountryWidget',
            'ATReferenceBrowserWidget',
            'ATVocabularyManager',
            'BlueLinguaLink',
            'CMFPlacefulWorkflow',
            'CMFSin',
            'Calendaring',
            'CaseStudy',
            'Clouseau',
            'DataGridField',
            'FCKeditor',
            'LinguaPlone',
            'Marshall',
            'OSHATranslations',
            'OSHContentLink',
            'PloneFormGen',
            'PloneHelpCenter',
            'PloneSoftwareCenter',
            'PressRoom',
            'Products.CallForContractors',
            'Products.CaseStudy',
            'Products.OSHContentLink',
            'Products.PloneFlashUpload',
            'Products.RALink',
            'Products.RemoteProvider',
            'Products.VocabularyPickerWidget',
            'PublicJobVacancy',
            'RALink',
            'RedirectionTool',
            'Relations',
            'RemoteProvider',
            'RichDocument',
            'Scrawl',
            'TextIndexNG3',
            'UserAndGroupSelectionWidget',
            'VocabularyPickerWidget',
            'collective.orderedmultiselectwidget',
            'collective.portlet.feedmixer',
            'collective.portlet.tal',
            'osha.aggregation',
            'osha.theme',
            'osha.whoswho',
            'p4a.plonevideo',
            'p4a.plonevideoembed',
            'p4a.subtyper',
            'plone.app.blob',
            'plone.app.imaging',
            'plone.app.iterate',
            'plone.app.ldap',
            'plone.browserlayer',
            'plone.portlet.collection',
            'plone.portlet.static',
            'qPloneCaptchas',
            'qPloneComments',
            'slc.aggregation',
            'slc.autotranslate',
            'slc.calendarfetcher',
            'slc.clicksearch',
            'slc.editonpro',
            'slc.foldercontentsfilter',
            'slc.publications',
            'slc.seminarportal',
            'slc.shoppinglist',
            'slc.subsite',
            'slc.treecategories',
            'slc.xliff',
            'syslabcom.filter',
            'osha.adaptation',
            ]

        ptc.setupPloneSite(products=PRODUCTS)

        fiveconfigure.debug_mode = True
        import plone.app.blob
        zcml.load_config('configure.zcml', plone.app.blob)

        import p4a.subtyper
        zcml.load_config('configure.zcml', p4a.subtyper)

        import osha.adaptation
        zcml.load_config('configure.zcml', osha.adaptation)
        fiveconfigure.debug_mode = False

        ztc.installPackage('slc.seminarportal')
        ztc.installPackage('osha.whoswho')

        if IOSHACommentsLayer:
            browserlayer.utils.register_layer(IOSHACommentsLayer, name='osha.policy')

        component.provideAdapter(instanceSchemaFactory)
        SiteLayer.setUp()


class OshaAdaptationTestCase(ptc.PloneTestCase):
    """We use this base class for all the tests in this package. If necessary,
    we can put common utility or setup code in here.
    """
    layer = OshaAdaptationLayer



