from sqlalchemy import Column, Integer, String, Date, VARCHAR, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import false
from atlassiandb import Base, engine


class Type(Base):
    __tablename__ = "type"

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(255),unique=True)

    def __repr__(self) -> str:
        return f"Type name {self.id}, {self.name}"


class Status(Base):
    __tablename__ = "status"

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(255),unique=True)

    def __repr__(self) -> str:
        return f"Status name {self.id}, {self.name}"


class Priority(Base):
    __tablename__ = "priority"

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(255),unique=True)

    def __repr__(self) -> str:
        return f"Priority name {self.id}, {self.name}"


class Resolution(Base):
    __tablename__ = "resolution"

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(255),unique=True)

    def __repr__(self) -> str:
        return f"Resolution name {self.id}, {self.name}"


class LinkType(Base):
    __tablename__ = "link_type"

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(255),unique=True)

    def __repr__(self) -> str:
        return f"Link type name {self.id}, {self.name}"


class Issue(Base):
    __tablename__ = "issue"

    id = Column(Integer, primary_key=True)
    key = Column(VARCHAR(255),unique=True, nullable=False)
    summary = Column(String(255), nullable=False)

    type_id = Column(Integer, ForeignKey('type.id'), nullable=False)
    type = relationship('Type', backref='issues')
    
    status_id = Column(Integer, ForeignKey('status.id'), nullable=False)
    status = relationship('Status', backref='issues')
    
    priority_id = Column(Integer, ForeignKey('priority.id'))
    priority = relationship('Priority', backref='issues')

    resolution_id = Column(Integer, ForeignKey('resolution.id'))
    resolution = relationship('Resolution', backref='issues')

    description = Column(String(10000))
    votes_quantity = Column(Integer,default=0)
    watchers_quantity = Column(Integer,default=0)
    fixed_version = Column(String(255))
    affected_version = Column(String(255))
    created_date = Column(Date, nullable=false)
    updated_date = Column(Date, nullable=false)

    def __repr__(self) -> str:
        return f"Issue Key {self.id}, {self.key}"


class Comments(Base):
    __tablename__ = "comment"

    id = Column(Integer, primary_key=True)
    
    issue_id = Column(Integer, ForeignKey('issue.id'), nullable=False, index=True)
    issue = relationship('Issue', backref='comments', lazy=True)
    
    content = Column(String(500))
    date_created = Column(Date, nullable=False)
    creator = Column(String(255))

    def __repr__(self) -> str:
        return f"Comment id {self.id}"


class IssueLink(Base):
    __tablename__ = "issue_link"

    id = Column(Integer, primary_key=True)

    child_issue_id = Column(Integer, ForeignKey('issue.id'), nullable=False, index=True)
    child_issue = relationship('Issue', backref='issue_links', lazy=True)

    parent_issue_id = Column(Integer, ForeignKey('issue.id'), nullable=False, index=True)
    parent_issue = relationship('Issue', backref='issue_links', lazy=True)

    type_id = Column(Integer, ForeignKey('link_type.id'), nullable=False)
    type = relationship('LinkType', backref='issue_links')

    def __repr__(self) -> str: 
        return f"Issue_link id {self.id}" 


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
