# Add additional fields to the standard content types
# For now I assume that nearly all fields only are relevant for OSHContent
# except:
#   - Keywords, which will be handled by the plone subject
#   - html_meta_keywords, which are used to optimize the SEO Keywords
#   -

import logging

import zope.interface

from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.field import ExtensionField

from Products.ATCountryWidget.Widget import MultiCountryWidget
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from Products.ATVocabularyManager.namedvocabulary import NamedVocabulary
from Products.Archetypes import atapi
from Products.Archetypes.utils import DisplayList
from Products.CMFCore.utils import getToolByName
from Products.DataGridField import DataGridField, DataGridWidget
from Products.DataGridField.Column import Column
from Products.DataGridField.SelectColumn import SelectColumn
from Products.LinguaPlone.utils import generateMethods
from Products.OSHATranslations import OSHAMessageFactory as _
from Products.VocabularyPickerWidget.VocabularyPickerWidget import VocabularyPickerWidget

from slc.treecategories.widgets.widgets import InlineTreeWidget

try:
    from osha.policy.interfaces import IOSHACommentsLayer
except ImportError:
    IOSHACommentsLayer = None

from osha.adaptation.vocabulary import AnnotatableLinkListVocabulary
from osha.adaptation.subtyper import IAnnotatedLinkList
from osha.adaptation import config

log = logging.getLogger('osha.adaptation/schemaextender.py')

LANGUAGE_INDEPENDENT_INITIALIZED = '_languageIndependent_initialized_oshapolicy'

# dummy
DUMMY = False
tags_default = ['A']
tags_vocab = ['A', 'B', 'C']
dummy_vocab = ['this', 'is', 'a', 'dummy', 'vocabulary']
dummy_string = "this is a dummy string"

class ExtensionFieldMixin:
    def _Vocabulary(self, content_instance, vocab_name):
        if DUMMY:
            return atapi.DisplayList([(x, x) for x in dummy_vocab])
        else:
            pv = getToolByName(content_instance, 'portal_vocabularies')
            VOCAB = getattr(pv, vocab_name, None)
            if VOCAB:
                return VOCAB.getDisplayList(VOCAB)
            else:
                return DisplayList()

    def getMutator(self, instance):
        def mutator(value, **kw):
            self.set(instance, value, **kw)

        methodName = getattr(self, 'mutator', None)
        if methodName is None:  # Use default setter
            return mutator
        
        method = getattr(instance, methodName, None)
        if method is None:   # Use default setter
            return mutator
        return method


class NACEField(ExtensionFieldMixin, ExtensionField, atapi.LinesField):

    def Vocabulary(self, content_instance):
        return self._Vocabulary(content_instance, 'NACE')

class SubcategoryField(ExtensionFieldMixin, ExtensionField, atapi.LinesField):

    def Vocabulary(self, content_instance):
        return self._Vocabulary(content_instance, 'Subcategory')

class CountryField(ExtensionFieldMixin, ExtensionField, atapi.LinesField):

    def Vocabulary(self, content_instance):
        return self._Vocabulary(content_instance, 'Country')

class MTSubjectField(ExtensionFieldMixin, ExtensionField, atapi.LinesField):

    def Vocabulary(self, content_instance):
        return self._Vocabulary(content_instance, 'MultilingualThesaurus')

class OSHAMetadataField(ExtensionFieldMixin, ExtensionField, atapi.LinesField):

    def Vocabulary(self, content_instance):
        return self._Vocabulary(content_instance, 'OSHAMetadata')


class AttachmentField(ExtensionField, atapi.FileField):
    """ additional file field for attachments """

class ReferencedContentField(ExtensionFieldMixin, ExtensionField, atapi.ReferenceField):
    """ Possibility to reference content objects, the text of which """
    """ can be used to display inside the current object. """

class NewsMarkerField(ExtensionFieldMixin, ExtensionField, atapi.BooleanField):
    """ Marker field to have object appear in news portlet """

