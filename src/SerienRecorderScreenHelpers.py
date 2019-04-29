# coding=utf-8

# This file contains the SerienRecoder Screen Helpers

from Tools.Directories import fileExists
from enigma import eListboxPythonMultiContent, gFont, getDesktop, eTimer
from Components.config import config
from Components.Label import Label
from Components.MenuList import MenuList
from Components.Pixmap import Pixmap
from Components.VideoWindow import VideoWindow
from Components.ScrollLabel import ScrollLabel
from Screens.MessageBox import MessageBox

from SerienRecorder import serienRecMainPath
from SerienRecorderDatabase import SRDatabase
from SerienRecorderHelpers import isDreamOS, SRMANUALURL

# check VPS availability
try:
	from Plugins.SystemPlugins.vps import Vps
except ImportError as ie:
	VPSPluginAvailable = False
else:
	VPSPluginAvailable = True

# init Opera Webbrowser
# if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/HbbTV/browser.pyo"):
# 	from Plugins.Extensions.HbbTV.browser import Browser
# 	OperaBrowserInstalled = True
# else:
# 	OperaBrowserInstalled = False

# init Opera Webbrowser
if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/WebkitHbbTV/hbbtv.pyo"):
	from Plugins.Extensions.WebkitHbbTV.hbbtv import HbbTVWindow
	OperaBrowserInstalled = True
else:
	OperaBrowserInstalled = False

# init DMM Webbrowser
if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/Browser/Browser.pyo"):
	from Plugins.Extensions.Browser.Browser import Browser
	DMMBrowserInstalled = True
else:
	DMMBrowserInstalled = False

import keymapparser

try:
	keymapparser.removeKeymap("%skeymap.xml" % serienRecMainPath)
except:
	pass
try:
	keymapparser.readKeymap("%skeymap.xml" % serienRecMainPath)
except:
	pass

longButtonText = False
buttonText_na = "-----"
skinName = "SerienRecorder3.0"
skin = "%sskins/SR_Skin.xml" % serienRecMainPath
default_skinName = skinName
default_skin = skin
skinFactor = 1
num_bt_text = ()

# Check if is Full HD / UHD
DESKTOP_WIDTH = getDesktop(0).size().width()
if DESKTOP_WIDTH > 1920:
	skinFactor = 3.0
elif DESKTOP_WIDTH > 1280:
	skinFactor = 1.5
else:
	skinFactor = 1
print "[SerienRecorder] Skinfactor: %s" % skinFactor

def SelectSkin():
	global longButtonText
	longButtonText = False
	global buttonText_na
	buttonText_na = "-----"

	global skinName
	skinName = default_skinName
	global skin
	skin = default_skin

	if "FHD" in config.plugins.serienRec.SkinType.value and DESKTOP_WIDTH < 1920:
		config.plugins.serienRec.SkinType.value = ""
		config.save()

	if config.plugins.serienRec.SkinType.value == "Skinpart":
		try:
			from skin import lookupScreen
			x, path = lookupScreen("SerienRecorder", 0)
			if x:
				skinName = "SerienRecorder"
		except:
			pass

	elif config.plugins.serienRec.SkinType.value in ("", "Skin2", "AtileHD", "StyleFHD", "Black Box"):
		skin = "%sskins/%s/SR_Skin.xml" % (serienRecMainPath, config.plugins.serienRec.SkinType.value)
		skin = skin.replace("//", "/")
		if config.plugins.serienRec.SkinType.value in ("Skin2", "StyleFHD", "Black Box"):
			config.plugins.serienRec.showAllButtons.value = True
		if config.plugins.serienRec.SkinType.value in ("Skin2", "AtileHD", "Black Box"):
			buttonText_na = ""
	else:
		if fileExists("%sskins/%s/SR_Skin.xml" % (serienRecMainPath, config.plugins.serienRec.SkinType.value)):
			skin = "%sskins/%s/SR_Skin.xml" % (serienRecMainPath, config.plugins.serienRec.SkinType.value)
			buttonText_na = ""


