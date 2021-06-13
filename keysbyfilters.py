from jira import JIRA
import settings

jira = JIRA(server=settings.SERVER_NAME)


def getting_keys_by_filter(jql):
    """Getting all issue keys from jql filter and return as a list."""
    keys = [ issue.key for issue in jira.search_issues(f'{jql}', maxResults=False, fields='key')]
    return keys

def read_filters_file(path_to_file):
    with open(path_to_file, 'r', encoding='utf-8') as recieved_file:
        read_text = recieved_file.readlines()

    with open('keys.txt', 'w', encoding='utf-8') as file_with_keys:
        for filter in read_text:
            print(filter)
            keys = getting_keys_by_filter(filter.rstrip())
            file_with_keys.write("\n".join([",".join(keys[i:i+100]) for i in range(0,len(keys),100)]))
            file_with_keys.write("\n")


if __name__ == "__main__":
    read_filters_file('filters.txt')
