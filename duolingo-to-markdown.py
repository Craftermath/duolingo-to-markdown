import requests, os, sys
from datetime import datetime


def duolingo_request():
    username = os.getenv('DUOLINGO_USERNAME')
    url = f"https://api.duolingo.com/profile/{username}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        sys.exit(1)


def get_duloingo_info(data):
    num_language = int(os.getenv('DUOLINGO_LANGUAGE_LENGTH'))
    lang_list = [
            (
                language_list["language_string"],
                language_list["level"],
                language_list["points"]
            ) for language_list in response["languages"]]  # if language_list["learning"] == True]
    lang_list.sort(key=lambda lang:lang[2], reverse= True)  # guessing here
    lang_list = [lang for lang in lang_list[:num_language]]
    return lang_list


def update_readme(data):
    username = os.getenv('DUOLINGO_USERNAME')
    streak_str = os.getenv('DUOLINGO_STREAK')
    with open('README.md', 'r', encoding='utf-8') as file:
        readme = file.readlines()
    duolingo_line_index = readme.index('<!-- duolingo -->\n') + 1
    duolingo_line = '<p align="center"><img src="https://d35aaqx5ub95lt.clo'\
                    'udfront.net/images/dc30aa15cf53a51f7b82e6f3b7e63c68.svg">'\
                    f'Duolingo username: <strong> {username} </strong> </br>' 
    if streak_str == 'true':
        duolingo_line += f'Last Streak: <strong> {data["last_streak"]["length"]}'\
        '</strong> <img width="20.5px" height="15.5px" src="https://d35aaqx5ub95lt.'\
        'cloudfront.net/vendor/398e4298a3b39ce566050e5c041949ef.svg"></br>'

    lang_list = get_duloingo_info(data)

    duolingo_line += """<table align="center"><tr><th>Language</th><th>Level</th><th>Experience</th></tr>"""
    for lang in lang_list:
        duolingo_line += f"""<tr><th>{lang[0]} </th><th><span><img width="20.5px" height="15.5px" src=\
                "https://d35aaqx5ub95lt.cloudfront.net/vendor/b3ede3d53c932ee30d981064671c8032.svg"\
                ><span>{lang[1]}</span></span></th><th><span><img width="20.5px" height="15.5px" src=\
                "https://d35aaqx5ub95lt.cloudfront.net/images/profile/01ce3a817dd01842581c3d18debcbc46.svg"\
                ><span >{lang[2]}</span></span></th></tr>"""
    if (readme[duolingo_line_index] == duolingo_line):
        sys.exit(0)
    else:
        duolingo_line = duolingo_line + '</table></p> \n'
        readme[duolingo_line_index] = duolingo_line
    with open('README.md', 'w', encoding='utf-8') as file:
        file.writelines(readme)



update_readme(duolingo_request())
