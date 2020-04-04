# Telegram Bot to manage torrents in your raspberry

This repository contains the instructions to create a simple bot that manages torrents. It is intended to be deployed on a raspberry and in turn, a streaming server can be installed to play content in your smart TV.

Use carefully and under social and legal responsibility. Be free to improve or modify the code.

## The recipe:
It is a very rudimentary project, but it works. Maybe you need to complement some steps with external tutorials.
You can avoid some steps if you are not a noob:

1. Configure your Raspberry installing Raspbian Buster Lite in your SD card: https://www.raspberrypi.org/downloads/raspbian/
2. In /boot partition of your SD card, create a file named "ssh" ($touch ssh).
3. Connect the Raspberry to your router with a network wired and try to connect via ssh. 
  From your terminal $ssh pi@IP-of-your-raspberry (to obtain the IP check your router) 
  Default user: pi
  Default password: raspberry
4. Update your rasbpian: 

```
sudo apt-get update
```


5. Configure your USB pen or external hard drive 
```
sudo blkid
#check the name partition, in my case: /dev/sda1
sudo mount /dev/sda1 /media/HardDrive -o umask=000
#test it
sudo umount /dev/sda1
```
To automatically mount the device:
```
#get the UUID
sudo blkid
#Add the next line in fstab, and put your UUID!
sudo nano /etc/fstab

    UUID=YOUR_UUID /media/HardDrive auto user,umask=000,utf8, defaults,nofail 0 0
```
Reset and check
```
sudo shutdown -r now
#connect again via ssh
ls /media/HardDrive
#works?
```
5.B Install minidlna (the streaming server). 
```
sudo apt-get install minidlna
```
And change the configuration (feel free):
From /etc/minidlna.conf, I only changes these two lines:
```
sudo nano /etc/minidlna.conf

#media_dir=/var/lib/minidlna
media_dir=PV,/media/HardDrive/
```
And reset the configuration
```
sudo service minidlna restart
```
The media content from /media/HardDrive is available for all your compatible devices connected in your network such as smart TVs, mobiles, etc.

6. Configure your python libs
```
sudo apt-get install python-pip
pip install python-telegram-bot
pip install python-libtorrent
````

7. Create the folders. Feel free to modify all the paths and names of this project.

```
mkdir ~\botcontrol
mkdir ~\botcontrol\logs
touch ~\botcontrol\aDescargar.log  
touch ~\botcontrol\completados.log
touch ~\botcontrol\estado.log
mkdir ~\botcontrol\torrents
```
8. Create a Telegram a bot (https://core.telegram.org/bots) and copy your secret token.

9. Download both python scripts from this repository.

10. Put your token in myBot.py file:
```
TELEGRAM_TOKEN = "YOUR TOKEN"
```
11. For security, all interactions with your bot are wrapped with a user filter. Put your ID-user in myBot.py file: (https://stackoverflow.com/questions/32683992/find-out-my-own-user-id-for-sending-a-message-with-telegram-api)
```
LIST_OF_ADMINS =[YOUR ID USER. It is a number]
```
12. Copy both python files in your raspberry. Be careful with your secret token.
```
scp myBot.py pi@IP:~\botcontrol
scp dwTorrent.py pi@IP:~\botcontrol
```
13. In your raspberry, run mybot.py
```
python myBot.py &
```

14. Open your telegram and chat with your bot


## Bot commands:

   - To download a torrent send/attach in the chat the torrent file (Drag and drop the file). 
   - To see the state.log write: /e #number of lines, for example: /e 10
   - To see the complete.log write: /c #number of lines, for example: /c 3
   - To obtain a list of movies and folder files from /media/HardDrive: /remove
   - To remove a movie or a folder from /media/HardDrive: /remove #id, for example: /remove 10 (The ids is the number of files, this number changes when you remove a file or there is a new file. USE WITH CAUTION! As I said, this project is not elegant...


## Test on:

- Raspbian Buster Lite - Release date:2020-02-13
- python-libtorrent==1.1.11
- python-telegram-bot==12.5.1