def setSkinProperties(self, isLayoutFinshed=True):
	global longButtonText
	if isLayoutFinshed:
		try:
			x = self['text_3'].instance.size()
			if x.width() > 250:
				longButtonText = True
			else:
				longButtonText = False
		except:
			longButtonText = False

	if longButtonText:
		self.num_bt_text = (["Zeige Log", buttonText_na, "Abbrechen"],
							[buttonText_na, "Konflikt-Liste", "Wunschliste"],
							[buttonText_na, "Merkzettel", "Timer suchen"],
							["Neue Serienstarts", buttonText_na, "Hilfe"],
							["Serien Beschreibung", buttonText_na, "Einstellungen"])
	else:
		self.num_bt_text = (["Zeige Log", buttonText_na, "Abbrechen"],
							[buttonText_na, "Konflikt-Liste", "Wunschliste"],
							[buttonText_na, "Merkzettel", "Timer suchen"],
							["Neue Serienstarts", buttonText_na, "Hilfe"],
							["Serien Beschreibung", buttonText_na, "Einstellungen"])

	if config.plugins.serienRec.showAllButtons.value:
		setMenuTexts(self)

def InitSkin(self):
	global longButtonText
	global buttonText_na
	global skin
	global skinName

	self.skinName = skinName

	if skin:
		try:
			SRSkin = open(skin)
			self.skin = SRSkin.read()
			SRSkin.close()
		except:
			config.plugins.serienRec.showAllButtons.value = False
			longButtonText = False
			buttonText_na = "-----"

			skinName = default_skinName
			skin = default_skin

			SRSkin = open(skin)
			self.skin = SRSkin.read()
			SRSkin.close()

	self['bt_red'] = Pixmap()
	self['bt_green'] = Pixmap()
	self['bt_yellow'] = Pixmap()
	self['bt_blue'] = Pixmap()

	self['bt_ok'] = Pixmap()
	self['bt_exit'] = Pixmap()
	self['bt_text'] = Pixmap()
	self['bt_epg'] = Pixmap()
	self['bt_info'] = Pixmap()
	self['bt_menu'] = Pixmap()
	self['bt_0'] = Pixmap()
	self['bt_1'] = Pixmap()
	self['bt_2'] = Pixmap()
	self['bt_3'] = Pixmap()
	self['bt_4'] = Pixmap()
	self['bt_5'] = Pixmap()
	self['bt_6'] = Pixmap()
	self['bt_7'] = Pixmap()
	self['bt_8'] = Pixmap()
	self['bt_9'] = Pixmap()

	self['text_red'] = Label("")
	self['text_green'] = Label("")
	self['text_yellow'] = Label("")
	self['text_blue'] = Label("")

	self['text_ok'] = Label("")
	self['text_exit'] = Label("")
	self['text_text'] = Label("")
	self['text_epg'] = Label("")
	self['text_info'] = Label("")
	self['text_menu'] = Label("")

	self['text_0'] = Label("")
	self['text_1'] = Label("")
	self['text_2'] = Label("")
	self['text_3'] = Label("")
	self['text_4'] = Label("")
	self['text_5'] = Label("")
	self['text_6'] = Label("")
	self['text_7'] = Label("")
	self['text_8'] = Label("")
	self['text_9'] = Label("")

	self['Web_Channel'] = Label("")
	self['Web_Channel'].hide()
	self['STB_Channel'] = Label("")
	self['STB_Channel'].hide()
	self['alt_STB_Channel'] = Label("")
	self['alt_STB_Channel'].hide()
	self['separator'] = Label("")
	self['separator'].hide()
	self['path'] = Label("")
	self['path'].hide()
	self['menu_list'] = MenuList([])
	self['menu_list'].hide()
	self['config'] = MenuList([])
	self['config'].hide()
	self['log'] = MenuList([])
	self['log'].hide()
	self['list'] = MenuList([])
	self['list'].hide()
	self['popup_list'] = MenuList([])
	self['popup_list'].hide()
	self['popup_list2'] = MenuList([])
	self['popup_list2'].hide()
	self['popup_bg'] = Pixmap()
	self['popup_bg'].hide()
	self['cover'] = Pixmap()
	self['cover'].hide()
	self['config_information'] = Label("")
	self['config_information'].hide()
	self['config_information_text'] = Label("")
	self['config_information_text'].hide()
	self['info'] = ScrollLabel()
	self['info'].hide()
	desktopSize = getDesktop(0).size()
	self["video"] = VideoWindow(decoder=0, fb_width=desktopSize.width(), fb_height=desktopSize.height())

	self['title'] = Label("")
	self['version'] = Label("SerienRecorder v%s" % config.plugins.serienRec.showversion.value)
	self['headline'] = Label("")

	setSkinProperties(self, False)

	if not config.plugins.serienRec.showAllButtons.value:
		self['bt_red'].hide()
		self['bt_green'].hide()
		self['bt_yellow'].hide()
		self['bt_blue'].hide()

		self['bt_ok'].hide()
		self['bt_exit'].hide()
		self['bt_text'].hide()
		self['bt_epg'].hide()
		self['bt_info'].hide()
		self['bt_menu'].hide()
		self['bt_0'].hide()
		self['bt_1'].hide()
		self['bt_2'].hide()
		self['bt_3'].hide()
		self['bt_4'].hide()
		self['bt_5'].hide()
		self['bt_6'].hide()
		self['bt_7'].hide()
		self['bt_8'].hide()
		self['bt_9'].hide()

		self['text_red'].hide()
		self['text_green'].hide()
		self['text_yellow'].hide()
		self['text_blue'].hide()

		self['text_ok'].hide()
		self['text_0'].hide()
		self['text_1'].hide()
		self['text_2'].hide()
		self['text_3'].hide()
		self['text_4'].hide()
		self['text_5'].hide()
		self['text_6'].hide()
		self['text_7'].hide()
		self['text_8'].hide()
		self['text_9'].hide()

