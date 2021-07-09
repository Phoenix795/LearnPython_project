from jira import JIRA
from datetime import datetime
import settings
import filters as fl
import logging
import re

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='writing_issue.log')

jira = JIRA(server=settings.SERVER_NAME)

FIELDS = 'summary,issuetype,status,priority,resolution,description,\
        votes,created,updated,issuelinks,comment,fixVersions,versions, resolutiondate'


def demoji(text):
    """Clearing strings from characters unsupported by the database"""
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U00010000-\U0010ffff"
                               "]+", flags=re.UNICODE)
    return(emoji_pattern.sub(r'', text))


def nested_gettatr(obj, attr, default=None):
    """Applying several attributes to one object and return default value if attribur does not exist."""
    attributes = attr.split(".")
    for i in attributes:
        try:
            obj = getattr(obj, i)
        except AttributeError:
            return default
    return obj


def get_date_from_field(issue, attributes):
    """Getting date data from issue if exist and return as a date object."""
    value = nested_gettatr(issue, attributes)
    if value:
        return datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f%z').date()
    return None

def limit_description_size(issue):
    """Limits the number of characters in the description field"""
    description = issue.fields.description
    if description != None:
        description = demoji(description)
        if len(description) > 10000:
            return description[0:10000]
    return description


def get_issue_data(issue):
    """Getting all basic data from issue and return as a dict."""
    logging.info(f"Start reading {issue.key}!")
    issuedata = {
        'key': issue.key,
        'type': issue.fields.issuetype.name,
        'summary': demoji(issue.fields.summary),
        'status': issue.fields.status.name,
        'priority': nested_gettatr(issue, 'fields.priority.name'),
        'resolution': nested_gettatr(issue, 'fields.resolution.name'),
        'description': limit_description_size(issue),
        'votes': issue.fields.votes.votes,
        'watchers': jira.watchers(issue).watchCount,
        'created': get_date_from_field(issue,'fields.created'),
        'updated': get_date_from_field(issue, 'fields.updated'),
        'resolved': get_date_from_field(issue, 'fields.resolutiondate'),
        'comments': get_issue_comments(issue),
        'links': get_issue_links(issue),
        'versions': get_issue_version(issue)
    }
    return issuedata


def get_issue_links(issue):
    """Getting all links from issue and return as a list of dicts."""
    links = issue.fields.issuelinks
    issue_links = [ {'linktype' : link.type.name, 'outwardIssue' : nested_gettatr(link, 'outwardIssue.key','None')} for link in links]
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
    affects_versions = [getattr(aversion,'name') for aversion in nested_gettatr(issue, 'fields.fixVersions', '')]
    fixed_versions = [getattr(fversion,'name') for fversion in nested_gettatr(issue, 'fields.versions','')]
    affects_versions = filter(None, affects_versions)
    fixed_versions = filter(None, fixed_versions)
    return {'fixed' : max(fixed_versions, default=None), 'affected' : max(affects_versions, default=None)}


def get_issues_by_filter(jql):
    """Getting all issues from jql filter and return their data as a list."""
    issues = [get_issue_data(issue) for issue in jira.search_issues(f'{jql}', maxResults=False, fields=FIELDS)]
    return issues


if __name__ == "__main__":
    for jql in fl.ALL_FILTERS:
        get_issues_by_filter(jql)
