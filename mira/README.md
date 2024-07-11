# Folder Structure

### On the MIRA PC
Make the following directories on the mira pc: \
/home/data/awaca_scriptsnlogs \
/home/data/awaca_scriptsnlogs/scripts \
/home/data/awaca_scriptsnlogs/logs \
/home/data/awaca_scriptsnlogs/watchdog

Add the following files to the scripts folder: \
config.conf \
sync_data_mira.py \
delete_data_mira.py \
watchdog_mira_local.py

### On both control PCs
Make the following directories as the mira user

/home/mira/scripts \
/home/mira/logs \
/home/mira/watchdog

Add the following files to the scripts folder: \
watchdog_mira_ctrlpc.py


# Crontabs

### On the MIRA PC (as data user)

```
#mira transfer to nas
20,30,40 1 * * * /usr/bin/python3 /home/data/awaca_scriptsnlogs/scripts/sync_data_mira.py >> /home/data/awaca_scriptsnlogs/logs/mi>

#mira delete old moments files if safely stored on nas
45 1 * * * /usr/bin/python3 /home/data/awaca_scriptsnlogs/scripts/delete_data_mira.py >> /home/data/awaca_scriptsnlogs/logs/delete>

#mira watchdog local kibble creation and sync to ctrlpc
5,35 * * * * /usr/bin/python3 /home/data/awaca_scriptsnlogs/scripts/watchdog_mira_local.py

```
### On both control PCs (as mira user) with times offset
```
# mira watchdog
15 * * * * /usr/bin/python3 /home/mira/scripts/watchdog_mira_ctrlpc.py > /home/mira/logs/watchdog_mira.log 2>&1
```

# Checklist of things to check/change in the scripts
- make sure all scripts are executable by data user
- add crontab and check timings and paths

### In config.conf
- paths

### In sync_data_mira.py
- path to config file
- set sync_current_month = True

### In delete_data_mira.py
- days_old

### In watchdog_mira_local.py
- path to config file

### In watchdog_mira_ctrlpc.py
- path to kibble file

# Watchdog
The script on the MIRA pc makes a local kibble file in the watchdog folder and syncs it to the 2 control pcs via ftp. The script should be run every 30 minutes. The sync to the control pc is untested!

The script on the control PC checks the age of the kibble and powers the mira relay off and on if the kibble is too old. This script is untested!

# Quicklooks

## Installing conda
```
08/07/2024 12:56 sudo zypper refresh
08/07/2024 12:59 pwd
08/07/2024 12:59 ls
08/07/2024 12:59 cd --
08/07/2024 12:59 pwd
08/07/2024 12:59 ls
08/07/2024 12:59 cd Downloads/
08/07/2024 12:59 ls
08/07/2024 12:59 wget https://repo.anaconda.com/archive/Anaconda3-2023.03-Linux-x86_64.sh
08/07/2024 13:00 sha256sum Anaconda3-2023.03-Linux-x86_64.sh
08/07/2024 13:03 bash Anaconda3-2023.03-Linux-x86_64.sh
08/07/2024 13:05 logout
08/07/2024 13:06 ls -la
08/07/2024 13:06 ~/anaconda3/bin/conda init
08/07/2024 13:06 source ~/.bashrc
08/07/2024 13:07 .conda --version
08/07/2024 13:07 sudo .conda --version
08/07/2024 13:07 ls -la
08/07/2024 13:08 poweroff
08/07/2024 14:00 /anaconda3/bin/conda init
```

