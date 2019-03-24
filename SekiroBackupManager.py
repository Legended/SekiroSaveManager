from os import popen, chdir, getcwd, listdir, getenv, makedirs
from shutil import copyfile
from datetime import datetime
from win32gui import FindWindow, SetForegroundWindow
from pynput import keyboard

def detect():
    print('Loading Game')
    while True:
        if 'sekiro.exe' in popen('tasklist').read():
            run_script()
            break

def run_script():
    print('Running Script. ALT+F5 to save. ALT+F6 to load.')

    try:
        sekiro = getenv('APPDATA') + '\\Sekiro'
        chdir(sekiro)
        chdir(getcwd() + '\\' + listdir(getcwd())[0])
    except FileNotFoundError as error:
        print(error)

    if 'backup' not in listdir(getcwd()):
        makedirs(getcwd() + '\\backup')

    savefile = 'S0000.sl2'
    console = 'C:\WINDOWS\py.exe'
    console_window = FindWindow(None, console)
    app_name = 'Sekiro'
    app_window = FindWindow(None, app_name)


    combo = {keyboard.Key.alt_l, keyboard.Key.f5}
    save = set()

    combo2 = {keyboard.Key.alt_l, keyboard.Key.f6}
    load = set()

    def on_press(key):

        if key in combo:
            save.add(key)
            if all(k in save for k in combo):
                try:
                    copyfile(getcwd() + '\\' + savefile, getcwd() + '\\backup\\' + savefile)
                    print('[' + str(datetime.now()) + ']' + ' Backup created.')
                except FileNotFoundError as backup_error:
                    print(backup_error)

        if key in combo2:
            load.add(key)
            if all(k in load for k in combo2):
                try:
                    copyfile(getcwd() + '\\backup\\' + savefile, getcwd() + '\\' + savefile)
                    print('[' + str(datetime.now()) + ']' + ' Restored backup.')
                except FileNotFoundError as restore_error:
                    print(restore_error)

    def on_release(key):
        try:
            save.remove(key)
            load.remove(key)
        except KeyError:
            pass

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == '__main__':
    try:
        popen('sekiro.exe')
    except FileNotFoundError as e:
        input(e)
    chdir('C:/Windows/System32')
    detect()
