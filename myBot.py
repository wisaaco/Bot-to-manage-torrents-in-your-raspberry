import os
from functools import wraps
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
import time
import subprocess
import glob


TELEGRAM_TOKEN = "SECRET_TOKEN"
LIST_OF_ADMINS =[YOU_USER_ID]

def click():
    #py.click()
    return "Accion realizada"

def restricted(func):
    """
    This decorator restricts access of a command to users specified in
    LIST_OF_ADMINS.
    Taken from: https://git.io/v5KpI
    """
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in LIST_OF_ADMINS:
            print("Unauthorized access denied for {}.".format(user_id))
            # tell the unauthorized user to go away
            update.message.reply_text('Go away.')
            return
        return func(bot, update, *args, **kwargs)
    return wrapped


def hello(bot, update):
    """
    Greet the user with their first name and Telegram ID.
    """
    user_firstname = update.message.from_user.first_name
    user_id = update.message.from_user.id
    return update.message.reply_text(
        'Hello {}, your Telegram ID is {}'.format(user_firstname, user_id)
    )

@restricted
def click_handler(bot,update,args):
    return update.message.reply_text(click())

@restricted
def document_handler(bot,update):
    update.message.reply_text("Ok, descargando...")
    file_id = update.message.document
#    update.message.reply_text("file_id0: " + str(file_id))
    filed = bot.getFile(update.message.document.file_id)
    name_file = update.message.caption+".torrent"
    if name_file == ".torrent":
        name_file  = file_id["file_name"]
    filed.download("torrents/"+name_file)    
    update.message.reply_text(update.message.caption)    
    filelog = open('logs/aDescargar.log', 'a+')
    process = runCommand("torrents/"+name_file,update) #TODO catch control error in running command
    print(process.pid)
    datestamp = time.strftime('%Y%m%d%H%M%S')
    filelog.write("%s, file: %s, PID: %i\n" %(datestamp,name_file,process.pid))
    filelog.close()

def runCommand(arg1,update):
    cmd = ["python","dwTorrent.py",str(arg1)]
    update.message.reply_text(cmd)
    with open(os.devnull, 'w') as devnull:
        proc = subprocess.Popen(cmd,stdout=devnull,stderr=devnull)
    return proc
 

def tail(f, lines=1, _buffer=4098):
    """Tail a file and get X lines from the end"""
    lines_found = []
    block_counter = -1
    while len(lines_found) < lines:
        try:
            f.seek(block_counter * _buffer, os.SEEK_END)
        except IOError:  
            f.seek(0)
            lines_found = f.readlines()
            break

        lines_found = f.readlines()
        block_counter -= 1
    return lines_found[-lines:]

@restricted
def estado_handler(bot,update,args):
    update.message.reply_text("State: "+str(args[0])) 
    filelog = open('logs/estado.log', 'r')
    if len(args) == 1:
        if args[0].isdigit():            
            lines = tail(filelog,int(args[0]))
    else:
        lines = tail(filelog)
    filelog.close()
    texto = ""
    for l in lines:
        if len(l)>2:
            texto = texto + l + "\n"
    return update.message.reply_text(texto)
    
@restricted
def completado_handler(bot,update,args):
    update.message.reply_text("Completed: "+str(args[0])) 
    filelog = open('logs/completados.log', 'r')
    if len(args) == 1:
        if args[0].isdigit():            
            lines = tail(filelog,int(args[0]))
    else:
        lines = tail(filelog)
    filelog.close()
    texto = ""
    for l in lines:
        if len(l)>2:
            texto = texto + l + "\n"
    return update.message.reply_text(texto)

@restricted
def removefiles(bot,update,args):
    mypath = "/media/HardDrive/"
    
    mylist1 = [f for f in glob.glob(mypath+"*.mp4")]
    mylist2 = [f for f in glob.glob(mypath+"*.mkv")]
    folders = [f for f in glob.glob(mypath + "**/")]
    allfiles = mylist1 + mylist2 + folders


    if len(args) == 1:
        if args[0].isdigit():
            idx = int(args[0])
            pathToRemove = allfiles[idx]
            if pathToRemove[-1]=="/":
                os.rmdir(pathToRemove)             
                return update.message.reply_text("Removing directory: %s" % allfiles[idx])
            else:
                os.remove(pathToRemove)
                return update.message.reply_text("Removing file: %s" % allfiles[idx])
    else:

        texto=""
        for e,l in enumerate(allfiles):
                texto +="%s\t%s\n"%(e,str(l).replace(mypath,""))

        return update.message.reply_text(texto)

 
if __name__ == '__main__':
    updater = Updater(TELEGRAM_TOKEN)

    updater.dispatcher.add_handler(
        CommandHandler('hello', hello)
    )
    updater.dispatcher.add_handler(
        CommandHandler('c', completado_handler, pass_args=True)
    )
    
    updater.dispatcher.add_handler(
        CommandHandler('e', estado_handler, pass_args=True)
    )
    
    updater.dispatcher.add_handler(
        CommandHandler('remove', removefiles, pass_args=True)
    )
        
    updater.dispatcher.add_handler(
        MessageHandler(Filters.document,document_handler))
    
    
    updater.start_polling()
    updater.idle()
