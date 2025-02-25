# This script automates regular upgrades of your Homebrew packages on macOS.
# It performs the following tasks:
# 1. Updates Homebrew itself to the latest version.
# 2. Upgrades all installed formulae to their latest versions.
# 3. Upgrades all installed casks to their latest versions.
# 4. Cleans up old versions and cached downloads to free up disk space.
# 5. Checks for potential problems with the Homebrew installation.
#!/bin/bash

echo "Updating Homebrew and upgrading packages..."
echo `date`
echo `whoami`
echo `pwd`
echo 
echo "Update Homebrew itself"
/opt/homebrew/bin/brew update

echo "Upgrade all formulae"
/opt/homebrew/bin/brew upgrade

echo "Upgrade all casks"
/opt/homebrew/bin/brew upgrade --cask

echo "Remove outdated versions"
/opt/homebrew/bin/brew cleanup

# echo "Check for potential problems"
# brew link certifi