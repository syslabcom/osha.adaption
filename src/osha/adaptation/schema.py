# Add additional fields to the standard content types
# For now I assume that nearly all fields only are relevant for OSHContent
# except:
#   - Keywords, which will be handled by the plone subject
#   - html_meta_keywords, which are used to optimize the SEO Keywords

import logging

import zope.interface

from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.field import ExtensionField
from collective.dynatree.atwidget import DynatreeWidget

from Products.ATCountryWidget.Widget import MultiCountryWidget
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from Products.ATVocabularyManager import NamedVocabulary
from Products.Archetypes import atapi
from Products.Archetypes.utils import DisplayList
from Products.ATContentTypes.configuration import zconf
from Products.CMFCore.utils import getToolByName
from Products.DataGridField import DataGridField, DataGridWidget
from Products.DataGridField.Column import Column
from Products.DataGridField.SelectColumn import SelectColumn
from Products.LinguaPlone.utils import generateMethods
# from Products.VocabularyPickerWidget.VocabularyPickerWidget import VocabularyPickerWidget

from osha.adaptation import config
from osha.adaptation.subtyper import IAnnotatedLinkList
from osha.adaptation.vocabulary import AnnotatableLinkListVocabulary
from osha.policy.interfaces import IOSHACommentsLayer
from osha.theme import OSHAMessageFactory as _

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

    def getAccessor(self, instance):
        def accessor(**kw):
            self.get(instance, **kw)

        methodName = getattr(self, 'accessor', None)
        if methodName is None:  # Use default getter
            return accessor

        method = getattr(instance, methodName, None)
        if method is None:   # Use default getter
            return accessor
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


class ReferencedContentField(ExtensionFieldMixin, ExtensionField,
                             atapi.ReferenceField):
    """ Possibility to reference content objects, the text of which """
    """ can be used to display inside the current object. """


class NewsMarkerField(ExtensionFieldMixin, ExtensionField, atapi.BooleanField):
    """ Marker field to have object appear in news portlet """


class SELinesField(ExtensionFieldMixin, ExtensionField, atapi.LinesField):
    """ A schema-extender aware LinesField """


class SEBooleanField(ExtensionField, atapi.BooleanField):
    """ A schema-extender aware BooleanField """


class SEDataGridField(ExtensionFieldMixin, ExtensionField, DataGridField):
    """ A schema-extender aware DataGridWidget """


class SEFileField(ExtensionField, atapi.FileField):
    """ A schema-extender aware FileField """


class SETextField(ExtensionFieldMixin, ExtensionField, atapi.TextField):
    """ A schema-extender aware TextField """


