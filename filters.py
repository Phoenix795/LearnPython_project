B_CLSD_LOW_NEC_EFV = 'project = JRASERVER AND issuetype = Bug AND status = Closed AND priority = Low and component is not EMPTY and fixVersion is EMPTY'
B_CLSD_LOW_NEC_NEFV = 'project = JRASERVER AND issuetype = Bug AND status = Closed AND priority = Low and component is not EMPTY and fixVersion is not EMPTY'
B_CLSD_LOW_EC = 'project = JRASERVER AND issuetype = Bug AND status = Closed AND priority = Low and component is EMPTY'
B_CLSD_MED_EC = 'project = JRASERVER AND issuetype = Bug AND status = Closed AND priority = Medium AND component is EMPTY'
B_CLSD_MED_NEC = 'project = JRASERVER AND issuetype = Bug AND status = Closed AND priority = Medium AND component is not EMPTY'
B_CLSD_HIGH = 'project = JRASERVER AND issuetype = Bug AND status = Closed AND priority in (Highest, High)'
B_NT = 'project = JRASERVER AND issuetype = Bug AND status = "Needs Triage"'
B_IN_OTHER_S = 'project = JRASERVER AND issuetype = Bug AND status in ("In Progress", "In Review", "Gathering Impact", "Long Term Backlog", "Short Term Backlog", "Waiting for Release")'
S_CLSD_EL_NEC = 'project = JRASERVER AND issuetype = Suggestion AND status = Closed AND labels is EMPTY AND component is not EMPTY'
S_CLSD_EL_EC = 'project = JRASERVER AND issuetype = Suggestion AND status = Closed AND labels is EMPTY AND component is EMPTY'
S_CLSD_NEL_EC = 'project = JRASERVER AND issuetype = Suggestion AND status = Closed AND labels is not EMPTY AND component is EMPTY'
S_CLSD_NEL_NEL = 'project = JRASERVER AND issuetype = Suggestion AND status = Closed AND labels is not EMPTY AND component is not EMPTY'
S_GI_EL = 'project = JRASERVER AND issuetype = Suggestion AND status = "Gathering Interest" and labels is EMPTY'
S_GI_NEL = 'project = JRASERVER AND issuetype = Suggestion AND status = "Gathering Interest" and labels is not EMPTY'
S_IN_OTHER_S = 'project = JRASERVER AND issuetype = Suggestion AND status in ("In Progress", Reviewing, "Under Consideration", "Future Consideration", "Not Being Considered", "Waiting for Release")'
ALL_VULNARAB ='project = JRASERVER AND issuetype = "Public Security Vulnerability"'

ALL_FILTERS = [
                B_CLSD_LOW_NEC_EFV, B_CLSD_LOW_NEC_NEFV, B_CLSD_LOW_NEC_EFV, B_CLSD_LOW_EC, 
                B_CLSD_MED_EC, B_CLSD_MED_NEC, B_CLSD_HIGH, B_NT, B_IN_OTHER_S,
                S_CLSD_EL_NEC, S_CLSD_EL_EC, S_CLSD_NEL_EC, S_CLSD_NEL_NEL,
                S_GI_EL, S_GI_NEL, S_IN_OTHER_S, ALL_VULNARAB
            ]