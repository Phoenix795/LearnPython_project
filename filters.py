CLOSED_LOW_BUGS_WITH_COMPONENTS = 'project = JRASERVER AND issuetype = Bug AND status = Closed AND priority = Low and component is not EMPTY and fixVersion is EMPTY AND created >= 2017-01-01'
CLOSED_LOW_BUGS_WITH_COMPONENTS_AND_FIXES = 'project = JRASERVER AND issuetype = Bug AND status = Closed AND priority = Low and component is not EMPTY and fixVersion is not EMPTY AND created >= 2017-01-01'
CLOSED_LOW_BUGS = 'project = JRASERVER AND issuetype = Bug AND status = Closed AND priority = Low and component is EMPTY AND created >= 2017-01-01'
CLOSED_MEDIUM_BUGS = 'project = JRASERVER AND issuetype = Bug AND status = Closed AND priority = Medium AND component is EMPTY AND created >= 2017-01-01'
CLOSED_MEDIUM_BUGS_WITH_COMPONENTS = 'project = JRASERVER AND issuetype = Bug AND status = Closed AND priority = Medium AND component is not EMPTY AND created >= 2017-01-01'
CLOSED_HIGH_BUGS = 'project = JRASERVER AND issuetype = Bug AND status = Closed AND priority in (Highest, High) AND created >= 2017-01-01'
NEEDS_TRIAGE_BUGS = 'project = JRASERVER AND issuetype = Bug AND status = "Needs Triage" AND created >= 2017-01-01'
OTHERS_BUGS = 'project = JRASERVER AND issuetype = Bug AND status in ("In Progress", "In Review", "Gathering Impact", "Long Term Backlog", "Short Term Backlog", "Waiting for Release") AND created >= 2017-01-01'
CLOSED_SUGGESTIONS_WITH_COMPONENTS = 'project = JRASERVER AND issuetype = Suggestion AND status = Closed AND labels is EMPTY AND component is not EMPTY AND created >= 2017-01-01'
CLOSED_SUGGESTIONS = 'project = JRASERVER AND issuetype = Suggestion AND status = Closed AND labels is EMPTY AND component is EMPTY AND created >= 2017-01-01'
CLOSED_SUGGESTIONS_WITH_LABELS = 'project = JRASERVER AND issuetype = Suggestion AND status = Closed AND labels is not EMPTY AND component is EMPTY AND created >= 2017-01-01'
CLOSED_SUGGESTIONS_WITH_LABELS_AND_COMPONENTS = 'project = JRASERVER AND issuetype = Suggestion AND status = Closed AND labels is not EMPTY AND component is not EMPTY AND created >= 2017-01-01'
GATHERING_INTERESTS_SUGGESTIONS = 'project = JRASERVER AND issuetype = Suggestion AND status = "Gathering Interest" and labels is EMPTY AND created >= 2017-01-01'
GATHERING_INTERESTS_SUGGESTIONS_WITH_LABLES = 'project = JRASERVER AND issuetype = Suggestion AND status = "Gathering Interest" and labels is not EMPTY AND created >= 2017-01-01'
OTHERS_SUGGESTIONS = 'project = JRASERVER AND issuetype = Suggestion AND status in ("In Progress", Reviewing, "Under Consideration", "Future Consideration", "Not Being Considered", "Waiting for Release") AND created >= 2017-01-01'
VULNERABILITIES ='project = JRASERVER AND issuetype = "Public Security Vulnerability" AND created >= 2017-01-01'

ALL_FILTERS = [ 
                CLOSED_LOW_BUGS_WITH_COMPONENTS, CLOSED_LOW_BUGS_WITH_COMPONENTS_AND_FIXES, CLOSED_LOW_BUGS, 
                CLOSED_MEDIUM_BUGS, CLOSED_MEDIUM_BUGS_WITH_COMPONENTS, CLOSED_HIGH_BUGS, NEEDS_TRIAGE_BUGS, 
                OTHERS_BUGS, CLOSED_SUGGESTIONS_WITH_COMPONENTS, CLOSED_SUGGESTIONS, CLOSED_SUGGESTIONS_WITH_LABELS, 
                CLOSED_SUGGESTIONS_WITH_LABELS_AND_COMPONENTS, GATHERING_INTERESTS_SUGGESTIONS,
                GATHERING_INTERESTS_SUGGESTIONS_WITH_LABLES, OTHERS_SUGGESTIONS, VULNERABILITIES
                ]
