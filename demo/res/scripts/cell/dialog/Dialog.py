# -*- coding: utf-8 -*-
#
"""
"""
import KBEngine
import dialog.funcs
import GlobalDefine
from KBEDebug import *

class Dialog:
	"""
	"""
	c_dialogMgr = None
	def __init__(self, datas):
		self.__key = datas.get("id", 0)
		self.__title = datas.get("title", 0)
		self.__body = datas.get("body", 0)
		self.__funcFailMsg = datas.get("funcFailMsg", "")
		self.__menus = []
		self.__funcs = {}
		
		for idx in range(5):
			menu = datas.get("menu%i" % (idx + 1))
			if menu > 0:
				self.__menus.append(menu)
				
			func = datas.get("func%i" % (idx + 1))
			if len(func) <= 0:
				continue;

			self.__funcs[func] = funcs.g_funcs[func](datas.get("funcargs%i" % (idx + 1)))

	def getTitle(self):
		return self.__title

	def getBody(self):
		return self.__body

	def getKey(self):
		return self.__key

	def canTalk(self, avatar, talker):
		"""
		"""
		for key, func in self.__funcs.items():
			if not func.valid(avatar, talker):
				return False
		
		return True
	
	def do(self, avatar, talker):
		for key, func in self.__funcs.items():
			func.do(avatar, talker)

	def onTalk(self, avatar, talker):
		"""
		"""
		INFO_MSG("onTalk title %s,__func %s, __menus %s, __body %d,"%(self.__title, self.__funcs, self.__menus, self.__body))
		
		# 执行功能
		self.do(avatar, talker)
		
		# 列出菜单
		for mkey in self.__menus:
			dialog = c_dialogMgr.getDialog(mkey)
			if dialog.canTalk(avatar, talker):
				avatar.client.dialog_addOption(GlobalDefine.DIALOG_TYPE_NORMAL, dialog.getKey(), dialog.getTitle(), 0)

		# 显示主内容
		avatar.client.dialog_setText(self.getBody())