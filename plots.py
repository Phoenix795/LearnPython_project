import matplotlib.pyplot as plt
import pandas as pd
import reading_database as rd
import os

PATH = 'figs'


def write_html_to_file(filename, dataframe):
    """Writing dataframe to HTML file"""
    html = dataframe.to_html(index=False)
    with open(f'{PATH}/{filename}.html', "w") as text_file:
        text_file.write(html)


def create_most_voted_suggestions_table():
    """Creating a table in html format with data on the most voted suggestions"""
    most_voted_suggestions = pd.DataFrame(
        rd.most_voted_issues('Suggestion', 10), 
        columns =['Key', 'Summary', 'Status','Created date',  'Votes_quantity']
        )
    write_html_to_file('most_voted_suggestions', most_voted_suggestions)


def create_most_voted_bugs_table(): 
    """Creating a table in html format with data on the most voted bugs"""
    most_voted_bugs = pd.DataFrame(
        rd.most_voted_issues('Bug', 10), 
        columns =['Key', 'Summary', 'Status','Created date',  'Votes_quantity']
        )
    write_html_to_file('most_voted_bugs', most_voted_bugs)


def create_most_watched_suggestions_table():
    """Creating a table in html format with data on the most watched suggestions"""
    most_watched_suggestions = pd.DataFrame(
        rd.most_watched_issues('Suggestion', 10),
        columns =['Key', 'Summary', 'Status','Created date',  'Watchers_quantity']
        )
    write_html_to_file('most_watched_suggestions', most_watched_suggestions)


def create_most_watched_bugs_table():
    """Creating a table in html format with data on the most watched bugs"""
    most_watched_bugs = pd.DataFrame(
        rd.most_watched_issues('Bug', 10),
        columns =['Key', 'Summary', 'Status','Created date',  'Watchers_quantity']
        )
    write_html_to_file('most_watched_bugs', most_watched_bugs)


def create_suggestion_in_status_pie():
    """Creating a pie chart in png format with data on the percentage suggestion statuses"""
    suggestion_in_status = pd.DataFrame(rd.count_issues_in_status('Suggestion'), columns =['Status', 'Number of issues'])
    suggestion_in_status['Percentage'] = round(
        suggestion_in_status['Number of issues'] / suggestion_in_status['Number of issues'].sum() * 100, 2
        )
    suggestion_in_status.loc[suggestion_in_status['Percentage'] < 1, 'Status'] = 'Others'
    suggestion_in_status = suggestion_in_status.groupby('Status').sum()
    pie_diagram = suggestion_in_status.plot(
        y='Number of issues',
        kind="pie",
        autopct='%1.1f%%',
        title="Statuses of Suggestions",
        figsize=(10, 10),
        legend=False
        )
    plt.ylabel('')
    pie_diagram.figure.savefig(f'{PATH}/suggestion_in_status_pie')


def create_bug_in_status_pie():
    """Creating a pie chart in png format with data on the percentage bugs statuses"""
    bug_in_status = pd.DataFrame(rd.count_issues_in_status('Bug'), columns =['Status', 'Number of issues'])
    bug_in_status['Percentage'] = round(
        bug_in_status['Number of issues'] / bug_in_status['Number of issues'].sum() * 100, 2
        )
    bug_in_status.loc[bug_in_status['Percentage'] < 1, 'Status'] = 'Others'
    bug_in_status = bug_in_status.groupby('Status').sum()
    pie_diagram = bug_in_status.plot(
        y='Number of issues',
        kind="pie",
        autopct='%1.1f%%',
        title="Statuses of Bugs",
        figsize=(10, 10),
        legend=False
        )
    plt.ylabel('')
    pie_diagram.figure.savefig(f'{PATH}/bug_in_status_pie')


def create_completed_issue_destribution_bar():
    """Creating a bar chart in png format with data on the issues distribution by versions"""
    completed_issue_destribution = pd.DataFrame(
        rd.distribution_of_issues_by_fixed_versions(), 
        columns =['Version', 'Number of issues']
        )
    completed_issue_destribution = completed_issue_destribution.loc[completed_issue_destribution['Version'].str.match(r'^\d+[\d\.]*$')]
    completed_issue_destribution['Version'] = completed_issue_destribution['Version'].str.extract(r'^(\d{1,2}\.+\d{0,2})')
    completed_issue_destribution = completed_issue_destribution.groupby('Version').sum()
    bar_diagram = completed_issue_destribution.plot(
        y='Number of issues',
        kind='bar',
        figsize=(10, 10),
        color=(completed_issue_destribution['Number of issues'] > 100).map({True: 'g',False: 'r'}),
        legend=False
        )
    plt.title("Distribution of completed issues", fontsize=25)
    plt.xlabel('Version', fontsize=20)
    plt.ylabel('Number of Issues', fontsize=20)
    bar_diagram.figure.savefig(f'{PATH}/completed_issue_destribution')


if __name__ == "__main__":
    functions_to_call = [
        create_most_voted_suggestions_table,
        create_most_voted_bugs_table,
        create_most_watched_suggestions_table,
        create_most_watched_bugs_table,
        create_suggestion_in_status_pie,
        create_bug_in_status_pie,
        create_completed_issue_destribution_bar
        ]

    os.makedirs(PATH,exist_ok=True)
    for function in functions_to_call:
        function()
