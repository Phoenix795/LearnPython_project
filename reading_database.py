from atlassiandb import db_session
from dbmodels import Type, Status, Priority, Resolution, Issue
from sqlalchemy import select, and_, or_
from sqlalchemy.sql import func
from datetime import datetime, timedelta

def count_issues_in_status():
    """Counts the number of issues in various statuses"""
    query = db_session.query(
        Status.name, func.count(Issue.id)
    ).join(
        Issue.status
    ).group_by(Status.name).order_by(func.count(Issue.id).desc())
    
    status_list = [[status_name, issue_quantity] for status_name, issue_quantity in query]
    return status_list


def count_issues_in_resolution():
    """Counts the number of issues in various resolutions"""
    query = db_session.query(
        Resolution.name, func.count(Issue.id)
    ).join(
        Issue.resolution
    ).group_by(
        Resolution.name
    ).order_by(func.count(Issue.id).desc())
    resolutions_list = [[resolution_name, issue_quantity] for resolution_name, issue_quantity in query]
    return resolutions_list


def most_voted_issues(issue_type, num_rows=5):
    """Most requested unresolved issues"""
    query = db_session.query(
        Issue.key, Status.name, Issue.votes_quantity
    ).join(
        Issue.resolution, Issue.status, Issue.type
    ).filter(
        Resolution.name == 'None', Type.name == issue_type
    ).order_by(Issue.votes_quantity.desc()).limit(num_rows)
    votes_list = [[issue_key, status_name, issue_votes] for issue_key, status_name, issue_votes in query]
    return votes_list


def most_watched_issues(issue_type, num_rows=5):
    """Most tracked unresolved issues"""
    query = db_session.query(
        Issue.key, Status.name, Issue.watchers_quantity
    ).join(
        Issue.resolution, Issue.status, Issue.type
    ).filter(
        Resolution.name == 'None', Type.name == issue_type
    ).order_by(Issue.watchers_quantity.desc()).limit(num_rows)
    
    watchers_list = [[issue_key, status_name, issue_watchers] for issue_key, status_name, issue_watchers in query]
    return watchers_list


def number_of_issues_with_workarounds():
    """Counts the number of unresolved issues with workarounds"""
    query = db_session.query(
        Type.name, Status.name, func.count(Issue.id)
    ).join(
        Issue.type, Issue.status, Issue.resolution
    ).filter( 
        Resolution.name == 'None', 
        or_(
            Issue.description.like('%Workaround%'), Issue.description.like('%workaround%')
        )
    ).group_by(
        Type.name, Status.name
    ).order_by(Type.name, func.count(Issue.id).desc())
    workaround_list = [[type_name, status_name, issue_quantity] for type_name,status_name, issue_quantity in query]
    return workaround_list

def potentially_abandoned_issues():
    """Counts the number of issues that most likely will not be fixed"""
    two_year_ago = datetime.today() - timedelta(days = 365*2)
    query = db_session.query(
        Type.name, Status.name, Priority.name, func.count(Issue.id)
    ).join(
        Issue.resolution, Issue.status, Issue.type, Issue.priority
    ).filter(
        and_(
            
            Issue.resolved_date == None, 
            Resolution.name.in_(['Won\'t Fix', 'None', 'Timed out', 'Obsolete']),
            Issue.created_date < two_year_ago,
            Issue.votes_quantity < 150,
            Issue.watchers_quantity < 150
        )
    ).group_by(
        Type.name, Status.name, Priority.name
    ).order_by(func.count(Issue.id).desc(), Type.name)
    abandoned_issues = [[type_name, status_name, priority_name, issue_quantity] for type_name, status_name, priority_name, issue_quantity in query]
    return abandoned_issues


def distribution_of_issues_by_fixed_versions():
    """Counts the number of issues that are fixed in different versions"""
    query = db_session.query(
        Issue.fixed_version, Type.name, func.count(Issue.id)
    ).join(
        Issue.type, Issue.resolution
    ).filter(
        and_(
            Issue.fixed_version != None, 
            Resolution.name.in_(['Fixed', 'Done', 'Deployed']),
        )
    ).group_by(
        Issue.fixed_version, Type.name
    ).order_by(Issue.fixed_version.desc(), func.count(Issue.id).desc())
    resolved_issues = [[fixed_version, type_name, issue_quantity] for fixed_version, type_name, issue_quantity in query]
    return resolved_issues