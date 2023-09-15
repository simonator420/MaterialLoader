import os.path
import sys
import socket

import c4d
from c4d import plugins, bitmaps, threading, gui, PLUGINFLAG_COMMAND_OPTION_DIALOG

import time
import json

ROOT_DIR = os.path.split(__file__)[0]

REAWOTE_PLUGIN_ID=1056421
REAWOTE_APP_PORT=46515

texturepath=""

class CommandThread(c4d.threading.C4DThread):
    def Main(self):
        global texturepath
        src = os.path.join(ROOT_DIR, "src")
        if src not in sys.path: 
            sys.path.append(src)
        import reawotefileloader as ReawoteFileLoader

        # sock = socket.socket()
        # sock.connect(("localhost", REAWOTE_APP_PORT))
        # sock.send("{\"type\": \"registerPlugin\", \"data\": {\"plugin\": \"cinema4d\", \"fullName\": \"Cinema4D - Corona renderer\"}}".encode())
        # while True:
        #     if self.TestBreak():
        #         print("Canceled thread-execution.")
        #         return
        #     msg = sock.recv(512)
        #     if len(msg) > 0:
        #         print(str(msg))
        #         c4d.StatusSetText("Reawote plugin is running" + msg.decode())
        #         data=json.loads(msg)
        #         if data["type"] == "loadMaterial":
        #             newpath=data["data"]["path"]
        #             print("Path is: " + newpath)
        #             if (len(newpath)) > 0:
        #                 texturepath = newpath
        #                 print("TEXTUREPATH WAS SET: " + texturepath)
        #             c4d.SpecialEventAdd(REAWOTE_PLUGIN_ID)
        #     # Tohle nefunguje, jako dalsi krok je tady potreba vyvolat udalost, ktera se preda do hlavniho vlakna
        #     # https://developers.maxon.net/docs/Cinema4DCPPSDK/html/page_manual_cinemathreads.html
        #     # https://plugincafe.maxon.net/topic/10739/14183_creating-custom-callback/3
        #     # https://developers.maxon.net/docs/Cinema4DPythonSDK/html/modules/c4d.documents/BaseDocument/index.html#BaseDocument.InsertMaterial
        #     # https://developers.maxon.net/docs/Cinema4DPythonSDK/html/modules/c4d.threading/index.html

        #     time.sleep(30)
        c4d.StatusClear()

class TimerMessage(c4d.plugins.MessageData):

    def GetTimer(self):
        return 100

    def CoreMessage(self, id, bc):
        global texturepath
        if id == REAWOTE_PLUGIN_ID:
            print("YES")
            print("Path is: " + texturepath)
            import reawotefileloader as ReawoteFileLoader
            loader=ReawoteFileLoader.ReawoteFileLoader()
            loader.materialFolder=texturepath
            loader.HandleLoadMaterial()
        return True
    
if __name__=='__main__':
    src = os.path.join(ROOT_DIR, "src")
    if src not in sys.path: 
        sys.path.append(src)
    import reawotematerialloader as ReawoteMaterialLoader

    icon = c4d.bitmaps.BaseBitmap()
    icon.InitWith(os.path.join(ROOT_DIR, "res", "images", "icon.png"))

    loader=ReawoteMaterialLoader.ReawoteMaterialLoader()
    loader.thread=CommandThread()
    
    c4d.plugins.RegisterMessagePlugin(id=1234567, str="", info=0, dat=TimerMessage())

    c4d.plugins.RegisterCommandPlugin(id=REAWOTE_PLUGIN_ID, 
        str="Reawote PBR Loader",
        help="HELP",
        dat=loader, 
        info=0, 
        icon=icon)
    
    loader.thread.Start()
