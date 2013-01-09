from Products.Archetypes.utils import OrderedDict

fdict = {
    "PressRelease": OrderedDict(),
    'Event': OrderedDict(),
    'Link': OrderedDict(),
    "ATFile": OrderedDict(),
    "Image": OrderedDict(),
    "Document": OrderedDict(),
    "RichDocument": OrderedDict(),
    "News Item": OrderedDict(),
    # "RALink": OrderedDict(),
    # 'CaseStudy': OrderedDict(),
    "OSH_Link": OrderedDict(),
    "PressRoom": OrderedDict(),
    "Provider": OrderedDict(),
    'HelpCenterFAQ': OrderedDict(),
    'SPSpeechVenue': OrderedDict(),
    'SPSpeaker': OrderedDict(),
    'whoswho': OrderedDict()
}
# See Products/Archetypes/BaseObject.py for default 'id' and 'title'

# fdict['CaseStudy']['id']  = {'view': 'invisible'}
# fdict['CaseStudy']['title'] = {'view': 'invisible'}
# fdict['CaseStudy']['description'] = {'edit': False, 'view': True}   # FIXME
# fdict['CaseStudy']['seoDescription'] = {'edit': 'visible', 'view': 'invisible'}
# fdict['CaseStudy']['isNews'] = {'edit': 'visible', 'view': 'visible'}
# fdict['CaseStudy']['external_link'] = {'edit': 'invisible', 'view': 'invisible'}
# fdict['CaseStudy']['text']  = {'edit': 'visible', 'view': 'visible'}
# fdict['CaseStudy']['displayImages'] = {
#     'edit': 'invisible', 'view': 'invisible'}
# fdict['CaseStudy']['action'] = {'edit': 'visible', 'view': 'visible'}
# fdict['CaseStudy']['results']  = {'edit': 'visible', 'view': 'visible'}
# fdict['CaseStudy']['publication_year'] = {'edit': 'visible', 'view': 'visible'}
# fdict['CaseStudy']['organisation'] = {'edit': 'visible', 'view': 'visible'}
# fdict['CaseStudy']['remoteLanguage'] = {'edit': 'visible', 'view': 'visible'}
# fdict['CaseStudy']['remoteUrl']  = {'edit': 'visible', 'view': 'visible'}
# fdict['CaseStudy']['displayAttachments'] = {
#     'edit': 'visible', 'view': 'visible'}
# fdict['CaseStudy']['relatedItems'] = {'edit': 'invisible', 'view': 'invisible'}
# fdict['CaseStudy']['location'] = {'edit': 'invisible', 'view': 'invisible'}
# fdict['CaseStudy']['subject']  = {'edit': 'invisible', 'view': 'invisible'}
# fdict['CaseStudy']['nace']  = {'edit': 'visible', 'view': 'visible'}
# fdict['CaseStudy']['country']  = {'edit': 'visible', 'view': 'visible'}
# fdict['CaseStudy']['subcategory'] = {'edit': 'visible', 'view': 'visible'}
# fdict['CaseStudy']['multilingual_thesaurus'] = {
#     'edit': 'visible', 'view': 'visible'}
# fdict['CaseStudy']['reindexTranslations'] = {
#     'edit': 'visible', 'view': 'invisible'}
# fdict['CaseStudy']['osha_metadata']  = {'edit': 'visible', 'view': 'visible'}


fdict['Event']['id']  = {'view': 'invisible'}
fdict['Event']['title'] = {'view': 'invisible'}
fdict['Event']['description']  = {'edit': 'visible', 'view': 'visible'}
fdict['Event']['seoDescription'] = {'edit': 'visible', 'view': 'invisible'}
fdict['Event']['isNews']  = {'edit': 'visible', 'view': 'visible'}
fdict['Event']['startDate'] = {'edit': 'visible', 'view': 'visible'}
fdict['Event']['endDate'] = {'edit': 'visible', 'view': 'visible'}
fdict['Event']['dateToBeConfirmed']  = {'edit': 'visible', 'view': 'invisible'}
fdict['Event']['text']  = {'edit': 'visible', 'view': 'visible'}
fdict['Event']['attendees'] = {'edit': 'visible', 'view': 'visible'}
fdict['Event']['eventUrl']  = {'edit': 'visible', 'view': 'visible'}
fdict['Event']['contactName']  = {'edit': 'visible', 'view': 'visible'}
fdict['Event']['contactEmail'] = {'edit': 'visible', 'view': 'visible'}
fdict['Event']['contactPhone'] = {'edit': 'visible', 'view': 'visible'}
fdict['Event']['subcategory']  = {'edit': 'visible', 'view': 'visible'}
fdict['Event']['multilingual_thesaurus'] = {
    'edit': 'visible', 'view': 'visible'}
