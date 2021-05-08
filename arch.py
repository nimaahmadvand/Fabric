from fabric import Connection, task
from termcolor import cprint

c = Connection("host1", user="root", port=22, connect_kwargs={"key_filename":"~/.ssh/id_rsa"})

@task
def partitioning(c):
    cprint('[partitioning]', 'green')
    c.run('parted -s /dev/sda mklabel msdos mkpart primary ext4 1MiB 100%')
    c.run('mkfs.ext4 /dev/sda1')

@task
def pacman(c):
    cprint('[pacman]', 'green')
    c.run('pacman -Syy')
    c.run('pacman -S reflector --noconfirm')
    c.run('reflector -c \'TR\' -f 12 -l 10 -n 12 --save /etc/pacman.d/mirrorlist')

@task
def mounting(c):
    cprint('[mounting]', 'green')
    c.run('mount /dev/sda1 /mnt')

@task
def requirements(c):
    cprint('[requirements]', 'green')
    c.run('pacstrap /mnt base linux linux-firmware nano net-tools')

@task
def fstab(c):
    cprint('[fstab]', 'green')
    c.run('genfstab -U /mnt >> /mnt/etc/fstab')

#@task
#def chroot(c):
#    cprint('[chroot]', 'green')
#    c.run('arch-chroot /mnt')

@task
def script(c):
    cprint('[script]', 'green')
    c.run('touch /mnt/script.sh')
    c.run('chmod +x /mnt/script.sh')

@task
def timezone(c):
    cprint('[timezone]', 'green')
    c.run('echo "#!/bin/bash" > /mnt/script.sh')
    c.run('echo "timedatectl set-timezone Asia/Tehran" >> /mnt/script.sh')
    c.run('arch-chroot /mnt ./script.sh')

@task
def lang(c):
    cprint('[lang]', 'green')
    c.run('echo "#!/bin/bash" > /mnt/script.sh')
    c.run('echo "locale-gen" >> /mnt/script.sh')
    c.run('echo "echo LANG=en_US.UTF-8 > /etc/locale.conf" >> /mnt/script.sh')
    c.run('echo "export LANG=en_US.UTF-8" >> /mnt/script.sh')
    c.run('arch-chroot /mnt ./script.sh')

@task
def hostname(c):
    cprint('[hostname]', 'green')
    c.run('echo "#!/bin/bash" > /mnt/script.sh')
    c.run('echo "echo my-arch-vm > /etc/hostname" >> /mnt/script.sh')
    c.run('arch-chroot /mnt ./script.sh')

@task
def hosts(c):
    cprint('[hosts]', 'green')
    c.run('echo "#!/bin/bash" > /mnt/script.sh')
    c.run('echo "echo \'127.0.0.1    localhost\' >> /etc/hosts\" >> /mnt/script.sh')
    c.run('echo "echo \'127.0.1.1    my-arch-vm\' >> /etc/hosts\" >> /mnt/script.sh')
    c.run('arch-chroot /mnt ./script.sh')

@task
def passwd(c):
    cprint('[passwd]', 'green')
    c.run('echo "#!/bin/bash" > /mnt/script.sh')
    c.run('echo "echo -e \'nima#1377\nnima#1377\n\' | passwd" >> /mnt/script.sh')
    c.run('arch-chroot /mnt ./script.sh')

@task
def bootloader(c):
    cprint('[bootloader]', 'green')
    c.run('echo "#!/bin/bash" > /mnt/script.sh')
    c.run('echo "pacman -S grub  --noconfirm" >> /mnt/script.sh')
    c.run('echo "grub-install /dev/sda" >> /mnt/script.sh')
    c.run('echo "grub-mkconfig -o /boot/grub/grub.cfg" >> /mnt/script.sh')
    c.run('arch-chroot /mnt ./script.sh')

@task
def desktop(c):
    cprint('[desktop]', 'green')
    c.run('echo "#!/bin/bash" > /mnt/script.sh')
    c.run('echo "pacman -S xorg slim slim-themes archlinux-themes-slim xfce4 xfce4-goodies --noconfirm" >> /mnt/script.sh')
    c.run('echo "echo \'exec xfce4-session\' > ~/.xinitrc" >> /mnt/script.sh')
    c.run('echo "systemctl enable slim" >> /mnt/script.sh')
    c.run('arch-chroot /mnt ./script.sh')

@task
def network(c):
    cprint('[network]', 'green')
    c.run('echo "#!/bin/bash" > /mnt/script.sh')
    c.run('echo "pacman -S dhcpcd --noconfirm" >> /mnt/script.sh')
    c.run('echo "systemctl enable dhcpcd.service" >> /mnt/script.sh')
    c.run('arch-chroot /mnt ./script.sh')


@task
def extra(c):
    cprint('[extra]', 'green')
    c.run('echo "#!/bin/bash" > /mnt/script.sh')
    c.run('echo "pacman -S openssh doas vim screenfetch celluloid firefox htop ncdu curl git --noconfirm" >> /mnt/script.sh')
    c.run('echo "systemctl enable sshd" >> /mnt/script.sh')
    c.run('echo "useradd --create-home nahmadvand" >> /mnt/script.sh')
    c.run('echo "echo -e \'nima#1377\nnima#1377\n\' | passwd nahmadvand" >> /mnt/script.sh')
    c.run('echo "echo "permit nahmadvand as root" > /etc/doas.conf" >> /mnt/script.sh')
    c.run('echo "echo \'exec xfce4-session\' > /home/nahmadvand/.xinitrc" >> /mnt/script.sh')
    c.run('arch-chroot /mnt ./script.sh')

@task
def theme(c):
    cprint('[theme]', 'green')
    c.run('wget https://raw.githubusercontent.com/nimaahmadvand/repo/master/theme.tar.gz')
    c.run('tar xvf theme.tar.gz -C /mnt/home/nahmadvand')

@task
def finishing(c):
    cprint('[finishing]', 'green')
    c.run('rm -rf /mnt/script.sh')
    c.run('poweroff')

@task
def all(c):
    partitioning(c)
    pacman(c)
    mounting(c)
    requirements(c)
    fstab(c)
    #chroot(c)
    script(c)
    timezone(c)
    lang(c)
    hostname(c)
    hosts(c)
    passwd(c)
    bootloader(c)
    pacman(c)
    desktop(c)
    network(c)
    extra(c)
    theme(c)
    finishing(c)