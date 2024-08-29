To enable the rsync daemon only during the night from 10 PM to 7 AM, you can use macOS's built-in scheduling tool, launchd, to create a scheduled task. Here's how you can set it up:

Step 1: Create the Launch Daemon Configuration
Create the .plist file for the rsync daemon:

```bash
sudo nano /Library/LaunchDaemons/com.rsync.server.night.plist
```
Add the following content to schedule the rsync daemon to start at 10 PM and stop at 7 AM:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.rsync.server.night</string>
    
    <!-- Start at 10 PM -->
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>22</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>

    <!-- Program to run (starting the rsync daemon) -->
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/rsync</string>
        <string>--daemon</string>
        <string>--config=/etc/rsyncd.conf</string>
    </array>

    <!-- Stop at 7 AM -->
    <key>StartInterval</key>
    <integer>32400</integer> <!-- 9 hours (from 10 PM to 7 AM) -->

    <key>KeepAlive</key>
    <false/>
</dict>
</plist>
```

Step 2: Load the Launch Daemon
Set the correct permissions for the .plist file:

```bash
sudo chmod 644 /Library/LaunchDaemons/com.rsync.server.night.plist
sudo chown root:wheel /Library/LaunchDaemons/com.rsync.server.night.plist
```

Load the daemon to activate the schedule:

```bash
sudo launchctl load /Library/LaunchDaemons/com.rsync.server.night.plist
```
Step 3: Test the Setup
You can manually test the setup by unloading and reloading the daemon to see if the rsync daemon starts and stops as expected:
To manually start the daemon (mimicking 10 PM):

```bash
sudo launchctl start com.rsync.server.night
```

To manually stop the daemon (mimicking 7 AM):

```bash
sudo launchctl stop com.rsync.server.night
```
Explanation
 - The StartCalendarInterval key schedules the rsync daemon to start at 10 PM.
 - The StartInterval key keeps the daemon running for 9 hours (from 10 PM to 7 AM).
 - The KeepAlive key is set to false so that the daemon stops automatically after the interval.
This setup ensures that the rsync daemon will only run between 10 PM and 7 AM daily.