from jira import JIRA
from datetime import datetime
import settings

jira = JIRA(server=settings.SERVER_NAME)


def get_issue_data(issuekey):
    """Getting all basic data from issue and return as a dict."""
    issue = jira.issue(issuekey, fields='summary,issuetype,status,priority,resolution,description,votes,created,updated')
    issuedata = {
        'key': issuekey,
        'type': issue.fields.issuetype.name,
        'summary': issue.fields.summary,
        'status': issue.fields.status.name,
        'priority': issue.fields.priority.name,
        'resolution': issue.fields.resolution,
        'description': issue.fields.description,
        'votes': issue.fields.votes.votes,
        'watchers': jira.watchers(issue).watchCount,
        'created': datetime.strptime(issue.fields.created, '%Y-%m-%dT%H:%M:%S.%f%z').date(),
        'updated': datetime.strptime(issue.fields.updated, '%Y-%m-%dT%H:%M:%S.%f%z').date()
    }
    return issuedata


def get_issue_links(issuekey):
    """Getting all links from issue and return as a list of dicts."""
    issue = jira.issue(issuekey, fields='issuelinks')
    links = issue.fields.issuelinks
    issue_links = [ {'linktype' : link.type.name, 'outwardIssue' : link.outwardIssue.key} for link in links if link.type.name != 'Reference']
    return issue_links


def get_issue_comments(issuekey):
    """Getting all comments from issue and return as a list of dicts."""
    issue = jira.issue(issuekey, fields='comment')
    issue_comments = []
    for comment in issue.fields.comment.comments:
        comment_content = comment.body
        comment_author = comment.author.name
        comment_date = datetime.strptime(comment.created, '%Y-%m-%dT%H:%M:%S.%f%z').date()
        issue_comments.append({'body' : comment_content, 'author' : comment_author, 'date' : comment_date})
    return issue_comments


def get_issue_version(issuekey):
    """Getting all versions from issue and return max value."""
    issue = jira.issue(issuekey, fields='fixVersions,versions')
    affects_versions = [fversion.name for fversion in issue.fields.fixVersions]
    fixed_versions = [aversion.name for aversion in issue.fields.versions]
    return {'fixed' : max(fixed_versions, default='None'), 'affected' : max(affects_versions, default='None')}