class SEStringField(ExtensionFieldMixin, ExtensionField, atapi.StringField):
    """ A schema-extender aware String field """


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
                description=(
                    u'Select one or more countries appropriate for this '
                    u'content'),
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
            enforceVocabulary=False,
            languageIndependent=True,
            multiValued=True,
            mutator='setSubcategory',
            accessor='getSubcategory',
            vocabulary=NamedVocabulary("Subcategory"),
            widget=DynatreeWidget(
                label=u"Subcategory",
                description=u"Pick one or more values by ticking a checkbox" \
                " in the tree. You can use the quick search field below to " \
                "find values by typing the first letters. Click 'Close' " \
                "when you are finished picking values.",
                selectMode=2,
                rootVisible=False,
                minExpandLevel=1,
                overlay=True,
                flatlist=True,
            ),
            # widget=VocabularyPickerWidget(
            #     label="Subcategory (Site position)",
            #     description= \
            #         u'Choose the most relevant subcategories. This will '
            #         u'decide where the information is displayed',
            #     vocabulary="Subcategory",
            #     label_msgid='label_subcategory',
            #     description_msgid='help_subcategory',
            #     i18n_domain='osha',
            #     condition="python:len(object.getField(
            #             'subcategory').Vocabulary(object))",
            # ),
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
            vocabulary=NamedVocabulary("MultilingualThesaurus"),
            widget=DynatreeWidget(
                label=u"Multilingual Thesaurus Subject",
                description=u"Pick one or more values by ticking a checkbox" \
                " in the tree. You can use the quick search field below to " \
                "find values by typing the first letters. Click 'Close' " \
                "when you are finished picking values.",
                selectMode=2,
                showKey=True,
                rootVisible=False,
                minExpandLevel=1,
                overlay=True,
                flatlist=True,
            ),
            # widget=VocabularyPickerWidget(
            #     label='Multilingual Thesaurus Subject',
            #     description='Select one or more entries',
            #     vocabulary="MultilingualThesaurus",
            #     label_msgid='label_multilingual_thesaurus',
            #     description_msgid='help_multilingual_thesaurus',
            #     i18n_domain='osha',
            #     condition="python:len(object.getField(
            #           'multilingual_thesaurus').Vocabulary(object))",
            # ),
        ),
    'nace':
        NACEField('nace',
            schemata='default',
            languageIndependent=True,
            multiValued=True,
            mutator='setNace',
            accessor='getNace',
            vocabulary=NamedVocabulary("NACE"),
            widget=DynatreeWidget(
                label=u"Sector (NACE Code)",
                description=u"Pick one or more values by ticking a checkbox" \
                " in the tree. You can use the quick search field below to " \
                "find values by typing the first letters. Click 'Close' " \
                "when you are finished picking values.",
                selectMode=2,
                showKey=True,
                rootVisible=False,
                minExpandLevel=1,
                overlay=True,
                flatlist=True,
            ),
            # widget=VocabularyPickerWidget(
            #     label="Sector (NACE Code)",
            #     description= \
            #         u"Pick one or more values by clicking the Add button or "
            #         "using the Quicksearch field below.",
            #     vocabulary="NACE",
            #     label_msgid='label_nace',
            #     description_msgid='help_nace',
            #     i18n_domain='osha',
            #     condition="python:len(object.getField(
            #      'nace').Vocabulary(object))",
            # ),
        ),
    'osha_metadata':
        OSHAMetadataField('osha_metadata',
            schemata='default',
            enforceVocabulary=True,
            languageIndependent=True,
            multiValued=True,
            mutator='setOsha_metadata',
            accessor='getOsha_metadata',
            vocabulary=NamedVocabulary("OSHAMetadata"),
            widget=DynatreeWidget(
                label=_(u'OSHAMetadata_label', default=u"OSHA Metadata"),
                description=_(u'OSHAMetadata_description',
                         default="Choose the relevant metadata"),
                selectMode=2,
                showKey=False,
                rootVisible=False,
                minExpandLevel=1,
                overlay=True,
                flatlist=True,
                ),
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
                description=("Check to have this appear as News in the "
                             "portlet."),
                label_msgid='label_isnews',
                description_msgid='help_isnews',
                i18n_domain='osha',
            ),
        ),
    'reindexTranslations':
        SEBooleanField('reindexTranslations',
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
            widget=DataGridWidget(
                label=u"List of Links",
                description=(
                    u"Add as many links as you wish by adding new rows on "
                    u"the right. Choose a section from the dropdown to order "
                    u"the links."),
                columns={
                    'linktext': Column("Linktext"),
                    'title': Column("Title"),
                    'url': Column("URL"),
                    'section': SelectColumn("Section",
                            vocabulary=AnnotatableLinkListVocabulary()),
                    },
            ),
        ),
    'attachment':
        SEFileField('attachment',
            schemata='default',
            widget=atapi.FileWidget(
                label=_(u'osha_event_attachment_label',
                         default=u'Attachment'),
                description=_(u'osha_event_attachment_description',
                    default=(u"You can upload an optional attachment that "
                             u"will be displayed with the event.")),
            ),
        ),
    'seoDescription':
        SETextField('seoDescription',
            schemata='default',
            widget=atapi.TextAreaWidget(
                label=_(
                    u'osha_seo_description_label',
                    default=u'SEO Description'
                    ),
                description=_(u'osha_seo_description_description',
                    default=(
                        u"Provide here a description that is purely for SEO "
                        "(Search Engine Optimisation) purposes. It will "
                        "appear in the <meta> tag in the "
                        "<head> section of the HTML document, but nowhere "
                        "in the actual website content.")
                        ),
                visible={'edit': 'visible', 'view': 'invisible'},
            ),
        ),
    'dateToBeConfirmed':
        SEBooleanField('dateToBeConfirmed',
            schemata='default',
            default=False,
            languageIndependent=False,
            widget=atapi.BooleanWidget(
                label=_(u'Date to be confirmed'),
                description=_(
                    u'label_date_to_be_confirmed',
                    default=(
                        u"Check this box if the date has not yet been "
                        "confirmed.")
                    ),
                visible={'edit': 'visible', 'view': 'invisible'},
                condition="python:object.isCanonical()",
            ),
        ),
    'external_link':
        SEStringField('external_link',
            schemata='default',
            languageIndependent=False,
            widget=atapi.StringField._properties['widget'](
                label=_(u'label_external_link', default=u"External link"),
                description=_(u'description_external_link',
                    default=u"Enter a link to which this item should " \
                              "point to."),
                size=80,
            ),
        ),
    }


