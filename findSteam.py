import os
import winreg
import win32api
import win32com.client


# https://stackoverflow.com/a/73012757/19789649
def findSteam():
    def read_reg(ep, p=r"", k=''):
        try:
            key = winreg.OpenKeyEx(ep, p)
            value = winreg.QueryValueEx(key,k)
            if key:
                winreg.CloseKey(key)
            return value[0]
        except Exception as e:
            return None

    Path1 = "{}\\Microsoft\\Windows\\Start Menu\\Programs\\Steam\\Steam.lnk".format(os.getenv('APPDATA'))
    if os.path.exists(Path1):

        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(Path1)
        Path1Res = shortcut.Targetpath
    else:
        Path1Res = None
    Path2 = str(read_reg(ep = winreg.HKEY_LOCAL_MACHINE, p = r"SOFTWARE\Wow6432Node\Valve\Steam", k = 'InstallPath'))+r"\steam.exe"
    Path3 = str(read_reg(ep = winreg.HKEY_LOCAL_MACHINE, p = r"SOFTWARE\Valve\Steam", k = 'InstallPath'))+r"\steam.exe"
    if not os.path.exists(Path2):
        Path2 = None
    if not os.path.exists(Path3):
        Path3 = None
    PossiblePaths = [r"X:\Steam\steam.exe", r"X:\Program Files\Steam\steam.exe", r"X:\Program Files (x86)\Steam\steam.exe"]
    ValidHardPaths = []
    for Drive in win32api.GetLogicalDriveStrings().split('\000')[:-1]:
        Drive = Drive.replace(':\\', '')
        for path in PossiblePaths:
            path = path.replace("X", Drive)
            if os.path.exists(path):
                ValidHardPaths.append(path)
    it = [Path2, Path1Res, Path3]
    if len(ValidHardPaths) > 0:
        it.extend(ValidHardPaths)
    for i in it:
        if i is not None:
            return os.path.join(os.path.dirname(i), "steamapps")