def setMenuTexts(self):
	self['text_0'].setText(self.num_bt_text[0][0])
	self['text_1'].setText(self.num_bt_text[1][0])
	self['text_2'].setText(self.num_bt_text[2][0])
	self['text_3'].setText(self.num_bt_text[3][0])
	self['text_4'].setText(self.num_bt_text[4][0])
	self['text_5'].setText(self.num_bt_text[0][1])
	self['text_6'].setText(self.num_bt_text[1][1])
	self['text_7'].setText(self.num_bt_text[2][1])
	self['text_8'].setText(self.num_bt_text[3][1])
	self['text_9'].setText(self.num_bt_text[4][1])
	self['text_exit'].setText(self.num_bt_text[0][2])
	self['text_text'].setText(self.num_bt_text[1][2])
	self['text_epg'].setText(self.num_bt_text[2][2])
	self['text_info'].setText(self.num_bt_text[3][2])
	self['text_menu'].setText(self.num_bt_text[4][2])

def updateMenuKeys(self):
	if self.displayMode == 0:
		self.displayMode = 1
		self['bt_0'].hide()
		self['bt_1'].hide()
		self['bt_2'].hide()
		self['bt_3'].hide()
		self['bt_4'].hide()
		self['bt_5'].show()
		self['bt_6'].show()
		self['bt_7'].show()
		self['bt_8'].show()
		self['bt_9'].show()
		self['bt_exit'].hide()
		self['bt_text'].hide()
		self['bt_epg'].hide()
		self['bt_info'].hide()
		self['bt_menu'].hide()
	elif self.displayMode == 1:
		self.displayMode = 2
		self['bt_0'].hide()
		self['bt_1'].hide()
		self['bt_2'].hide()
		self['bt_3'].hide()
		self['bt_4'].hide()
		self['bt_5'].hide()
		self['bt_6'].hide()
		self['bt_7'].hide()
		self['bt_8'].hide()
		self['bt_9'].hide()
		self['bt_exit'].show()
		self['bt_text'].show()
		self['bt_epg'].show()
		self['bt_info'].show()
		self['bt_menu'].show()
	else:
		self.displayMode = 0
		self['bt_0'].show()
		self['bt_1'].show()
		self['bt_2'].show()
		self['bt_3'].show()
		self['bt_4'].show()
		self['bt_5'].hide()
		self['bt_6'].hide()
		self['bt_7'].hide()
		self['bt_8'].hide()
		self['bt_9'].hide()
		self['bt_exit'].hide()
		self['bt_text'].hide()
		self['bt_epg'].hide()
		self['bt_info'].hide()
		self['bt_menu'].hide()
	self['text_0'].setText(self.num_bt_text[0][self.displayMode])
	self['text_1'].setText(self.num_bt_text[1][self.displayMode])
	self['text_2'].setText(self.num_bt_text[2][self.displayMode])
	self['text_3'].setText(self.num_bt_text[3][self.displayMode])
	self['text_4'].setText(self.num_bt_text[4][self.displayMode])