class OSHASchemaExtender(object):
    """This is the base class for all other schema extenders. It sets the
    layer, the interfaces being implemented and provides a helper method
    that generates accessors and mutators for language independent fields.
    """
    zope.interface.implements(IOrderableSchemaExtender)

    def __init__(self, context):
        self.context = context
        self._generateMethods(context, self._fields)

    def _generateMethods(self, context, fields, initialized=True,
                         marker=LANGUAGE_INDEPENDENT_INITIALIZED):
        """ Call LinguaPlone's generateMethods method to generate accessors
            which automatically update the values of languageIndependent
            fields on all translations.
        """
        klass = context.__class__
        if not getattr(klass, marker, False):  # or not initialized:
            fields = [field for field in fields if field.languageIndependent]
            generateMethods(klass, fields)
            log.info("calling generateMethods on %s (%s) for these "
                "fields: %s " % (klass, self.__class__.__name__,
                                 str([x.getName() for x in fields]))
                 )
            setattr(klass, marker, True)

    def getOrder(self, original):
        """ Try to set the fields order according to the ordering provided in
            osha.adaptation/config.py

            If no such ordering was provided, then return the original.
        """
        portal_type = self.context.portal_type
        ordered_fields_dict = \
            config.EXTENDED_TYPES_DEFAULT_FIELDS.get(portal_type)

        if ordered_fields_dict is None:
            # Ticket 999:
            # seoDescription must be directly below description
            if 'seoDescription' not in original['default']:
                return original

            of = original['default']
            i = of.index('description')
            of.remove('seoDescription')
            of = of[:i + 1] + ['seoDescription'] + of[i + 1:]
            original['default'] = of
            return original

        ordered_fields = ordered_fields_dict.keys()
        original_fields = original['default']

        if len(ordered_fields) != len(original_fields):
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
        else:
            original['default'] = ordered_fields

        return original

    def getFields(self):
        return self._fields


class OSHContentExtender(OSHASchemaExtender):
    _fields = [
        extended_fields_dict.get('country').copy(),
        extended_fields_dict.get('subcategory').copy(),
        extended_fields_dict.get('multilingual_thesaurus').copy(),
        extended_fields_dict.get('nace').copy(),
        extended_fields_dict.get('isNews').copy(),
        extended_fields_dict.get('osha_metadata').copy(),
        extended_fields_dict.get('seoDescription').copy(),
        ]

    def __init__(self, context):
        self.context = context
        #_myfields = list()
        self._generateMethods(context, self._fields)


class DocumentExtender(OSHASchemaExtender):
    # Note: suncategory is not explicitly needed on Document. But on
    # FAQ items, that derived from ATDocument
    _fields = [
        extended_fields_dict.get('nace').copy(),
        extended_fields_dict.get('country').copy(),
        extended_fields_dict.get('multilingual_thesaurus').copy(),
        extended_fields_dict.get('reindexTranslations').copy(),
        extended_fields_dict.get('osha_metadata').copy(),
        extended_fields_dict.get('external_link').copy(),
        extended_fields_dict.get('seoDescription').copy(),
        extended_fields_dict.get('subcategory').copy(),
        ]

    def __init__(self, context):
        self.context = context
        if IAnnotatedLinkList.providedBy(context):
            self._fields.append(
                        extended_fields_dict.get('annotatedlinklist').copy()
                        )

        self._generateMethods(context, self._fields)


class SEOExtender(OSHASchemaExtender):
    _fields = [
        extended_fields_dict.get('seoDescription').copy(),
        ]

    def __init__(self, context):
        self.context = context
        self._generateMethods(context, self._fields)


