from jira import JIRA
from datetime import datetime

jira = JIRA(server="https://jira.atlassian.com")


#getting all basic data from issue and return as a dict
def get_issuedata(issuekey):
    issue = jira.issue(issuekey)
    issuedata = dict()
    issuedata['key'] = issuekey
    issuedata['type'] = issue.fields.issuetype
    issuedata['summary'] = issue.fields.summary
    issuedata['status'] = issue.fields.status
    issuedata['priority'] = issue.fields.priority
    issuedata['resolution'] = issue.fields.resolution
    issuedata['description'] = issue.fields.description
    issuedata['votes'] = issue.fields.votes
    issuedata['watchers'] = jira.watchers(issue).watchCount
    issuedata['created'] = datetime.strptime(issue.fields.created, '%Y-%m-%dT%H:%M:%S.%f%z').date()
    issuedata['updated'] = datetime.strptime(issue.fields.updated, '%Y-%m-%dT%H:%M:%S.%f%z').date()
    return issuedata


#getting all links from issue and return as a list of dicts
def get_issuelinks(issuekey):
    issue = jira.issue(issuekey)
    links = issue.fields.issuelinks
    issuelinks = []
    for link in links:
        linktype = link.type
        outwardIssue = link.outwardIssue
        issuelinks.append({'linktype' : linktype, 'outwardIssue' : outwardIssue})
    return issuelinks


#getting all comments from issue and return as a list of dicts
def get_issuecomments(issuekey):
    issue = jira.issue(issuekey)
    issuecomments = []
    for comment in issue.fields.comment.comments:
        comment_content = comment.body
        comment_author = comment.author
        comment_date = datetime.strptime(comment.created, '%Y-%m-%dT%H:%M:%S.%f%z').date()
        issuecomments.append({'body' : comment_content, 'author' : comment_author, 'date' : comment_date})
    return issuecomments


#getting all versions from issue and return as a dict of lists
def get_issueversion(issuekey):
    issue = jira.issue(issuekey)
    fixedversions = []
    affectsversions = []
    for fversion in issue.fields.fixVersions:
        fixedversions.append(fversion.name)
    for aversion in issue.fields.versions:
        affectsversions.append(aversion.name)
    return {'fixed' : fixedversions, 'affected' : affectsversions}