class SEDataGridField(ExtensionFieldMixin, ExtensionField, DataGridField):
    """ Marker field to have object appear in news portlet """

class BaseLinesField(ExtensionFieldMixin, ExtensionField, atapi.LinesField):
    """ """

class ReindexTranslationsField(ExtensionField, atapi.BooleanField):
    """ Indicate whether translations should be reindexd upon saving """

description_reindexTranslations = \
    u"Check this box to have all translated versions reindexed. This is " \
    u"useful when you change language-independent fields suchs as dates " \
    u"and want the changes to be effective in the catalog, too. WARNING: " \
    u"depending on the number of translations, this will lead to " \
    u"a delay in the time it takes to save."

extended_fields_dict = {
    'country':
        CountryField('country',
            schemata='default',
            enforceVocabulary=False,
            languageIndependent=True,
            required=False,
            multiValued=True,
            mutator='setCountry',
            accessor='getCountry',
            widget=MultiCountryWidget(
                label="Countries",
                description= \
                    u'Select one or more countries appropriate for this '
                    u'content',
                description_msgid='help_country',
                provideNullValue=1,
                nullValueTitle="Select...",
                label_msgid='label_country',
                i18n_domain='osha',
            ),
        ),
    'subcategory':
        SubcategoryField('subcategory',
            schemata='default',
            enforceVocabulary=True,
            languageIndependent=True,
            multiValued=True,
            mutator='setSubcategory',
            accessor='getSubcategory',
            widget=VocabularyPickerWidget(
                label="Subcategory (Site position)",
                description= \
                    u'Choose the most relevant subcategories. This will '
                    u'decide where the information is displayed',
                vocabulary="Subcategory",
                label_msgid='label_subcategory',
                description_msgid='help_subcategory',
                i18n_domain='osha',
                condition="python:len(object.getField('subcategory').Vocabulary(object))",
            ),
        ),
    'multilingual_thesaurus':
        MTSubjectField('multilingual_thesaurus',
            schemata='default',
            enforceVocabulary=False,
            languageIndependent=True,
            required=False,
            multiValued=True,
            mutator='setMultilingual_thesaurus',
            accessor='getMultilingual_thesaurus',
            widget=VocabularyPickerWidget(
                label='Multilingual Thesaurus Subject',
                description='Select one or more entries',
                vocabulary="MultilingualThesaurus",
                label_msgid='label_multilingual_thesaurus',
                description_msgid='help_multilingual_thesaurus',
                i18n_domain='osha',
                condition="python:len(object.getField('multilingual_thesaurus').Vocabulary(object))",
            ),
        ),
    'nace':
        NACEField('nace',
            schemata='default',
            languageIndependent=True,
            multiValued=True,
            mutator='setNace',
            accessor='getNace',
            widget=VocabularyPickerWidget(
                label="Sector (NACE Code)",
                description= \
                    u"Pick one or more values by clicking the Add button or "
                    "using the Quicksearch field below.",
                vocabulary="NACE",
                label_msgid='label_nace',
                description_msgid='help_nace',
                i18n_domain='osha',
                condition="python:len(object.getField('nace').Vocabulary(object))",
            ),
        ),
    'osha_metadata':
        OSHAMetadataField('osha_metadata',
            schemata='default',
            enforceVocabulary=True,
            languageIndependent=True,
            multiValued=True,
            mutator='setOsha_metadata',
            accessor='getOsha_metadata',
            widget=VocabularyPickerWidget(
                label=_(u'OSHAMetadata_label', default=u"OSHA Metadata"),
                description=_(u'OSHAMetadata_description', default="Choose the relevant metadata"),
                vocabulary="OSHAMetadata",
                i18n_domain='osha',
                condition="python:len(object.getField('osha_metadata').Vocabulary(object))",
                ),
            vocabulary="OSHAMetadata"
        ),
    'isNews':
        NewsMarkerField('isNews',
            schemata='default',
            read_permission="Review portal content",
            write_permission="Review portal content",
            languageIndependent=True,
            default=False,
            mutator='setIsNews',
            accessor='getIsNews',
            widget=atapi.BooleanWidget(
                label="Mark as News",
                description="Check to have this appear as News in the portlet.",
                label_msgid='label_isnews',
                description_msgid='help_isnews',
                i18n_domain='osha',
            ),
        ),
    'reindexTranslations':
        ReindexTranslationsField('reindexTranslations',
            schemata='default',
            default=False,
            languageIndependent=False,
            widget=atapi.BooleanWidget(
                label=u"Reindex translations on saving.",
                description=description_reindexTranslations,
                visible={'edit': 'visible', 'view': 'invisible'},
                condition="python:object.isCanonical()",
            ),
        ),
    'annotatedlinklist':
        SEDataGridField('annotatedlinklist',
            schemata='default',
            enforceVocabulary=False,
            languageIndependent=False,
            required=False,
            multiValued=True,
            columns=("linktext", "title", "url", "section"),
            widget = DataGridWidget(
                label=u"List of Links",
                description= \
                    u"Add as many links as you wish by adding new rows on "
                    u"the right. Choose a section from the dropdown to order "
                    u"the links.",
                columns={
                    'linktext' : Column("Linktext"),
                    'title' : Column("Title"),
                    'url' : Column("URL"),
                    'section' : SelectColumn("Section", vocabulary=AnnotatableLinkListVocabulary()),
                    },
            ),
        ),
    'attachment':
        AttachmentField('attachment',
            schemata='default',
            widget=atapi.FileWidget(
                label= _(u'osha_event_attachment_label', default=u'Attachment'),
                description= _(u'osha_event_attachment_label',
                    default= \
                        u"You can upload an optional attachment that will "
                        u"be displayed with the event."),
            ),
        ),
    }

