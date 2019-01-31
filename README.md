# ev3-nabiralec
Demonstracijski program za robota Lego Mindstorms EV3, ki se zna premikati po danih točkah na poligonu. Namenjeno tekmovanju !(Robo liga FRI 2019: Sadovnjak)[https://www.fri.uni-lj.si/sl/robo-liga-fri].

Program je napisan v Python3 in deluje na operacijskem sistemu ![ev3dev](https://www.ev3dev.org/). 

## Priprava okolja

Sledite navodilom ![ev3dev Getting Started](https://www.ev3dev.org/docs/getting-started/), da pridobite operacijski sistem `ev3dev-stretch` in ga namestite na SD kartico, ki ste jo dobili s kompletom. Za priklop v brezžično omrežje uporabite adapter za WiFi, ki ste ga prav tako dobili v kompletu.

Na robota se povežete prek protokola SSH, datoteke pa nalagate nanj prek protokola SFTP. Privzeto je uporabniško ime `robot` in geslo `maker`. 
 - Če uporabljate Windows, vam priporočamo uporabo programa ![MobaXterm](https://mobaxterm.mobatek.net/), ki združuje odjemalca za SSH in SFTP v učinkovitem grafičnem uporabniškem vmesniku.
 - Enostavnejša možnost pa je uporaba urejevalnika ![Visual Studio Code](https://code.visualstudio.com/) v kombinaciji z razširitvijo ![EV3 Device Browser](https://github.com/ev3dev/vscode-ev3dev-browser). Za namestitev in konfiguracijo ![sledite tem izčrpnim navodilom](https://sites.google.com/site/ev3python/setting-up-vs-code). 

## Namestitev potrebnih paketov

Povežite se na robota in v terminalu izvršite naslednje ukaze za namestitev paketov `pycurl` in `ujson`:

`sudo apt-get update`

`sudo apt-get install python3-pycurl`

`sudo apt-get install python3-ujson`

## Zagon programa
Na robota prenesite (SFTP) datoteko `nabiralec.py`.
V terminalu na robotu se premaknite v mapo, ki vsebuje zgornjo datoteko. Najprej dajte datoteki pravice za izvajanje:

`chmod +x nabiralec.py`

Nato lahko program poženete:

`./nabiralec.py`


## Kratek opis delovanja programa

 
## Priporočeni viri
- Uradna stran projekta ev3dev: https://www.ev3dev.org/
- Vodiči za programiranje EV3 v Pythonu: https://sites.google.com/site/ev3python/
- Dokumentacija knjižnice `python-ev3dev`: https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/ 









