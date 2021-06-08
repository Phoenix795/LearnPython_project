from jira import JIRA
from datetime import datetime

SERVER_NAME = "https://jira.atlassian.com"
jira = JIRA(server=SERVER_NAME)


def get_issue_data(issuekey):
    """Getting all basic data from issue and return as a dict."""
    issue = jira.issue(issuekey)
    issuedata = {
        'key': issuekey,
        'type': issue.fields.issuetype,
        'summary': issue.fields.summary,
        'status': issue.fields.status,
        'priority': issue.fields.priority,
        'resolution': issue.fields.resolution,
        'description': issue.fields.description,
        'votes': issue.fields.votes,
        'watchers': jira.watchers(issue).watchCount,
        'created': datetime.strptime(issue.fields.created, '%Y-%m-%dT%H:%M:%S.%f%z').date(),
        'updated': datetime.strptime(issue.fields.updated, '%Y-%m-%dT%H:%M:%S.%f%z').date()
    }
    return issuedata


def get_issue_links(issuekey):
    """Getting all links from issue and return as a list of dicts."""
    issue = jira.issue(issuekey)
    links = issue.fields.issuelinks
    issue_links = []
    for link in links:
        link_type = link.type
        outward_issue = link.outwardIssue
        issue_links.append({'linktype' : link_type, 'outwardIssue' : outward_issue})
    return issue_links


def get_issue_comments(issuekey):
    """Getting all comments from issue and return as a list of dicts."""
    issue = jira.issue(issuekey)
    issue_comments = []
    for comment in issue.fields.comment.comments:
        comment_content = comment.body
        comment_author = comment.author
        comment_date = datetime.strptime(comment.created, '%Y-%m-%dT%H:%M:%S.%f%z').date()
        issue_comments.append({'body' : comment_content, 'author' : comment_author, 'date' : comment_date})
    return issue_comments


def get_issue_version(issuekey):
    """Getting all versions from issue and return max value."""
    issue = jira.issue(issuekey)
    affects_versions = [fversion.name for fversion in issue.fields.fixVersions]
    fixed_versions = [aversion.name for aversion in issue.fields.versions]
    return {'fixed' : max(fixed_versions), 'affected' : max(affects_versions)}