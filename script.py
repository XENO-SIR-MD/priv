import os
import json
import subprocess
import sys
import time
from datetime import datetime, timedelta

# ============================================
# GitHub Contribution Graph Hack
#
# Created by Aura Farmer
# GitHub: https://github.com/aurafarmerone
#
# If you like this project, give it a ⭐
# ============================================

PATTERN_FILE = "pattern.json"
FILE_PATH = "info.txt"

COMMITS_PER_PIXEL = 5   # lighter than darkest green


# -------------------------------
# Credit Banner (Start)
# -------------------------------
def show_start_credit():
    print(r"""
          
┏┓• ┓┏  ┓   ┏┓        •   ┓   ┓ 
┃┓┓╋┣┫┓┏┣┓  ┃ ┏┓┏┳┓┏┳┓┓╋  ┃ ┏┓┣┓
┗┛┗┗┛┗┗┻┗┛  ┗┛┗┛┛┗┗┛┗┗┗┗  ┗┛┗┻┗┛                       

Created by Aura Farmer
GitHub: https://github.com/aurafarmerone
----------------------------------------
""")


# -------------------------------
# Credit Banner (End)
# -------------------------------
def show_end_credit():
    print(r"""
          
┳┳┓┳┏┓┏┓┳┏┓┳┓  ┏┓┏┓┏┓┏┓┏┓┳┓  ╻
┃┃┃┃┗┓┗┓┃┃┃┃┃  ┃┃┣┫┗┓┗┓┣ ┃┃  ┃
┛ ┗┻┗┛┗┛┻┗┛┛┗  ┣┛┛┗┗┛┗┛┗┛┻┛  •
                                                        

☑️ History Has Been Rewritten.  
☑️ The Timeline Has Changed.
☑️ Success! Pretend This Was Hard.           

----------------------------------------
⭐ If you like this project, give it a star on GitHub!
👉 https://github.com/aurafarmerone/github-contribution-graph-hack

Made with ❤️  by Aura Farmer
----------------------------------------
""")


# -------------------------------
# Git Commit (FIXED)
# -------------------------------
def git_commit(message, commit_date):
    subprocess.run(["git", "add", FILE_PATH], check=True)

    env = os.environ.copy()
    date_str = commit_date.strftime("%Y-%m-%dT12:00:00")

    env["GIT_AUTHOR_DATE"] = date_str
    env["GIT_COMMITTER_DATE"] = date_str

    subprocess.run(
        [
            "git",
            "commit",
            "--allow-empty",   # ✅ FIX: allows commit even if no file changes
            "-m",
            message,
            "--date",
            date_str
        ],
        env=env,
        check=True
    )


def git_push():
    subprocess.run(["git", "push"], check=True)


def load_pattern():
    with open(PATTERN_FILE, "r") as f:
        data = json.load(f)
        if isinstance(data, dict) and "pattern" in data:
            return data["pattern"]
        return data


def first_sunday(year):
    d = datetime(year, 1, 1)
    while d.weekday() != 6:  # Sunday
        d += timedelta(days=1)
    return d


def make_commits_from_pattern(year):
    pattern = load_pattern()
    start_date = first_sunday(year)

    for row_idx, row in enumerate(pattern):
        for col_idx, char in enumerate(row):
            if char == " ":
                continue  # empty pixel

            commit_date = start_date + timedelta(
                weeks=col_idx,
                days=row_idx
            )

            commits_count = int(char) if char.isdigit() else COMMITS_PER_PIXEL

            for i in range(1, commits_count + 1):
                msg = f"{commit_date.date()} pixel commit {i}"

                with open(FILE_PATH, "w") as f:
                    f.write(msg)

                git_commit(msg, commit_date)

    git_push()


# -------------------------------
# Entry Point
# -------------------------------
if __name__ == "__main__":
    show_start_credit()

    if len(sys.argv) > 1:
        year = int(sys.argv[1])
    else:
        try:
            year = int(input("👉 Enter year to draw pattern 📆 ➤ "))
        except (EOFError, ValueError):
            year = 2024

    make_commits_from_pattern(year)

    show_end_credit()
