#!/usr/bin/env sh
cd /Library/Server/Web/Data/Sites/Nikola/blog
git reset --hard
git fetch --all
git reset --hard origin/master
source ../bin/activate
sed -i '' 's/^SITE_URL = "https:\/\/bwinton.github.io\/weblog.latte.ca\/"$/SITE_URL = "https:\/\/weblog.latte.ca\/"/' conf.py
nikola build -v 0 -r zero
nikola check --clean-files
