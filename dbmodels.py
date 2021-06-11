from sqlalchemy import Column, Integer, String, Date, VARCHAR, ForeignKey
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
    type_id = Column(Integer, ForeignKey('type.id'), nullable=False)
    summary = Column(String(255), nullable=False)
    status_id = Column(Integer, ForeignKey('status.id'), nullable=False)
    priority_id = Column(Integer, ForeignKey('priority.id'))
    resolution_id = Column(Integer, ForeignKey('resolution.id'))
    description = Column(String(10000))
    votes_quantity = Column(Integer,default=0)
    watchers_quantity = Column(Integer,default=0)
    fixed_version = Column(String(255))
    affected_version = Column(String(255))
    created_date = Column(Date, nullable=false)
    updated_date = Column(Date, nullable=false)

    def __repr__(self) -> str:
        return f"Issue Key {self.id}, {self.key}"


class Comment(Base):
    __tablename__ = "comment"

    id = Column(Integer, primary_key=True)
    issue_id = Column(Integer, ForeignKey('issue.id'), nullable=False)
    content = Column(String(500))
    date_created = Column(Date, nullable=False)
    creator = Column(String(255))

    def __repr__(self) -> str:
        return f"Comment id {self.id}"


class IssueLinks(Base):
    __tablename__ = "issue_link"

    id = Column(Integer, primary_key=True)
    child_issue= Column(Integer, ForeignKey('issue.id'), nullable=False)
    parent_issue = Column(Integer, ForeignKey('issue.id'), nullable=False)
    type_id = Column(Integer, ForeignKey('link_type.id'), nullable=False)

    def __repr__(self) -> str:
        return f"Issue_link id {self.id}" 


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)