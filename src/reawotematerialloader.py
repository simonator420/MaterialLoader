import os
import sys

import c4d
from c4d import plugins, gui, storage, documents

REAWOTE_PLUGIN_ID=1056421

dialog = None

checkbox_list = []
same_path_dirs = []
material_to_add = []
path = ""

ID_CHECKBOX = 999
ID_NAME = 998
ID_OTHER = 997

IDS_REAWOTE_PBR_CONVERTER = 10000
IDS_DIALOG_BROWSE = 10001
IDS_DIALOG_TEXTURE_FOLDER = 10002

IDS_DIALOG_MAIN_GROUP = 10014
IDS_DIALOG_SCROLL_GROUP = 10012
IDS_DIALOG_SCROLL_GROUP_TWO = 10016
IDS_DIALOG_SECONDARY_GROUP = 10015
IDS_DIALOG_LIST_CHECKBOX = 10011
IDS_DIALOG_LIST_BUTTON = 10017
IDS_DIALOG_SELECT_ALL_BUTTON = 10018
IDS_DIALOG_FOLDER_LIST = 10013

IDS_DIALOG_INCLUDE_AO = 10003
IDS_DIALOG_INCLUDE_DISPLACEMENT = 10004
IDS_DIALOG_USE_16_BIT_DISPLACEMENT_MAPS = 10005
IDS_DIALOG_LOAD = 10006
IDS_DIALOG_USE_16_BIT_NORMAL_MAPS = 10007

