CREATE TABLE "issues" (
	"id" serial NOT NULL,
	"issue_key" varchar(255) NOT NULL UNIQUE,
	"issue_type_id" integer NOT NULL,
	"summary" TEXT NOT NULL,
	"status_id" integer NOT NULL,
	"priority_id" integer NOT NULL,
	"resolution_id" integer NOT NULL,
	"description" TEXT,
	"votes_quantity" integer NOT NULL DEFAULT '0',
	"watchers_quantity" integer NOT NULL DEFAULT '0',
	"created_date" DATE NOT NULL,
	"updated_date" DATE NOT NULL,
	CONSTRAINT "issues_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Status" (
	"id" serial NOT NULL,
	"status_name" varchar(255) NOT NULL UNIQUE,
	CONSTRAINT "Status_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Priority" (
	"id" serial NOT NULL,
	"priority_name" varchar(255) NOT NULL UNIQUE,
	CONSTRAINT "Priority_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Resolution" (
	"id" serial NOT NULL,
	"resolution_name" varchar(255) NOT NULL UNIQUE,
	CONSTRAINT "Resolution_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Comments" (
	"id" serial NOT NULL,
	"issue_id" integer NOT NULL,
	"content" TEXT NOT NULL,
	"date_created" DATE NOT NULL,
	"creator" VARCHAR(255) NOT NULL,
	CONSTRAINT "Comments_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "AV_issues" (
	"id" serial NOT NULL,
	"issue_id" integer NOT NULL,
	"server_version" VARCHAR(255) NOT NULL,
	CONSTRAINT "AV_issues_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "FV_issue" (
	"id" serial NOT NULL,
	"issue_id" integer NOT NULL,
	"server_version" VARCHAR(255) NOT NULL,
	CONSTRAINT "FV_issue_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Issue_links" (
	"id" serial NOT NULL,
	"child_issue" integer NOT NULL,
	"parent_issue" integer NOT NULL,
	"link_type_id" integer NOT NULL,
	CONSTRAINT "Issue_links_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Link_type" (
	"id" serial NOT NULL,
	"link_type_name" varchar(255) NOT NULL UNIQUE,
	CONSTRAINT "Link_type_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Type" (
	"id" serial NOT NULL,
	"Issue_type_name" varchar(255) NOT NULL UNIQUE,
	CONSTRAINT "Type_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



ALTER TABLE "issues" ADD CONSTRAINT "issues_fk0" FOREIGN KEY ("issue_type_id") REFERENCES "Type"("id");
ALTER TABLE "issues" ADD CONSTRAINT "issues_fk1" FOREIGN KEY ("status_id") REFERENCES "Status"("id");
ALTER TABLE "issues" ADD CONSTRAINT "issues_fk2" FOREIGN KEY ("priority_id") REFERENCES "Priority"("id");
ALTER TABLE "issues" ADD CONSTRAINT "issues_fk3" FOREIGN KEY ("resolution_id") REFERENCES "Resolution"("id");




ALTER TABLE "Comments" ADD CONSTRAINT "Comments_fk0" FOREIGN KEY ("issue_id") REFERENCES "issues"("id");

ALTER TABLE "AV_issues" ADD CONSTRAINT "AV_issues_fk0" FOREIGN KEY ("issue_id") REFERENCES "issues"("id");

ALTER TABLE "FV_issue" ADD CONSTRAINT "FV_issue_fk0" FOREIGN KEY ("issue_id") REFERENCES "issues"("id");

ALTER TABLE "Issue_links" ADD CONSTRAINT "Issue_links_fk0" FOREIGN KEY ("child_issue") REFERENCES "issues"("id");
ALTER TABLE "Issue_links" ADD CONSTRAINT "Issue_links_fk1" FOREIGN KEY ("parent_issue") REFERENCES "issues"("id");
ALTER TABLE "Issue_links" ADD CONSTRAINT "Issue_links_fk2" FOREIGN KEY ("link_type_id") REFERENCES "Link_type"("id");



