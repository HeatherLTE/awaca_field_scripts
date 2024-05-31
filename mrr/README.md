# Crontabs

```
#mrr transfer from mrr to ctrl pc with rsync
20, 2 * * * bash /home/mrr/data_movement_scripts/rsync_mrr2ctrl.py >> /home/mrr/data_movement_scripts/mrr_ctrl2nas.log 2>&1

#mrr transfer to nas
25 2 * * * /usr/bin/python3 /home/mrr/data_movement_scripts/sync_data_mrr.py >> /home/mrr/data_movement_scripts/mrr_ctrl2nas.log 2>&1

# delete old moments files if safely stored on nas
45 1 * * * /usr/bin/python3 /home/mrr/data_movement_scripts/delete_data_mrr.py >> /home/mrr/data_movement_scripts/mrr_delete_safe_files.log 2>&1
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

### In sync_data_mrr.py
- path to config file
- set sync_current_month = True

### In delete_data_mrr.py
- days_old


