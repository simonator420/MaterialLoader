import os
import sys

import c4d
from c4d import plugins, gui
import maxon

REAWOTE_PLUGIN_ID=1056421

ROOT_DIR = os.path.split(__file__)[0]
dialog = None
__res__ = None

# def GetVersion():
#     config = ConfigParser()
#     config.read(os.path.join(PLUGIN_PATH, "version.ini"))
#     return config.get("Version", "PluginVersion")


class SettingsDialog(c4d.gui.GeDialog):

    text_file_path = os.path.join(ROOT_DIR, "renderer.txt")

    def __init__(self):
        super(SettingsDialog, self).__init__()
        pass

    def InitValues(self):
        text_file_path = os.path.join(ROOT_DIR, "renderer.txt")
        f = open(text_file_path, "r")
        print(f.read()) 
        self.SetInt32(2202, 2210)
        return True
    def CreateLayout(self):
        self.SetTitle("PBR Loader Settings")

        self.GroupBegin(2200,  c4d.BFH_SCALEFIT, 2, 1, "Renderer", 0, 10, 10)
        self.GroupBorderSpace(5,5,5,5)
        self.AddStaticText(2201, c4d.BFH_SCALEFIT, 0, 0, "Select Default Renderer", 0)
        renderers = self.AddComboBox(2202, c4d.BFH_SCALEFIT, inith=10, initw=50)
        physical = self.AddChild(renderers, 2210, "Physical")
        corona = self.AddChild(renderers, 2211, "Corona")
        vray = self.AddChild(renderers, 2212, "V-ray")
        redshift = self.AddChild(renderers, 2213, "Redshift")
        octane = self.AddChild(renderers, 2214, "Octane")
        self.GroupEnd()
        
        self.GroupEnd()

        return True

    def Command(self, id, msg):

        return True

def get_dialog():
    global dialog
    return dialog


def main():
    global dialog
    if dialog is None:
        dialog = SettingsDialog()
    if dialog.IsOpen():
        return True
    return dialog.Open(dlgtype=c4d.DLG_TYPE_ASYNC, pluginid=REAWOTE_PLUGIN_ID, defaultw=360, defaulth=380, subid=1)