class serienRecBaseScreen:
	def __init__(self, session):
		self.session = session
		self.skin = None
		self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.displayTimer = None
		self.skinName = None
		self.num_bt_text = ()

	def setupSkin(self):
		InitSkin(self)

		self.chooseMenuList.l.setFont(0, gFont('Regular', 20 + int(config.plugins.serienRec.listFontsize.value)))
		self.chooseMenuList.l.setItemHeight(int(50*skinFactor))
		self[self.modus] = self.chooseMenuList

	def setSkinProperties(self):
		setSkinProperties(self)

	def startDisplayTimer(self):
		self.displayTimer = None
		if config.plugins.serienRec.showAllButtons.value:
			setMenuTexts(self)
		else:
			self.displayMode = 2
			self.updateMenuKeys()

			self.displayTimer = eTimer()
			if isDreamOS():
				self.displayTimer_conn = self.displayTimer.timeout.connect(self.updateMenuKeys)
			else:
				self.displayTimer.callback.append(self.updateMenuKeys)
			self.displayTimer.start(config.plugins.serienRec.DisplayRefreshRate.value * 1000)

	def updateMenuKeys(self):
		updateMenuKeys(self)

	def readLogFile(self):
		from SerienRecorderLogScreen import serienRecReadLog
		self.session.open(serienRecReadLog)

	def showProposalDB(self):
		from SerienRecorderSeasonBeginsScreen import serienRecShowSeasonBegins
		self.session.open(serienRecShowSeasonBegins)

	def serieInfo(self):
		from SerienRecorderSeriesInfoScreen import serienRecShowInfo
		self.session.open(serienRecShowInfo, self.serien_name, self.serien_id)

	def showConflicts(self):
		from SerienRecorderConflictsScreen import serienRecShowConflicts
		self.session.open(serienRecShowConflicts)

	def showWishlist(self):
		from SerienRecorderWishlistScreen import serienRecWishlistScreen
		self.session.open(serienRecWishlistScreen)

	def wunschliste(self, seriesID):
		url = "https://www.wunschliste.de/" + str(seriesID)
		if OperaBrowserInstalled:
			self.session.open(HbbTVWindow, url, None)
		elif DMMBrowserInstalled:
			self.session.open(Browser, True, url)
		else:
			self.session.open(MessageBox, "Um diese Funktion nutzen zu können muss das Plugin '%s' installiert sein." % "Webbrowser", MessageBox.TYPE_INFO, timeout = 10)

	def showManual(self):
		if OperaBrowserInstalled:
			self.session.open(HbbTVWindow, SRMANUALURL, None)
		elif DMMBrowserInstalled:
			self.session.open(Browser, True, SRMANUALURL)
		else:
			self.session.open(MessageBox, "Um diese Funktion nutzen zu können muss das Plugin '%s' installiert sein." % "Webbrowser", MessageBox.TYPE_INFO, timeout = 10)

	def showAbout(self):
		from SerienRecorderAboutScreen import serienRecAboutScreen
		self.session.open(serienRecAboutScreen)

	def recSetup(self):
		from SerienRecorderSetupScreen import serienRecSetup
		self.session.openWithCallback(self.setupClose, serienRecSetup)

	def setupClose(self, result):
		if not result[2]:
			self.close()
		else:
			if result[0]:
				if config.plugins.serienRec.timeUpdate.value:
					from SerienRecorder import serienRecCheckForRecording
					serienRecCheckForRecording(self.session, False)

	def keyLeft(self):
		self[self.modus].pageUp()

	def keyRight(self):
		self[self.modus].pageDown()

	def keyDown(self):
		self[self.modus].down()

	def keyUp(self):
		self[self.modus].up()

	def keyRed(self):
		if config.plugins.serienRec.refreshViews.value:
			self.close(self.changesMade)
		else:
			self.close(False)

	def keyCancel(self):
		if config.plugins.serienRec.refreshViews.value:
			self.close(self.changesMade)
		else:
			self.close(False)

	def stopDisplayTimer(self):
		if self.displayTimer:
			self.displayTimer.stop()
			self.displayTimer = None

	def getCover(self, serienName):
		serien_id = None
		from SerienRecorder import serienRecDataBaseFilePath, getCover
		database = SRDatabase(serienRecDataBaseFilePath)
		url = database.getMarkerURL(serienName)
		if url:
			serien_id = url
		getCover(self, serienName, serien_id)