class OSHASchemaExtender(object):
    """ This is the base class for all other schema extenders. It sets the 
        layer, the interfaces being implemented and provides a helper method 
        that generates accessors and mutators for language independent fields.
    """
    if IOSHACommentsLayer:
        zope.interface.implements(
                            IOrderableSchemaExtender, 
                            IBrowserLayerAwareExtender
                            )
        layer = IOSHACommentsLayer
    else:
        zope.interface.implements(IOrderableSchemaExtender)

    def __init__(self, context):
        self.context = context
        self._generateMethods(context, self._fields)

    def _generateMethods(self, context, fields, initialized=True):
        """ Call LinguaPlone's generateMethods method to generate accessors 
            which automatically update the values of languageIndependent 
            fields on all translations.
        """
        klass = context.__class__
        if not getattr(klass, LANGUAGE_INDEPENDENT_INITIALIZED, False) \
                                                        or not initialized:

            fields = [field for field in fields if field.languageIndependent]
            generateMethods(klass, fields)
            log.info("called generateMethods on %s (%s) " \
                                    % (klass, self.__class__.__name__))

            setattr(klass, LANGUAGE_INDEPENDENT_INITIALIZED, True)

    def getOrder(self, original):
        """ Try to set the fields order according to the ordering provided in
            osha.adaptation/config.py

            If no such ordering was provided, then return the original.
        """
        portal_type = self.context.portal_type
        original_fields = original['default']
        ordered_fields = \
            config.EXTENDED_TYPES_DEFAULT_FIELDS.get(portal_type, {}).keys()

        if ordered_fields == original['default']:
            original['default'] = ordered_fields
            
        elif len(ordered_fields) >= len(original['default']):
            # The ordered_fields defined in config, contains all the
            # schemaextended fields, not just the ones of the particular
            # extender on which this method is being called. Since the 
            # extenders are being called on after another, the case will arise 
            # where not all the extension fields have been added. We attempt
            # then to return the order for all the fields that *have* been
            # extended.
            actual_fields = [f for f in ordered_fields if f in original_fields]
            if len(actual_fields) < len(original_fields):
                actual_fields += \
                        [f for f in original_fields if f not in ordered_fields]

            original['default'] = actual_fields 

        return original

    def getFields(self):
        return self._fields


