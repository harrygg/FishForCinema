#!/bin/bash -e

cd /home/g/FishForCinema/FishForCinema/

echo "Fetching remote repo"
git fetch origin

echo "Scrapping movies"
python ./scrap.py

echo "Adding changes to local repo"
git add -A

echo "Comiiting changes"
git commit -m "db update"

echo "Pushing local commits to remote repo"
git push

