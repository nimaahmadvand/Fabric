from fabric import Connection, task

ip = input("target ip address : 192.168.1.")
c = Connection("192.168.1."+ip, user="nahmadvand", port=22, connect_kwargs={"password":"nima#1377"})

@task
def update(c):
    c.sudo('apt update')

@task
def install_barrier(c):
    c.sudo('apt install barrier -y')

@task
def install_brave(c):
    c.sudo('apt install apt-transport-https curl -y')
    c.sudo('curl -fsSLo /usr/share/keyrings/brave-browser-archive-keyring.gpg https://brave-browser-apt-release.s3.brave.com/brave-browser-archive-keyring.gpg')
    c.sudo('echo "deb [signed-by=/usr/share/keyrings/brave-browser-archive-keyring.gpg arch=amd64] https://brave-browser-apt-release.s3.brave.com/ stable main"|sudo tee /etc/apt/sources.list.d/brave-browser-release.list')
    c.sudo('apt update')
    c.sudo('apt install brave-browser -y')

@task
def install_celluloid(c):
    c.sudo('add-apt-repository ppa:xuzhen666/gnome-mpv -y')
    c.sudo('apt update')
    c.sudo('apt install celluloid -y')

@task
def install_other_things(c):
    c.sudo('apt install vim tmux screenfetch kget kazam -y')

@task
def disable_snap(c):
    c.sudo('systemctl disable snapd.service')
    c.sudo('systemctl stop snapd.service')

@task
def all(c):
    update(c)
    install_barrier(c)
    install_brave(c)
    install_celluloid(c)
    install_other_things(c)
    disable_snap(c)