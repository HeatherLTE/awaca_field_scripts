# Folder Structure

### On the MIRA PC
Make the following directories on the mira pc: \
/home/data/awaca_scriptsnlogs \
/home/data/awaca_scriptsnlogs/scripts \
/home/data/awaca_scriptsnlogs/logs \
/home/data/awaca_scriptsnlogs/watchdog \
/home/data/awaca_scriptsnlogs/quicklooks_plots 

Add the following files to the scripts folder: \
config.conf \
sync_data_mira.py \
delete_data_mira.py \
watchdog_mira_local.py \
rsync_recent_mrr2mira.sh 

Add the whole quicklooks_scripts folder to the scripts folder

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
# AWACA data movement
#mira transfer to nas
20,30,40 1 * * * /usr/bin/python3 /home/data/awaca_scriptsnlogs/scripts/sync_data_mira.py >> /home/data/awaca_scriptsnlogs/logs/mira2nas.log 2>&1

# mira delete old moments files if safely stored on nas
45 1 * * * /usr/bin/python3 /home/data/awaca_scriptsnlogs/scripts/delete_data_mira.py >> /home/data/awaca_scriptsnlogs/logs/delete_safe_moments.log 2>&1

# mira watchdog local kibble creation and sync to ctrlpc
5,35 * * * * /usr/bin/python3 /home/data/awaca_scriptsnlogs/scripts/watchdog_mira_local.py

# sync recent data from the mrr for quicklook creation
2 * * * * bash /home/data/awaca_scriptsnlogs/scripts/rsync_recent_mrr2mira.sh >> /home/data/awaca_scriptsnlogs/logs/rsync_recent_mrr2mira.log 2>&1

#quicklooks using a conda python environment
SHELL=/bin/bash
BASH_ENV=~/.bashrc_conda
5 * * * * conda activate quicklook_env; python3 /home/data/awaca_scriptsnlogs/quicklooks_scripts/plot_quicklooks_mira.py >> /home/data/awaca_scriptsnlogs/logs/quicklooks_mira.log 2>&1
10 * * * * conda activate quicklook_env; python3 /home/data/awaca_scriptsnlogs/quicklooks_scripts/plot_quicklooks_mrr.py >> /home/data/awaca_scriptsnlogs/logs/quicklooks_mira.log 2>&1


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

### In rsync_recent_mrr2mira.sh
- mrr ip
- check paths

# Watchdog
The script on the MIRA pc makes a local kibble file in the watchdog folder and syncs it to the 2 control pcs via ftp. The script should be run every 30 minutes. The sync to the control pc is untested!

The script on the control PC checks the age of the kibble and powers the mira relay off and on if the kibble is too old. This script is untested!

# Quicklooks
The quicklooks are created using the python scripts in the quicklooks_scripts folder. Since xarray is required, the script run in a conda environemnet. The mrr quicklooks are also made on the mira pc. For this the mrr data from the last 2 days are synced to the mira pc using rsync_recent_mrr2mira.sh. Only the last 2 days of mrr data are stored on the mira pc.

## Installing conda on the MIRA PC
Either download the correct .sh file directly from the repo, or copy from another computer if no internet.
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

## Setting up conda environment
The required packages for the quicklooks scripts are numpy, pandas, netdf4, xarray, matplotlib
The environment can be made from the .yml file if the computer has access to the internet:
```
conda env create -f quicklook_env.yml
```
If the computer does not have internet, the folder for the environment can be copied from Heather's laptop to the mira pc and unzipped.
This creates the environment
```
scp quicklook_env.zip data@IPMIRA:/home/data/anaconda3/envs/
```
```
cd /home/data/anaconda3/envs/
unzip quicklook_env.zip
```
The quicklooks can then be run 'hands-on' with 
```
conda activate quicklook_env
cd ~/awaca_scriptsnlogs/quicklooks_scripts
python3 plot_quicklooks_mira.py
python3 plot_quicklooks_mrr.py
```
Remember to check and change the paths and overwrite options at the start of the script.

## Quicklooks automatic operation
The conda environment must be used to run the quicklook scripts.
Follow the instructions in https://stackoverflow.com/questions/36365801/run-a-crontab-job-using-an-anaconda-env i.e
- copy the conda snippet from the end of the .bashrc file to a new file .bashrc_conda:
```
cd ~
cat .bashrc #copy the conda snippet
nano .bashrc_conda #paste the conda snippet
```
- make sure the crontab uses the correct bashrc file and activates the environment (see crontab above)



