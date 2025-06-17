# duolingo-to-markdown

![cover](cover.png)

📚Update your duolingo progress to your github README profile.

## Example Output

<!-- duolingo -->
<p align="center"><img src="https://d35aaqx5ub95lt.cloudfront.net/images/dc30aa15cf53a51f7b82e6f3b7e63c68.svg">Duolingo username: <strong> Caoticarol </strong> </br>Last Streak: <strong> 329 </strong> <img width="20.5px" height="15.5px" src="https://d35aaqx5ub95lt.cloudfront.net/vendor/398e4298a3b39ce566050e5c041949ef.svg"></br><table align="center"><tr><th>Language</th><th>Experience</th></tr><tr><th>Japanese </th><th><span><img width="20.5px" height="15.5px" src=                "https://d35aaqx5ub95lt.cloudfront.net/images/profile/01ce3a817dd01842581c3d18debcbc46.svg"                ><span >20566</span></span></th></tr><tr><th>German </th><th><span><img width="20.5px" height="15.5px" src=                "https://d35aaqx5ub95lt.cloudfront.net/images/profile/01ce3a817dd01842581c3d18debcbc46.svg"                ><span >5596</span></span></th></tr><tr><th>Spanish </th><th><span><img width="20.5px" height="15.5px" src=                "https://d35aaqx5ub95lt.cloudfront.net/images/profile/01ce3a817dd01842581c3d18debcbc46.svg"                ><span >2769</span></span></th></tr></table></p> 


## SETUP
* A README.md file.
* Duolingo Account.
* Set up a GitHub Secret called  ```DUOLINGO_USERNAME``` with your Duolingo username.
* Add a ```<!-- duolingo -->``` tag in your README.md file, with three blank lines below it. The Duolingo progress will be placed here.

## Instructions


To use this release, add a ```duolingo-to-markdown.yml``` workflow file to the ```.github/workflows``` folder in your repository with the following code:

```diff
name: duolingo-to-markdown

on:
  schedule:
    - cron: '1 1 * * *'
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: repo checkout
        uses: actions/checkout@v4
        with:
          persist-credentials: false

      - name: python setup
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'

      - name: python packages installation
        run: |
          python -m pip install --upgrade pip
          pip install -r requests beautifulsoup

      - name: duolingo to markdown with fstrings
        env:
          DUOLINGO_USERNAME: ${{ secrets.DUOLINGO_USERNAME }}
          DUOLINGO_LANGUAGE_LENGTH: 3 # Optional. Defaults to 2. Language you want to show (are sort of higher experience to lower).
        run: python .github/scripts/duolingo-to-markdown.py

      - name: commit changes
        continue-on-error: true
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add -A
          git commit -m "Updated duolingo-to-markdown daily progress" -a

      - name: push changes
        continue-on-error: true
        uses: ad-m/github-push-action@v0.6.0
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}\
          branch: main
```          
The cron job is scheduled to run once a day, but you can do it weekly changing  ```- cron: '1 1 * * *' ```. You can manually run the workflow to test the code, going to the Actions tab in your repository.
          
## About:   
This is a copy with slighty modifications from [the original work here](https://github.com/diegoaichele/duolingo-to-markdown).

