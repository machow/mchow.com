#%%
import json
import os

from gh_reader.download  import Downloader
from gh_reader.extractors import users
from pathlib import Path

#%%
# assumes GITHUB_TOKEN env variable
downloader = Downloader("data")
downloader.dump_repo("posit-dev", "great-tables")
downloader.dump_repo("posit-dev", "quartodoc")

#%%
all_comments = []
for fname in ["data/posit-dev+great-tables", "data/machow+quartodoc"]:
    # this is super inefficient, but fine for our purposes
    comments = Path(fname) / "issue_comments.ndjson"
    lines = comments.read_text().split("\n")

    for line in lines:
        if line == "": continue
        all_comments.append(json.loads(line))

user_ids = set(comment["user_id"] for comment in all_comments)

users_raw = users.fetch(list(user_ids), os.environ["GITHUB_TOKEN"])
users_clean = users.clean(users_raw)
json.dump(users_clean, open("data/users.json", "w"))


# %%