class ID(): 
    DIALOG_FOLDER_GROUP = 100000
    DIALOG_FOLDER_TEXT =  100001
    DIALOG_FOLDER_BUTTON = 100002
    # TODO zde pridat textove pole se slozkama


    DIALOG_MAIN_GROUP = 100014
    DIALOG_SCROLL_GROUP = 100012
    DIALOG_SCROLL_GROUP_TWO = 100016
    DIALOG_SECONDARY_GROUP = 10011
    DIALOG_FOLDER_LIST = 100015
    DIALOG_LIST_BUTTON = 100017
    DIALOG_LIST_CHECKBOX = 100013
    DIALOG_SELECT_ALL_BUTTON = 100018

    DIALOG_MAP_AO_CB = 100003
    DIALOG_MAP_DISPL_CB = 100004
    DIALOG_MAP_16B_DISPL_CB = 100005
    DIALOG_MAP_IOR_CB = 100006
    DIALOG_LOAD_BUTTON = 100007
    DIALOG_ERROR = 100008
    DIALOG_MAP_16B_NORMAL_CB = 100009

    # Todo: generate this with swig
    PLUGINID_CORONA4D_MATERIAL = 1032100
    PLUGINID_CORONA4D_NORMALSHADER = 1035405
    PLUGINID_CORONA4D_AOSHADER = 1034433

    CORONA_MATERIAL_PREVIEWSIZE = 4050
    CORONA_MATERIAL_PREVIEWSIZE_1024 = 10

    CORONA_DIFFUSE_TEXTURE = 4301
    CORONA_NORMALMAP_TEXTURE = 11321

    CORONA_MATERIAL_BUMPMAPPING = 4108
    CORONA_BUMPMAPPING_STRENGTH = 4850
    CORONA_BUMPMAPPING_TEXTURE = 4851

    CORONA_MATERIAL_DISPLACEMENT = 4106
    CORONA_DISPLACEMENT_TEXTURE = 4802
    CORONA_DISPLACEMENT_MIN_LEVEL = 4800
    CORONA_DISPLACEMENT_MAX_LEVEL = 4801

    CORONA_AO_UNOCCLUDED_TEXTURE = 11021
    CORONA_AO_CALCULATE_FROM = 11007
    CORONA_AO_CALCULATE_FROM_BOTH = 2

    CORONA_MATERIAL_ALPHA = 4109
    CORONA_ALPHA_TEXTURE = 4751

    CORONA_REFLECT_GLOSSINESS_TEXTURE = 4512

    CORONA_MATERIAL_REFLECT = 4103
    CORONA_REFLECT_TEXTURE = 4501

    CORONA_MATERIAL_VOLUME = 4110
    CORONA_VOLUME_SCATTER_TEXTURE = 4681
    CORONA_VOLUME_ABSORPTION_TEXTURE = 4631

    CORONA_REFLECT_FRESNELLOR_VALUE = 4541
    CORONA_REFLECT_FRESNELLOR_TEXTURE = 4542

    
    CORONA_STR_MATERIAL_PHYSICAL = 1056306
    CORONA_PHYSICAL_MATERIAL_HEADER = 20000

    CORONA_PHYSICAL_MATERIAL_GENERAL         = 20001
    CORONA_PHYSICAL_MATERIAL_BASE_LAYER      = 20002
    CORONA_PHYSICAL_MATERIAL_REFRACT         = 20003
    CORONA_PHYSICAL_MATERIAL_ALPHA           = 20004
    CORONA_PHYSICAL_MATERIAL_DISPLACEMENT    = 20005
    CORONA_PHYSICAL_MATERIAL_CLEARCOAT       = 20006
    CORONA_PHYSICAL_MATERIAL_SHEEN           = 20007
    CORONA_PHYSICAL_MATERIAL_VOLUMETRICS     = 20008
    CORONA_PHYSICAL_MATERIAL_SSS             = 20009
    CORONA_PHYSICAL_MATERIAL_EMISSION        = 20010
    CORONA_PHYSICAL_MATERIAL_THIN_ABSORPTION = 20012
    CORONA_PHYSICAL_MATERIAL_TRANSLUCENCY    = 20013

    ID_CORONA_PHYSICAL_MATERIAL_GENERAL         = 20051
    ID_CORONA_PHYSICAL_MATERIAL_BASE_LAYER      = 20052
    ID_CORONA_PHYSICAL_MATERIAL_REFRACT         = 20053
    ID_CORONA_PHYSICAL_MATERIAL_ALPHA           = 20054
    ID_CORONA_PHYSICAL_MATERIAL_DISPLACEMENT    = 20055
    ID_CORONA_PHYSICAL_MATERIAL_CLEARCOAT       = 20056
    ID_CORONA_PHYSICAL_MATERIAL_SHEEN           = 20057
    ID_CORONA_PHYSICAL_MATERIAL_VOLUMETRICS     = 20058
    ID_CORONA_PHYSICAL_MATERIAL_SSS             = 20059
    ID_CORONA_PHYSICAL_MATERIAL_EMISSION        = 20060
    ID_CORONA_PHYSICAL_MATERIAL_THIN_ABSORPTION = 20062
    ID_CORONA_PHYSICAL_MATERIAL_TRANSLUCENCY    = 20063

    CORONA_PHYSICAL_MATERIAL_METALLIC_MODE            = 20101
    CORONA_PHYSICAL_MATERIAL_METALLIC_MODE_VALUE      = 20102
    CORONA_PHYSICAL_MATERIAL_METALLIC_MODE_METALLIC   = 0
    CORONA_PHYSICAL_MATERIAL_METALLIC_MODE_DIELECTRIC = 1
    CORONA_PHYSICAL_MATERIAL_METALLIC_MODE_TEXTURE    = 20103

    CORONA_PHYSICAL_MATERIAL_PRESET           = 20104
    CORONA_PHYSICAL_MATERIAL_PRESET_NO_PRESET = 0 #Used when any presetable param is changed by the user
    CORONA_PHYSICAL_MATERIAL_PRESET_DEFAULT = 1 #Default settings


    CORONA_PHYSICAL_MATERIAL_BASE_COLOR                 = 20201
    CORONA_PHYSICAL_MATERIAL_BASE_COLOR_TEXTURE         = 20202
    CORONA_PHYSICAL_MATERIAL_BASE_COLOR_LEVEL           = 20203
    CORONA_PHYSICAL_MATERIAL_BASE_COLOR_MIX_VALUE       = 20204
    CORONA_PHYSICAL_MATERIAL_BASE_COLOR_MIX_MODE        = 20205
    CORONA_PHYSICAL_MATERIAL_BASE_ROUGHNESS             = 20207
    CORONA_PHYSICAL_MATERIAL_BASE_ROUGHNESS_VALUE       = 20208
    CORONA_PHYSICAL_MATERIAL_BASE_ROUGHNESS_TEXTURE     = 20209
    CORONA_PHYSICAL_MATERIAL_BASE_IOR                   = 20210
    CORONA_PHYSICAL_MATERIAL_BASE_IOR_VALUE             = 20211
    CORONA_PHYSICAL_MATERIAL_BASE_IOR_TEXTURE           = 20212
    CORONA_PHYSICAL_MATERIAL_BASE_EDGECOLOR             = 20226
    CORONA_PHYSICAL_MATERIAL_BASE_EDGECOLOR_COLOR       = 20227
    CORONA_PHYSICAL_MATERIAL_BASE_EDGECOLOR_TEXTURE     = 20228
    CORONA_PHYSICAL_MATERIAL_BASE_EDGECOLOR_LEVEL       = 20229
    CORONA_PHYSICAL_MATERIAL_BASE_EDGECOLOR_MIX_VALUE   = 20230
    CORONA_PHYSICAL_MATERIAL_BASE_EDGECOLOR_MIX_MODE    = 20231
    CORONA_PHYSICAL_MATERIAL_BASE_BUMPMAPPING           = 20216
    CORONA_PHYSICAL_MATERIAL_BASE_BUMPMAPPING_VALUE     = 20217
    CORONA_PHYSICAL_MATERIAL_BASE_BUMPMAPPING_TEXTURE   = 20218
    CORONA_PHYSICAL_MATERIAL_BASE_BUMPMAPPING_ENABLE    = 20225
    CORONA_PHYSICAL_MATERIAL_BASE_ANISOTROPY            = 20219
    CORONA_PHYSICAL_MATERIAL_BASE_ANISOTROPY_VALUE      = 20220
    CORONA_PHYSICAL_MATERIAL_BASE_ANISOTROPY_TEXTURE    = 20221
    CORONA_PHYSICAL_MATERIAL_BASE_ANISOROTATION         = 20222
    CORONA_PHYSICAL_MATERIAL_BASE_ANISOROTATION_VALUE   = 20223
    CORONA_PHYSICAL_MATERIAL_BASE_ANISOROTATION_TEXTURE = 20224

    CORONA_PHYSICAL_MATERIAL_TRANSLUCENCY_FRACTION         = 21307
    CORONA_PHYSICAL_MATERIAL_TRANSLUCENCY_FRACTION_VALUE   = 21308
    CORONA_PHYSICAL_MATERIAL_TRANSLUCENCY_FRACTION_TEXTURE = 21309
    CORONA_PHYSICAL_MATERIAL_TRANSLUCENCY_COLOR_TITLE      = 21301
    CORONA_PHYSICAL_MATERIAL_TRANSLUCENCY_COLOR            = 21302
    CORONA_PHYSICAL_MATERIAL_TRANSLUCENCY_TEXTURE          = 21303
    CORONA_PHYSICAL_MATERIAL_TRANSLUCENCY_LEVEL            = 21304
    CORONA_PHYSICAL_MATERIAL_TRANSLUCENCY_MIX_VALUE        = 21305
    CORONA_PHYSICAL_MATERIAL_TRANSLUCENCY_MIX_MODE         = 21306

    CORONA_PHYSICAL_MATERIAL_REFRACT_AMOUNT           = 20301
    CORONA_PHYSICAL_MATERIAL_REFRACT_AMOUNT_VALUE     = 20302
    CORONA_PHYSICAL_MATERIAL_REFRACT_AMOUNT_TEXTURE   = 20303
    CORONA_PHYSICAL_MATERIAL_REFRACT_BEHAVIOR         = 20311
    CORONA_PHYSICAL_MATERIAL_REFRACT_CAUSTICS         = 20312
    CORONA_PHYSICAL_MATERIAL_REFRACT_THIN             = 20313
    CORONA_PHYSICAL_MATERIAL_REFRACT_DISPERSION       = 20314
    CORONA_PHYSICAL_MATERIAL_REFRACT_DISPERSION_VALUE = 20315
    CORONA_PHYSICAL_MATERIAL_REFRACT_ABBE_NUMBER      = 20316

    CORONA_PHYSICAL_MATERIAL_ALPHA_COLOR     = 20401
    CORONA_PHYSICAL_MATERIAL_ALPHA_TEXTURE   = 20402
    CORONA_PHYSICAL_MATERIAL_ALPHA_LEVEL     = 20403
    CORONA_PHYSICAL_MATERIAL_ALPHA_MIX_VALUE = 20404
    CORONA_PHYSICAL_MATERIAL_ALPHA_MIX_MODE  = 20405
    CORONA_PHYSICAL_MATERIAL_ALPHA_CLIP      = 20407

    CORONA_PHYSICAL_MATERIAL_DISPLACEMENT_MIN_LEVEL           = 20501
    CORONA_PHYSICAL_MATERIAL_DISPLACEMENT_MAX_LEVEL           = 20502
    CORONA_PHYSICAL_MATERIAL_DISPLACEMENT_TEXTURE             = 20503
    CORONA_PHYSICAL_MATERIAL_DISPLACEMENT_WATER_LEVEL_ENABLE  = 20504
    CORONA_PHYSICAL_MATERIAL_DISPLACEMENT_WATER_LEVEL         = 20505
    CORONA_PHYSICAL_MATERIAL_DISPLACEMENT_MODE                = 20506
    CORONA_PHYSICAL_MATERIAL_DISPLACEMENT_MODE_NORMAL         = 0
    CORONA_PHYSICAL_MATERIAL_DISPLACEMENT_MODE_VECTOR_TANGENT = 1
    CORONA_PHYSICAL_MATERIAL_DISPLACEMENT_MODE_VECTOR_OBJECT  = 2

    CORONA_PHYSICAL_MATERIAL_CLEARCOAT_AMOUNT               = 20601
    CORONA_PHYSICAL_MATERIAL_CLEARCOAT_AMOUNT_VALUE         = 20602
    CORONA_PHYSICAL_MATERIAL_CLEARCOAT_AMOUNT_TEXTURE       = 20603
    CORONA_PHYSICAL_MATERIAL_CLEARCOAT_ROUGHNESS            = 20604
    CORONA_PHYSICAL_MATERIAL_CLEARCOAT_ROUGHNESS_VALUE      = 20605
    CORONA_PHYSICAL_MATERIAL_CLEARCOAT_ROUGHNESS_TEXTURE    = 20606
    CORONA_PHYSICAL_MATERIAL_CLEARCOAT_IOR                  = 20607
    CORONA_PHYSICAL_MATERIAL_CLEARCOAT_IOR_VALUE            = 20608
    CORONA_PHYSICAL_MATERIAL_CLEARCOAT_IOR_TEXTURE          = 20609
    CORONA_PHYSICAL_MATERIAL_CLEARCOAT_ABSORPTION           = 20610
    CORONA_PHYSICAL_MATERIAL_CLEARCOAT_ABSORPTION_COLOR     = 20611
    CORONA_PHYSICAL_MATERIAL_CLEARCOAT_ABSORPTION_TEXTURE   = 20612
    CORONA_PHYSICAL_MATERIAL_CLEARCOAT_ABSORPTION_LEVEL     = 20613
    CORONA_PHYSICAL_MATERIAL_CLEARCOAT_ABSORPTION_MIX_VALUE = 20614
    CORONA_PHYSICAL_MATERIAL_CLEARCOAT_ABSORPTION_MIX_MODE  = 20615
    CORONA_PHYSICAL_MATERIAL_CLEARCOAT_BUMPMAPPING          = 20617
    CORONA_PHYSICAL_MATERIAL_CLEARCOAT_BUMPMAPPING_VALUE    = 20618
    CORONA_PHYSICAL_MATERIAL_CLEARCOAT_BUMPMAPPING_TEXTURE  = 20619
    CORONA_PHYSICAL_MATERIAL_CLEARCOAT_BUMPMAPPING_ENABLE   = 20620


    CORONA_PHYSICAL_MATERIAL_SHEEN_AMOUNT            = 20701
    CORONA_PHYSICAL_MATERIAL_SHEEN_AMOUNT_VALUE      = 20702
    CORONA_PHYSICAL_MATERIAL_SHEEN_AMOUNT_TEXTURE    = 20703
    CORONA_PHYSICAL_MATERIAL_SHEEN_ROUGHNESS         = 20704
    CORONA_PHYSICAL_MATERIAL_SHEEN_ROUGHNESS_VALUE   = 20705
    CORONA_PHYSICAL_MATERIAL_SHEEN_ROUGHNESS_TEXTURE = 20706
    CORONA_PHYSICAL_MATERIAL_SHEEN_COLOR             = 20707
    CORONA_PHYSICAL_MATERIAL_SHEEN_COLOR_VALUE       = 20708
    CORONA_PHYSICAL_MATERIAL_SHEEN_COLOR_TEXTURE     = 20709
    CORONA_PHYSICAL_MATERIAL_SHEEN_COLOR_LEVEL       = 20710
    CORONA_PHYSICAL_MATERIAL_SHEEN_COLOR_MIX_VALUE   = 20711
    CORONA_PHYSICAL_MATERIAL_SHEEN_COLOR_MIX_MODE    = 20712

    CORONA_PHYSICAL_MATERIAL_VOLUME_MODE_VOLUMETRIC        = 20801
    CORONA_PHYSICAL_MATERIAL_VOLUME_MODE_SSS               = 20802
    CORONA_PHYSICAL_MATERIAL_VOLUME_ABSORPTION             = 20803
    CORONA_PHYSICAL_MATERIAL_VOLUME_ABSORPTION_COLOR       = 20804
    CORONA_PHYSICAL_MATERIAL_VOLUME_ABSORPTION_TEXTURE     = 20805
    CORONA_PHYSICAL_MATERIAL_VOLUME_ABSORPTION_LEVEL       = 20806
    CORONA_PHYSICAL_MATERIAL_VOLUME_ABSORPTION_MIX_VALUE   = 20807
    CORONA_PHYSICAL_MATERIAL_VOLUME_ABSORPTION_MIX_MODE    = 20808
    CORONA_PHYSICAL_MATERIAL_VOLUME_ABSORPTION_DISTANCE    = 20810
    CORONA_PHYSICAL_MATERIAL_VOLUME_SCATTER                = 20811
    CORONA_PHYSICAL_MATERIAL_VOLUME_SCATTER_COLOR          = 20812
    CORONA_PHYSICAL_MATERIAL_VOLUME_SCATTER_TEXTURE        = 20813
    CORONA_PHYSICAL_MATERIAL_VOLUME_SCATTER_LEVEL          = 20814
    CORONA_PHYSICAL_MATERIAL_VOLUME_SCATTER_MIX_VALUE      = 20815
    CORONA_PHYSICAL_MATERIAL_VOLUME_SCATTER_MIX_MODE       = 20816
    CORONA_PHYSICAL_MATERIAL_VOLUME_SCATTER_DIRECTIONALITY = 20818
    CORONA_PHYSICAL_MATERIAL_VOLUME_SCATTER_SINGLE         = 20819
    CORONA_PHYSICAL_MATERIAL_VOLUME_SCATTER_OTHER          = 20821

    CORONA_PHYSICAL_MATERIAL_VOLUME_SSS_FRACTION         = 20901
    CORONA_PHYSICAL_MATERIAL_VOLUME_SSS_FRACTION_VALUE   = 20902
    CORONA_PHYSICAL_MATERIAL_VOLUME_SSS_FRACTION_TEXTURE = 20903
    CORONA_PHYSICAL_MATERIAL_VOLUME_SSS_RADIUS           = 20904
    CORONA_PHYSICAL_MATERIAL_VOLUME_SSS_RADIUS_VALUE     = 20905
    CORONA_PHYSICAL_MATERIAL_VOLUME_SSS_RADIUS_TEXTURE   = 20906
    CORONA_PHYSICAL_MATERIAL_VOLUME_SSS                  = 20907
    CORONA_PHYSICAL_MATERIAL_VOLUME_SSS_BLEED            = 20908
    CORONA_PHYSICAL_MATERIAL_VOLUME_SSS_TEXTURE          = 20909
    CORONA_PHYSICAL_MATERIAL_VOLUME_SSS_LEVEL            = 20910
    CORONA_PHYSICAL_MATERIAL_VOLUME_SSS_MIX_VALUE        = 20911
    CORONA_PHYSICAL_MATERIAL_VOLUME_SSS_MIX_MODE         = 20912

    CORONA_PHYSICAL_MATERIAL_EMISSION_COLOR_LEVEL     = 21004
    CORONA_PHYSICAL_MATERIAL_EMISSION_COLOR_MIX_VALUE = 21005
    CORONA_PHYSICAL_MATERIAL_EMISSION_COLOR_MIX_MODE  = 21006
    CORONA_PHYSICAL_MATERIAL_SELFILLUM_NOTE           = 21008

    CORONA_PHYSICAL_MATERIAL_ROUGHNESS_MODE            = 21101
    CORONA_PHYSICAL_MATERIAL_ROUGHNESS_MODE_ROUGHNESS  = 0
    CORONA_PHYSICAL_MATERIAL_ROUGHNESS_MODE_GLOSSINESS = 1

    CORONA_PHYSICAL_MATERIAL_IOR_MODE          = 21109
    CORONA_PHYSICAL_MATERIAL_IOR_MODE_IOR      = 0
    CORONA_PHYSICAL_MATERIAL_IOR_MODE_SPECULAR = 1

    CORONA_PHYSICAL_MATERIAL_COMPLEX_IOR         = 21102
    CORONA_PHYSICAL_MATERIAL_COMPLEX_IOR_ENABLED = 21103
    CORONA_PHYSICAL_MATERIAL_COMPLEX_IOR_R       = 21104
    CORONA_PHYSICAL_MATERIAL_COMPLEX_IOR_G       = 21105
    CORONA_PHYSICAL_MATERIAL_COMPLEX_IOR_B       = 21106
    CORONA_PHYSICAL_MATERIAL_COMPLEX_IOR_ETA     = 21107
    CORONA_PHYSICAL_MATERIAL_COMPLEX_IOR_KAPPA   = 21108

    CORONA_PHYSICAL_MATERIAL_BASE_TAIL         = 21400
    CORONA_PHYSICAL_MATERIAL_BASE_TAIL_VALUE   = 21401
    CORONA_PHYSICAL_MATERIAL_BASE_TAIL_TEXTURE = 21402

    CORONA_PHYSICAL_MATERIAL_ABSORPTION_COLOR     = 21201
    CORONA_PHYSICAL_MATERIAL_ABSORPTION_TEXTURE   = 21202
    CORONA_PHYSICAL_MATERIAL_ABSORPTION_LEVEL     = 21203
    CORONA_PHYSICAL_MATERIAL_ABSORPTION_MIX_VALUE = 21204
    CORONA_PHYSICAL_MATERIAL_ABSORPTION_MIX_MODE  = 21205

    _CORONA_PHYSICAL_MATERIAL_REFRACT_ABSORPTION_COLOR     = 20305
    _CORONA_PHYSICAL_MATERIAL_REFRACT_ABSORPTION_TEXTURE   = 20306
    _CORONA_PHYSICAL_MATERIAL_REFRACT_ABSORPTION_MIX_VALUE = 20308
    _CORONA_PHYSICAL_MATERIAL_REFRACT_ABSORPTION_MIX_MODE  = 20309

    # xnormalshader.h
    CORONA_NORMALMAP_TEXTURE = 11321
    CORONA_NORMALMAP_ = 11319
    CORONA_NORMALMAP_MODE = 11301
    CORONA_NORMALMAP_MODE_TANGENT = 0
    CORONA_NORMALMAP_MODE_OBJECT = 1
    CORONA_NORMALMAP_MODE_WORLD = 2
    CORONA_NORMALMAP_FLIP_R = 11311
    CORONA_NORMALMAP_FLIP_G = 11312
    CORONA_NORMALMAP_FLIP_B = 11313
    CORONA_NORMALMAP_SWAP_RG = 11317
    CORONA_NORMALMAP_BUMP = 11330
    CORONA_NORMALMAP_BUMP_STRENGTH = 11331
    CORONA_NORMALMAP_BUMP_TEXTURE = 11332
    CORONA_NORMALMAP_NOTE = 11338
    CORONA_NORMALMAP_NOTE2 = 11339
    CORONA_NORMALMAP_CUSTOM_UVW_OVERRIDE = 11341
    CORONA_NORMALMAP_CUSTOM_UVW_CHANNEL = 11342