class CaseStudyExtender(OSHASchemaExtender):
    """ The following assupmtion turned out to be WRONG:
    <<CaseStudy inherits from RichDocument, therefore the DocumentExtender is
    already being applied. We add here only CaseStudy specific fields.>>

    Only if the document extender is initialised first does this work.
    Otherwise we only get the fields defined here explicitly.
    Therefore ALL required fields are defined now. For those fields which do
    not yet have generated methods, _generateMethods is called.
    """
    _fields = [
        extended_fields_dict.get('nace').copy(),
        extended_fields_dict.get('country').copy(),
        extended_fields_dict.get('subcategory').copy(),
        extended_fields_dict.get('multilingual_thesaurus').copy(),
        extended_fields_dict.get('reindexTranslations').copy(),
        extended_fields_dict.get('osha_metadata').copy(),
        extended_fields_dict.get('isNews').copy(),
        ]

    def __init__(self, context):
        self.context = context
        for f in self._fields:
            if f.getName() in ('country', 'multilingual_thesaurus'):
                f.required = True

        # Case Study inherits from ATDocument. We might get a false positive,
        # so check that the accessors are really there

        fields = [field for field in self._fields if field.languageIndependent]
        not_yet_initialised = list()
        for field in fields:
            if not getattr(context, field.accessor, None):
                not_yet_initialised.append(field)

        if not_yet_initialised:
            self._generateMethods(context, fields=not_yet_initialised,
                                  initialized=False)


class EventExtender(OSHASchemaExtender):
    _fields = [
        extended_fields_dict.get('subcategory').copy(),
        extended_fields_dict.get('multilingual_thesaurus').copy(),
        extended_fields_dict.get('isNews').copy(),
        extended_fields_dict.get('reindexTranslations').copy(),
        extended_fields_dict.get('attachment').copy(),
        extended_fields_dict.get('osha_metadata').copy(),
        extended_fields_dict.get('seoDescription').copy(),
        extended_fields_dict.get('dateToBeConfirmed').copy(),
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
        extended_fields_dict.get('nace').copy(),
        extended_fields_dict.get('country').copy(),
        extended_fields_dict.get('multilingual_thesaurus').copy(),
        extended_fields_dict.get('reindexTranslations').copy(),
        extended_fields_dict.get('osha_metadata').copy(),
        extended_fields_dict.get('external_link').copy(),
        extended_fields_dict.get('seoDescription').copy(),
        extended_fields_dict.get('subcategory').copy(),

        # We don't want the Subject field on FAQs any more. Instead, we use the
        # Subcategory field. #1195
        #
        #SELinesField(
        #     name='subject',
        #     multiValued=1,
        #     searchable=True,
        #     languageIndependent=True,
        #     mutator="setSubject",
        #     accessor="Subject",
        #     widget=atapi.KeywordWidget(
        #         label=_(u'label_categories', default=u'Categories'),
        #         description=_(u'help_categories',
        #                default=(u'Also known as keywords, tags or labels, '
        #                         u'these help you categorize your content.')),
        #         ),
        #     ),
        ]

    def __init__(self, context):
        self.context = context
        self._generateMethods(context, self._fields)


class RALinkExtender(OSHASchemaExtender):
    """ The following assupmtion turned out to be WRONG:
    <<RALinks are already extended by DocumentExtender because they subtype
    ATDocument. Here we add only the extra fields.>>

    Only if the document extender is initialised first does this work.
    Otherwise we only get the fields defined here explicitly.
    Therefore ALL required fields are defined now. For those fields which
    do not yet have generated methods, _generateMethods is called.
    """
    _fields = [
        extended_fields_dict.get('nace').copy(),
        extended_fields_dict.get('country').copy(),
        extended_fields_dict.get('subcategory').copy(),
        extended_fields_dict.get('multilingual_thesaurus').copy(),
        extended_fields_dict.get('reindexTranslations').copy(),
        extended_fields_dict.get('osha_metadata').copy(),
        extended_fields_dict.get('isNews').copy(),
        extended_fields_dict.get('seoDescription').copy(),
        ]

    def __init__(self, context):
        self.context = context
        for f in self._fields:
            if f.getName() in ('country',):
                f.required = True

        # RA Link inherits from ATDocument. We might get a false positive,
        # so check that the accessors are really there

        fields = [field for field in self._fields if field.languageIndependent]
        not_yet_initialised = list()
        for field in fields:
            if not getattr(context, field.accessor, None):
                not_yet_initialised.append(field)

        if not_yet_initialised:
            self._generateMethods(context, fields=not_yet_initialised,
                                  initialized=False)


