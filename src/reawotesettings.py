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

class ID():
    DIALOG_GROUP = 2200
    DIALOG_RENDERER_TEXT = 2201
    DIALOG_RENDERER_COMBOBOX = 2202
    DIALOG_OK_BUTTON = 2203

    PHYSICAL_RENDERER = 2210
    CORONA_RENDERER = 2211
    VRAY_RENDERER = 2212
    REDSHIFT_RENDERER = 2213
    OCTANE_RENDERER = 2214


class SettingsDialog(c4d.gui.GeDialog):

    def __init__(self):
        super(SettingsDialog, self).__init__()
        pass

    def InitValues(self):
        text_file_path = os.path.join(ROOT_DIR, "renderer.txt")
        f = open(text_file_path, "r")
        renderer = f.read()
        if renderer == "Physical":
            self.SetInt32(ID.DIALOG_RENDERER_COMBOBOX, ID.PHYSICAL_RENDERER)
        if renderer == "Corona":
            self.SetInt32(ID.DIALOG_RENDERER_COMBOBOX, ID.CORONA_RENDERER)
        if renderer == "V-ray":
            self.SetInt32(ID.DIALOG_RENDERER_COMBOBOX, ID.VRAY_RENDERER)
        if renderer == "Redshift":
            self.SetInt32(ID.DIALOG_RENDERER_COMBOBOX, ID.REDSHIFT_RENDERER)
        if renderer == "Octane":
            self.SetInt32(ID.DIALOG_RENDERER_COMBOBOX, ID.OCTANE_RENDERER)
        print(f"Tohle je renderer{renderer}")
        return True
    def CreateLayout(self):
        self.SetTitle("PBR Loader Settings")

        self.GroupBegin(ID.DIALOG_GROUP,  c4d.BFH_SCALEFIT, 2, 1, "Renderer", 0, 10, 10)
        self.GroupBorderSpace(5, 10, 5, 18)
        self.AddStaticText(ID.DIALOG_RENDERER_TEXT, c4d.BFH_SCALEFIT, 0, 0, "Select Default Renderer", 0)
        renderers = self.AddComboBox(ID.DIALOG_RENDERER_COMBOBOX, c4d.BFH_SCALEFIT, inith=10, initw=50)
        physical = self.AddChild(renderers, ID.PHYSICAL_RENDERER, "Physical")
        corona = self.AddChild(renderers, ID.CORONA_RENDERER, "Corona")
        vray = self.AddChild(renderers, ID.VRAY_RENDERER, "V-ray")
        redshift = self.AddChild(renderers, ID.REDSHIFT_RENDERER, "Redshift")
        octane = self.AddChild(renderers, ID.OCTANE_RENDERER, "Octane")
        self.GroupEnd()
        
        self.AddButton(ID.DIALOG_OK_BUTTON, c4d.BFH_CENTER, 60, 5, "OK")

        return True

    def Command(self, id, msg):

        if id == ID.DIALOG_OK_BUTTON:
            text_file_path = os.path.join(ROOT_DIR, "renderer.txt")
            f = open(text_file_path, "w")
            renderer_combobox = self.GetInt32(ID.DIALOG_RENDERER_COMBOBOX)
            if renderer_combobox == ID.PHYSICAL_RENDERER: 
                f.write("Physical")
            if renderer_combobox == ID.CORONA_RENDERER:
                f.write("Corona")
            if renderer_combobox == ID.VRAY_RENDERER:
                f.write("V-ray")
            if renderer_combobox == ID.REDSHIFT_RENDERER:
                f.write("Redshift")
            if renderer_combobox == ID.OCTANE_RENDERER:
                f.write("Octane")
            self.Close()

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
    return dialog.Open(dlgtype=c4d.DLG_TYPE_ASYNC, pluginid=REAWOTE_PLUGIN_ID, defaultw=360, defaulth=140, subid=1)