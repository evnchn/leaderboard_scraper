import pathlib
import requests
import pprint
import time
import json
import os
from dotenv import load_dotenv
load_dotenv()

latest_state_json_file = str(pathlib.Path(
    __file__).parent.absolute() / "all_stats.json")

last_retry_time = 0  # 0 means no retry limit. See `if last_retry_time`
remaining_quota = 0  # will always be initialized in first strike
key = os.getenv("KEY")


def held_response(url, headers):
    global remaining_quota
    global last_retry_time
    while True:
        if last_retry_time and remaining_quota <= 1 and time.time() < last_retry_time:
            print("Too hyk, wait",  last_retry_time - int(time.time()), "s")
            # time.sleep((last_retry_time - int(time.time())) // 2 + 1)
            time.sleep(1)
        else:
            break
    r = requests.get(url, headers=headers)
    rjson = r.json()
    # pprint.pprint(r.headers)
    remaining_quota = int(r.headers["x-ratelimit-remaining"])
    last_retry_time = int(r.headers["x-ratelimit-reset"])
    return rjson


internal_state = {}


while True:
    try:
        with open(latest_state_json_file, "r", encoding="utf-8") as f:
            internal_state = json.load(f)
    except:
        input("Loss of past memory!")

    try:
        assert isinstance(internal_state["SCORE_HISTORY"], dict)
    except:
        internal_state["SCORE_HISTORY"] = {}

    try:
        assert isinstance(internal_state["PROFILES"], dict)
    except:
        internal_state["PROFILES"] = {}
        
    try:
        all_user_data = held_response(
            "https://api.tatsu.gg/v1/guilds/880301598981648416/rankings/all", headers={"Authorization": key})
        # pprint.pprint(all_user_data)
        time.sleep(1)
        current_time = int(time.time())

        for ranking in all_user_data["rankings"]:
            internal_state["SCORE_HISTORY"][ranking["user_id"]
                                            ] = internal_state["SCORE_HISTORY"].get(ranking["user_id"], [])
            if not internal_state["SCORE_HISTORY"][ranking["user_id"]] or internal_state["SCORE_HISTORY"][ranking["user_id"]][-1]["SCORE"] != ranking["score"]:
                internal_state["SCORE_HISTORY"][ranking["user_id"]
                                                ] += [{"TIME": current_time, "SCORE": ranking["score"]}]
            if not internal_state["PROFILES"].get(ranking["user_id"], {}):
                internal_state["PROFILES"][ranking["user_id"]] = {
                    "FETCHED": False}
    except:
        pass

    current_time = int(time.time())
    for user_id, profile in internal_state["PROFILES"].items():
        if not profile["FETCHED"]:
            user_data = held_response(
                f"https://api.tatsu.gg/v1/users/{user_id}/profile", headers={"Authorization": key})
            internal_state["PROFILES"][user_id] = {
                "FETCHED": True, "DATA": user_data, "TIME": current_time}
            print("Updated profile ID", user_id)
            break

    updated_user_id_and_time = {}
    for user_id, profile in internal_state["PROFILES"].items():
        if profile.get("TIME", ""):
            updated_user_id_and_time[user_id] = profile["TIME"]

    updated_user_id_and_time = {k: v for k, v in sorted(
        updated_user_id_and_time.items(), key=lambda item: item[1])}
    user_id_to_update_data = list(updated_user_id_and_time.keys())[0]
    user_data = held_response(
        f"https://api.tatsu.gg/v1/users/{user_id_to_update_data}/profile", headers={"Authorization": key})
    internal_state["PROFILES"][user_id_to_update_data] = {
        "FETCHED": True, "DATA": user_data, "TIME": current_time}
    print("Updated profile ID", user_id_to_update_data)
    internal_state["SCORE_HISTORY"] = {k: v for k, v in sorted(
        internal_state["SCORE_HISTORY"].items(), key=lambda item: item[1][-1]["SCORE"], reverse=True)}
    try:
        with open(latest_state_json_file, "w", encoding="utf-8") as f:
            json.dump(internal_state, f, indent=2)
    except:
        print("Can't store memory!")
