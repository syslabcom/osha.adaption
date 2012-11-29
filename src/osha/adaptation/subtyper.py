import zope.component

from p4a.subtyper import interfaces


class IAnnotatedLinkList(zope.interface.Interface):
    """ Marker interface """


class AnnotatedLinkListDescriptor(object):
    zope.interface.implements(interfaces.IPortalTypedDescriptor)
    title = u'Annotated Links'
    description = \
        u'Annotated links can be used by portlets to display additional ' \
        u'information.'
    type_interface = IAnnotatedLinkList
    for_portal_type = 'Document'
