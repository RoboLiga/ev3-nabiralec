#!/home/robot/roboliga/bin/python
# -*- coding: utf-8 -*-

from ev3dev2.motor import OUTPUT_B, OUTPUT_C
from ev3dev2.sensor import INPUT_1


# Debug nastavitve
IGNORE_FUEL = False
IGNORE_PAUSE = False

# Nastavitev najpomembnjših parametrov
# ID robota. Spremenite, da ustreza številki označbe, ki je določena vaši ekipi.
ROBOT_ID = "25"
# URL igralnega strežnika.
SERVER_URL = "192.168.1.44:8088/game/"
# Številka ID igre, v kateri je robot.
GAME_ID = "0cca"

# Priklop motorjev na izhode.
MOTOR_LEFT_PORT = OUTPUT_C
MOTOR_RIGHT_PORT = OUTPUT_B

# Priklop tipal na vhode.
SENSOR_COLOR_PORT = INPUT_1

# Najvišja dovoljena hitrost motorjev (teoretično je to 1000).
SPEED_MAX = 600
# Najvišja dovoljena nazivna hitrost motorjev pri vožnji naravnost.
# Naj bo manjša kot SPEED_MAX, da ima robot še možnost zavijati.
SPEED_BASE_MAX = 500

# Parametri za PID
# Obračanje na mestu in zavijanje med vožnjo naravnost
PID_TURN_KP = 3.0
PID_TURN_KI = 0.5
PID_TURN_KD = 0.0
PID_TURN_INT_MAX = 100
# Nazivna hitrost pri vožnji naravnost.
PID_STRAIGHT_KP = 2.0
PID_STRAIGHT_KI = 0.5
PID_STRAIGHT_KD = 0.01
PID_STRAIGHT_INT_MAX = 100

# Dolžina FIFO vrste za hranjenje meritev (oddaljenost in kot do cilja).
HIST_QUEUE_LENGTH = 3

# Razdalje - tolerance
# Dovoljena napaka v oddaljenosti do cilja [mm].
DIST_EPS = 20
# Dovoljena napaka pri obračanju [stopinje].
DIR_EPS = 5
# Bližina cilja [mm].
DIST_NEAR = 100
# Koliko sekund je robot lahko stanju vožnje naravnost v bližini cilja
# (oddaljen manj kot DIST_NEAR), preden sprožimo varnostni mehanizem
# in ga damo v stanje obračanja na mestu.
TIMER_NEAR_TARGET = 3