fdict['Event']['attachment'] = {'edit': 'visible', 'view': 'visible'}
fdict['Event']['reindexTranslations'] = {
    'edit': 'visible', 'view': 'invisible'}
fdict['Event']['osha_metadata']  = {'edit': 'visible', 'view': 'visible'}

fdict['Link']['id'] = {'view': 'invisible'}
fdict['Link']['title']  = {'view': 'invisible'}
fdict['Link']['description'] = {'edit': 'visible', 'view': 'visible'}
fdict['Link']['seoDescription']  = {'edit': 'visible', 'view': 'invisible'}
fdict['Link']['isNews'] = {'edit': 'visible', 'view': 'visible'}
fdict['Link']['remoteUrl']  = {'edit': 'visible', 'view': 'visible'}
fdict['Link']['country']  = {'edit': 'visible', 'view': 'visible'}
fdict['Link']['subcategory'] = {'edit': 'visible', 'view': 'visible'}
fdict['Link']['multilingual_thesaurus'] = {
    'edit': 'visible', 'view': 'visible'}
fdict['Link']['nace'] = {'edit': 'visible', 'view': 'visible'}
fdict['Link']['reindexTranslations'] = {'edit': 'visible', 'view': 'invisible'}
fdict['Link']['osha_metadata'] = {'edit': 'visible', 'view': 'visible'}

fdict['ATFile']['id'] = {'view': 'invisible'}
fdict['ATFile']['title']  = {'view': 'invisible'}
fdict['ATFile']['description'] = {'edit': 'visible', 'view': 'visible'}
fdict['ATFile']['seoDescription'] = {'edit': 'visible', 'view': 'invisible'}
fdict['ATFile']['isNews'] = {'edit': 'visible', 'view': 'visible'}
fdict['ATFile']['country']  = {'edit': 'visible', 'view': 'visible'}
fdict['ATFile']['subcategory'] = {'edit': 'visible', 'view': 'visible'}
fdict['ATFile']['multilingual_thesaurus'] = {
    'edit': 'visible', 'view': 'visible'}
fdict['ATFile']['nace'] = {'edit': 'visible', 'view': 'visible'}
fdict['ATFile']['reindexTranslations'] = {
    'edit': 'visible', 'view': 'invisible'}
fdict['ATFile']['file'] = {'edit': 'visible', 'view': 'visible'}
fdict['ATFile']['osha_metadata'] = {'edit': 'visible', 'view': 'visible'}

fdict['Image']['id']  = {'view': 'invisible'}
fdict['Image']['title'] = {'view': 'invisible'}
fdict['Image']['description']  = {'edit': 'visible', 'view': 'visible'}
fdict['Image']['seoDescription'] = {'edit': 'visible', 'view': 'invisible'}
fdict['Image']['isNews']  = {'edit': 'visible', 'view': 'visible'}
fdict['Image']['country'] = {'edit': 'visible', 'view': 'visible'}
fdict['Image']['subcategory']  = {'edit': 'visible', 'view': 'visible'}
fdict['Image']['multilingual_thesaurus'] = {
    'edit': 'visible', 'view': 'visible'}
fdict['Image']['nace']  = {'edit': 'visible', 'view': 'visible'}
fdict['Image']['reindexTranslations'] = {
    'edit': 'visible', 'view': 'invisible'}
fdict['Image']['image'] = {'edit': 'visible', 'view': 'visible'}
fdict['Image']['osha_metadata'] = {'edit': 'visible', 'view': 'visible'}

