import subprocess
import sys
# Import config file
import configparser
config = configparser.ConfigParser()
config.read('/data_movement_scripts/config.conf')


def synchronize_with_ftp(host, username, password, local_dir, remote_dir):
    # Construct the lftp command
    lftp_command = [
        '/usr/bin/lftp',
        '-u', '{},{}'.format(username,password),
        host
    ]
    lftp_script = '''
        mirror --reverse --delete --verbose {} {}
        quit
    '''.format(local_dir,remote_dir)

    try:
        # Execute the lftp command with input from the script
        result = subprocess.run(lftp_command, input=lftp_script.encode(), check=True)
        return result.returncode
    except subprocess.CalledProcessError as e:
        print('Error: {}'.format(e))
        return None


def sync_NAS_OPU(NAS_name, ftp_user, ftp_password, local_folder, remote_folder):
    N = NAS_name
    ftp_host = config['NETWORK_ADDRESS'][ N + '_SW1']
    return_code = synchronize_with_ftp(ftp_host, ftp_user, ftp_password, local_folder, remote_folder)
    
    if return_code == 0:
        # synchronization achieved using the SW1
        print('Synchronization of '+ N +' successful through SW1')

    else:
        # NAS not found in the SW1, try using the SW2
        ftp_host = config['NETWORK_ADDRESS'][ N+'_SW2']
        return_code = synchronize_with_ftp(ftp_host, ftp_user, ftp_password, local_folder, remote_folder)

        if return_code == 0:
            print('Synchronization of '+N+' successful through SW2')
        else:
            print(N+' cannot be reached for database synchronization')

def main():
    
    # Correct the local folder path to make it discoverable by the WSL 
    local_folder = config['PATHS']['data_archive']  # path of your database
    remote_folder = config['PATHS']['NAS_archive_path'] 
    
    # FTP settings
    ftp_user = config['GENERAL']['NAS_ftp_user']
    ftp_password = config['GENERAL']['NAS_ftp_password']

    # Sync with the NAS database   --------------------------
    sync_NAS_OPU('NAS1', ftp_user, ftp_password, local_folder, remote_folder)
    sync_NAS_OPU('NAS2', ftp_user, ftp_password, local_folder, remote_folder)

    sys.exit(0)
    

if __name__ == '__main__':

    main()