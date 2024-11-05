import requests
import json

server = "http://192.168.1.44:8088"
team_name = "Demo"

req = requests.get(f"{server}/team/").json()

robot_id = -1

for team in req:
    if team["name"] == team_name:
        robot_id = team["id"]

cmd = input(f"Press enter to start a new game for team {team_name}, input no to abort: ")
if cmd.lower().strip() == "no":
    print("Game aborted.")
    exit()

game = requests.post(url=f"{server}/game", json={
    "team_1": robot_id,
    "team_2": 0
}).json()

game_id = game["game_id"]
game_passwd = game["password"]

while True:
    try:
        cmd = input("p = (un)pause, s = stop, t = time, e = exit, c = current state ")

        match cmd:
            case "p":
                requests.put(url=f"{server}/game/{game_id}/pause")
            case "s":
                requests.put(url=f"{server}/game/{game_id}/stop")
            case "t":
                new_time = input("Set time to how many seconds? ")
                requests.put(url=f"{server}/game/{game_id}/stop", json={
                    "game_time": new_time
                })
            case "c":
                print(json.dumps(requests.get(url=f"{server}/game/{game_id}").json(), indent=4))
            case "e":
                requests.put(url=f"{server}/game/{game_id}/stop")
                break
            case _:
                print("Not supported")

    except KeyboardInterrupt:
        requests.put(url=f"{server}/game/{game_id}/stop")
        break