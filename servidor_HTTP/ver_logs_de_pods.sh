#!/bin/bash

APP_LABEL="my-app"
CMD="kubectl get pods -w -l app=fastapi-server"

osascript <<EOF
tell application "iTerm"
  activate
  set newWindow to (create window with default profile)
  
  tell current session of newWindow
    write text "$CMD"
  end tell

  tell newWindow
    set firstSession to current session

    -- First split horizontally
    set secondSession to (split session firstSession horizontally with default profile)
    tell secondSession to write text "$CMD"

    -- Split the second session horizontally to make 3 panes
    set thirdSession to (split session secondSession horizontally with default profile)
    tell thirdSession to write text "$CMD"
  end tell
end tell
EOF