class OSHContentExtender(OSHASchemaExtender):
    _fields = [
        extended_fields_dict.get('country').copy(),
        extended_fields_dict.get('multilingual_thesaurus').copy(),
        extended_fields_dict.get('nace').copy(),
        extended_fields_dict.get('subcategory').copy(),
        extended_fields_dict.get('isNews').copy(),
        extended_fields_dict.get('reindexTranslations').copy(),
        ]

    def __init__(self, context):
        self.context = context
        _myfields= list()
        self._generateMethods(context, self._fields)


class DocumentExtender(OSHASchemaExtender):
    _fields = [
        extended_fields_dict.get('nace').copy(),
        extended_fields_dict.get('country').copy(),
        extended_fields_dict.get('multilingual_thesaurus').copy(),
        extended_fields_dict.get('reindexTranslations').copy(),
        ]

    def __init__(self, context):
        self.context = context
        if IAnnotatedLinkList.providedBy(context):
            self._fields.append(
                        extended_fields_dict.get('annotatedlinklist').copy()
                        )

        self._generateMethods(context, self._fields)


class CaseStudyExtender(OSHASchemaExtender):
    """ CaseStudy inherits from RichDocument, therefore the DocumentExtender is
        already being applied. We add here only CaseStudy specific fields.
    """
    _fields = [
        extended_fields_dict.get('isNews').copy(),
        ]

    def __init__(self, context):
        self.context = context
        for f in self._fields:
            if f.getName() in ('country', 'multilingual_thesaurus'):
                f.required = True

        # Case Study inherits from ATDocument. We might get a false positive, 
        # so check that the accessors are really there
        initialized = True
        fields = [field for field in self._fields if field.languageIndependent]
        for field in fields:
            if not getattr(context, field.accessor, None):
                initialized = False
                break

        self._generateMethods(context, fields, initialized)


class EventExtender(OSHASchemaExtender):
    _fields = [
        extended_fields_dict.get('subcategory').copy(),
        extended_fields_dict.get('multilingual_thesaurus').copy(),
        extended_fields_dict.get('isNews').copy(),
        extended_fields_dict.get('reindexTranslations').copy(),
        extended_fields_dict.get('attachment').copy(),
        ]

    def __init__(self, context):
        self.context = context
        for f in self._fields:
            if f.getName() in ('subcategory', 'multilingual_thesaurus'):
                f.required = False

        self._generateMethods(context, self._fields)


class FAQExtender(OSHASchemaExtender):
    """ 
    HelpCenterFAQ uses the AddRemoveWidget 'subject' widget instead of
    the standard one. Since we have override the standard keyword.pt
    template in osha/theme/skins/osha_theme_custom_templates/widgets/keyword.pt 
    to provide translations for the keywords, here we subtype HelpCenterFAQ
    so that it also uses the standard 'subject' widget.
    """
    _fields = [
        extended_fields_dict.get('multilingual_thesaurus').copy(),
        extended_fields_dict.get('nace').copy(),
        extended_fields_dict.get('subcategory').copy(),

        BaseLinesField(
            name='subject',
            multiValued=1,
            accessor="Subject",
            searchable=True,
            widget=atapi.KeywordWidget(
                label=_(u'label_categories', default=u'Categories'),
                description=_(u'help_categories',
                              default=u'Also known as keywords, tags or labels, '
                                      'these help you categorize your content.'),
                ),
            ),
        ]


