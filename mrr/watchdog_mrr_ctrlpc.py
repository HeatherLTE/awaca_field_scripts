#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 3 09:31:46 2024

@author: corden
"""
##NOTE THIS SCRIPT IS UNTESTED!!! TO BE TESTED IN ANTARCTICA...


########################################################################################################################
# WATCHDOG for MRR, adapted from watchdog for the SARA PC developed by Olivier
#
# - This script should be copied in /home/mrr/scripts/watchdog_mrr_ctrlpc.py
# - This script should be periodically triggered using mrr user's crontab.
# - The duration between two executions should be greater than `DURATION_BETWEEN_ON_OFF_REBOOT_SECONDS` plus the time
#   required by the target instrument to reboot and first update the kibble.
#
# - Known limitations:
#   - There is no check whether the reboot is actually performed or not. And so, no action if not performed...
########################################################################################################################

import socket
import datetime
import os
import time

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8082

KIBBLES_FILE_PATH = "/home/mrr/watchdog/"
#this is where the kibble is created by the script 'watchdog_mrr_kibble_creation.sh'
#it is also where a file is created recording the number of reboots

DURATION_BETWEEN_ON_OFF_REBOOT_SECONDS = 10
MAX_KIBBLE_AGE_SECONDS = 60 * 70


INSTRUMENTS = ["mrr"]


def is_kibble_old(instrument_code: str) -> bool:
    kibble_filepath = os.path.join(KIBBLES_FILE_PATH, 'kibble_' + instrument_code + ".txt")
    if not os.path.exists(kibble_filepath):
        print("Kibble file not found")
        return False

    # Check if the kibble is older than threshold.
    last_modification_datetime = os.path.getmtime(kibble_filepath)  # Timestamp in seconds
    now = datetime.datetime.utcnow().timestamp()
    if (now - last_modification_datetime) < MAX_KIBBLE_AGE_SECONDS:
        print("Kibble recent enough")
        reset_reboot_count(instrument_code)
        return False
    else:
        print("Kibble excessively old")
        return True


def is_last_reboot_old_enough(instrument_code: str) -> bool:
    reboots_filepath = os.path.join(KIBBLES_FILE_PATH, 'reboots_' + instrument_code)
    if not os.path.exists(reboots_filepath):
        print("'Reboots' file not found")
        return True

    last_reboot_datetime = os.path.getmtime(reboots_filepath)  # Timestamp in seconds
    now = datetime.datetime.utcnow().timestamp()
    duration_since_last_reboot = now - last_reboot_datetime
    next_reboot_duration = get_next_reboot_duration(instrument_code)
    print("Last reboot done at " + datetime.datetime.fromtimestamp(last_reboot_datetime).strftime('%Y-%m-%d %H:%M:%S'))
    print("Duration since last reboot: " + str(datetime.timedelta(seconds=duration_since_last_reboot))[:-7])
    print("Timespan between 2 reboots increase over time and ceil at 1 week.")
    print("Duration between last and next reboot: " + str(datetime.timedelta(seconds=next_reboot_duration)))

    if duration_since_last_reboot < next_reboot_duration:
        print("Previous reboot is too recent. Do not reboot yet.")
        return False
    else:
        print("Previous reboot is old enough.")
        return True


def is_network_up(network_id: int) -> bool:
    status_code, message = send_request("NetworkUp", [str(network_id)])
    if status_code == 0:
        if message == "UP":
            return True
        elif message == "DOWN":
            return False
    else:
        raise Exception("Server responded with errno " + str(status_code) + ": " + message)


def reboot(instrument_code: str):
    match instrument_code:
        case "mrr":
            relay_name = "MRR"
        case _:
            raise ValueError("Invalid instrument code")

    print("Rebooting instrument " + instrument_code)
    print("Turning " + relay_name + " OFF")
    send_request("SetRelay", [relay_name, "OFF"])
    print("Waiting " + str(DURATION_BETWEEN_ON_OFF_REBOOT_SECONDS) + "s...")
    time.sleep(DURATION_BETWEEN_ON_OFF_REBOOT_SECONDS)
    print("Turning " + relay_name + " ON")
    send_request("SetRelay", [relay_name, "ON"])
    increase_reboot_count(instrument_code)
    print("Done")


def get_next_reboot_duration(instrument_code: str):
    try:
        reboot_count = get_reboot_count(instrument_code)
    except FileNotFoundError:
        reboot_count = 0
    if reboot_count > 0:
        print(f"Already {str(reboot_count)} reboots done in a row.")
    age_minutes = 30 + (60 * (reboot_count ** 2))  # If previous reboot failed, wait longer than for the previous reboot
    age_minutes = min(age_minutes, 7 * 24 * 60)  # In any case, reboot at least every week (if kibble is still too old)
    return age_minutes * 60


def reset_reboot_count(instrument_code: str):
    with open(os.path.join(KIBBLES_FILE_PATH, "reboots_" + instrument_code), "w") as file:
        file.write("0")


def get_reboot_count(instrument_code: str) -> int:
    try:
        with open(os.path.join(KIBBLES_FILE_PATH, "reboots_" + instrument_code), "r") as file:
            count = int(file.read())
    except ValueError:
        count = 0
    return int(count)


def increase_reboot_count(instrument_code: str):
    count_before = get_reboot_count(instrument_code)
    with open(os.path.join(KIBBLES_FILE_PATH, "reboots_" + instrument_code), "w") as file:
        new_count = count_before + 1
        file.write(str(new_count))


def send_request(command: str, parameters: list=None):
    message = command + ":" + ",".join(parameters)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        client_socket.sendall(message.encode('utf-8'))

        # Receive response from the server
        response = client_socket.recv(1024).decode('utf-8')

        print(response)

        # Splitting the response into status code and message
        status_code, message = response.split('|', 1)
        return int(status_code), message


if __name__ == "__main__":
    print(datetime.datetime.utcnow())
    os.makedirs(KIBBLES_FILE_PATH, exist_ok=True)

    instrument_code = "mrr"
    if not (instrument_code in INSTRUMENTS):
        raise ValueError("First parameter should be a valid instrument code: " + ",".join(INSTRUMENTS))

    if not os.path.exists(os.path.join(KIBBLES_FILE_PATH, "reboots_" + instrument_code)):
        reset_reboot_count(instrument_code)

    if is_kibble_old(instrument_code):
        if is_last_reboot_old_enough(instrument_code):
            if is_network_up(1):
                reboot(instrument_code)
    #note for the MRR we only reboot if network 1 is up. If network 1 is not up, the ping kibble creation will not work and the MRR might be working fine.
    # the MRR is only connected to network 1