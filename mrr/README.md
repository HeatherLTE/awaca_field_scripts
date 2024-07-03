# Folder Structure

Make the following directories on each control pc: \
/home/mrr/scripts \
/home/mrr/logs \
/home/mrr/watchdog

Add the following files to the scripts folder: \
config_mrr.conf \
sync_data_mrr.py \
rsync_mrr2ctrl.sh\
delete_data_mrr.py \
watchdog_mrr_ctrlpc.py\
watchdog_mrr_ping_kibble.sh

# Crontabs

On each control pc, with TIMES OFFSET 
```
#mrr transfer from mrr to ctrl pc with rsync
20, 2 * * * bash /home/mrr/scripts/rsync_mrr2ctrl.sh >> /home/mrr/logs/mrr_rsync2ctrl.log 2>&1

#mrr transfer to nas
25 2 * * * /usr/bin/python3 /home/mrr/scripts/sync_data_mrr.py >> /home/mrr/logs/mrr_ctrl2nas.log 2>&1

# delete old moments files if safely stored on nas
45 1 * * * /usr/bin/python3 /home/mrr/scripts/delete_data_mrr.py >> /home/mrr/logs/mrr_delete_safe_files.log 2>&1

# mrr watchdog kibble creation
10,30 * * * * bash /home/mrr/scripts/rsync_mrr2ctrl.sh

# mrr watchdog check
15 * * * * /usr/bin/python3 /home/mrr/scripts/watchdog_mrr_ctrlpc.py > /home/mrr/logs/watchdog_mrr.log 2>&1
```

# checklist of things to check/change in the scripts
- make sure all scripts are executable by mrr user on the ctrl pc
- make an ssh key pair as mrr user
- add ssh key of ctrl pc to mrr authorised keys
- note need correct permissions on .ssh folder!
- add crontab and check timings and paths

### In config.conf
- paths

### In rsync_mrr2ctrl
- paths
- IP address of MRR

### In sync_data_mrr.py
- path to config file
- set sync_current_month = True

### In delete_data_mrr.py
- days_old

### In watchdog_mrr_ping_kibble.sh
- IP address of mrr
- kibble path

### In watchdog_mrr_ctrlpc.py
- paths

# Watchdog
Since the MRR can not make it's own watchdog kibble, the cntrol pc makes the pc. The script watchdog_mrr_pig_kibble.sh makes a new kibble if the mrr is accessible via a ping on network 1. The script watchdog_mrr_ctrlpc.py checks the age of this kibble and reboots only if network 1 is up.