class WhoswhoExtender(OSHASchemaExtender):
    """ Add required fields for whoswho
    """
    _fields = [
        extended_fields_dict.get('country').copy(),
        extended_fields_dict.get('osha_metadata').copy(),
        extended_fields_dict.get('reindexTranslations').copy(),
        extended_fields_dict.get('seoDescription').copy(),
        ]

    def __init__(self, context):
        self.context = context

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
        extended_fields_dict.get('osha_metadata').copy(),
        extended_fields_dict.get('isNews').copy(),
        extended_fields_dict.get('seoDescription').copy(),

        ReferencedContentField('referenced_content',
            languageIndependent=True,
            multiValued=True,
            relationship='referenced_content',
            allowed_types=('Document', 'RichDocument'),
            mutator='setReferenced_content',
            accessor='getReferenced_content',
            widget=ReferenceBrowserWidget(
                label=_(u'referenced_content_label',
                    default=u'Referenced content'),
                description=_(
                    u'referenced_content_description',
                    default=u'Select one or more content items. Their ' \
                        u'body text will be displayed as part of the ' \
                        u'press release.'),
                allow_search=True,
                allow_browse=False,
                base_query=dict(path=dict(
                    query='textpieces', level=-1),
                    Language=['en', '']),
                show_results_without_query=True,
                ),
        ),

        ReferencedContentField('relatedLinks',
            languageIndependent=True,
            multiValued=True,
            relationship='relatedLinks',
            mutator='setRelatedLinks',
            accessor='getRelatedLinks',
            referencesSortable=True,
            widget=ReferenceBrowserWidget(
                label=_(u'relatedLinks_label', default=u'Links'),
                description=_(
                    u'relatedLinks_description',
                    default=u'Select related content. Links will be ' \
                        u'displayed as part of the press release.'),
                allow_search=True,
                allow_browse=True,
                allow_sorting=True,
                force_close_on_insert=True
                ),
        ),

        ReferencedContentField('notesToEditors',
            languageIndependent=True,
            multiValued=True,
            relationship='notesToEditors',
            allowed_types=('Document', 'RichDocument'),
            mutator='setNotesToEditors',
            accessor='getNotesToEditors',
            widget=ReferenceBrowserWidget(
                label=_(u'notesToEditors_label', default=u'Notes to editors'),
                description=_(
                    u'notesToEditors_description',
                    default=u'Select one or more notes to editors. Their ' \
                        u'body text will be displayed as part of the ' \
                        u'press release.'),
                allow_search=True,
                allow_browse=False,
                base_query=dict(path=dict(
                    query='notes-to-editors', level=-1),
                    Language=['en', '']),
                show_results_without_query=True,
                ),
        ),

        SEBooleanField(
            'showContacts',
            default=True,
            languageIndependent=False,
            widget=atapi.BooleanWidget(
                label=_(u'showContacts_label', default=u'Show contacts?'),
                description=_(u'showContacts_description',
                    default=u'Select this if you want to show contact info ' \
                            u'at the end of the press release (you can ' \
                            u'edit contacts on Press Room edit form)'),
                visible={'edit': 'visible', 'view': 'invisible'},
                condition="python:object.isCanonical()",
            ),
        )

    ]


class PressRoomExtender(OSHASchemaExtender):
    _fields = [
        extended_fields_dict.get('seoDescription').copy(),

        SETextField(
            'contacts',
            required=False,
            searchable=True,
            primary=False,
            languageIndependent=False,
            # XXX: adding accessor/mutator methods doesn't seem to work
            # for this field?
            # mutator='setContacts',
            # accessor='getContacts',
            storage=atapi.AnnotationStorage(migrate=True),
            validators=('isTidyHtmlWithCleanup',),
            default_output_type='text/x-html-safe',
            widget=atapi.RichWidget(
                description=(
                    u'Global contacts for all Press Releases. They will be'
                    ' appended at the end of Press Relase page.'),
                label=_(u'label_contacts', default=u'Contacts'),
                rows=15,
                allow_file_upload=zconf.ATDocument.allow_document_upload),
        )
    ]


class FileContentExtender(OSHASchemaExtender):
    _fields = [
        extended_fields_dict.get('isNews').copy(),
        extended_fields_dict.get('country').copy(),
        extended_fields_dict.get('subcategory').copy(),
        extended_fields_dict.get('multilingual_thesaurus').copy(),
        extended_fields_dict.get('nace').copy(),
        extended_fields_dict.get('reindexTranslations').copy(),
        extended_fields_dict.get('osha_metadata').copy(),
        extended_fields_dict.get('seoDescription').copy(),
        ]

    def __init__(self, context):
        super(FileContentExtender, self).__init__(context)

        # NOTE!
        # The inline tree widget for FileContent is disabled for the moment.
        # Gorka requires the quick-search function, which this widget does
        # not have. See https://syslab.com/proj/issues/show/1293

        # from Products.ATVocabularyManager.namedvocabulary import NamedVocabulary
        # from slc.treecategories.widgets.widgets import InlineTreeWidget

        # for field in self._fields:
        #     if field.__name__ in ['subcategory','multilingual_thesaurus',
        #                           'nace']:
        #         vocabulary = NamedVocabulary(field.widget.vocabulary)
        #         widget_args = {}
        #         for arg in ('label', 'description', 'label_msgid',
        #                     'description_msgid, i18n_domain'):
        #             widget_args[arg] = getattr(field.widget, arg, '')
        #         widget_args['vocabulary'] = field.widget.vocabulary
        #         field.vocabulary = vocabulary
        #         if InlineTreeWidget:
        #             field.widget = InlineTreeWidget(**widget_args)

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


