from atlassiandb import db_session
from dbmodels import Type, Status, Priority, Resolution, Issue
import getting_issue


def get_or_create(model, name):
    instance = db_session.query(model).filter(model.name == name).first()
    if not instance:
        instance = model(name=name)
        db_session.add(instance)
        db_session.commit()
        print(instance)
    return instance


def upload_issues(issue):
    t1 = get_or_create(Type, issue['type'])
    s1 = get_or_create(Status,issue['status'])
    p1 = get_or_create(Priority, issue['priority'])
    r1 = get_or_create(Resolution, issue['resolution'])
    i1 = Issue(key = issue['key'], summary = issue['summary'], 
    type_id = t1.id, status_id = s1.id, priority_id = p1.id, resolution_id = r1.id,
    description = issue['description'], votes_quantity = issue['votes'], 
    watchers_quantity = issue['watchers'], fixed_version = issue['versions']['fixed'], 
    affected_version = issue['versions']['affected'], created_date = issue['created'], 
    updated_date = issue['updated'], resolved_date = issue['resolved'])
    db_session.add(i1)
    db_session.commit()

if __name__ == "__main__":
    for issue in getting_issue.get_issues_by_filter('project in (JSWSERVER, JRASERVER) AND issuetype in (Bug, "Public Security Vulnerability", Suggestion) AND created >= 2021-03-01 AND created <= 2021-03-10'):
        upload_issues(issue)
