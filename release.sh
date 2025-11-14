#!/bin/env bash

set -e

if [[ -z "$VIRTUAL_ENV" ]]; then
    source venv/Scripts/activate
fi

# DONE - Fetch tags and get the latest one
git fetch --tags
version=$(git describe --tags $(git rev-list --tags --max-count=1))
version_number="${version#v}"  # Remove 'v' prefix if the tag has it
echo "Version: $version_number"

# Extract major, minor, and patch versions
IFS='.' read -r MAJOR_VERSION MINOR_VERSION PATCH_VERSION <<< "$version_number"
export MAJOR_VERSION MINOR_VERSION PATCH_VERSION
echo "Major version: $MAJOR_VERSION"
echo "Minor version: $MINOR_VERSION"
echo "Patch version: $PATCH_VERSION"

# Write version file
envsubst < version_file.txt > version_file.tmp
mv version_file.tmp version_file.txt
cat version_file.txt

# Install dependencies
pip install -r requirements.txt

# Lint with pylint
#pylint src/mos_bot.py

# Test with pytest
#pytest src/test_mos_bot.py

# Build executable with pyinstaller
pyinstaller --icon mos_bot.ico --version-file version_file.txt --hidden-import lxml --onefile src/mos_bot.py

# Restore files with sensible data
cp src/mos_bot.conf src/mos_bot.conf.bak
git restore src/mos_bot.conf

# Compress executable and related files
zip -j dist/mos_bot.zip readme.md dist/mos_bot.exe src/mos_bot.conf src/mos_bot.path
cd src && zip -r ../dist/mos_bot.zip chromedriver-win64 && cd ..

# Write release notes
envsubst < release_notes.md > release_notes.tmp
mv release_notes.tmp release_notes.md
cat release_notes.md

# Create a release on GitHub
gh release create $version --verify-tag --notes-file release_notes.md --title "MOS_BOT ${version} release" dist/mos_bot.zip#mos_bot.zip

# Reverting placeholder files
git restore release_notes.md
git restore version_file.txt

# Retrieve sensible data from files
rm src/mos_bot.conf && mv src/mos_bot.conf.bak src/mos_bot.conf
