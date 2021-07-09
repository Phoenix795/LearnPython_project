import logging
from atlassiandb import db_session
from dbmodels import Type, Status, Priority, Resolution, Issue
import getting_issue
import filters as fl

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='writing_issue.log')


def get_or_create(model, name):
    """Load new value if it already exists only return object"""
    instance = db_session.query(model).filter(model.name == name).first()
    if not instance:
        instance = model(name=name)
        db_session.add(instance)
        db_session.commit()
    return instance


def upload_issues(issue):
    """Writing an issue to the database"""
    type = get_or_create(Type, issue['type'])
    status = get_or_create(Status,issue['status'])
    priority = get_or_create(Priority, issue['priority'])
    resolution = get_or_create(Resolution, issue['resolution'])
    loaded_issue = Issue(
        key=issue['key'],
        summary=issue['summary'], 
        type_id=type.id,
        status_id=status.id,
        priority_id=priority.id,
        resolution_id = resolution.id,
        description = issue['description'],
        votes_quantity = issue['votes'],
        watchers_quantity = issue['watchers'],
        fixed_version = issue['versions']['fixed'], 
        affected_version = issue['versions']['affected'],
        created_date = issue['created'], 
        updated_date = issue['updated'],
        resolved_date = issue['resolved']
        )
    db_session.add(loaded_issue)
    db_session.commit()
    


if __name__ == "__main__":
    logging.info("Process started!")
    for jql in fl.ALL_FILTERS:
        print(jql)
        for issue in getting_issue.get_issues_by_filter(jql):
            upload_issues(issue)
            logging.info(f"{issue['key']} was written into database!")
    logging.info("Process ended!")