class TextureObject(object):
    texturePath = "TexPath"
    otherData = "OtherData"
    _selected = False

    def __init__(self, texturePath):
        self.texturePath = texturePath
        self.otherData+= texturePath

    @property
    def IsSelected(self):
        return self._selected
 
    def Select(self):
        self._selected = True
 
    def Deselect(self):
        self._selected = False
 
    def __repr__(self):
        return str(self)
 
    def __str__(self):
        return self.texturePath

class ListView(c4d.gui.TreeViewFunctions):
 
    def __init__(self):
        self.listOfTexture = list() # Store all objects we need to display in this list
 
        # # Add some defaults values 
        # t1 = TextureObject("T1")
        # t2 = TextureObject("T2")
        # t3 = TextureObject("T3")
        # t4 = TextureObject("T4")
 
        # self.listOfTexture.extend([t1, t2, t3, t4])
 
 
    def IsResizeColAllowed(self, root, userdata, lColID):
        return True
 
    def IsTristate(self, root, userdata):
        return False
 
    def GetColumnWidth(self, root, userdata, obj, col, area):
        return 80  # All have the same initial width
 
    def IsMoveColAllowed(self, root, userdata, lColID):
        # The user is allowed to move all columns.
        # TREEVIEW_MOVE_COLUMN must be set in the container of AddCustomGui.
        return True
 
    def GetFirst(self, root, userdata):
        rValue = None if not self.listOfTexture else self.listOfTexture[0]
        return rValue
 
    def GetDown(self, root, userdata, obj):
        return None
 
    def GetNext(self, root, userdata, obj):
        rValue = None
        currentObjIndex = self.listOfTexture.index(obj)
        nextIndex = currentObjIndex + 1
        if nextIndex < len(self.listOfTexture):
            rValue = self.listOfTexture[nextIndex]
 
        return rValue
 
    def GetPred(self, root, userdata, obj):
        rValue = None
        currentObjIndex = self.listOfTexture.index(obj)
        predIndex = currentObjIndex - 1
        if 0 <= predIndex < len(self.listOfTexture):
            rValue = self.listOfTexture[predIndex]
 
        return rValue
 
    def GetId(self, root, userdata, obj):
        return hash(obj)
 
    def Select(self, root, userdata, obj, mode):
        if mode == c4d.SELECTION_NEW:
            for tex in self.listOfTexture:
                tex.Deselect()
            obj.Select()
        elif mode == c4d.SELECTION_ADD:
            obj.Select()
        elif mode == c4d.SELECTION_SUB:
            obj.Deselect()
 
    def IsSelected(self, root, userdata, obj):
        return obj.IsSelected
 
    def SetCheck(self, root, userdata, obj, column, checked, msg):
        if checked:
            obj.Select()
        else:
            obj.Deselect()
 
    def IsChecked(self, root, userdata, obj, column):
        if obj.IsSelected:
            return c4d.LV_CHECKBOX_CHECKED | c4d.LV_CHECKBOX_ENABLED
        else:
            return c4d.LV_CHECKBOX_ENABLED
 
    def GetName(self, root, userdata, obj):
        return str(obj) # Or obj.texturePath
 
    def DrawCell(self, root, userdata, obj, col, drawinfo, bgColor):
        if col == ID_OTHER:
            name = obj.otherData
            geUserArea = drawinfo["frame"]
            w = geUserArea.DrawGetTextWidth(name)
            h = geUserArea.DrawGetFontHeight()
            xpos = drawinfo["xpos"]
            ypos = drawinfo["ypos"] + drawinfo["height"]
            drawinfo["frame"].DrawText(name, xpos, ypos - h * 1.1)
 
    def DoubleClick(self, root, userdata, obj, col, mouseinfo):
        c4d.gui.MessageDialog("You clicked on " + str(obj))
        return True
 
    def DeletePressed(self, root, userdata):
        "Called when a delete event is received."
        for tex in reversed(self.listOfTexture):
            if tex.IsSelected:
                self.listOfTexture.remove(tex)

