# spotiCLI

## Description
super simple spotify-cli program made using [Spotify Web API](https://spotipy.readthedocs.io/) in Python3

## How to use
#### 1. clone the repo
```
git clone https://github.com/doer08736/spotiCLI
```

#### 2. create app ([developer.spotify.com](https://developer.spotify.com/dashboard))
Read [this](https://developer.spotify.com/documentation/web-api) for more information. To get the user_id sign-in to [spotify](https://spotify.com) and note the username

{NOTE: make sure to set Redirect URI to http://127.0.0.1:8080/ while creating app}

#### 3. create environment variables and set the values of the following that you got from the spotify developer web portal
```
spotify_user_id="<your_user_id>"
spotify_redirect_uri="http://127.0.0.1:8080/"
spotify_client_id="<your_client_id>"
spotify_client_secret="<your_client_secret>"
```

#### 4. head on to spotiCLI directory
```
cd spotiCLI
```

#### 5. create virtual enviroment & activate
Linux
```
python3 -m venv <any-name> && source <any-name>/bin/activate
```
Windows
```
python3 -m venv <any-name> && source <any-name>\Scripts\activate
```

#### 6. install required modules
```
pip3 install -r requirements.txt
```

#### 7. now run the commands (usage and options given below)
```
python3 spoticli.py
```

**{NOTE: When you run the script for the first time it will pop-up a login page in your browser, then you need to sign-in and verify your spotify account}**

## Usage
```
python3 spoticli.py --help
```

## Options
```
                      _   _  _____ _      _____ 
                     | | (_)/ ____| |    |_   _|
      ___ _ __   ___ | |_ _| |    | |      | |  
     / __| '_ \ / _ \| __| | |    | |      | |  
     \__ \ |_) | (_) | |_| | |____| |____ _| |_ 
     |___/ .__/ \___/ \__|_|\_____|______|_____|
         | |                                        v1.0
         |_|
        [https://github.com/doer08736/spotiCLI] 


Usage: python3 spoticli.py -h | -p | -v | -d | -i | -s
Usage: python3 spoticli.py -c <playlistname> | -t <trackname> | -a <artistname>

Options:
  -h, --help            show this help message and exit
  -p, --playing         display current playing track
  -v, --viewplaylist    display user playlist(s)
  -c, --createplaylist  create playlist(s)
  -d, --deleteplaylist  delete playlist(s)
  -t, --trackinfo       display given track info
  -a, --artistinfo      display given artist info
  -i, --insert          insert track into playlist at specific position
  -s, --sort            sort playlist(s) according to release date
```
## Features
* **view artist info**
* **view current playing track**
* **view track info**
* **delete playlist from playlist list**
* **view your all playlists**
* **create playlist with given name**
* **insert track into playlist**
* **sort playlist according to releasedate**

## Examples
### create playlist
```
python3 spoticli.py -c bangers
```

### view playlist
```
python3 spoticli.py -v
```

### track info
```
python3 spoticli.py --trackinfo "Never Gonna Give You Up"
```

## Authors
[doer08736](https://github.com/doer08736)

## Conclusion
The End.
