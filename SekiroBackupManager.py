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


    save_hotkey = {keyboard.Key.f5}
    save = set()

    load_hotkey = {keyboard.Key.f6}
    load = set()

    def on_press(key):

        if key in save_hotkey:
            save.add(key)
            if all(k in save for k in save_hotkey):
                try:
                    copyfile(getcwd() + '\\' + savefile, getcwd() + '\\backup\\' + savefile)
                    print('[' + str(datetime.now()) + ']' + ' Backup created.')
                except FileNotFoundError as backup_error:
                    print(backup_error)

        if key in load_hotkey:
            load.add(key)
            if all(k in load for k in load_hotkey):
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