fdict['Document']['id'] = {'view': 'invisible'}
fdict['Document']['title']  = {'view': 'invisible'}
fdict['Document']['description'] = {'edit': 'visible', 'view': 'visible'}
fdict['Document']['seoDescription']  = {'edit': 'visible', 'view': 'invisible'}
fdict['Document']['text'] = {'edit': 'visible', 'view': 'visible'}
fdict['Document']['country'] = {'edit': 'visible', 'view': 'visible'}
fdict['Document']['multilingual_thesaurus'] = {
    'edit': 'visible', 'view': 'visible'}
fdict['Document']['nace'] = {'edit': 'visible', 'view': 'visible'}
fdict['Document']['reindexTranslations'] = {
    'edit': 'visible', 'view': 'invisible'}
fdict['Document']['osha_metadata'] = {'edit': 'visible', 'view': 'visible'}
fdict['Document']['subcategory']  = {'edit': 'invisible', 'view': 'invisible'}
fdict['Document']['isNews']  = {'edit': 'invisible', 'view': 'invisible'}
fdict['Document']['external_link']  = {'edit': 'invisible', 'view': 'invisible'}


fdict['RichDocument']['id'] = {'view': 'invisible'}
fdict['RichDocument']['title'] = {'view': 'invisible'}
fdict['RichDocument']['description'] = {'edit': 'visible', 'view': 'visible'}
fdict['RichDocument']['seoDescription'] = {
    'edit': 'visible', 'view': 'invisible'}
fdict['RichDocument']['text']  = {'edit': 'visible', 'view': 'visible'}
fdict['RichDocument']['displayImages'] = {'edit': 'visible', 'view': 'visible'}
fdict['RichDocument']['displayAttachments'] = {
    'edit': 'visible', 'view': 'visible'}
fdict['RichDocument']['country'] = {'edit': 'visible', 'view': 'visible'}
fdict['RichDocument']['multilingual_thesaurus'] = {
    'edit': 'visible', 'view': 'visible'}
fdict['RichDocument']['nace']  = {'edit': 'visible', 'view': 'visible'}
fdict['RichDocument']['reindexTranslations'] = {
    'edit': 'visible', 'view': 'invisible'}
fdict['RichDocument']['osha_metadata'] = {'edit': 'visible', 'view': 'visible'}

fdict['whoswho']['id']  = {'view': 'invisible'}
fdict['whoswho']['title'] = {'view': 'invisible'}
fdict['whoswho']['description']  = {'edit': 'visible', 'view': 'visible'}
fdict['whoswho']['seoDescription'] = {'edit': 'visible', 'view': 'invisible'}
fdict['whoswho']['url'] = {'edit': 'visible', 'view': 'visible'}
fdict['whoswho']['email'] = {'edit': 'visible', 'view': 'visible'}
fdict['whoswho']['tel'] = {'edit': 'visible', 'view': 'visible'}
fdict['whoswho']['fax'] = {'edit': 'visible', 'view': 'visible'}
fdict['whoswho']['address'] = {'edit': 'visible', 'view': 'visible'}
fdict['whoswho']['targets'] = {'edit': 'visible', 'view': 'visible'}
fdict['whoswho']['activities'] = {'edit': 'visible', 'view': 'visible'}
fdict['whoswho']['sponsorUrl'] = {'edit': 'visible', 'view': 'visible'}
fdict['whoswho']['sponsorName']  = {'edit': 'visible', 'view': 'visible'}
fdict['whoswho']['relatedOrgUrl'] = {'edit': 'visible', 'view': 'visible'}
fdict['whoswho']['relatedOrgName'] = {'edit': 'visible', 'view': 'visible'}
fdict['whoswho']['description']  = {'edit': 'visible', 'view': 'visible'}
fdict['whoswho']['text']  = {'edit': 'visible', 'view': 'visible'}
fdict['whoswho']['country'] = {'edit': 'visible', 'view': 'visible'}
fdict['whoswho']['osha_metadata'] = {'edit': 'visible', 'view': 'visible'}
fdict['whoswho']['reindexTranslations'] = {
    'edit': 'visible', 'view': 'invisible'}


