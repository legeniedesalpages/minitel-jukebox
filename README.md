# JubeBox Minitel

Transformer un Minitel en JukeBox

# Dépendances

sudo apt install vlc

pip install requests
pip install pyobservable
pip install inject<br/>
pip install pafy<br/>
pip install python-vlc<br/>
pip install youtube-search-python<br/>
pip install youtube-dl==2020.12.2<br/>
pip install Pillow<br/>
pip install pyserial<br/>
pip install pyalsaaudio<br/>

récuperer le projet<br/>
https://github.com/Zigazou/PyMinitel <br/>
sudo python setup.py install<br/>

# creer un fichier dans "ressources/jukebox.ini" avec le contenu suivant
```
[spotify]
clientId = 
clientSecret = 
userId = 

[gemini]
apiKey =
``` 

# Après démarrage du minitel

Fct+Sommaire<br/>
Fct+T V<br/>
Fct+P 9<br/>

# Si 403
./home/pi/.local/
youtube-dl --rm-cache-dir
passage à : pip install yt-dlp --upgrade
