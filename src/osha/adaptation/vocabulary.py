from zope.interface import implements

from zope.app.component.hooks import getSite

from Products.Archetypes.atapi import DisplayList
from Products.Archetypes.interfaces import IVocabulary

class AnnotatableLinkListVocabulary(object):
    """Vocabulary factory returning Section names for the AnnotatableLinkList 
       Mechanism in the Document.
    """
    implements(IVocabulary)

    display_list = [
        ("authorities", "Authorities"), 
        ("social_partners", "Social Partners"),
        ("research_organisations", "Research Organisations"), 
        ("other_national", "Other National Sites"), 
        ("more", "More Related Content"),
    ]

    def getDisplayList(self, context=None):
        """ """
        site = getSite()
        # perhaps check context for some settings, otherwise return a default
        return DisplayList(self.display_list)

    def getVocabularyDict(self, instance=None):
        """ """
        d = {}
        for i in self.display_list:
            d[i[0]] = i[1]
        return d

    def isFlat(self):
        """ returns true if the underlying vocabulary is flat, otherwise
            if its hierachical (tree-like) it returns false.
        """
        return True

    def showLeafsOnly(self):
        """ returns true for flat vocabularies. In hierachical (tree-like)
            vocabularies it defines if only leafs should be displayed, or
            knots and leafs.
        """
        return True