class ReawoteMaterialDialog(gui.GeDialog):
    has16bDisp = False
    has16bNormal = False
    hasDisp = False
    hasAO = False
    hasIor = False
    materialFolder = None

    _treegui = None # Our CustomGui TreeView
    _listView = ListView() # Our Instance of c4d.gui.TreeViewFunctions

    def __init__(self):
        super(ReawoteMaterialDialog, self).__init__()
        pass


    def CreateLayout(self):

        defaultFlags: int = c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT
        scrollflags = c4d.SCROLLGROUP_VERT | c4d.SCROLLGROUP_HORIZ | c4d.SCROLLGROUP_AUTOHORIZ|c4d.SCROLLGROUP_AUTOVERT

        self.SetTitle("REAWOTE PBR converter")

        self.ScrollGroupBegin(ID.DIALOG_SCROLL_GROUP, defaultFlags, c4d.SCROLLGROUP_VERT | c4d.SCROLLGROUP_HORIZ)
        self.GroupBegin(ID.DIALOG_MAIN_GROUP, defaultFlags, 1)

        self.GroupBegin(ID.DIALOG_FOLDER_GROUP, c4d.BFH_SCALEFIT, 2, 1, "Material folder", 0, 10, 10)
        self.AddStaticText(ID.DIALOG_FOLDER_TEXT, c4d.BFH_SCALEFIT, 0, 0, "Material folder", 0)
        self.AddButton(ID.DIALOG_FOLDER_BUTTON, c4d.BFH_SCALEFIT, 1, 1, "Browse")
        self.GroupEnd()

        pathBox = self.AddEditText(ID.DIALOG_FOLDER_LIST,  c4d.BFH_SCALEFIT, inith=10, initw=50)
        cbAO = self.AddCheckbox(ID.DIALOG_MAP_AO_CB, c4d.BFH_SCALEFIT, 1, 1, "Include ambient occlusion (AO) maps")
        cbDispl = self.AddCheckbox(ID.DIALOG_MAP_DISPL_CB, c4d.BFH_SCALEFIT, 1, 1, "Include displacement maps")
        cb16bdispl = self.AddCheckbox(ID.DIALOG_MAP_16B_DISPL_CB, c4d.BFH_SCALEFIT, 1, 1, "Use 16 bit displacement maps (when available)")
        cb16bnormal = self.AddCheckbox(ID.DIALOG_MAP_16B_NORMAL_CB, c4d.BFH_SCALEFIT, 1, 1, "Use 16 bit normal maps (when available)")
        # bLoad = self.AddButton(ID.DIALOG_LOAD_BUTTON, c4d.BFH_SCALEFIT, 1, 1, "Load material")
        strErr = self.AddStaticText(ID.DIALOG_ERROR, c4d.BFH_SCALEFIT, 64, 10, "", 0)
        customgui = c4d.BaseContainer()
        customgui.SetBool(c4d.TREEVIEW_BORDER, c4d.BORDER_THIN_IN)
        customgui.SetBool(c4d.TREEVIEW_HAS_HEADER, True)
        customgui.SetBool(c4d.TREEVIEW_HIDE_LINES, False)
        customgui.SetBool(c4d.TREEVIEW_MOVE_COLUMN, True)
        customgui.SetBool(c4d.TREEVIEW_RESIZE_HEADER, True)
        customgui.SetBool(c4d.TREEVIEW_FIXED_LAYOUT, True)
        customgui.SetBool(c4d.TREEVIEW_ALTERNATE_BG, True)
        customgui.SetBool(c4d.TREEVIEW_CURSORKEYS, True)
        customgui.SetBool(c4d.TREEVIEW_NOENTERRENAME, False)
        # self.AddButton(1001, c4d.BFH_CENTER, name="Add")
        selectMaterials = self.AddButton(ID.DIALOG_LIST_BUTTON, c4d.BFH_SCALEFIT, 1, 1, "Load selected materials")
        self.AddButton(ID.DIALOG_SELECT_ALL_BUTTON, c4d.BFH_LEFT, 70, 5, "Select All")

        self.GroupBegin(ID.DIALOG_SCROLL_GROUP, c4d.BFH_SCALEFIT, 2, 1, "Material folder", 0, 10, 10)
        self.GroupEnd()


        self._treegui = self.AddCustomGui( 9300, c4d.CUSTOMGUI_TREEVIEW, "", c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, 100, 30, customgui)
        if not self._treegui:
            print ("[ERROR]: Could not create TreeView")
            return False
    
        self.GroupEnd(ID.DIALOG_MAIN_GROUP)
        self.GroupEnd(ID.DIALOG_SCROLL_GROUP)
        self.Reset()

        color = c4d.Vector(1, 0, 0)
        # self.SetDefaultColor(strErr, c4d.COLOR_TEXT, color)

        self.SetTimer(1000)

        return True
    
    def InitValues(self):
        self.materialFolder = None
    
        self.has16bDisp = False
        self.has16bNormal = False
        self.hasDisp = False
        self.hasAO = False
        self.hasIor = False
        
        self.SetBool(ID.DIALOG_MAP_AO_CB, False)
        self.Enable(ID.DIALOG_MAP_AO_CB, False)
        self.SetBool(ID.DIALOG_MAP_DISPL_CB, False)
        self.Enable(ID.DIALOG_MAP_DISPL_CB, False)
        self.SetBool(ID.DIALOG_MAP_16B_DISPL_CB, False)
        self.Enable(ID.DIALOG_MAP_16B_DISPL_CB, False)
        self.SetBool(ID.DIALOG_MAP_16B_NORMAL_CB, False)
        self.Enable(ID.DIALOG_MAP_16B_NORMAL_CB, False)
        self.SetBool(ID.DIALOG_MAP_IOR_CB, False)
        self.Enable(ID.DIALOG_MAP_IOR_CB, False)

        self.Enable(ID.DIALOG_LOAD_BUTTON, False)

        self.Enable(ID.DIALOG_LIST_BUTTON, False)
        # self.Enable(ID.DIALOG_SELECT_ALL_BUTTON, False)

        layout = c4d.BaseContainer()
        layout.SetLong(ID_CHECKBOX, c4d.LV_CHECKBOX)
        layout.SetLong(ID_NAME, c4d.LV_TREE)
        # layout.SetLong(ID_OTHER, c4d.LV_USER)
        self._treegui.SetLayout(3, layout)
 
        # Set the header titles.
        self._treegui.SetHeaderText(ID_CHECKBOX, "Check")
        self._treegui.SetHeaderText(ID_NAME, "Name")
        self._treegui.SetHeaderText(ID_OTHER, "Other")
        self._treegui.Refresh()
 
        # Set TreeViewFunctions instance used by our CUSTOMGUI_TREEVIEW
        self._treegui.SetRoot(self._treegui, self._listView, None)

        return True

    def Command(self, id, msg,):

        if id == ID.DIALOG_FOLDER_BUTTON:
            path = c4d.storage.LoadDialog(title="Choose material folder", flags=c4d.FILESELECT_DIRECTORY)
            if path == None:
                return True
            try:
                #python2
                path = path.decode("utf-8")
            except: 
                pass
            
            # TextBox se vyplni cestou do vybrane slozky
            self.SetString(ID.DIALOG_FOLDER_LIST, path)

            print(path)
            # ulozeni vsech souboru a slozek v ceste do slozky
            dir = os.listdir(path)

            same_path_dirs = [d for d in dir if os.path.isdir(os.path.join(path, d)) and d.startswith(os.path.basename(path))]

            folder_dict = {}
            checkbox_dict = {}
            targetFolders = ["1K", "2K", "3K", "4K", "5K", "6K", "7K", "8K", "9K", "10K", "11K", "12K", "13K", "14K", "15K", "16K"]
            
            for index, folder in enumerate(sorted(same_path_dirs)):
                folder_path = os.path.join(path, folder)
                subdirs = [subdir for subdir in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, subdir))]
                folder_dict[folder] = True
                # Add data to our DataStructure (ListView)
                newID = len(self._listView.listOfTexture) + 1 
                tex = TextureObject(folder.format(newID))
                self._listView.listOfTexture.append(tex)
                checkbox_list.append(tex)
                print(f"{folder} checkbox byl vytvořen a přidán do listu")
                print(folder_path)
                print(index)
                print(" ")
                # Refresh the TreeView
                self._treegui.Refresh()
                for targetFolderName in targetFolders:
                    if targetFolderName in subdirs:
                        targetFolder = os.path.join(folder_path, targetFolderName)
                        dirPath = os.listdir(targetFolder)
                        hasColor = False
                        for file in dirPath:
                                try: 
                                    parts = file.split(".")[0].split("_")
                                    manufacturer = parts[0]
                                    productNumber = parts[1]
                                    product = parts[2]
                                    mapID = parts[3]
                                    resolution = parts[4]
                                    if mapID == "DIFF" or mapID == "COLOR" or mapID == "COL":
                                        hasColor = True
                                    if mapID == "DISP16":
                                        self.has16bDisp = True
                                        self.hasDisp = True
                                    if mapID == "DISP":
                                        self.hasDisp = True
                                    if mapID == "AO":
                                        self.hasAO = True
                                    if mapID == "IOR":
                                        self.hasIor = True
                                    if mapID == "NRM16":
                                        self.has16bNormal = True
                                except:
                                    pass
                        if self.hasAO:
                            self.SetBool(ID.DIALOG_MAP_AO_CB, True)
                            self.Enable(ID.DIALOG_MAP_AO_CB, True)
                        if self.hasDisp:
                            self.SetBool(ID.DIALOG_MAP_DISPL_CB, True)
                            self.Enable(ID.DIALOG_MAP_DISPL_CB, True)
                        if self.has16bDisp:
                            self.SetBool(ID.DIALOG_MAP_16B_DISPL_CB, True)
                            self.Enable(ID.DIALOG_MAP_16B_DISPL_CB, True)
                        if self.has16bNormal:
                            self.SetBool(ID.DIALOG_MAP_16B_NORMAL_CB, True)
                            self.Enable(ID.DIALOG_MAP_16B_NORMAL_CB, True)
                        if self.hasIor:
                            self.SetBool(ID.DIALOG_MAP_IOR_CB, False)
                            self.Enable(ID.DIALOG_MAP_IOR_CB, True)
                        if hasColor:
                            self.materialFolder = path
                            self.Enable(ID.DIALOG_LOAD_BUTTON, True)
                            self.SetError("")
                        else:
                            self.SetError("One or more folders do not contain the correct Reawote material.")
                            print(mat, " neobsahuje spravnou slozku")

                # povoli se klikani na Load Selected Materials
                self.Enable(ID.DIALOG_LIST_BUTTON, True)
                # povoli se klikani na Select All
                self.Enable(ID.DIALOG_SELECT_ALL_BUTTON, True)
                # self.Enable(ID.DIALOG_FOLDER_BUTTON, False)

        active_checkbox_list = []

        # pokud se klikne na Browse button
        # if id == 1001:
        #     # cesta do slozky (napr. Kobe se ulozi do path)
        #     path = c4d.storage.LoadDialog(title="Choose material folder", flags=c4d.FILESELECT_DIRECTORY)
        #     if path == None:
        #         return True
        #     try:
        #         #python2
        #         path = path.decode("utf-8")
        #     except: 
        #         pass
            
        #     # TextBox se vyplni cestou do vybrane slozky
        #     self.SetString(ID.DIALOG_FOLDER_LIST, path)

        #     print(path)
        #     # ulozeni vsech souboru a slozek v ceste do slozky
        #     dir = os.listdir(path)
            
        #     # nalezeni slozky se stejnym nazvem jako je parent folder
        #     same_path_dirs = [d for d in dir if os.path.isdir(os.path.join(path, d)) and d.startswith(os.path.basename(path))]

        #     folder_dict = {}
        #     checkbox_dict = {}
        #     targetFolders = ["1K", "2K", "3K", "4K", "5K", "6K", "7K", "8K", "9K", "10K", "11K", "12K", "13K", "14K", "15K", "16K"]
        #     # pro vsechny slozky ktere maji stejny nazev jako parent folder
        #     for index, folder in enumerate(sorted(same_path_dirs)):
        #         folder_path = os.path.join(path, folder)
        #         subdirs = [subdir for subdir in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, subdir))]
        #         folder_dict[folder] = True

        #         # pridani checkboxu, ktery ma stejny nazev jako slozka, ktera je prave prochazena
        #         checkbox = self.AddCheckbox(ID.DIALOG_LIST_CHECKBOX, c4d.BFH_SCALEFIT, 1, 1, folder)
        #         # pridani checkboxu do seznamu se vsemi checkboxy
        #         checkbox_list.append(checkbox)
        #         checkbox_dict[folder] = checkbox
        #         print(f"{folder} checkbox byl vytvořen a přidán do listu")
        #         print(index)
        #         print(" ")
        #         for targetFolderName in targetFolders:
        #             if targetFolderName in subdirs:
        #                 targetFolder = os.path.join(folder_path, targetFolderName)
        #                 dirPath = os.listdir(targetFolder)
        #                 hasColor = False
        #                 for file in dirPath:
        #                         try: 
        #                             parts = file.split(".")[0].split("_")
        #                             manufacturer = parts[0]
        #                             productNumber = parts[1]
        #                             product = parts[2]
        #                             mapID = parts[3]
        #                             resolution = parts[4]
        #                             if mapID == "DIFF" or mapID == "COLOR" or mapID == "COL":
        #                                 hasColor = True
        #                             if mapID == "DISP16":
        #                                 self.has16bDisp = True
        #                                 self.hasDisp = True
        #                             if mapID == "DISP":
        #                                 self.hasDisp = True
        #                             if mapID == "AO":
        #                                 self.hasAO = True
        #                             if mapID == "IOR":
        #                                 self.hasIor = True
        #                             if mapID == "NRM16":
        #                                 self.has16bNormal = True
        #                         except:
        #                             pass
        #                 if self.hasAO:
        #                     self.SetBool(ID.DIALOG_MAP_AO_CB, True)
        #                     self.Enable(ID.DIALOG_MAP_AO_CB, True)
        #                 if self.hasDisp:
        #                     self.SetBool(ID.DIALOG_MAP_DISPL_CB, True)
        #                     self.Enable(ID.DIALOG_MAP_DISPL_CB, True)
        #                 if self.has16bDisp:
        #                     self.SetBool(ID.DIALOG_MAP_16B_DISPL_CB, True)
        #                     self.Enable(ID.DIALOG_MAP_16B_DISPL_CB, True)
        #                 if self.has16bNormal:
        #                     self.SetBool(ID.DIALOG_MAP_16B_NORMAL_CB, True)
        #                     self.Enable(ID.DIALOG_MAP_16B_NORMAL_CB, True)
        #                 if self.hasIor:
        #                     self.SetBool(ID.DIALOG_MAP_IOR_CB, False)
        #                     self.Enable(ID.DIALOG_MAP_IOR_CB, True)
        #                 if hasColor:
        #                     self.materialFolder = path
        #                     self.Enable(ID.DIALOG_LOAD_BUTTON, True)
        #                     self.SetError("")
        #                 else:
        #                     self.SetError("One or more folders do not contain the correct Reawote material.")
        #                     print(mat, " neobsahuje spravnou slozku")



        #         # povoli se klikani na Load Selected Materials
        #         self.Enable(ID.DIALOG_LIST_BUTTON, True)
        #         # povoli se klikani na Select All
        #         self.Enable(ID.DIALOG_SELECT_ALL_BUTTON, True)
        #         # self.Enable(ID.DIALOG_FOLDER_BUTTON, False)

        # active_checkbox_list = []

        # pokud se klikne Select All button        
        if id == ID.DIALOG_SELECT_ALL_BUTTON:
            # tak se vsechny checkboxy zaskrtnou
            # for checkbox in checkbox_list:
            #     self.SetBool(checkbox, True)
            for item in checkbox_list:
                item.Select()
                # if item.IsSelected:
                #     print(item)
            self._treegui.Refresh()

        #TODO Select all, Hledani obecne materialu mimo reawote, hledani podle zkratek


        if id == ID.DIALOG_LIST_BUTTON:
            path = self.GetString(ID.DIALOG_FOLDER_LIST)
            dir = os.listdir(path)
            targetFolder = None
            targetFolders = ["1K", "2K", "3K", "4K", "5K", "6K", "7K", "8K", "9K", "10K", "11K", "12K", "13K", "14K", "15K", "16K"]
            same_path_dirs = [d for d in dir if os.path.isdir(os.path.join(path, d)) and d.startswith(os.path.basename(path))]
            same_path_dirs = sorted(same_path_dirs)
            folder_dict = {}
            for index, folder in enumerate(same_path_dirs):
                folder_dict[folder] = True
            for index, checkbox in enumerate(checkbox_list):
                if checkbox.IsSelected:
                    active_checkbox_list.append(index)
                    # zde se ulozi slozka, ktera ma stejny index jako checkbox
                    # musi se to vyresit takhle, protoze checkbox sam o sobe nema stejny nazev jako slozka, index ano
                    folder_name = same_path_dirs[index]
                    # ulozeni slozky, ktera ma stejny nazev jako text u daneho checkboxu
                    folder_path = os.path.join(path, folder_name)
                    print(folder_name)
                    subdirs = [subdir for subdir in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, subdir))]
                    # pro vsechny slozky, ktere obsahuji material (napr 4K, 5K, atd...)
                    for targetFolderName in targetFolders:
                        # pokud je slozka 4K, 5K, atd... v te kterou prochazime
                        if targetFolderName in subdirs:
                            # cesta do slozky s 4K, 5K, atd...
                            targetFolder = os.path.join(folder_path, targetFolderName)
                            print("Slozka s materialem byla nalezena v ceste " + targetFolder)
                            # ulozeni vsech bitmapa ve slozce 4K, 5K, atd...
                            dirPath = os.listdir(targetFolder)
                            hasColor = False
                            if targetFolder is not None:
                                loadAO = self.GetBool(ID.DIALOG_MAP_AO_CB)
                                loadDispl = self.GetBool(ID.DIALOG_MAP_DISPL_CB)
                                load16bdispl = self.GetBool(ID.DIALOG_MAP_16B_DISPL_CB)
                                loadIor = self.GetBool(ID.DIALOG_MAP_IOR_CB)

                                mat = c4d.BaseMaterial(ID.CORONA_STR_MATERIAL_PHYSICAL)
                                mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_ROUGHNESS_MODE, ID.CORONA_PHYSICAL_MATERIAL_ROUGHNESS_MODE_GLOSSINESS, c4d.DESCFLAGS_SET_NONE)
                                mat.SetParameter(ID.CORONA_MATERIAL_PREVIEWSIZE, ID.CORONA_MATERIAL_PREVIEWSIZE_1024, c4d.DESCFLAGS_SET_NONE)
                                mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_BASE_IOR_VALUE, 1.56, c4d.DESCFLAGS_SET_NONE)

                                fusionShader = None

                                dir = os.listdir(targetFolder)
                                for file in dir:
                                    fullPath = os.path.join(targetFolder, file)
                                    # print("Type of fullpath: ", type(fullPath))
                                    parts = file.split(".")[0].split("_")
                                    mapID = parts[3]
                                    if mapID == "COL" or mapID == "COLOR":
                                        mat.SetName("_".join(parts[0:3]))
                                        if not loadAO:
                                            bitmap = c4d.BaseShader(c4d.Xbitmap)
                                            bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
                                            mat.InsertShader(bitmap)
                                            mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_BASE_COLOR_TEXTURE, bitmap, c4d.DESCFLAGS_SET_NONE)
                                        else:
                                            if not fusionShader:
                                                fusionShader = c4d.BaseShader(c4d.Xfusion)
                                                fusionShader.SetParameter(c4d.SLA_FUSION_MODE, c4d.SLA_FUSION_MODE_MULTIPLY, c4d.DESCFLAGS_SET_NONE)
                                                fusionShader.SetParameter(c4d.SLA_FUSION_BLEND, 1.0, c4d.DESCFLAGS_SET_NONE)
                                                mat.InsertShader(fusionShader)
                                                mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_BASE_COLOR_TEXTURE, fusionShader, c4d.DESCFLAGS_SET_NONE)
                                            bitmap = c4d.BaseShader(c4d.Xbitmap)
                                            bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
                                            fusionShader.InsertShader(bitmap)
                                            fusionShader.SetParameter(c4d.SLA_FUSION_BASE_CHANNEL, bitmap, c4d.DESCFLAGS_SET_NONE)
                                    elif mapID == "NRM":
                                        bitmap = c4d.BaseShader(c4d.Xbitmap)
                                        bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
                                        texture = c4d.BaseShader(ID.PLUGINID_CORONA4D_NORMALSHADER)
                                        texture.SetParameter(ID.CORONA_NORMALMAP_TEXTURE, bitmap, c4d.DESCFLAGS_SET_NONE)
                                        texture.SetParameter(ID.CORONA_NORMALMAP_FLIP_G, True, c4d.DESCFLAGS_SET_NONE)
                                        mat.InsertShader(bitmap)
                                        mat.InsertShader(texture)
                                        mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_BASE_BUMPMAPPING_ENABLE, True, c4d.DESCFLAGS_SET_NONE)
                                        mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_BASE_BUMPMAPPING_VALUE, 1.0, c4d.DESCFLAGS_SET_NONE)
                                        mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_BASE_BUMPMAPPING_TEXTURE, texture, c4d.DESCFLAGS_SET_NONE)
                                    elif loadDispl and (load16bdispl and mapID == "DISP16") or (not load16bdispl and mapID == "DISP"):
                                        bitmap = c4d.BaseShader(c4d.Xbitmap)
                                        bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
                                        mat.InsertShader(bitmap)
                                        mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_DISPLACEMENT, True, c4d.DESCFLAGS_SET_NONE)
                                        mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_DISPLACEMENT_TEXTURE, bitmap, c4d.DESCFLAGS_SET_NONE)
                                        mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_DISPLACEMENT_MIN_LEVEL, 0, c4d.DESCFLAGS_SET_NONE)
                                        mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_DISPLACEMENT_MAX_LEVEL, 1, c4d.DESCFLAGS_SET_NONE)
                                    elif loadAO and mapID == "AO":
                                        if not fusionShader:
                                            fusionShader = c4d.BaseShader(c4d.Xfusion)
                                            fusionShader.SetParameter(c4d.SLA_FUSION_MODE, c4d.SLA_FUSION_MODE_MULTIPLY, c4d.DESCFLAGS_SET_NONE)
                                            fusionShader.SetParameter(c4d.SLA_FUSION_BLEND, 1.0, c4d.DESCFLAGS_SET_NONE)
                                            mat.InsertShader(fusionShader)
                                            mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_BASE_COLOR_TEXTURE, fusionShader, c4d.DESCFLAGS_SET_NONE)
                                        bitmap = c4d.BaseShader(c4d.Xbitmap)
                                        bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
                                        fusionShader.InsertShader(bitmap)
                                        fusionShader.SetParameter(c4d.SLA_FUSION_BLEND_CHANNEL, bitmap, c4d.DESCFLAGS_SET_NONE)
                                    elif mapID == "OPAC":
                                        bitmap = c4d.BaseShader(c4d.Xbitmap)
                                        bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
                                        mat.InsertShader(bitmap)
                                        mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_ALPHA, True, c4d.DESCFLAGS_SET_NONE)
                                        mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_ALPHA_TEXTURE, bitmap, c4d.DESCFLAGS_SET_NONE)
                                    elif mapID == "GLOSS":
                                        bitmap = c4d.BaseShader(c4d.Xbitmap)
                                        bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
                                        mat.InsertShader(bitmap)
                                        mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_BASE_ROUGHNESS_TEXTURE, bitmap, c4d.DESCFLAGS_SET_NONE)
                                        mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_BASE_ROUGHNESS_VALUE, 100.0, c4d.DESCFLAGS_SET_NONE)
                                    elif mapID == "REFL":
                                        bitmap = c4d.BaseShader(c4d.Xbitmap)
                                        bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
                                        mat.InsertShader(bitmap)
                                        mat.SetParameter(ID.CORONA_MATERIAL_REFLECT, True, c4d.DESCFLAGS_SET_NONE)
                                        mat.SetParameter(ID.CORONA_REFLECT_TEXTURE, bitmap, c4d.DESCFLAGS_SET_NONE)
                                    elif mapID == "SSS":
                                        bitmap = c4d.BaseShader(c4d.Xbitmap)
                                        bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
                                        mat.InsertShader(bitmap)
                                        mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_SSS, True, c4d.DESCFLAGS_SET_NONE)
                                        mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_VOLUME_SSS_TEXTURE, bitmap, c4d.DESCFLAGS_SET_NONE)
                                    elif mapID == "SSSABSORB":
                                        bitmap = c4d.BaseShader(c4d.Xbitmap)
                                        bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
                                        mat.InsertShader(bitmap)
                                        mat.SetParameter(ID.CORONA_MATERIAL_VOLUME, True, c4d.DESCFLAGS_SET_NONE)
                                        mat.SetParameter(ID.CORONA_VOLUME_ABSORPTION_TEXTURE, bitmap, c4d.DESCFLAGS_SET_NONE)
                                    elif loadIor and mapID == "IOR":
                                        bitmap = c4d.BaseShader(c4d.Xbitmap)
                                        bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
                                        mat.InsertShader(bitmap)
                                        mat.SetParameter(ID.CORONA_REFLECT_FRESNELLOR_TEXTURE, bitmap, c4d.DESCFLAGS_SET_NONE)
                                    elif mapID == "METAL":
                                        bitmap = c4d.BaseShader(c4d.Xbitmap)
                                        bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
                                        mat.InsertShader(bitmap)
                                        mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_METALLIC_MODE_TEXTURE, bitmap, c4d.DESCFLAGS_SET_NONE)

                                    doc = c4d.documents.GetActiveDocument()
                                    doc.StartUndo()
                                    # nevim proc to je bile, ale funguje to takze save
                                    doc.InsertMaterial(mat)
                                    # print("uz to proslo Insertem")
                                    doc.AddUndo(c4d.UNDOTYPE_NEW, mat)
                                    doc.EndUndo()
                                    material_to_add.append(mat)                                   
                                    self.SetString(ID.DIALOG_ERROR, "")
            c4d.EventAdd()

            return True






        # Pokud se klikne na Load Selected Materials
        # if id == ID.DIALOG_LIST_BUTTON:
        #     # tak se do path ulozi cesta ktera je ulozena v CheckBoxu
        #     path = self.GetString(ID.DIALOG_FOLDER_LIST)
        #     # do dir se ulozi vsechny soubory ve slozce
        #     dir = os.listdir(path)
        #     targetFolder = None
        #     # ulozeni vsech slozek, ktere obsahuji materialy
        #     targetFolders = ["1K", "2K", "3K", "4K", "5K", "6K", "7K", "8K", "9K", "10K", "11K", "12K", "13K", "14K", "15K", "16K"]
        #     # nalezeni slozky se stejnym nazvem jako je parent folder
        #     same_path_dirs = [d for d in dir if os.path.isdir(os.path.join(path, d)) and d.startswith(os.path.basename(path))]
        #     same_path_dirs = sorted(same_path_dirs)
        #     folder_dict = {}
        #     # pro vsechny slozky, ktere jsou ulozeny v listu se slozkami se stejnym nazvem
        #     for index, folder in enumerate(same_path_dirs):
        #         folder_dict[folder] = True
        #     # print(checkbox_list)
        #     print("Active checkboxes:")
        #     # projde vsechny checkboxy, ktere jsou ulozeny v listu
        #     for index, checkbox in enumerate(checkbox_list):
        #         # pokud je checkobox zaskrtly
        #         if self.GetBool(checkbox):
        #             # pride se do listu s aktivnimi checkboxy
        #             active_checkbox_list.append(index)
        #             # zde se ulozi slozka, ktera ma stejny index jako checkbox
        #             # musi se to vyresit takhle, protoze checkbox sam o sobe nema stejny nazev jako slozka, index ano
        #             folder_name = same_path_dirs[index]
        #             # ulozeni slozky, ktera ma stejny nazev jako text u daneho checkboxu
        #             folder_path = os.path.join(path, folder_name)
        #             print(folder_name)
        #             subdirs = [subdir for subdir in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, subdir))]
        #             # pro vsechny slozky, ktere obsahuji material (napr 4K, 5K, atd...)
        #             for targetFolderName in targetFolders:
        #                 # pokud je slozka 4K, 5K, atd... v te kterou prochazime
        #                 if targetFolderName in subdirs:
        #                     # cesta do slozky s 4K, 5K, atd...
        #                     targetFolder = os.path.join(folder_path, targetFolderName)
        #                     print("Slozka s materialem byla nalezena v ceste " + targetFolder)
        #                     # ulozeni vsech bitmapa ve slozce 4K, 5K, atd...
        #                     dirPath = os.listdir(targetFolder)
        #                     hasColor = False
        #                     # pro kazdou bitmapu ve slozce
        #                     # for file in dirPath:
        #                     #     try: 
        #                     #         parts = file.split(".")[0].split("_")
        #                     #         manufacturer = parts[0]
        #                     #         productNumber = parts[1]
        #                     #         product = parts[2]
        #                     #         mapID = parts[3]
        #                     #         resolution = parts[4]
        #                     #         if mapID == "DIFF" or mapID == "COLOR" or mapID == "COL":
        #                     #             hasColor = True
        #                     #         if mapID == "DISP16":
        #                     #             self.has16bDisp = True
        #                     #             self.hasDisp = True
        #                     #         if mapID == "DISP":
        #                     #             self.hasDisp = True
        #                     #         if mapID == "AO":
        #                     #             self.hasAO = True
        #                     #         if mapID == "IOR":
        #                     #             self.hasIor = True
        #                     #         if mapID == "NRM16":
        #                     #             self.has16bNormal = True
        #                     #     except:
        #                     #         pass

        #                     # if self.hasAO:
        #                     #     self.SetBool(ID.DIALOG_MAP_AO_CB, True)
        #                     #     self.Enable(ID.DIALOG_MAP_AO_CB, True)

        #                     # if self.hasDisp:
        #                     #     self.SetBool(ID.DIALOG_MAP_DISPL_CB, True)
        #                     #     self.Enable(ID.DIALOG_MAP_DISPL_CB, True)

        #                     # if self.has16bDisp:
        #                     #     self.SetBool(ID.DIALOG_MAP_16B_DISPL_CB, True)
        #                     #     self.Enable(ID.DIALOG_MAP_16B_DISPL_CB, True)

        #                     # if self.has16bNormal:
        #                     #     self.SetBool(ID.DIALOG_MAP_16B_NORMAL_CB, True)
        #                     #     self.Enable(ID.DIALOG_MAP_16B_NORMAL_CB, True)

        #                     # if self.hasIor:
        #                     #     self.SetBool(ID.DIALOG_MAP_IOR_CB, False)
        #                     #     self.Enable(ID.DIALOG_MAP_IOR_CB, True)
                            
        #                     # if hasColor:
        #                     #     self.materialFolder = path
        #                     #     self.Enable(ID.DIALOG_LOAD_BUTTON, True)
        #                     #     self.SetError("")
        #                     # else:
        #                     #     self.SetError("One or more folders do not contain the correct Reawote materialssssss.")
        #                     #     print(mat, " neobsahuje spravnou slozku")                        
        #                     if targetFolder is not None:
        #                         loadAO = self.GetBool(ID.DIALOG_MAP_AO_CB)
        #                         loadDispl = self.GetBool(ID.DIALOG_MAP_DISPL_CB)
        #                         load16bdispl = self.GetBool(ID.DIALOG_MAP_16B_DISPL_CB)
        #                         loadIor = self.GetBool(ID.DIALOG_MAP_IOR_CB)

        #                         mat = c4d.BaseMaterial(ID.CORONA_STR_MATERIAL_PHYSICAL)
        #                         mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_ROUGHNESS_MODE, ID.CORONA_PHYSICAL_MATERIAL_ROUGHNESS_MODE_GLOSSINESS, c4d.DESCFLAGS_SET_NONE)
        #                         mat.SetParameter(ID.CORONA_MATERIAL_PREVIEWSIZE, ID.CORONA_MATERIAL_PREVIEWSIZE_1024, c4d.DESCFLAGS_SET_NONE)
        #                         mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_BASE_IOR_VALUE, 1.56, c4d.DESCFLAGS_SET_NONE)

        #                         fusionShader = None

        #                         dir = os.listdir(targetFolder)
        #                         for file in dir:
        #                             fullPath = os.path.join(targetFolder, file)
        #                             # print("Type of fullpath: ", type(fullPath))
        #                             parts = file.split(".")[0].split("_")
        #                             mapID = parts[3]
        #                             if mapID == "COL" or mapID == "COLOR":
        #                                 mat.SetName("_".join(parts[0:3]))
        #                                 if not loadAO:
        #                                     bitmap = c4d.BaseShader(c4d.Xbitmap)
        #                                     bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
        #                                     mat.InsertShader(bitmap)
        #                                     mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_BASE_COLOR_TEXTURE, bitmap, c4d.DESCFLAGS_SET_NONE)
        #                                 else:
        #                                     if not fusionShader:
        #                                         fusionShader = c4d.BaseShader(c4d.Xfusion)
        #                                         fusionShader.SetParameter(c4d.SLA_FUSION_MODE, c4d.SLA_FUSION_MODE_MULTIPLY, c4d.DESCFLAGS_SET_NONE)
        #                                         fusionShader.SetParameter(c4d.SLA_FUSION_BLEND, 1.0, c4d.DESCFLAGS_SET_NONE)
        #                                         mat.InsertShader(fusionShader)
        #                                         mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_BASE_COLOR_TEXTURE, fusionShader, c4d.DESCFLAGS_SET_NONE)
        #                                     bitmap = c4d.BaseShader(c4d.Xbitmap)
        #                                     bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
        #                                     fusionShader.InsertShader(bitmap)
        #                                     fusionShader.SetParameter(c4d.SLA_FUSION_BASE_CHANNEL, bitmap, c4d.DESCFLAGS_SET_NONE)
        #                             elif mapID == "NRM":
        #                                 bitmap = c4d.BaseShader(c4d.Xbitmap)
        #                                 bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
        #                                 texture = c4d.BaseShader(ID.PLUGINID_CORONA4D_NORMALSHADER)
        #                                 texture.SetParameter(ID.CORONA_NORMALMAP_TEXTURE, bitmap, c4d.DESCFLAGS_SET_NONE)
        #                                 texture.SetParameter(ID.CORONA_NORMALMAP_FLIP_G, True, c4d.DESCFLAGS_SET_NONE)
        #                                 mat.InsertShader(bitmap)
        #                                 mat.InsertShader(texture)
        #                                 mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_BASE_BUMPMAPPING_ENABLE, True, c4d.DESCFLAGS_SET_NONE)
        #                                 mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_BASE_BUMPMAPPING_VALUE, 1.0, c4d.DESCFLAGS_SET_NONE)
        #                                 mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_BASE_BUMPMAPPING_TEXTURE, texture, c4d.DESCFLAGS_SET_NONE)
        #                             elif loadDispl and (load16bdispl and mapID == "DISP16") or (not load16bdispl and mapID == "DISP"):
        #                                 bitmap = c4d.BaseShader(c4d.Xbitmap)
        #                                 bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
        #                                 mat.InsertShader(bitmap)
        #                                 mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_DISPLACEMENT, True, c4d.DESCFLAGS_SET_NONE)
        #                                 mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_DISPLACEMENT_TEXTURE, bitmap, c4d.DESCFLAGS_SET_NONE)
        #                                 mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_DISPLACEMENT_MIN_LEVEL, 0, c4d.DESCFLAGS_SET_NONE)
        #                                 mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_DISPLACEMENT_MAX_LEVEL, 1, c4d.DESCFLAGS_SET_NONE)
        #                             elif loadAO and mapID == "AO":
        #                                 if not fusionShader:
        #                                     fusionShader = c4d.BaseShader(c4d.Xfusion)
        #                                     fusionShader.SetParameter(c4d.SLA_FUSION_MODE, c4d.SLA_FUSION_MODE_MULTIPLY, c4d.DESCFLAGS_SET_NONE)
        #                                     fusionShader.SetParameter(c4d.SLA_FUSION_BLEND, 1.0, c4d.DESCFLAGS_SET_NONE)
        #                                     mat.InsertShader(fusionShader)
        #                                     mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_BASE_COLOR_TEXTURE, fusionShader, c4d.DESCFLAGS_SET_NONE)
        #                                 bitmap = c4d.BaseShader(c4d.Xbitmap)
        #                                 bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
        #                                 fusionShader.InsertShader(bitmap)
        #                                 fusionShader.SetParameter(c4d.SLA_FUSION_BLEND_CHANNEL, bitmap, c4d.DESCFLAGS_SET_NONE)
        #                             elif mapID == "OPAC":
        #                                 bitmap = c4d.BaseShader(c4d.Xbitmap)
        #                                 bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
        #                                 mat.InsertShader(bitmap)
        #                                 mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_ALPHA, True, c4d.DESCFLAGS_SET_NONE)
        #                                 mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_ALPHA_TEXTURE, bitmap, c4d.DESCFLAGS_SET_NONE)
        #                             elif mapID == "GLOSS":
        #                                 bitmap = c4d.BaseShader(c4d.Xbitmap)
        #                                 bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
        #                                 mat.InsertShader(bitmap)
        #                                 mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_BASE_ROUGHNESS_TEXTURE, bitmap, c4d.DESCFLAGS_SET_NONE)
        #                                 mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_BASE_ROUGHNESS_VALUE, 100.0, c4d.DESCFLAGS_SET_NONE)
        #                             elif mapID == "REFL":
        #                                 bitmap = c4d.BaseShader(c4d.Xbitmap)
        #                                 bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
        #                                 mat.InsertShader(bitmap)
        #                                 mat.SetParameter(ID.CORONA_MATERIAL_REFLECT, True, c4d.DESCFLAGS_SET_NONE)
        #                                 mat.SetParameter(ID.CORONA_REFLECT_TEXTURE, bitmap, c4d.DESCFLAGS_SET_NONE)
        #                             elif mapID == "SSS":
        #                                 bitmap = c4d.BaseShader(c4d.Xbitmap)
        #                                 bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
        #                                 mat.InsertShader(bitmap)
        #                                 mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_SSS, True, c4d.DESCFLAGS_SET_NONE)
        #                                 mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_VOLUME_SSS_TEXTURE, bitmap, c4d.DESCFLAGS_SET_NONE)
        #                             elif mapID == "SSSABSORB":
        #                                 bitmap = c4d.BaseShader(c4d.Xbitmap)
        #                                 bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
        #                                 mat.InsertShader(bitmap)
        #                                 mat.SetParameter(ID.CORONA_MATERIAL_VOLUME, True, c4d.DESCFLAGS_SET_NONE)
        #                                 mat.SetParameter(ID.CORONA_VOLUME_ABSORPTION_TEXTURE, bitmap, c4d.DESCFLAGS_SET_NONE)
        #                             elif loadIor and mapID == "IOR":
        #                                 bitmap = c4d.BaseShader(c4d.Xbitmap)
        #                                 bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
        #                                 mat.InsertShader(bitmap)
        #                                 mat.SetParameter(ID.CORONA_REFLECT_FRESNELLOR_TEXTURE, bitmap, c4d.DESCFLAGS_SET_NONE)
        #                             elif mapID == "METAL":
        #                                 bitmap = c4d.BaseShader(c4d.Xbitmap)
        #                                 bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
        #                                 mat.InsertShader(bitmap)
        #                                 mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_METALLIC_MODE_TEXTURE, bitmap, c4d.DESCFLAGS_SET_NONE)

        #                             doc = c4d.documents.GetActiveDocument()
        #                             doc.StartUndo()
        #                             # nevim proc to je bile, ale funguje to takze save
        #                             doc.InsertMaterial(mat)
        #                             # print("uz to proslo Insertem")
        #                             doc.AddUndo(c4d.UNDOTYPE_NEW, mat)
        #                             doc.EndUndo()
        #                             material_to_add.append(mat)                                   
        #                             self.SetString(ID.DIALOG_ERROR, "")
        #     c4d.EventAdd()

        #     return True

    def SetError(self, message):
        if not message:
            message = ""
        self.SetString(ID.DIALOG_ERROR, message)

    def SetListItems(self, message):
        if not message:
            message= ""
            self.SetString(ID.DIALOG_FOLDER_LIST, message)

    def LoadMaterial(self):
        if not self.materialFolder:
            self.SetError("Material folder was not selected")
            return False

        loadAO = self.GetBool(ID.DIALOG_MAP_AO_CB)
        loadDispl = self.GetBool(ID.DIALOG_MAP_DISPL_CB)
        load16bdispl = self.GetBool(ID.DIALOG_MAP_16B_DISPL_CB)
        loadIor = self.GetBool(ID.DIALOG_MAP_IOR_CB)

        mat = c4d.BaseMaterial(ID.CORONA_STR_MATERIAL_PHYSICAL)
        mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_ROUGHNESS_MODE, ID.CORONA_PHYSICAL_MATERIAL_ROUGHNESS_MODE_GLOSSINESS, c4d.DESCFLAGS_SET_NONE)
        mat.SetParameter(ID.CORONA_MATERIAL_PREVIEWSIZE, ID.CORONA_MATERIAL_PREVIEWSIZE_1024, c4d.DESCFLAGS_SET_NONE)
        mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_BASE_IOR_VALUE, 1.56, c4d.DESCFLAGS_SET_NONE)
        

        fusionShader = None

        # 4K 8K atd.
        dir = os.listdir(self.materialFolder)
        for file in dir:
            fullPath = os.path.join(self.materialFolder, file)
            try:
                # python2 unicode string handling
                if sys.version_info < (3, 0):
                    fullPath = fullPath.encode("utf-8")
            except:
                pass
            print("Type of fullpath: ", type(fullPath))
            parts = file.split(".")[0].split("_")
            mapID = parts[3]

            if mapID == "COL" or mapID == "COLOR":
                mat.SetName("_".join(parts[0:3]))
                if not loadAO:
                    bitmap = c4d.BaseShader(c4d.Xbitmap)
                    bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
                    mat.InsertShader(bitmap)
                    mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_BASE_COLOR_TEXTURE, bitmap, c4d.DESCFLAGS_SET_NONE)
                else:
                    if not fusionShader:
                        fusionShader = c4d.BaseShader(c4d.Xfusion)
                        fusionShader.SetParameter(c4d.SLA_FUSION_MODE, c4d.SLA_FUSION_MODE_MULTIPLY, c4d.DESCFLAGS_SET_NONE)
                        fusionShader.SetParameter(c4d.SLA_FUSION_BLEND, 1.0, c4d.DESCFLAGS_SET_NONE)
                        mat.InsertShader(fusionShader)
                        mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_BASE_COLOR_TEXTURE, fusionShader, c4d.DESCFLAGS_SET_NONE)
                    bitmap = c4d.BaseShader(c4d.Xbitmap)
                    bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
                    fusionShader.InsertShader(bitmap)
                    fusionShader.SetParameter(c4d.SLA_FUSION_BASE_CHANNEL, bitmap, c4d.DESCFLAGS_SET_NONE)
            elif mapID == "NRM":
                bitmap = c4d.BaseShader(c4d.Xbitmap)
                bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
                texture = c4d.BaseShader(ID.PLUGINID_CORONA4D_NORMALSHADER)
                texture.SetParameter(ID.CORONA_NORMALMAP_TEXTURE, bitmap, c4d.DESCFLAGS_SET_NONE)
                texture.SetParameter(ID.CORONA_NORMALMAP_FLIP_G, True, c4d.DESCFLAGS_SET_NONE)
                mat.InsertShader(bitmap)
                mat.InsertShader(texture)
                mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_BASE_BUMPMAPPING_ENABLE, True, c4d.DESCFLAGS_SET_NONE)
                mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_BASE_BUMPMAPPING_VALUE, 1.0, c4d.DESCFLAGS_SET_NONE)
                mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_BASE_BUMPMAPPING_TEXTURE, texture, c4d.DESCFLAGS_SET_NONE)
            elif loadDispl and (load16bdispl and mapID == "DISP16") or (not load16bdispl and mapID == "DISP"):
                bitmap = c4d.BaseShader(c4d.Xbitmap)
                bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
                mat.InsertShader(bitmap)
                mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_DISPLACEMENT, True, c4d.DESCFLAGS_SET_NONE)
                mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_DISPLACEMENT_TEXTURE, bitmap, c4d.DESCFLAGS_SET_NONE)
                mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_DISPLACEMENT_MIN_LEVEL, 0, c4d.DESCFLAGS_SET_NONE)
                mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_DISPLACEMENT_MAX_LEVEL, 1, c4d.DESCFLAGS_SET_NONE)
            elif loadAO and mapID == "AO":
                if not fusionShader:
                    fusionShader = c4d.BaseShader(c4d.Xfusion)
                    fusionShader.SetParameter(c4d.SLA_FUSION_MODE, c4d.SLA_FUSION_MODE_MULTIPLY, c4d.DESCFLAGS_SET_NONE)
                    fusionShader.SetParameter(c4d.SLA_FUSION_BLEND, 1.0, c4d.DESCFLAGS_SET_NONE)
                    mat.InsertShader(fusionShader)
                    mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_BASE_COLOR_TEXTURE, fusionShader, c4d.DESCFLAGS_SET_NONE)
                bitmap = c4d.BaseShader(c4d.Xbitmap)
                bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
                fusionShader.InsertShader(bitmap)
                fusionShader.SetParameter(c4d.SLA_FUSION_BLEND_CHANNEL, bitmap, c4d.DESCFLAGS_SET_NONE)
            elif mapID == "OPAC":
                bitmap = c4d.BaseShader(c4d.Xbitmap)
                bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
                mat.InsertShader(bitmap)
                mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_ALPHA, True, c4d.DESCFLAGS_SET_NONE)
                mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_ALPHA_TEXTURE, bitmap, c4d.DESCFLAGS_SET_NONE)
            elif mapID == "GLOSS":
                bitmap = c4d.BaseShader(c4d.Xbitmap)
                bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
                mat.InsertShader(bitmap)
                mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_BASE_ROUGHNESS_TEXTURE, bitmap, c4d.DESCFLAGS_SET_NONE)
                mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_BASE_ROUGHNESS_VALUE, 100.0, c4d.DESCFLAGS_SET_NONE)
            elif mapID == "REFL":
                bitmap = c4d.BaseShader(c4d.Xbitmap)
                bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
                mat.InsertShader(bitmap)
                mat.SetParameter(ID.CORONA_MATERIAL_REFLECT, True, c4d.DESCFLAGS_SET_NONE)
                mat.SetParameter(ID.CORONA_REFLECT_TEXTURE, bitmap, c4d.DESCFLAGS_SET_NONE)
            elif mapID == "SSS":
                bitmap = c4d.BaseShader(c4d.Xbitmap)
                bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
                mat.InsertShader(bitmap)
                mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_SSS, True, c4d.DESCFLAGS_SET_NONE)
                mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_VOLUME_SSS_TEXTURE, bitmap, c4d.DESCFLAGS_SET_NONE)
            elif mapID == "SSSABSORB":
                bitmap = c4d.BaseShader(c4d.Xbitmap)
                bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
                mat.InsertShader(bitmap)
                mat.SetParameter(ID.CORONA_MATERIAL_VOLUME, True, c4d.DESCFLAGS_SET_NONE)
                mat.SetParameter(ID.CORONA_VOLUME_ABSORPTION_TEXTURE, bitmap, c4d.DESCFLAGS_SET_NONE)
            elif loadIor and mapID == "IOR":
                bitmap = c4d.BaseShader(c4d.Xbitmap)
                bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
                mat.InsertShader(bitmap)
                mat.SetParameter(ID.CORONA_REFLECT_FRESNELLOR_TEXTURE, bitmap, c4d.DESCFLAGS_SET_NONE)
            elif mapID == "METAL":
                bitmap = c4d.BaseShader(c4d.Xbitmap)
                bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
                mat.InsertShader(bitmap)
                mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_METALLIC_MODE_TEXTURE, bitmap, c4d.DESCFLAGS_SET_NONE)

        doc = c4d.documents.GetActiveDocument()
        doc.StartUndo()
        doc.InsertMaterial(mat)
        doc.AddUndo(c4d.UNDOTYPE_NEW, mat)
        doc.EndUndo()
        
        self.SetString(ID.DIALOG_ERROR, "")

        return True

    def Reset(self):
        self.materialFolder = None
    
        self.has16bDisp = False
        self.has16bNormal = False
        self.hasDisp = False
        self.hasAO = False
        self.hasIor = False
        
        self.SetBool(ID.DIALOG_MAP_AO_CB, False)
        self.Enable(ID.DIALOG_MAP_AO_CB, False)
        self.SetBool(ID.DIALOG_MAP_DISPL_CB, False)
        self.Enable(ID.DIALOG_MAP_DISPL_CB, False)
        self.SetBool(ID.DIALOG_MAP_16B_DISPL_CB, False)
        self.Enable(ID.DIALOG_MAP_16B_DISPL_CB, False)
        self.SetBool(ID.DIALOG_MAP_16B_NORMAL_CB, False)
        self.Enable(ID.DIALOG_MAP_16B_NORMAL_CB, False)
        self.SetBool(ID.DIALOG_MAP_IOR_CB, False)
        self.Enable(ID.DIALOG_MAP_IOR_CB, False)

        self.Enable(ID.DIALOG_LOAD_BUTTON, False)
        # self.Enable(ID.DIALOG_LIST_BUTTON, False)
        

class ReawoteMaterialLoader(plugins.CommandData):
    
    thread = None

    def __init__(self) -> None:
        super().__init__()
        global dialog
        if not dialog:
            dialog = ReawoteMaterialDialog()

    def Execute(self, doc):
        dialog.Open(c4d.DLG_TYPE_ASYNC, REAWOTE_PLUGIN_ID, -1, -1, 450, 950)
        return True
        
    def CoreMessage(self, id, msg):
        # Checks if texture baking has finished
        if id==REAWOTE_PLUGIN_ID:
            print("Command received!")
            print("Path is: " + self.thread.path)
            return True

        return gui.GeDialog.CoreMessage(self, id, msg)