# class OshaMetadataExtender(OSHASchemaExtender):
#     """ This is a general content agnostic extender.
#
#         For details, please see the description in the LinkListExtender.
#
#         NB!!!
#         The OshaMetadataExtender used to be in use, set via a local site
#         manager.
#         This made indexing the osha_metadata field impossible, since in the
#         context of the catalog, no object has this field (= the catalog is
#         outside of the LSM's context).
#         Therefore, this field is being set via o global extender again,
#         but we use CSS to hide it eveywhery we don't want it
#     """
#     _fields = [
#         extended_fields_dict.get('osha_metadata').copy(),
#         ]
#
#     def __init__(self, context):
#         self.context = context
#         # make sure _generateMethods is also called on derived content types
#         initialized = True
#         fields = [field for field in self._fields if
#                    field.languageIndependent]
#         for field in fields:
#             if not getattr(context, field.accessor, None):
#                 initialized = False
#                 break
#
#         self._generateMethods(context, self._fields, initialized,
#             marker=LANGUAGE_INDEPENDENT_INITIALIZED + 'osha_metadata')


class ProviderModifier(object):
    """ This is a schema modifier, not extender.
    """
    zope.interface.implements(
                        ISchemaModifier,
                        IBrowserLayerAwareExtender
                        )
    layer = IOSHACommentsLayer

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
                field.widget.visible = {
                    'edit': 'invisible',
                    'view': 'invisible'
                }
                schema[name] = field

        for name in moveToDefault:
            if schema.get(name):
                schema.changeSchemataForField(name, 'default')

        # we used to hide the language field (unwanted), now we just move
        # it the settings tab
        schema.changeSchemataForField('language', 'settings')

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
    zope.interface.implements(
                        ISchemaModifier,
                        IBrowserLayerAwareExtender
                        )
    layer = IOSHACommentsLayer

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

        schema.changeSchemataForField('location', 'categorization')
        portal_type = self.context.portal_type
        ordered_fields = \
            config.EXTENDED_TYPES_DEFAULT_FIELDS.get(portal_type, {}).keys()

        for name in ordered_fields:
            position = ordered_fields.index(name)
            schema.moveField(name, pos=position)


class FAQModifier(object):
    """ This is a schema modifier, not extender.
    """
    zope.interface.implements(ISchemaModifier)

    def __init__(self, context):
        self.context = context

    def fiddle(self, schema):
        """Fiddle the schema.
        """
        if self.context.portal_type != 'HelpCenterFAQ':
            return

        subject = schema['subject'].copy()
        subject.widget.visible['edit'] = 'invisible'
        schema['subject'] = subject


class SeminarModifier(object):
    """ This is a schema modifier, not extender.
    """
    zope.interface.implements(ISchemaModifier)

    def __init__(self, context):
        self.context = context

    def fiddle(self, schema):
        """Fiddle the schema.
        """
        if self.context.portal_type not in ('SPSeminar', 'SPSpeech'):
            return

        attachment = schema['attachment'].copy()
        attachment.widget.visible['edit'] = 'invisible'
        schema['attachment'] = attachment


class PressReleaseModifier(object):
    """ This is a schema modifier, not extender.
    """
    zope.interface.implements(ISchemaModifier)

    def __init__(self, context):
        self.context = context

    def fiddle(self, schema):
        """Fiddle the schema.
        """
        if self.context.portal_type != 'PressRelease':
            return

        subhead = schema['subhead'].copy()
        subhead.languageIndependent = False
        schema['subhead'] = subhead

        release_contacts = schema['releaseContacts'].copy()
        release_contacts.widget.visible['edit'] = 'invisible'
        release_contacts.widget.visible['view'] = 'invisible'
        schema['releaseContacts'] = release_contacts
