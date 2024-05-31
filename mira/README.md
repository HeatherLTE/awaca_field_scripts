# Crontabs

```
#mira transfer to nas
20,30,40 1 * * * /usr/bin/python3 /data_movement_scripts/sync_data_mira.py >> /data_movement_scripts/mira2nas.log 2>&1

#mira delete old moments files if safely stored on nas
45 1 * * * /usr/bin/python3 /data_movement_scripts/delete_data_mira.py >> /data_movement_scripts/delete_safe_moments.log 2>&1
```

# checklist of things to check/change in the scripts
- make sure all scripts are executable by data user
- add crontab and check timings and paths

### In config.conf
- paths

### In sync_data_mira.py
- path to config file
- set sync_current_month = True

### In delete_data_mira.py
- days_old


