# ev3-nabiralec

Demonstracijski program za robota Lego Mindstorms EV3, ki se zna premikati po danih točkah na poligonu. Namenjeno tekmovanju [Robo liga FRI](https://www.fri.uni-lj.si/sl/robo-liga-fri).

Program je napisan v Python3 ([knjižnica python-ev3dev](https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/ev3dev-jessie/)) in deluje na operacijskem sistemu [ev3dev](https://www.ev3dev.org/).

## Priprava okolja - ev3dev

Sledite navodilom [ev3dev Getting Started](https://www.ev3dev.org/docs/getting-started/), da pridobite operacijski sistem `ev3dev-stretch` in ga namestite na SD kartico, ki ste jo dobili s kompletom. Za priklop v brezžično omrežje uporabite adapter za WiFi, ki ste ga prav tako dobili v kompletu.

Na robota se povežete prek protokola SSH, datoteke pa nalagate nanj prek protokola SFTP. Privzeto je uporabniško ime `robot` in geslo `maker`.

### VS Code in ev3dev-browser

Priporočamo vam uporabo urejevalnika [Visual Studio Code](https://code.visualstudio.com/) v kombinaciji z razširitvijo [ev3dev-browser](https://github.com/ev3dev/vscode-ev3dev-browser). Za namestitev in konfiguracijo [sledite tem izčrpnim navodilom](https://sites.google.com/site/ev3devpython/setting-up-vs-code).

Da pri povezovanju na robota ne boste vpisovali gesla vedno znova, ga lahko vpišete v `.vscode/settings.json` (ustvarite mapo `.vscode` in v njej datoteko `settings.json`, če še ne obstaja):

```json
{
    "ev3devBrowser.password": "sem-vstavi-geslo-svojega-robota"
}
```

### Sprememba imena kocke (hostname) in gesla

Privzeto ime kocke je `ev3dev` in privzeto geslo je `maker`. Priporočamo, da ta dva podatka nemudoma spremenite. 

Uporabite ukaz:

`sudo ev3dev-config`

in sledite navodilom.


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

### VS Code in ev3dev-browser

Če uporabljate Visual Studio Code in razširitev ev3dev-browser, lahko program naložite na kocko in ga poženete preprosto s pritiskom na tipko <kbd>F5</kbd>. 

Pri tem morate imeti v mapi `.vscode` datoteko `launch.json` in v njej naslednjo konfiguracijo:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Download and Run Current File",
            "type": "ev3devBrowser",
            "request": "launch",
            "program": "/home/robot/${workspaceFolderBasename}/${relativeFile}"
        }
    ]
}
```

## Kratek opis delovanja programa

- Ključni parametri, ki jih morate nujno nastaviti:

    ```Python
    # ID robota. Spremenite, da ustreza številki označbe, ki je določena vaši ekipi.
    ROBOT_ID = 10
    # URL igralnega strežnika.
    SERVER_URL = "192.168.1.130:8088/game/"
    # Datoteka na igralnem strežniku s podatki o tekmi.
    GAME_ID = "ec0a"
    ```

- Na naslovu `SERVER_URL/GAME_ID` dobimo podatke o tekmi v formatu JSON.

- Vzpostavitev povezave s strežnikom in pošiljanje zahteve:

    ```Python
    conn = Connection(url)
    game_state = conn.request()
    ```

- Predpostavljamo, da ste velika motorja priklopili na izhoda B in C, lahko pa to nastavite v spremenljivkah `MOTOR_LEFT_PORT` in `MOTOR_RIGHT_PORT`.

- Del programa je namenjen preverjanju, ali je dotično tipalo priklopljeno na vhod - funkcija `init_sensor_touch`. Za zgled smo uporabili tipalo za dotik (`TouchSensor`), vendar v sami kodi nismo uporabili njegove vrednosti. Klic te funkcije lahko mirno zakomentirate, morda pa vam vseeno pride kdaj prav.

- Program se konča, če ugotovimo, da robot v trenutni tekmi ne tekmuje. Se pravi, da njegovega IDja (`ROBOT_ID`) ni na seznamu `teams` na strežniku.

- Robot miruje, če tekma ne teče (preverimo `game_state['game_on']`), če oznaka robota ni zaznana (to pove spremenljivka `robot_data_valid`) ali če je robotu zmanjkalo goriva (preverimo `game_state['teams'][ROBOT_ID]['fuel']`).

- Program na robotu izvaja premikanje po vnaprej določenih točkah na poligonu. Seznam je definiran kot `targets_list`. V našem primeru se bo robot vozil po notranjih kotih obeh košar.

    ```Python
    targets_list = [
        Point(game_state['fields']['blue_basket']['bottom_right']),
        Point(game_state['fields']['blue_basket']['top_right']),
        Point(game_state['fields']['red_basket']['top_left']),
        Point(game_state['fields']['red_basket']['bottom_left']),
    ]
    ```
- Robot izvaja štiri stanja, katerim seveda lahko dodate poljubna druga, denimo za zaznavanje bližnjega trka.
  - `IDLE`: stanje mirovanja in tudi začetno stanje. Tu se odločamo, kaj bo robot sedaj počel.
  - `LOAD_NEXT_TARGET`: kot trenutno ciljno točko naložimo naslednjo točko iz seznama `targets_list`. Ko pridemo do konca seznama, gremo spet od začetka.
  - `TURN`: stanje obračanja robota na mestu z regulatorjem PID. Hitrost levega motorja je nasprotna vrednost hitrosti desnega motorja. Stanje je zaključeno, ko je robot obrnjen proti ciljni točki v toleranci `DIR_EPS` stopinj.
  - `DRIVE_STRAIGHT`: stanje vožnje "naravnost" (robot vmes tudi zavija, da ohranja ničelno napako v kotu med sabo in ciljem). Hitrost na motorju je sestavljena iz dveh delov: nazivna hitrost (base) in hitrost obračanja (turn). Vsaka od njih je podvržena regulaciji s svojim regulatorjem PID.

- Za nastavitev hitrosti obeh motorjev uporabljamo regulator PID (sestavljen iz Proporcionalnega, Integrirnega in diferencirnega člena), ki je določen z naslednjimi parametri:
  - `Kp`: ojačitev proporcionalnega dela regulatorja. Visoke vrednosti pomenijo hitrejši odziv sistema, vendar pozor: previsoke vrednosti povzročijo oscilacije in nestabilnost.
  - `Ki`: ojačitev integrirnega člena regulatorja. Izniči napako v ustaljenem stanju. Zmanjša odzivnost.
  - `Kd`: ojačitev odvoda napake. Zmanjša čas umirjanja in poveča odzivnost.
  - `integral_limit`: najvišja dovoljena vrednost integrirnega člena. Sčasoma namreč lahko njegova vrednost zelo naraste in ga je modro omejiti.
  
  Povabljeni ste, da preizkušate različne nastavitve teh parametrov in s tem dosežete boljši (hitrejši/stabilnejši) odziv.

## Priporočeni viri

- [Uradna stran projekta ev3dev](https://www.ev3dev.org/)

- [Vodiči za programiranje EV3 v Pythonu](https://sites.google.com/site/ev3devpython/)

- [Dokumentacija knjižnice `python-ev3dev`](https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/ev3dev-jessie/)

- [Programiranje robota v Pythonu z urejevalnikom Visual Studio Code](https://github.com/ev3dev/vscode-hello-python)