fdict['News Item']['id']  = {'view': 'invisible'}
fdict['News Item']['title'] = {'view': 'invisible'}
fdict['News Item']['description'] = {'edit': 'visible', 'view': 'visible'}
fdict['News Item']['seoDescription'] = {'edit': 'visible', 'view': 'invisible'}
fdict['News Item']['text']  = {'edit': 'visible', 'view': 'visible'}
fdict['News Item']['image'] = {'edit': 'visible', 'view': 'visible'}
fdict['News Item']['imageCaption'] = {'edit': 'visible', 'view': 'visible'}
fdict['News Item']['country'] = {'edit': 'visible', 'view': 'visible'}
fdict['News Item']['multilingual_thesaurus'] = {
    'edit': 'visible', 'view': 'visible'}
fdict['News Item']['isNews'] = {'edit': 'invisible', 'view': 'invisible'}
fdict['News Item']['nace']  = {'edit': 'visible', 'view': 'visible'}
fdict['News Item']['reindexTranslations'] = {
    'edit': 'visible', 'view': 'invisible'}
fdict['News Item']['osha_metadata'] = {'edit': 'visible', 'view': 'visible'}
fdict['News Item']['external_link'] = {'edit': 'invisible', 'view': 'invisible'}
fdict['News Item']['subcategory'] = {'edit': 'invisible', 'view': 'invisible'}

# fdict['RALink']['id'] = {'view': 'invisible'}
# fdict['RALink']['title']  = {'edit': 'visible', 'view': 'visible'}
# fdict['RALink']['description'] = {'edit': 'visible', 'view': 'visible'}
# fdict['RALink']['seoDescription'] = {'edit': 'visible', 'view': 'invisible'}
# fdict['RALink']['isNews'] = {'edit': 'visible', 'view': 'visible'}
# fdict['RALink']['external_link'] = {'edit': 'invisible', 'view': 'invisible'}
# fdict['RALink']['text'] = 0  # FIXME
# fdict['RALink']['remoteUrl'] = {'edit': 'visible', 'view': 'visible'}
# fdict['RALink']['remoteLanguage'] = {'edit': 'visible', 'view': 'visible'}
# fdict['RALink']['country']  = {'edit': 'visible', 'view': 'visible'}
# fdict['RALink']['remoteProvider'] = {'edit': 'visible', 'view': 'visible'}
# fdict['RALink']['subcategory'] = {'edit': 'visible', 'view': 'visible'}
# fdict['RALink']['multilingual_thesaurus'] = {
#     'edit': 'visible', 'view': 'visible'}
# fdict['RALink']['nace'] = {'edit': 'visible', 'view': 'visible'}
# fdict['RALink']['dateOfEditing'] = {'edit': 'visible', 'view': 'visible'}
# fdict['RALink']['occupation']  = {'edit': 'visible', 'view': 'visible'}
# fdict['RALink']['ra_contents'] = {'edit': 'visible', 'view': 'visible'}
# fdict['RALink']['type_methodology']  = {'edit': 'visible', 'view': 'visible'}
# fdict['RALink']['subject']  = {'edit': 'invisible', 'view': 'invisible'}
# fdict['RALink']['allowDiscussion'] = {'edit': 'invisible', 'view': 'invisible'}
# fdict['RALink']['excludeFromNav'] = {'edit': 'invisible', 'view': 'invisible'}
# fdict['RALink']['tableContents'] = {'edit': 'invisible', 'view': 'invisible'}
# fdict['RALink']['presentation']  = {'edit': 'invisible', 'view': 'invisible'}
# fdict['RALink']['relatedItems']  = {'edit': 'invisible', 'view': 'invisible'}
# fdict['RALink']['location'] = {'edit': 'invisible', 'view': 'invisible'}
# fdict['RALink']['reindexTranslations'] = {
#     'edit': 'visible', 'view': 'invisible'}
# fdict['RALink']['osha_metadata'] = {'edit': 'visible', 'view': 'visible'}

fdict['OSH_Link']['id'] = {'view': 'invisible'}
fdict['OSH_Link']['title']  = {'view': 'invisible'}
fdict['OSH_Link']['description'] = {
    'edit': 'invisible', 'view': 'invisible'}  # FIXME
