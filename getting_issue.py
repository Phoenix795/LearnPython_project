from jira import JIRA
from datetime import datetime
import settings
import filters as fl

jira = JIRA(server=settings.SERVER_NAME)

FIELDS = 'summary,issuetype,status,priority,resolution,description,\
        votes,created,updated,issuelinks,comment,fixVersions,versions'


def multi_getattr(obj, attr, default=None):
    attributes = attr.split(".")
    for i in attributes:
        try:
            obj = getattr(obj, i)
        except AttributeError:
            if default:
                return default
            else:
                raise
    return obj


def get_issue_data(issue):
    """Getting all basic data from issue and return as a dict."""
    issuedata = {
        'key': issue.key,
        'type': issue.fields.issuetype.name,
        'summary': issue.fields.summary,
        'status': issue.fields.status.name,
        'priority': multi_getattr(issue, 'fields.priority.name','None'),
        'resolution': multi_getattr(issue, 'fields.resolution.name','None'),
        'description': multi_getattr(issue, 'fields.description', 'None'),
        'votes': issue.fields.votes.votes,
        'watchers': jira.watchers(issue).watchCount,
        'created': datetime.strptime(issue.fields.created, '%Y-%m-%dT%H:%M:%S.%f%z').date(),
        'updated': datetime.strptime(issue.fields.updated, '%Y-%m-%dT%H:%M:%S.%f%z').date(),
        'resolved': datetime.strptime(issue.fields.resolutiondate, '%Y-%m-%dT%H:%M:%S.%f%z').date() if issue.fields.resolutiondate != None else 'None',
        'comments': get_issue_comments(issue),
        'links': get_issue_links(issue),
        'versions': get_issue_version(issue)
    }
    return issuedata


def get_issue_links(issue):
    """Getting all links from issue and return as a list of dicts."""
    links = issue.fields.issuelinks
    issue_links = [ {'linktype' : link.type.name, 'outwardIssue' : multi_getattr(link, 'outwardIssue.key','None')} for link in links]
    return issue_links


def get_issue_comments(issue):
    """Getting all comments from issue and return as a list of dicts."""
    issue_comments = []
    for comment in issue.fields.comment.comments:
        comment_content = comment.body
        comment_author = comment.author.name
        comment_date = datetime.strptime(comment.created, '%Y-%m-%dT%H:%M:%S.%f%z').date()
        issue_comments.append({'body' : comment_content, 'author' : comment_author, 'date' : comment_date})
    return issue_comments


def get_issue_version(issue):
    """Getting all versions from issue and return max value."""
    affects_versions = [getattr(fversion,'name','None') for fversion in multi_getattr(issue, 'fields.fixVersions', 'None')]
    fixed_versions = [getattr(aversion,'name','None') for aversion in multi_getattr(issue, 'fields.versions', 'None')]
    return {'fixed' : max(fixed_versions, default='None'), 'affected' : max(affects_versions, default='None')}


def getting_issues_by_filter(jql):
    """Getting all issue keys from jql filter and return as a list."""
    issues = [ get_issue_data(issue) for issue in jira.search_issues(f'{jql}', maxResults=False, fields=FIELDS)]
    return issues


if __name__ == "__main__":
    for jql in fl.ALL_FILTERS:
        getting_issues_by_filter(jql)