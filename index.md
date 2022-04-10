# Welcome to GitHub Pages for LeagueBuilds

LeagueBuilds is a console application written in python. It utilizes the Riot API to find the most popular builds for champions in League of Legends.

## Overview

![overview](https://user-images.githubusercontent.com/61245108/162573774-a20691ec-78a8-41bd-9d98-10b84bf23c29.jpg)

### LeagueBuilds Server

The LeagueBuilds Server uses the Riot API to access the matchhistory of all Master/Grandmaster/Challenger players in EUW. By utilizing the Timeline of these matches builds for each Champion are generated. These Builds consist of:
- all runes chosen
- picked summonerspells
- startitems bought at the beginning of the match
- first three finished items
- items at the end of the match
- skillorder

The generated builds are stored in an SQLite database on the server. To save on storage space and sqlite query time, builds older than two weeks are automatically deleted.
To make those builds accessible the sever listens on port 12345 for requests, which include a champion id and the appointed team position. Using this information all relevant builds are send to the requesting client.

### LeagueBuilds Client

The LeaguBuilds Client runs on the same machine as the League of Legends gameclient. Using the LCU API the client listens to pick events during championselect. If an event gets triggered a request with champion id and team position is send to the LeagueBuilds Server to get the relevant builds of the picked champion. When the builds are successfully received, they are sorted to find the most popular one. Then again using the LCU API following information is send to the League of Legends client:
- Summonerspells
- Runes
- Itembuilds(include the most popular three Startitem combinations, the most popular three combinations of first three finished items, and a general list of the most popular items)

To interpret the recived item/champion/rune ids the LeagueBuilds client uses the most recent available Data Dragon information, which gets saved in an sqlite database on startup of the LeagueBuilds client.

The most recent version of LeagueBuilds Client can be downloaded [here](https://github.com/CookieDecide/LeagueBuilds/releases).
The LeagueBuilds Server is not available for download, but the source code can be accessed [here](https://github.com/CookieDecide/LeagueBuilds)