fdict['OSH_Link']['seoDescription']  = {'edit': 'visible', 'view': 'invisible'}
fdict['OSH_Link']['isNews'] = {'edit': 'visible', 'view': 'visible'}
fdict['OSH_Link']['text'] = {'edit': 'visible', 'view': 'visible'}
fdict['OSH_Link']['remoteUrl'] = {'edit': 'visible', 'view': 'visible'}
fdict['OSH_Link']['provider']  = {'edit': 'visible', 'view': 'visible'}
fdict['OSH_Link']['remoteProvider']  = {'edit': 'visible', 'view': 'visible'}
fdict['OSH_Link']['remoteLanguage']  = {'edit': 'visible', 'view': 'visible'}
fdict['OSH_Link']['country'] = {'edit': 'visible', 'view': 'visible'}
fdict['OSH_Link']['subcategory'] = {'edit': 'visible', 'view': 'visible'}
fdict['OSH_Link']['multilingual_thesaurus'] = {
    'edit': 'visible', 'view': 'visible'}
fdict['OSH_Link']['nace'] = {'edit': 'visible', 'view': 'visible'}
fdict['OSH_Link']['cas']  = {'edit': 'visible', 'view': 'visible'}
fdict['OSH_Link']['einecs'] = {'edit': 'visible', 'view': 'visible'}
fdict['OSH_Link']['general_comments']  = {'edit': 'visible', 'view': 'visible'}
fdict['OSH_Link']['author'] = {'edit': 'visible', 'view': 'visible'}
fdict['OSH_Link']['printref']  = {'edit': 'visible', 'view': 'visible'}
fdict['OSH_Link']['organisation_name'] = {'edit': 'visible', 'view': 'visible'}
fdict['OSH_Link']['isbn_d'] = {'edit': 'visible', 'view': 'visible'}
fdict['OSH_Link']['publication_date']  = {'edit': 'visible', 'view': 'visible'}
fdict['OSH_Link']['relatedItems'] = {'edit': 'invisible', 'view': 'invisible'}
fdict['OSH_Link']['location'] = {'edit': 'invisible', 'view': 'invisible'}
fdict['OSH_Link']['excludeFromNav'] = {
    'edit': 'invisible', 'view': 'invisible'}
fdict['OSH_Link']['tableContents'] = {'edit': 'invisible', 'view': 'invisible'}
fdict['OSH_Link']['presentation'] = {'edit': 'invisible', 'view': 'invisible'}
fdict['OSH_Link']['allowDiscussion'] = {
    'edit': 'invisible', 'view': 'invisible'}
fdict['OSH_Link']['effectiveDate'] = {'edit': 'invisible', 'view': 'invisible'}
fdict['OSH_Link']['expirationDate']  = {'edit': 'visible', 'view': 'visible'}
fdict['OSH_Link']['osha_metadata'] = {'edit': 'visible', 'view': 'visible'}

fdict['PressRelease']['id'] = {'view': 'invisible'}
fdict['PressRelease']['releaseTiming'] = {'edit': 'visible', 'view': 'visible'}
fdict['PressRelease']['title'] = {'view': 'invisible'}
fdict['PressRelease']['subhead'] = {'edit': 'visible', 'view': 'visible'}
fdict['PressRelease']['releaseDate'] = {'edit': 'visible', 'view': 'visible'}
fdict['PressRelease']['description'] = {'edit': 'visible', 'view': 'visible'}
fdict['PressRelease']['seoDescription'] = {
    'edit': 'visible', 'view': 'invisible'}
fdict['PressRelease']['text'] = {'edit': 'visible', 'view': 'visible'}
fdict['PressRelease']['image'] = {'edit': 'visible', 'view': 'visible'}
fdict['PressRelease']['imageCaption'] = {'edit': 'visible', 'view': 'visible'}
fdict['PressRelease']['releaseContacts'] = {
    'edit': 'invisible', 'view': 'invisible'}
fdict['PressRelease']['referenced_content'] = {
    'edit': 'invisible', 'view': 'invisible'}
fdict['PressRelease']['relatedLinks'] = {
    'edit': 'visible', 'view': 'visible'}
fdict['PressRelease']['notesToEditors'] = {
    'edit': 'visible', 'view': 'visible'}
fdict['PressRelease']['showContacts'] = {
    'edit': 'visible', 'view': 'invisible'}
fdict['PressRelease']['isNews'] = {'edit': 'visible', 'view': 'visible'}
fdict['PressRelease']['country'] = {'edit': 'visible', 'view': 'visible'}
fdict['PressRelease']['reindexTranslations'] = {
    'edit': 'visible', 'view': 'invisible'}
