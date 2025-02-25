# Setup
First you need to insttal the plextraktsyc from https://github.com/Taxel/PlexTraktSync

Login to your plex server and traktv account by running the following commands
```
plextraktsync plex-login
```
```
plextraktsync trakt-login
```

Then you can run the following command to sync your plex server with traktv
```
plextraktsync sync
```

To run the script every 24 hours you can add the local.plextraktsync.job.plist file to launchd at the `/Library/LaunchDaemons` directory on your mac. You can do this by running the following command
```
sudo cp local.plextraktsync.job.plist /Library/LaunchDaemons/
```

Then you can load the job by running the following command
```
sudo launchctl load /Library/LaunchDaemons/local.plextraktsync.job.plist
```


launchd knows about daemons based on .plist in
```
User Agents     ~/Library/LaunchAgents         specific user
Global Agents   /Library/LaunchAgents          all users
System Agents   /System/Library/LaunchAgents   MacOS

Global Daemons  /Library/LaunchDaemon          installed apps
System Daemons  /System/Library/LaunchDaemons  MacOS
```