class RALinkExtender(OSHASchemaExtender):
    """ RALinks are already extended by DocumentExtender because they subtype 
        ATDocument. Here we add only the extra fields.
    """
    _fields = [
        extended_fields_dict.get('isNews').copy(),
        ]

    def __init__(self, context):
        self.context = context
        for f in self._fields:
            if f.getName() in ('country',): 
                f.required = True

        # RA Link inherits from ATDocument. We might get a false positive, so check that the
        # accessors are really there
        initialized = True
        fields = [field for field in self._fields if field.languageIndependent]
        for field in fields:
            if not getattr(context, field.accessor, None):
                initialized = False
                break

        self._generateMethods(context, fields, initialized)


class PressReleaseExtender(OSHASchemaExtender):
    _fields = [
        extended_fields_dict.get('country').copy(),
        extended_fields_dict.get('reindexTranslations').copy(),
        extended_fields_dict.get('isNews').copy(),

        ReferencedContentField('referenced_content',
            languageIndependent=True,
            multiValued=True,
            relationship='referenced_content',
            allowed_types=('Document', 'RichDocument'),
            mutator='setReferenced_content',
            accessor='getReferenced_content',
            widget=ReferenceBrowserWidget(
                label=u"Referenced content",
                description=
                    u"Select one or more content items. Their body text "
                    u"will be displayed as part of the press release",
                allow_search=True,
                allow_browse=False,
                base_query=dict(path=dict(query='textpieces', level=-1), Language=['en','']),
                show_results_without_query=True,
                ),
        ),
        ]


class FileContentExtender(OSHASchemaExtender):
    _fields = [
        extended_fields_dict.get('isNews').copy(),
        extended_fields_dict.get('country').copy(),
        extended_fields_dict.get('subcategory').copy(),
        extended_fields_dict.get('multilingual_thesaurus').copy(),
        extended_fields_dict.get('nace').copy(),
        extended_fields_dict.get('reindexTranslations').copy(),
        ]
 
    def __init__(self, context):
        super(FileContentExtender, self).__init__(context)
        for field in self._fields:
            if field.__name__ in ['subcategory','multilingual_thesaurus','nace']:
                vocabulary = NamedVocabulary(field.widget.vocabulary)
                widget_args = {}
                for arg in ('label', 'description', 'label_msgid', 
                            'description_msgid, i18n_domain'):
                    widget_args[arg] = getattr(field.widget, arg, '')
                widget_args['vocabulary'] = field.widget.vocabulary
                field.vocabulary = vocabulary
                if InlineTreeWidget:
                    field.widget = InlineTreeWidget(**widget_args)

        self._generateMethods(context, self._fields)


class LinkListExtender(OSHASchemaExtender):
    """ This is a general content agnostic extender.

        We would like this extender to only be applicable to the OSHNetwork
        area. Luckily OSHNetwork is in its own subsite and thus has its own
        sitemanager.

        So we should be able to register the extender locally, by just doing 
        this:
            sm = portal.getSiteManager()
            sm.registerAdapter(
                            LinkListExtender,
                            (IATEvent,),
                            IOrderableSchemaExtender,
                            )

        We do this in an external method:
            osha.policy/Extensions/setLinkListExtension.py
        
        For more info on the mechanism, see 
        five.localsitemanager.localsitemaqnager.txt
    """
    _fields = [
        extended_fields_dict.get('annotatedlinklist').copy(),
        ]


class OshaMetadataExtender(OSHASchemaExtender):
    """ This is a general content agnostic extender.
        
        For details, please see the description in the LinkListExtender.
    """
    _fields = [
        extended_fields_dict.get('osha_metadata').copy(),
        ]