fdict['PressRelease']['osha_metadata'] = {'edit': 'visible', 'view': 'visible'}

fdict['PressRoom']['id'] = {'view': 'invisible'}
fdict['PressRoom']['title'] = {'view': 'invisible'}
fdict['PressRoom']['description'] = {'edit': 'visible', 'view': 'visible'}
fdict['PressRoom']['constrainTypesMode'] = {
    'edit': 'invisible', 'view': 'invisible'}
fdict['PressRoom']['locallyAllowedTypes'] = {
    'edit': 'invisible', 'view': 'invisible'}
fdict['PressRoom']['immediatelyAddableTypes'] = {
    'edit': 'invisible', 'view': 'invisible'}
fdict['PressRoom']['show_releases'] = {'edit': 'visible', 'view': 'visible'}
fdict['PressRoom']['num_releases'] = {'edit': 'visible', 'view': 'visible'}
fdict['PressRoom']['show_clips'] = {'edit': 'visible', 'view': 'visible'}
fdict['PressRoom']['num_clips'] = {'edit': 'visible', 'view': 'visible'}
fdict['PressRoom']['show_contacts'] = {'edit': 'visible', 'view': 'visible'}
fdict['PressRoom']['contacts'] = {'edit': 'visible', 'view': 'invisible'}
fdict['PressRoom']['text'] = {'edit': 'visible', 'view': 'visible'}
fdict['PressRoom']['seoDescription'] = {
    'edit': 'visible', 'view': 'invisible'}

fdict['Provider']['id'] = {'view': 'invisible'}
fdict['Provider']['title'] = {'edit': 'visible', 'view': 'visible'}
fdict['Provider']['description'] = {'edit': 'visible', 'view': 'visible'}
fdict['Provider']['seoDescription'] = {'edit': 'visible', 'view': 'invisible'}
fdict['Provider']['remoteUrl'] = {'edit': 'visible', 'view': 'visible'}
fdict['Provider']['providerCategory']  = {'edit': 'visible', 'view': 'visible'}
fdict['Provider']['remoteLanguage'] = {'edit': 'visible', 'view': 'visible'}
fdict['Provider']['location'] = {'edit': 'visible', 'view': 'visible'}
fdict['Provider']['effectiveDate'] = {'edit': 'visible', 'view': 'visible'}
fdict['Provider']['expirationDate'] = {'edit': 'visible', 'view': 'visible'}
fdict['Provider']['country'] = {'edit': 'visible', 'view': 'visible'}
fdict['Provider']['subcategory'] = {'edit': 'visible', 'view': 'visible'}
fdict['Provider']['multilingual_thesaurus'] = {
    'edit': 'visible', 'view': 'visible'}
fdict['Provider']['nace'] = {'edit': 'visible', 'view': 'visible'}
fdict['Provider']['isNews'] = {'edit': 'visible', 'view': 'visible'}
fdict['Provider']['osha_metadata'] = {'edit': 'visible', 'view': 'visible'}

fdict['HelpCenterFAQ']['id'] = {'view': 'invisible'}
fdict['HelpCenterFAQ']['title'] = {'view': 'invisible'}
fdict['HelpCenterFAQ']['description']  = {'edit': 'visible', 'view': 'visible'}
fdict['HelpCenterFAQ']['seoDescription'] = {
    'edit': 'visible', 'view': 'invisible'}
fdict['HelpCenterFAQ']['versions'] = {'edit': 'visible', 'view': 'visible'}
fdict['HelpCenterFAQ']['sections'] = {'edit': 'visible', 'view': 'visible'}
fdict['HelpCenterFAQ']['text'] = {'edit': 'visible', 'view': 'visible'}
fdict['HelpCenterFAQ']['audiences'] = {'edit': 'visible', 'view': 'visible'}
fdict['HelpCenterFAQ']['osha_metadata'] = {
    'edit': 'visible', 'view': 'visible'}
fdict['HelpCenterFAQ']['reindexTranslations'] = {
    'edit': 'visible', 'view': 'invisible'}
