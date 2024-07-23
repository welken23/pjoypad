#!/usr/bin/env bash

# notification display time in milliseconds
time=1800
# notification id
id=10000
# close notification with id
gdbus call --session --dest org.freedesktop.Notifications --object-path /org/freedesktop/Notifications --method org.freedesktop.Notifications.CloseNotification $id > /dev/null
$1 $2 $3 &
