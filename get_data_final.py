import requests as rq
import pandas as pd


# Make API request
def api_request(user_name, repo_name):
    api_url = "https://api.github.com/repos/" + user_name + "/" + repo_name
    response = rq.get(url=api_url, params={}).json()

    return response


# Get total number of commits on main/master
def get_commits_main(user_name, repo_name):
    url = "https://github.com/" + user_name + "/" + repo_name
    source_code = str(rq.get(url).content).replace(",", "")
    i = source_code.find("Commits on")
    j = i - 1
    commits_reversed = ""
    while not source_code[j].isnumeric():
        j = j - 1
    while source_code[j].isnumeric():
        commits_reversed = commits_reversed + source_code[j]
        j = j - 1

    commits = commits_reversed[::-1]

    return commits


# Get number of open and closed issues
def get_issues(user_name, repo_name, response):
    # Get open issues from API
    open_issues = str(response["open_issues"])

    # Get closed issues from source code
    url = "https://github.com/" + user_name + "/" + repo_name + "/issues"
    source_code = str(rq.get(url).content).replace(",", "")
    i = source_code.find("Closed")
    source_code = source_code[i + 6 :]
    i = source_code.find("Closed")
    j = i - 1
    closed_issues_reversed = ""
    while not source_code[j].isnumeric():
        j = j - 1
    while source_code[j].isnumeric():
        closed_issues_reversed = closed_issues_reversed + source_code[j]
        j = j - 1

    closed_issues = closed_issues_reversed[::-1]

    return open_issues, closed_issues


# Get number of contributors
def get_contributors(user_name, repo_name):
    url = "https://github.com/" + user_name + "/" + repo_name
    source_code = str(rq.get(url).content).replace(",", "")
    i = source_code.find("Contributors <span")
    j = i
    contributors = ""
    while not source_code[j].isnumeric():
        j = j + 1
    while source_code[j].isnumeric():
        contributors = contributors + source_code[j]
        j = j + 1

    return contributors


# Get languages
def get_languages(response):
    languages_url = response["languages_url"]
    r = rq.get(url=languages_url, params={})
    languages = r.json()

    return languages


# Get total number of lines
def get_total_lines(languages):
    total_lines = 0
    for language in languages:
        total_lines = total_lines + languages[language]

    return str(total_lines)


# Get most used language and total number of lines in that language
def get_most_used_lang(languages):
    most_used_lang = "None"
    max_lang_lines = 0
    for language in languages:
        if languages[language] > max_lang_lines:
            most_used_lang = language
            max_lang_lines = languages[language]

    return most_used_lang, str(max_lang_lines)


repo_info = pd.read_csv("./mostPopularRepositories.csv", sep=";")
repo_info = repo_info.drop_duplicates()
owners = repo_info.loc[:, ["RepositoryOwner"]]
repos = repo_info.loc[:, ["RepositoryName"]]

start = 997

for i in range(start, start + 31):

    deleted_repos = (("Marak", "faker.js"),)

    try:
        user_name, repo_name = (
            owners.loc[i, "RepositoryOwner"],
            repos.loc[i, "RepositoryName"],
        )

        if (user_name, repo_name) in deleted_repos:
            continue

        response = api_request(user_name, repo_name)

        commits = get_commits_main(user_name, repo_name)
        open_issues, closed_issues = get_issues(user_name, repo_name, response)
        contributors = get_contributors(user_name, repo_name)
        languages = get_languages(response)
        total_lines = get_total_lines(languages)
        most_used_lang, max_lang_lines = get_most_used_lang(languages)
        with open("repo_data.csv", "a") as l:
            l.write(
                ";".join(
                    [
                        user_name,
                        repo_name,
                        commits,
                        open_issues,
                        closed_issues,
                        contributors,
                        total_lines,
                        most_used_lang,
                        max_lang_lines,
                    ]
                )
                + "\n"
            )

        print(i)
    except KeyError as e:
        if e.args[0] == i:
            continue
        elif e.args[0] in ("open_issues", "languages_url"):
            print("Change VPN.")
            break
    except TypeError as e:
        if e.args[0] == "unsupported operand type(s) for +: 'int' and 'str'":
            print("Change VPN.")
            break