fdict['HelpCenterFAQ']['country'] = {'edit': 'visible', 'view': 'visible'}
fdict['HelpCenterFAQ']['startHere'] = {'edit': 'visible', 'view': 'visible'}
fdict['HelpCenterFAQ']['subcategory'] = {'edit': 'visible', 'view': 'visible'}
fdict['HelpCenterFAQ']['nace'] = {'edit': 'visible', 'view': 'visible'}
fdict['HelpCenterFAQ']['multilingual_thesaurus'] = {
    'edit': 'visible', 'view': 'visible'}
fdict['HelpCenterFAQ']['external_link']  = {'edit': 'visible', 'view': 'visible'}

fdict['SPSpeechVenue']['id'] = {'view': 'invisible'}
fdict['SPSpeechVenue']['title'] = {'view': 'invisible'}
fdict['SPSpeechVenue']['description'] = {'edit': 'visible', 'view': 'visible'}
fdict['SPSpeechVenue']['seoDescription'] = {
    'edit': 'visible', 'view': 'invisible'}
fdict['SPSpeechVenue']['isNews'] = {'edit': 'visible', 'view': 'visible'}
fdict['SPSpeechVenue']['constrainTypesMode'] = {
    'edit': 'invisible', 'view': 'invisible'}
fdict['SPSpeechVenue']['locallyAllowedTypes'] = {
    'edit': 'invisible', 'view': 'invisible'}
fdict['SPSpeechVenue']['immediatelyAddableTypes'] = {
    'edit': 'invisible', 'view': 'invisible'}
fdict['SPSpeechVenue']['country'] = {'edit': 'visible', 'view': 'visible'}
fdict['SPSpeechVenue']['subcategory'] = {'edit': 'visible', 'view': 'visible'}
fdict['SPSpeechVenue']['multilingual_thesaurus'] = {
    'edit': 'visible', 'view': 'visible'}
fdict['SPSpeechVenue']['nace'] = {'edit': 'visible', 'view': 'visible'}
fdict['SPSpeechVenue']['osha_metadata'] = {
    'edit': 'visible', 'view': 'visible'}

fdict['SPSpeaker']['id'] = {'view': 'invisible'}
fdict['SPSpeaker']['title'] = {'edit': 'invisible', 'view': 'visible'}
fdict['SPSpeaker']['firstName'] = {'edit': 'visible', 'view': 'visible'}
fdict['SPSpeaker']['middleName'] = {'edit': 'visible', 'view': 'visible'}
fdict['SPSpeaker']['lastName'] = {'edit': 'visible', 'view': 'visible'}
fdict['SPSpeaker']['suffix'] = {'edit': 'visible', 'view': 'visible'}
fdict['SPSpeaker']['email'] = {'edit': 'visible', 'view': 'visible'}
fdict['SPSpeaker']['jobTitles']  = {'edit': 'visible', 'view': 'visible'}
fdict['SPSpeaker']['officeAddress'] = {'edit': 'visible', 'view': 'visible'}
fdict['SPSpeaker']['officeCity'] = {'edit': 'visible', 'view': 'visible'}
fdict['SPSpeaker']['officeState'] = {'edit': 'visible', 'view': 'visible'}
fdict['SPSpeaker']['officePostalCode'] = {'edit': 'visible', 'view': 'visible'}
fdict['SPSpeaker']['officePhone'] = {'edit': 'visible', 'view': 'visible'}
fdict['SPSpeaker']['image'] = {'edit': 'visible', 'view': 'visible'}
fdict['SPSpeaker']['biography'] = {'edit': 'visible', 'view': 'visible'}
fdict['SPSpeaker']['education'] = {'edit': 'visible', 'view': 'visible'}
fdict['SPSpeaker']['website'] = {'edit': 'visible', 'view': 'visible'}
fdict['SPSpeaker']['speeches'] = {'edit': 'visible', 'view': 'visible'}
fdict['SPSpeaker']['nationality']  = {'edit': 'visible', 'view': 'visible'}
fdict['SPSpeaker']['employer'] = {'edit': 'visible', 'view': 'visible'}
fdict['SPSpeaker']['socialPartnerGroup'] = {
    'edit': 'visible', 'view': 'visible'}
fdict['SPSpeaker']['expertise'] = {'edit': 'visible', 'view': 'visible'}

EXTENDED_TYPES_DEFAULT_FIELDS = fdict.copy()
