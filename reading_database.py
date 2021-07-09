from atlassiandb import db_session
from dbmodels import Type, Status, Priority, Resolution, Issue
from sqlalchemy import select, and_, or_
from sqlalchemy.sql import func
from datetime import datetime, timedelta

def count_issues_in_status():
    """Counts the number of issues in various statuses"""
    status_list = db_session.query(
        Status.name, func.count(Issue.id)
    ).join(
        Issue.status
    ).group_by(Status.name).order_by(func.count(Issue.id).desc()).all()

    return status_list


def count_issues_in_resolution():
    """Counts the number of issues in various resolutions"""
    resolutions_list = db_session.query(
        Resolution.name, func.count(Issue.id)
    ).join(
        Issue.resolution
    ).group_by(
        Resolution.name
    ).order_by(func.count(Issue.id).desc()).all()

    return resolutions_list


def most_voted_issues(issue_type, num_rows=5):
    """Most requested unresolved issues"""
    votes_list = db_session.query(
        Issue.key, Status.name, Issue.votes_quantity
    ).join(
        Issue.resolution, Issue.status, Issue.type
    ).filter(
        Resolution.name == None, Type.name == issue_type
    ).order_by(Issue.votes_quantity.desc()).limit(num_rows).all()

    return votes_list


def most_watched_issues(issue_type, num_rows=5):
    """Most tracked unresolved issues"""
    watchers_list = db_session.query(
        Issue.key, Status.name, Issue.watchers_quantity
    ).join(
        Issue.resolution, Issue.status, Issue.type
    ).filter(
        Resolution.name == None, Type.name == issue_type
    ).order_by(Issue.watchers_quantity.desc()).limit(num_rows).all()
    
    return watchers_list


def number_of_issues_with_workarounds():
    """Counts the number of unresolved issues with workarounds"""
    workaround_list = db_session.query(
        Type.name, Status.name, func.count(Issue.id)
    ).join(
        Issue.type, Issue.status, Issue.resolution
    ).filter( 
        Resolution.name == None, 
        Issue.description.ilike('%workaround%')
    ).group_by(
        Type.name, Status.name
    ).order_by(Type.name, func.count(Issue.id).desc()).all()

    return workaround_list


def potentially_abandoned_issues():
    """Counts the number of issues that most likely will not be fixed"""
    two_year_ago = datetime.today() - timedelta(days = 365*2)
    abandoned_issues = db_session.query(
        Type.name, Status.name, Priority.name, func.count(Issue.id)
    ).join(
        Issue.resolution, Issue.status, Issue.type, Issue.priority
    ).filter(
        and_(
            
            Issue.resolved_date == None, 
            Issue.created_date < two_year_ago,
            Issue.votes_quantity < 150,
            Issue.watchers_quantity < 150
        )
    ).group_by(
        Type.name, Status.name, Priority.name
    ).order_by(func.count(Issue.id).desc(), Type.name).all()

    return abandoned_issues


def distribution_of_issues_by_fixed_versions():
    """Counts the number of issues that are fixed in different versions"""
    resolved_issues = db_session.query(
        Issue.fixed_version, Type.name, func.count(Issue.id)
    ).join(
        Issue.type, Issue.resolution
    ).filter(
        and_(
            Issue.resolved_date != None,
            Issue.fixed_version != None, 
            Resolution.name.in_(['Fixed', 'Done', 'Deployed']),
        )
    ).group_by(
        Issue.fixed_version, Type.name
    ).order_by(Issue.fixed_version.desc(), func.count(Issue.id).desc()).all()

    return resolved_issues
