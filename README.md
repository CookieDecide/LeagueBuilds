# LeagueBuilds

LeagueBuild uses a centralized server to get recent builds of Master, Grandmaster and Challenger League of Legends Players and store them in a local database. Those builds, which include runes, summoner spells and most bought items, can be accessed per a client. During championselect the client will inject the most popular build for the champion the player currently hovers using the LCU API.

# Requirements

* Google Chrome

# HowTo

If you want to use the finished client download the latest release and execute the main_client.exe. This will open the GUI and load the build when you picked your champion.

If you want to run your own version locally:
* edit config.py to your own RIOT API-KEY
* make sure the sockets in client.py and server.py are set to localhost
* start the server via the server_main.py (this will take some time to get the most recent builds)
* start the client on the machine, which runs League of Legends via client_main.py

# ToDo:
- add suport for ARAM matches
