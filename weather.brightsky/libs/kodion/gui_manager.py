# -*- coding: utf-8 -*-
# Copyright 2024 WebEye
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import xbmcplugin
import xbmcgui
import xbmc

import urllib.parse


def getScreenHeight():
    return xbmcgui.getScreenHeight()


def getScreenWidth():
    return xbmcgui.getScreenWidth()

def getWindow(window_id):
    return xbmcgui.Window(window_id)

def getKeyboardText(default=None, heading=None, hidden=False):
    kb = xbmc.Keyboard(default=default, heading=heading,hidden= hidden)
    kb.doModal()
    if kb.isConfirmed():
        return kb.getText()

    return None


class GuiManager:

    SORT_METHOD_NONE = xbmcplugin.SORT_METHOD_NONE
    SORT_METHOD_DATE = xbmcplugin.SORT_METHOD_DATE
    SORT_METHOD_DURATION = xbmcplugin.SORT_METHOD_DURATION
    SORT_METHOD_TITLE = xbmcplugin.SORT_METHOD_TITLE

    def __init__(self, argv, addon_id, default_image_url, fanart):
        self._argv = int(argv)
        self._addon_id = addon_id
        self._default_image_url = default_image_url
        self._fanart = fanart

        xbmcplugin.setPluginFanart(self._argv, self._fanart)

    def setContent(self, content):
        xbmcplugin.setContent(self._argv, content)

    def __setEntity(self, title, url, art=None, _property=None, _type=None, infoLabels=None, contextmenu=None, isFolder=True):
        li = xbmcgui.ListItem(label=str(title))
        if art is not None:
            li.setArt(art)

        if _property is not None:
            for key, value in _property.items():
                li.setProperty(key, value)

        if _type is not None and infoLabels is not None:
            li.setInfo(type=_type, infoLabels=infoLabels)

        if contextmenu:
            li.addContextMenuItems(contextmenu)

        xbmcplugin.addDirectoryItem(handle=self._argv, url=url, listitem=li, isFolder=isFolder)

    def addDirectory(self, title, poster=None, fanArt=None, _type=None, infoLabels=None, contextmenu=None, args=None):
        art = {}
        _property = {}

        if poster is not None:
            art['thumb'] = poster
        else:
            art['thumb'] = self._default_image_url

        if fanArt is not None:
            _property['Fanart_Image'] = fanArt
        elif self._fanart is not None:
            _property['Fanart_Image'] = self._fanart

        url = 'plugin://' + self._addon_id + '/?' + urllib.parse.urlencode(args)
        self.__setEntity(title=title, url=url, art=art, _property=_property, _type=_type, infoLabels=infoLabels, contextmenu=contextmenu, isFolder=True)

    def addItem(self, title, url, poster=None, fanArt=None, _type=None, infoLabels=None, contextmenu=None):
        art = {}
        _property = {}

        if poster is not None:
            art['thumb'] = poster
        else:
            art['thumb'] = self._default_image_url

        if fanArt is not None:
            _property['Fanart_Image'] = fanArt
        elif self._fanart is not None:
            _property['Fanart_Image'] = self._fanart

        if not _type is None and _type == 'video':
            _property['IsPlayable'] = 'true'

        self.__setEntity(title=title, url=url, art=art, _property=_property, _type=_type, infoLabels=infoLabels, contextmenu=contextmenu, isFolder=False)

    def addSortMethod(self, sortMethod):
        xbmcplugin.addSortMethod(self._argv, sortMethod)

    def endOfDirectory(self):
        xbmcplugin.endOfDirectory(self._argv)

    @staticmethod
    def setToastNotification(heading, message, time=5000, icon=None):
        xbmcgui.Dialog().notification(heading=heading, message=message, time=time, icon=icon)

    @staticmethod
    def MsgBoxYesNo(heading, message, nolabel=None, yeslabel=None):
        return xbmcgui.Dialog().yesno(heading=heading, message=message, nolabel=nolabel, yeslabel=yeslabel)

    @staticmethod
    def MsgBoxSelect(heading, _list, autoclose: int = 0, preselect: int = -1, useDetails: bool = False):
        return xbmcgui.Dialog().select(heading, _list, autoclose, preselect, useDetails)
