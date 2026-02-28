# Vortexi Gameserver
Here is how to setup the gameserver, if you are a person with 0 experience, hire a developer or ask your current one to help. If they don't know, please fire them.

## Patching RCC

Replace all urls with either kronus.co or kronus.co (maybe kronus.co if those dont match anywhere) with your domain.

## Setting Access Key
Make a simple .reg file and put this inside of it (replace keyhere with your accesskey)
```
Windows Registry Editor Version 5.00

[HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\ROBLOX Corporation\Roblox]
"AccessKey"="keyhere"
"SettingsKey"="keyhere"

[HKEY_CURRENT_USER\SOFTWARE\WOW6432Node\ROBLOX Corporation\Roblox]
"AccessKey"="keyhere"
"SettingsKey"="keyhere"

[HKEY_LOCAL_MACHINE\SOFTWARE\ROBLOX Corporation\Roblox]
"AccessKey"="keyhere"
"SettingsKey"="keyhere"

[HKEY_CURRENT_USER\SOFTWARE\ROBLOX Corporation\Roblox]
"AccessKey"="keyhere"
"SettingsKey"="keyhere"
```
## Running it
You need Python on your server and you just py main.py

I wont go in depth with this lol, I really cant be bothered writing all of this.
