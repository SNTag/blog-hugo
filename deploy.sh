#!/bin/sh

# If a command fails then the deploy stops
set -e

printf "\033[0;32mDeploying updates to GitHub...\033[0m\n"

# Convert Obsidian ![[wikilink]] embeds to Markdown for the build only.
# We back up content/ and restore it on exit so the working tree keeps the
# wikilink syntax (and any unpushed edits) untouched.
restore_content() {
	if [ -d .content.bak ]; then
		rm -rf content
		mv .content.bak content
	fi
}
trap restore_content EXIT
rm -rf .content.bak
cp -r content .content.bak
python3 scripts/obsidian_to_hugo.py

# Build the project.
hugo -t tale-hugo # if using a theme, replace with `hugo -t <YOURTHEME>`

# Go To Public folder
cd public

# Add changes to git.
git add .

# Commit changes.
msg="rebuilding site $(date)"
if [ -n "$*" ]; then
	msg="$*"
fi
git commit -m "$msg"

# Push source and build repos.
git push origin master