class ProviderModifier(object):
    """ This is a schema modifier, not extender.
    """
    if IOSHACommentsLayer:
        zope.interface.implements(
                            ISchemaModifier, 
                            IBrowserLayerAwareExtender
                            )
        layer = IOSHACommentsLayer
    else:
        zope.interface.implements(ISchemaModifier)
    
    def __init__(self, context):
        self.context = context
    
    def fiddle(self, schema):
        """Fiddle the schema.

        This is a copy of the class' schema, with any ISchemaExtender-provided
        fields added. The schema may be modified in-place: there is no
        need to return a value.

        In general, it will be a bad idea to delete or materially change
        fields, since other components may depend on these ones.

        If you change any fields, then you are responsible for making a copy of
        them first and place the copy in the schema.
        """
        if self.context.portal_type != 'Provider':
            return 

        unwantedFields = (
                'subject', 
                'allowDiscussion', 
                'creation_date', 
                'modification_date', 
                'language', 
                'sme', 
                'provider'
                )

        moveToDefault = (
                'remoteLanguage', 
                'location', 
                'effectiveDate', 
                'expirationDate'
                )

        for name in unwantedFields:
            if schema.get(name):
                field = schema[name].copy()
                field.widget.visible = {'edit': 'invisible', 'view': 'invisible'}
                schema[name] = field

        for name in moveToDefault:
            if schema.get(name):
                schema.changeSchemataForField(name, 'default')

        field = schema['providerCategory'].copy()
        field.required = True
        schema['providerCategory'] = field
                
        # Make sure that the desired ordering is achieved
        portal_type = self.context.portal_type
        ordered_fields = \
            config.EXTENDED_TYPES_DEFAULT_FIELDS.get(portal_type, {}).keys()
        for name in ordered_fields:
            position = ordered_fields.index(name)
            schema.moveField(name, pos=position)



class EventModifier(object):
    """ This is a schema modifier, not extender.
    """
    if IOSHACommentsLayer:
        zope.interface.implements(
                            ISchemaModifier, 
                            IBrowserLayerAwareExtender
                            )
        layer = IOSHACommentsLayer
    else:
        zope.interface.implements(ISchemaModifier)
    
    def __init__(self, context):
        self.context = context
    
    def fiddle(self, schema):
        """Fiddle the schema.

        This is a copy of the class' schema, with any ISchemaExtender-provided
        fields added. The schema may be modified in-place: there is no
        need to return a value.

        In general, it will be a bad idea to delete or materially change
        fields, since other components may depend on these ones.

        If you change any fields, then you are responsible for making a copy of
        them first and place the copy in the schema.
        """
        if self.context.portal_type != 'Event':
            return 

        eventType = schema['eventType'].copy()
        eventType.widget.visible['edit'] = 'invisible'
        schema['eventType'] = eventType

        schema.changeSchemataForField('location', 'categorization')
        portal_type = self.context.portal_type
        ordered_fields = \
            config.EXTENDED_TYPES_DEFAULT_FIELDS.get(portal_type, {}).keys()

        for name in ordered_fields:
            position = ordered_fields.index(name)
            schema.moveField(name, pos=position)

        # schema['subject'].widget.visible['edit'] = 'invisible'

        # schema.moveField('relatedItems', pos='bottom')
        # schema['relatedItems'].widget.visible['edit'] = 'invisible'
        # schema.moveField('excludeFromNav', after='allowDiscussion')
        # schema.moveField('allowDiscussion', after='relatedItems')

        # schema.changeSchemataForField('subject', 'categorization')
        # schema.changeSchemataForField('relatedItems', 'categorization')
        # schema.changeSchemataForField('language', 'categorization')

        # schema.changeSchemataForField('effectiveDate', 'dates')
        # schema.changeSchemataForField('expirationDate', 'dates')    
        # schema.changeSchemataForField('creation_date', 'dates')    
        # schema.changeSchemataForField('modification_date', 'dates')    

        # schema.changeSchemataForField('creators', 'ownership')
        # schema.changeSchemataForField('contributors', 'ownership')
        # schema.changeSchemataForField('rights', 'ownership')

        # schema.changeSchemataForField('allowDiscussion', 'settings')
        # schema.changeSchemataForField('excludeFromNav', 'settings')



