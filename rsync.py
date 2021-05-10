from fabric import Connection, task
from termcolor import cprint

for i in ("host1", "host2"):
    c = Connection(i, user="nahmadvand", port=22, connect_kwargs={"key_filename":"~/.ssh/id_rsa"})

@task
def check_backups_dir(c):
    if c.run('test -d /backups', warn=True).failed:
        c.sudo('mkdir /backups')
        c.sudo('chmod ugo+rwx /backups')
    if c.local('test -d ~/backups', warn=True).failed:
        c.local('mkdir ~/backups')

@task
def backup(c):
    cprint('[BACKUP]', 'green')
    c.sudo('rsync -aAXv --delete / --exclude={"/backups/*","/dev/*","/proc/*","/sys/*","/tmp/*","/run/*","/mnt/*","/media/*","/cdrom/*","/lost+found"} /backups/bk')
    #with c.cd("/backups"):               -->
    #    c.sudo('tar -czvf bk.tar.gz bk') --> c.sudo('cd /backups && tar -czvf bk.tar.gz bk') --> sudo: cd: command not found
    with c.cd("/backups"):
        c.run('sudo -S tar -czvf bk.tar.gz bk')
    cprint('------------------------------------------', 'green')
    c.run('cat /etc/hostname && date +%Y-%m-%d')
    cprint('Please enter a name for the backup file: ', 'yellow')
    bk_f_name = 'backups/' + input()
    cprint('downloading the backup files...', 'green')
    c.get('/backups/bk.tar.gz', bk_f_name) #dst --> ~/backups/backup_file_name
    c.sudo('rm -rf /backups/bk')
    c.sudo('rm -rf /backups/bk.tar.gz')

@task
def restore(c):
    cprint('[RESTORE]', 'green')
    c.local('ls -1 ~/backups')
    cprint('Please select a backup file to restore: ', 'yellow')
    restore_file = 'backups/' + input() #src --> ~/backups/backup_file_name
    cprint('pushing the backup files...', 'green')
    c.put(restore_file, '/backups/bk.tar.gz')
    c.sudo('tar --same-owner -xzvf /backups/bk.tar.gz -C /backups')
    c.sudo('rsync -aAXv --delete /backups/bk --exclude={"/backups/*","/dev/*","/proc/*","/sys/*","/tmp/*","/run/*","/mnt/*","/media/*","/cdrom/*","/lost+found"} /')
    c.sudo('rm -rf /backups/bk')
    c.sudo('rm -rf /backups/bk.tar.gz')