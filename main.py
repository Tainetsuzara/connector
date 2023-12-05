'''
'''
#!/usr/bin/env python
# -*- coding: shift_jis -*-
#HA = Hisakazu_Aoki
import maya.cmds as mc
class connector():
	def __init__(self):
		#リメンバーについてのグローバルリストを宣言します
		global HA_parentListRemember
		global HA_childrenListRemember
		global HA_vectorListRemember
		global HA_constraintTypeDict
		HA_parentListRemember = []
		HA_childrenListRemember = []
		HA_vectorListRemember = []
		HA_constraintTypeDict = {}
		

#UIを作成します
	def createUI(self, *args):
		if mc.window('connectorWindow', q=True, ex=True) == True:
			mc.deleteUI('connectorWindow')
		
		mc.window('connectorWindow',title='connector_1.0.0')
		#メインタブを設定します
		mc.tabLayout('mainTab', p='connectorWindow')
		#リレーションリストとタブをレイアウトします
		mc.paneLayout('relativePane', p='mainTab', configuration='vertical3')
		#リストパンを設定します
		mc.paneLayout('allScrollListPane', p='relativePane', configuration='vertical3')
		
		#ペアレントフレームをレイアウトします
		mc.paneLayout('parentItemPane', p='allScrollListPane', configuration='vertical2')
		#ペアレントアイテムフレームをレイアウトします
		mc.frameLayout('parentItemFrame', p='parentItemPane', l='parent item')		
		mc.paneLayout('parentItemListPane', p='parentItemFrame', configuration='horizontal4')
		#ペアレントアイテムリストインをレイアウトします
		mc.paneLayout('parentItemListInAddPane', p='parentItemListPane', configuration='horizontal2')
		mc.button('parentItemListInButton', p='parentItemListInAddPane', l='List Replace', c=self.listInParent)
		mc.button('parentItemListAddButton', p='parentItemListInAddPane', l='List Add', c=self.listAddParent)
		#ペアレントアイテムリストインをレイアウトしました
		mc.setParent('parentItemListInAddPane')		
		#ペアレントアイテムリストスクロールをレイアウトしました		
		mc.textScrollList('parentItemScrollList', p='parentItemListPane', ams=True, sc=self.selectParentItem, dcc=self.deselectParent, dgc=self.parentDrag, dpc=self.parentDrop)
		mc.popupMenu('parentItemScrollListPopMenu', p='parentItemScrollList', button=3)
		mc.menuItem('parentItemScrollListMenuSel', p='parentItemScrollListPopMenu', l='select all List', c=self.selectAllParent)
		mc.menuItem('parentItemScrollListMenuHi', p='parentItemScrollListPopMenu', l='select List Items Hi')
		mc.menuItem('parentItemScrollListMenuShape', p='parentItemScrollListPopMenu', l='shape list', c=self.parentSwitchShape)
		mc.menuItem('parentItemScrollListMenuColl_A', p='parentItemScrollListPopMenu', l='call constraint child', c=self.collingConstraintChildren)
		mc.menuItem('parentItemScrollListMenuColl_B', p='parentItemScrollListPopMenu', l='call connection child', c=self.collingConnectionChildren)

		#ペアレントアイテムリストカウントをレイアウトします
		mc.paneLayout('parentCountNumberPane', p='parentItemListPane', configuration='vertical2')
		mc.intField('parentAllNumber', p='parentCountNumberPane')
		mc.intField('parentSelectNumber', p='parentCountNumberPane')
		#ペアレントアイテムリストカウントをレイアウトしました
		mc.setParent('parentCountNumberPane')		
		#ペアレントアイテムリストリムーブをレイアウトします
		mc.paneLayout('parentItemListRemovePane', p='parentItemListPane', configuration='horizontal3')
		mc.button('parentItemListRemoveButton', p='parentItemListRemovePane', l='remove', c=self.removeParent)
		mc.button('parentItemListMoveButton', p='parentItemListRemovePane', l='-->', c=self.moveToChild)
		mc.button('parentItemListSwapButton', p='parentItemListRemovePane', l='<-->', c=self.swap)
		#ペアレントアイテムリストリムーブをレイアウトしました
		mc.setParent('parentItemListRemovePane')
		#ペアレントアイテムフレームをレイアウトしました
		mc.setParent('parentItemListPane')
		#ペアレントアイテムフレームをレイアウトしました
		mc.setParent('parentItemFrame')
		
		#ペアレントアトリビュートをレイアウトします
		mc.frameLayout('parentAttrFrame', p='parentItemPane', l='parent attr')
		mc.paneLayout('parentAttrPane', p='parentAttrFrame', configuration='horizontal2')
		mc.textScrollList('parentAttrScrollList', p='parentAttrPane', ams=True)#
		mc.popupMenu('parentAttrScrollListPopMenu', p='parentAttrScrollList', button=3)
		mc.menuItem('parentAttrScrollListMenuTransforms', p='parentAttrScrollListPopMenu', l='transform only')
		mc.menuItem('parentAttrScrollListMenuAllChannnels', p='parentAttrScrollListPopMenu', l='all channnels')
		#mc.menuItem('parentAttrScrollListMenuSel_TR', p='parentAttrScrollListPopMenu', l='connect TR')
		#mc.menuItem('parentAttrScrollListMenuSel_TRS', p='parentAttrScrollListPopMenu', l='connect TRS')	
		mc.menuItem('parentAttrScrollListMenuSel_T', p='parentAttrScrollListPopMenu', l='connect T', c=self.connectTranslateChannels)
		mc.menuItem('parentAttrScrollListMenuSel_R', p='parentAttrScrollListPopMenu', l='connect R', c=self.connectRotateChannels)
		mc.menuItem('parentAttrScrollListMenuSel_S', p='parentAttrScrollListPopMenu', l='connect S', c=self.connectScaleChannels)	
		mc.menuItem('parentAttrScrollListMenuSel_same', p='parentAttrScrollListPopMenu', l='same attr', c=self.connectSelectChannels)		
		mc.setParent('parentAttrPane')
		#ペアレントアイテムフレームをレイアウトしました
		mc.setParent('parentAttrFrame')
		#ペアレントフレームをレイアウトしました
		mc.setParent('parentItemPane')
				
		#チルドレンフレームをレイアウトします
		mc.paneLayout('childrenItemPane', p='allScrollListPane', configuration='vertical2')
		#チルドレンアトリビュートをレイアウトします
		mc.frameLayout('childrenAttrFrame', p='childrenItemPane', l='children attr')
		mc.paneLayout('childrenAttrPane', p='childrenAttrFrame', configuration='horizontal2')
		mc.textScrollList('childrenAttrScrollList', p='childrenAttrPane', ams=True)#
		mc.popupMenu('childrenAttrScrollListPopMenu', p='childrenAttrScrollList', button=3)
		mc.menuItem('childrenAttrScrollListMenuTransforms', p='childrenAttrScrollListPopMenu', l='transform only')
		mc.menuItem('childrenAttrScrollListMenuAllChannnels', p='childrenAttrScrollListPopMenu', l='all channnels')
		#mc.menuItem('childrenAttrScrollListMenuSel_TR', p='childrenAttrScrollListPopMenu', l='connect TR')	
		#mc.menuItem('childrenAttrScrollListMenuSel_TRS', p='childrenAttrScrollListPopMenu', l='connect TRS')
		mc.menuItem('childrenAttrScrollListMenuSel_T', p='childrenAttrScrollListPopMenu', l='connect T', c=self.connectTranslateChannels)
		mc.menuItem('childrenAttrScrollListMenuSel_R', p='childrenAttrScrollListPopMenu', l='connect R', c=self.connectRotateChannels)	
		mc.menuItem('childrenAttrScrollListMenuSel_S', p='childrenAttrScrollListPopMenu', l='connect S', c=self.connectScaleChannels)	
		mc.menuItem('childrenAttrScrollListMenuSel_same', p='childrenAttrScrollListPopMenu', l='same attr', c=self.connectSelectChannels)	
		
		mc.button('childrenScrollButton', p='childrenAttrPane', l='Switch Attr')
		mc.setParent('childrenAttrPane')
		#チルドレンアイテムフレームをレイアウトしました
		mc.setParent('childrenAttrFrame')
		
		#チルドレンアイテムフレームをレイアウトします
		mc.frameLayout('childrenItemFrame', p='childrenItemPane', l='children item')		
		mc.paneLayout('childrenItemListPane', p='childrenItemFrame', configuration='horizontal4')
		#チルドレンアイテムリストインをレイアウトします
		mc.paneLayout('childrenItemListInAddPane', p='childrenItemListPane', configuration='horizontal2')
		mc.button('childrenItemListInButton', p='childrenItemListInAddPane', l='List Replace', c=self.listInChildren)
		mc.button('childrenItemListAddButton', p='childrenItemListInAddPane', l='List Add', c=self.listAddChildren)
		#チルドレンアイテムリストインをレイアウトしました
		mc.setParent('parentItemListInAddPane')		
		#チルドレンアイテムリストスクロールをレイアウトしました		
		mc.textScrollList('childrenItemScrollList', p='childrenItemListPane', ams=True, sc=self.selectChildrenItem, dcc=self.deselectChildren, dgc=self.childrenDrag, dpc=self.childrenDrop)
		mc.popupMenu('childrenItemScrollListPopMenu', p='childrenItemScrollList', button=3)
		mc.menuItem('childrenItemScrollListMenuSel', p='childrenItemScrollListPopMenu', l='select all List', c=self.selectAllChildren)
		mc.menuItem('childrenItemScrollListMenuHi', p='childrenItemScrollListPopMenu', l='select List Items Hi', c=self.childrenHi)
		mc.menuItem('childrenItemScrollListMenuShape', p='childrenItemScrollListPopMenu', l='shape list', c=self.childrenSwitchShape)
		mc.menuItem('childrenItemScrollListMenuColl_A', p='childrenItemScrollListPopMenu', l='call constraint parent', c=self.collingConstraintParent)
		mc.menuItem('childrenItemScrollListMenuColl_B', p='childrenItemScrollListPopMenu', l='call connection parent', c=self.collingConnectionParent)
		
		#チルドレンアイテムリストカウントをレイアウトします
		mc.paneLayout('childrenCountNumberPane', p='childrenItemListPane', configuration='vertical2')
		mc.intField('childrenAllNumber', p='childrenCountNumberPane')
		mc.intField('childrenSelectNumber', p='childrenCountNumberPane')
		#チルドレンアイテムリストカウントをレイアウトしました
		mc.setParent('childrenCountNumberPane')		
		#チルドレンアイテムリストリムーブをレイアウトします
		mc.paneLayout('childrenItemListRemovePane', p='childrenItemListPane', configuration='horizontal3')
		mc.button('childrenItemListRemoveButton', p='childrenItemListRemovePane', l='remove', c=self.removeChildren)
		mc.button('childrenItemListMoveButton', p='childrenItemListRemovePane', l='<--', c=self.moveToParent)
		mc.button('childrenItemListSwapButton', p='childrenItemListRemovePane', l='Remember', c=self.remenber)
		#チルドレンアイテムリストリムーブをレイアウトしました
		mc.setParent('childrenItemListRemovePane')
		#チルドレンアイテムフレームをレイアウトしました
		mc.setParent('childrenItemListPane')
		#チルドレンアイテムフレームをレイアウトしました
		mc.setParent('childrenItemFrame')
		#チルドレンフレームをレイアウトしました
		mc.setParent('childrenItemPane')
		
		#ペアレントとチルドレンのリストをレイアウトしました
		mc.setParent('allScrollListPane')		
		
		#ベクターアイテムフレームをレイアウトします
		mc.frameLayout('vectorItemFrame', p='relativePane', l='vector item')
		#ベクターアイテム制御パンをレイアウトします
		mc.paneLayout('vectorItemPane', p='vectorItemFrame', configuration='horizontal4')		
		#ベクターアイテムをリストインするための制御パンをレイアウトします
		mc.paneLayout('vectorItemListInAddPane',p='vectorItemPane', configuration='horizontal2')
		mc.button('vectorItemListInButton', p='vectorItemListInAddPane', l='List Replace', c=self.listInVector)
		mc.button('vectorItemListAddButton', p='vectorItemListInAddPane', l='List Add', c=self.listAddVector)
		#ベクターアイテムをリストインするための制御パンをレイアウトしました
		mc.setParent('vectorItemListInAddPane')
		#ベクターアイテムをリストスクロールをレイアウトします
		mc.textScrollList('vectorItemScrollList', p='vectorItemPane', ams=True, sc=self.selectVectorItem, dcc=self.deselectVector, dgc=self.vectorDrag, dpc=self.vectorDrop)
		mc.popupMenu('vectorItemScrollListPopMenu', p='vectorItemScrollList', button=3)
		mc.menuItem('vectorItemScrollListMenuSel', p='vectorItemScrollListPopMenu', l='select List Items', c=self.selectAllVector)
		mc.menuItem('vectorItemScrollListMenuHi', p='vectorItemScrollListPopMenu', l='select List Items Hi', c=self.vectorHi)
		mc.menuItem('vectorItemScrollListMenuShape', p='vectorItemScrollListPopMenu', l='shape list', c=self.vectorSwitchShape)
		#mc.menuItem('vectorItemScrollListMenuColl', p='vectorItemScrollListPopMenu', l='coll others')
		
		#ベクターアイテムの数を表示するイントフィールドをレイアウトします
		mc.paneLayout('vectorCountNumberPane',p='vectorItemPane', configuration='vertical2')
		mc.intField('vectorAllNumber', p='vectorCountNumberPane')
		mc.intField('vectorSelectNumber', p='vectorCountNumberPane')
		#ベクターアイテムの数を表示するイントフィールドをレイアウトしました
		mc.setParent('vectorCountNumberPane')
		#ベクターアイテムをリムーブするための制御パンをレイアウトします
		mc.paneLayout('vectorItemRemovePane',p='vectorItemPane', configuration='horizontal2')
		mc.button('vectorItemListRemoveButton', p='vectorItemRemovePane', l='Remove', c=self.removeVector)
		mc.button('vectorItemListClearButton', p='vectorItemRemovePane', l='All Clear')
		#ベクターアイテムをリムーブするための制御パンをレイアウトしました
		mc.setParent('vectorItemRemovePane')
		#ベクターアイテム制御パンをレイアウトしました
		mc.setParent('vectorItemPane')
		#ベクターアイテムフレームをレイアウトしました
		mc.setParent('vectorItemFrame')
		
		
		#リレーションコントロールタブをレイアウトします
		mc.tabLayout('relativeTab', p='relativePane')
		#様々なコンストレイントのフレームをタイプ別にレイアウトするペインをレイアウトします
		mc.scrollLayout('constraintTypeScroll', p='relativeTab', childResizable=True)
		#トランスレートコンストレイント（いわゆるベーシックなコンストレイント）を行うフレームをレイアウトします
#ペアレントコンストレイントのレイアウトを行います
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		mc.frameLayout('parentConstraintFrame', p='constraintTypeScroll', l='parent constraint', bgc=[0,0,0], collapsable=True, collapse=True)
		mc.paneLayout('parentConstraintPane', p='parentConstraintFrame', configuration='top3')	
		mc.gridLayout('parentConstraintGrid', p='parentConstraintPane')
		mc.checkBox('parentTxCheck', p='parentConstraintGrid', l='tx', value=True)
		mc.checkBox('parentTyCheck', p='parentConstraintGrid', l='ty', value=True)
		mc.checkBox('parentTzCheck', p='parentConstraintGrid', l='tz', value=True)
		mc.checkBox('parentRxCheck', p='parentConstraintGrid', l='rx', value=True)
		mc.checkBox('parentRyCheck', p='parentConstraintGrid', l='ry', value=True)
		mc.checkBox('parentRzCheck', p='parentConstraintGrid', l='rz', value=True)
		mc.setParent('parentConstraintGrid')		
		mc.checkBox('parentConstraintMaintainCheck', p='parentConstraintPane', l='maintain offset')
		mc.paneLayout('parentConstraintExecutePane', p='parentConstraintPane', configuration='horizontal4')
		mc.button('parentConstraintButton',  p='parentConstraintExecutePane', l='parent constraint', c=self.parentC)
		mc.button('parentConstraintSnapButton',  p='parentConstraintExecutePane', l='parent snap constraint', c=self.parentSConst)
		#mc.button('parentConstraintSnapShapeButton',  p='parentConstraintExecutePane', l='parent snap shape')
		#mc.button('parentConstraintSnapValueButton',  p='parentConstraintExecutePane', l='parent snap value')
		mc.setParent('parentConstraintExecutePane')
		mc.setParent('parentConstraintPane')
		mc.setParent('parentConstraintFrame')
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#ペアレントコンストレイントのレイアウトを行いました
#ポイントコンストレイントのレイアウトを行います
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		mc.frameLayout('pointConstraintFrame', p='constraintTypeScroll', l='point constraint', bgc=[0,0,0], collapsable=True, collapse=True)
		mc.paneLayout('pointConstraintPane', p='pointConstraintFrame', configuration='top3')	
		mc.gridLayout('pointConstraintGrid', p='pointConstraintPane')
		mc.checkBox('pointTxCheck', p='pointConstraintGrid', l='tx', value=True)
		mc.checkBox('pointTyCheck', p='pointConstraintGrid', l='ty', value=True)
		mc.checkBox('pointTzCheck', p='pointConstraintGrid', l='tz', value=True)
		mc.setParent('pointConstraintGrid')		
		mc.checkBox('pointConstraintMaintainCheck', p='pointConstraintPane', l='maintain offset')
		mc.paneLayout('pointConstraintExecutePane', p='pointConstraintPane', configuration='horizontal4')
		mc.button('pointConstraintButton',  p='pointConstraintExecutePane', l='point constraint', c=self.pointC)
		mc.button('pointConstraintSnapButton',  p='pointConstraintExecutePane', l='point snap constraint', c=self.pointSConst)
		#mc.button('pointConstraintSnapShapeButton',  p='pointConstraintExecutePane', l='point snap shape')
		#mc.button('pointConstraintSnapValueButton',  p='pointConstraintExecutePane', l='point snap value')
		mc.setParent('pointConstraintExecutePane')
		mc.setParent('pointConstraintPane')
		mc.setParent('pointConstraintFrame')
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#ポイントコンストレイントのレイアウトを行います
#回転コンストレイントのレイアウトを行います
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		mc.frameLayout('rotateConstraintFrame', p='constraintTypeScroll', l='rotate constraint', bgc=[0,0,0], collapsable=True, collapse=True)
		mc.paneLayout('rotateConstraintPane', p='rotateConstraintFrame', configuration='top3')	
		mc.gridLayout('rotateConstraintGrid', p='rotateConstraintPane')
		mc.checkBox('rotateTxCheck', p='rotateConstraintGrid', l='rx', value=True)
		mc.checkBox('rotateTyCheck', p='rotateConstraintGrid', l='ry', value=True)
		mc.checkBox('rotateTzCheck', p='rotateConstraintGrid', l='rz', value=True)
		mc.setParent('rotateConstraintGrid')		
		mc.checkBox('rotateConstraintMaintainCheck', p='rotateConstraintPane', l='maintain offset')
		mc.paneLayout('rotateConstraintExecutePane', p='rotateConstraintPane', configuration='horizontal4')
		mc.button('rotateConstraintButton',  p='rotateConstraintExecutePane', l='rotate constraint', c=self.rotateC)
		mc.button('rotateConstraintSnapButton',  p='rotateConstraintExecutePane', l='rotate snap constraint', c=self.rotateSConst)
		#mc.button('rotateConstraintSnapShapeButton',  p='rotateConstraintExecutePane', l='rotate snap shape')
		#mc.button('rotateConstraintSnapValueButton',  p='rotateConstraintExecutePane', l='rotate snap value')
		mc.setParent('rotateConstraintExecutePane')
		mc.setParent('rotateConstraintPane')
		mc.setParent('rotateConstraintFrame')
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#回転コンストレイントのレイアウトを行います
#伸縮コンストレイントのレイアウトを行います
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		mc.frameLayout('scaleConstraintFrame', p='constraintTypeScroll', l='scale constraint', bgc=[0,0,0], collapsable=True, collapse=True)
		mc.paneLayout('scaleConstraintPane', p='scaleConstraintFrame', configuration='top3')	
		mc.gridLayout('scaleConstraintGrid', p='scaleConstraintPane')
		mc.checkBox('scaleTxCheck', p='scaleConstraintGrid', l='rx', value=True)
		mc.checkBox('scaleTyCheck', p='scaleConstraintGrid', l='ry', value=True)
		mc.checkBox('scaleTzCheck', p='scaleConstraintGrid', l='rz', value=True)
		mc.setParent('scaleConstraintGrid')		
		mc.checkBox('scaleConstraintMaintainCheck', p='scaleConstraintPane', l='maintain offset')
		mc.paneLayout('scaleConstraintExecutePane', p='scaleConstraintPane', configuration='horizontal4')
		mc.button('scaleConstraintButton',  p='scaleConstraintExecutePane', l='scale constraint', c=self.scaleC)
		mc.button('scaleConstraintSnapButton',  p='scaleConstraintExecutePane', l='scale snap constraint', c=self.scaleSConst)
		#mc.button('scaleConstraintSnapShapeButton',  p='scaleConstraintExecutePane', l='scale snap shape')
		#mc.button('scaleConstraintSnapValueButton',  p='scaleConstraintExecutePane', l='scale snap value')
		mc.setParent('scaleConstraintExecutePane')
		mc.setParent('scaleConstraintPane')
		mc.setParent('scaleConstraintFrame')
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#伸縮コンストレイントのレイアウトを行います
		#トランスレートコンストレイント（いわゆるベーシックなコンストレイント）を行うフレームをレイアウトしました		
		#mc.setParent('transformConstrainFrame')
		
		#シェイプを使用したコンストレイントノードの構築を行うフレームをレイアウトします
#フォリクルコンストレイントのレイアウトを行います				
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		mc.frameLayout('follicleConstraintFrame', p='constraintTypeScroll', l='follicle constraint', bgc=[0,0,0], collapsable=True, collapse=True)
		mc.paneLayout('follicleOffsetPane', p='follicleConstraintFrame', configuration='horizontal4')
		mc.checkBox('meshFollicleOffsetCheck', p='follicleOffsetPane', l='offset')		
		mc.button('meshFollicleConstraintButton', p='follicleOffsetPane', l='meshFollicle constraint', c=self.follicleMeshC)		
		mc.checkBox('nubFollicleOffsetCheck', p='follicleOffsetPane', l='offset')
		mc.button('nubFollicleConstraintButton', p='follicleOffsetPane', l='nubFollicle constraint', c=self.follicleSafaceC)
		mc.setParent('follicleOffsetPane')		
		mc.setParent('follicleConstraintFrame')
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#フォリクルコンストレイントのレイアウトを行います		
#カーブインフォコンストレイントのレイアウトを行います		
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		mc.frameLayout('curveShapeConstraintFrame', p='constraintTypeScroll', l='curveShape constraint', bgc=[0,0,0], collapsable=True, collapse=True)
		mc.button('curveInfoConstraintButton', p='curveShapeConstraintFrame', l='curveInfo constraint', c=self.curveInfoC)
		mc.setParent('curveShapeConstraintFrame')		
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#カーブインフォコンストレイントのレイアウトを行います
#タンジェントコンストレイントのレイアウトを行います------------------------------------------------------------------------------------------------------------------------------------------------------
		mc.frameLayout('tangentConstraintFrame', p='constraintTypeScroll', l='tangent constraint', bgc=[0,0,0], collapsable=True, collapse=True)
		mc.paneLayout('tangentConstraintPane', p='tangentConstraintFrame', configuration='horizontal4')
		mc.intFieldGrp('tangentConstraintAimVecto', p='tangentConstraintPane', numberOfFields=3, v1=1, v2=0, v3=0, cw3=[50,50,50])
		mc.intFieldGrp('tangentConstraintUpVecto', p='tangentConstraintPane', numberOfFields=3, v1=1, v2=0, v3=0, cw3=[50,50,50])
		mc.optionMenu('tangentConstraintUpVector', p='tangentConstraintPane')
		mc.menuItem( label='opjectUp' )
		mc.menuItem( label='opjectRotationUp')
		mc.button('tangentConstraintButton', p='tangentConstraintPane', l='tangent constraint', c=self.tangentC)
		mc.setParent('tangentConstraintPane')
		mc.setParent('tangentConstraintFrame')
#タンジェントコンストレイントのレイアウトを行います------------------------------------------------------------------------------------------------------------------------------------------------------
		#シェイプを使用したコンストレイントノードの構築を行うフレームをレイアウトしました
		#mc.setParent('shapeConstraintFrame')
		
		#特殊コンストレイントを構築するフレームをレイアウトします
#エイムコンストレイントのレイアウトを行います		
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		#mc.frameLayout('otherConstraintFrame', p='constraintTypeScroll', l='other constraint', collapsable=True, collapse=True)
		mc.frameLayout('aimConstraintFrame', p='constraintTypeScroll', l='aim constraint', bgc=[0,0,0], collapsable=True, collapse=True)
		mc.paneLayout('aimConstraintPane', p='aimConstraintFrame', configuration='quad')		
		mc.text('aimVectText', p='aimConstraintPane', l='aimVect')
		mc.intFieldGrp('aimConstraintVectField', p='aimConstraintPane', numberOfFields=3, v1=1, v2=0, v3=0, cw3=[50,50,50])
		mc.intFieldGrp('aimUpConstraintVectField', p='aimConstraintPane', numberOfFields=3, v1=0, v2=1, v3=0, cw3=[50,50,50])
		mc.text('aimUpVectText', p='aimConstraintPane', l='upVect')
		mc.paneLayout('aimOptionConstraintPane', p='aimConstraintFrame', configuration='top3')
		mc.gridLayout('aimConstraintGrid', p='aimOptionConstraintPane')
		mc.checkBox('aimRxCheck', p='aimConstraintGrid', l='rx', value=True)
		mc.checkBox('aimRyCheck', p='aimConstraintGrid', l='ry', value=True)
		mc.checkBox('aimRzCheck', p='aimConstraintGrid', l='rz', value=True)		
		mc.setParent('aimConstraintGrid')		
		mc.checkBox('aimConstraintMaintainCheck', p='aimOptionConstraintPane', l='maintain offset')
		mc.paneLayout('aimConstraintOptionExcutPane',p='aimOptionConstraintPane', configuration='horizontal2')
		mc.optionMenu('aimConstraintUpVector', p='aimConstraintOptionExcutPane')
		mc.menuItem( label='opjectUp' )
		mc.menuItem( label='opjectRotationUp' )
		mc.button('aimConstraintButton',  p='aimConstraintOptionExcutPane', l='aim constraint', c=self.aimC)
		mc.setParent('aimConstraintOptionExcutPane')		
		mc.setParent('aimOptionConstraintPane')
		mc.setParent('aimConstraintPane')	
		mc.setParent('aimConstraintFrame')		
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#エイムコンストレイントのレイアウトを行います		
		#特殊コンストレイントを構築するフレームをレイアウトしました
		#mc.setParent('shapeConstraintFrame')		
		#様々なコンストレイントのフレームをタイプ別にレイアウトするペインをレイアウトしました
		mc.setParent('constraintTypeScroll')
		
		#コネクション時にインサートするユーティリティーの種類のリストをレイアウトします
		mc.paneLayout('insertUtirilyListPane', p='relativeTab')
		#コネクション時にインサートするユーティリティーの種類のリストをレイアウトしました
		mc.setParent('insertUtirilyListPane')		
		#リレーションコントロールタブをレイアウトしました
		mc.setParent('relativeTab')
		
		#リレーションさせるリストとリレーションのタイムについてタブをレイアウトしました
		mc.setParent('relativePane')
		
		#コンストレイントノードのリストを分類してレイアウトします
		mc.paneLayout('listConstraintNodesPane', p='mainTab', configuration='right3')
		mc.frameLayout('constraintTypeListFrame', p='listConstraintNodesPane', l='Constraint Type')
		mc.paneLayout('constraintTypeListPane', p='constraintTypeListFrame', configuration='horizontal2')
		mc.textScrollList('constraintTypeScroll', p='constraintTypeListPane', sc=self.listInConstrainGrp)#
		mc.button('constraintTypeScrollButton', p='constraintTypeListPane', l='Reload', c=self.listInConstraintType)
		mc.setParent('constraintTypeListPane')
		mc.setParent('constraintTypeListFrame')
		mc.paneLayout('constraintGrpListPane', p='listConstraintNodesPane', configuration='vertical3')
		mc.frameLayout('constraintGrpScrollFrame', p='constraintGrpListPane', l='Constrain grp')
		mc.textScrollList('constraintGrpScrollList', p='constraintGrpScrollFrame',sc=self.listInConstrainContent)#
		mc.setParent('constraintGrpScrollFrame')
		mc.frameLayout('constraintGrpInsideScrollFrame', p='constraintGrpListPane', l='Inside node')
		mc.textScrollList('constraintGrpInsideScrollList', p='constraintGrpInsideScrollFrame', ams=True)#
		mc.setParent('constraintGrpInsideScrollFrame')
		mc.frameLayout('constraintGrpOutsideScrollFrame', p='constraintGrpListPane', l='Outside node')
		mc.textScrollList('constraintGrpOutsideScrollList', p='constraintGrpOutsideScrollFrame', ams=True)#
		mc.setParent('constraintGrpOutsideScrollFrame')		
		mc.setParent('constraintGrpListPane')
		mc.paneLayout('constraintRelativeListPane', p='listConstraintNodesPane', configuration='vertical3')
		#mc.button('constraintItemOutButton', p='constraintRelativeListPane', l='List Out')
		mc.button('constraintItemInButton', p='constraintRelativeListPane', l='List In', c=self.callingFromConstraint)		
		mc.button('constraintItemDeleteButton', p='constraintRelativeListPane', l='Delete Item', c=self.delListConstraint)
		mc.setParent('constraintRelativeListPane')
		#コンストレイントノードのリストを分類してレイアウトしました
		mc.setParent('listConstraintNodesPane')

		
		mc.setParent('relativePane')
		#メインタブを設定します
		mc.setParent('mainTab')
		mc.showWindow('connectorWindow')
		
	#ウィンドウをリサイズします
	def windowResize(self, *args):
		#コンストレイントを作成リストのタブ名を変更します
		mc.tabLayout('mainTab', e=True, tabLabel=['relativePane', 'Conect list'])
		#コンストレイントの種類をリストするタブ名を変更します
		mc.tabLayout('mainTab', e=True, tabLabel=['listConstraintNodesPane', 'Constraint Type'])
		
		#コンストレイントのタイプをリストするタブをリネームします
		mc.tabLayout('relativeTab', e=True, tabLabel=['constraintTypeScroll', 'Constraint list'])
		#コネクションを作成するときの補助を行うユーティリティーノードを作成するタブをリネームします
		mc.tabLayout('relativeTab', e=True, tabLabel=['insertUtirilyListPane', 'Utirily list'])
		
		#コンストレイントを作成するパンレイアウトの比率を変更します
		mc.paneLayout('relativePane', e=True, paneSize=[1,70,100])
		mc.paneLayout('relativePane', e=True, paneSize=[2,0,100])
		
		#コンストレイントを作成するそれぞれのアトリビュートパンレイアウトの比率を変更します
		mc.paneLayout('parentAttrPane', e=True, paneSize=[1,100,98])
		mc.paneLayout('childrenAttrPane', e=True, paneSize=[1,100,98])
		
		#コンストレイントを作成するそれぞれのリストパンレイアウトの左右比率を変更します		
		mc.paneLayout('parentItemPane', e=True, paneSize=[1,100,100])
		mc.paneLayout('childrenItemPane', e=True, paneSize=[2,100,100])
		
		#リストされているアイテムの数を表すintフィールドの比率を変更します
		mc.paneLayout('parentCountNumberPane', e=True, paneSize=[1,50,100])
		mc.paneLayout('childrenCountNumberPane', e=True, paneSize=[1,50,100])
		
		#コンストレイントを作成するそれぞれのリストパン内部のレイアウトの比率を変更します		
		mc.paneLayout('parentItemListPane', e=True, paneSize=[1,100,5])		
		mc.paneLayout('parentItemListPane', e=True, paneSize=[2,100,80])
		mc.paneLayout('parentItemListPane', e=True, paneSize=[3,100,3])
		mc.paneLayout('parentItemListPane', e=True, paneSize=[4,100,7])		
		mc.paneLayout('childrenItemListPane', e=True, paneSize=[1,100,5])		
		mc.paneLayout('childrenItemListPane', e=True, paneSize=[2,100,80])
		mc.paneLayout('childrenItemListPane', e=True, paneSize=[3,100,3])
		mc.paneLayout('childrenItemListPane', e=True, paneSize=[4,100,7])		
		mc.paneLayout('vectorItemPane', e=True, paneSize=[1,100,5])		
		mc.paneLayout('vectorItemPane', e=True, paneSize=[2,100,66])
		mc.paneLayout('vectorItemPane', e=True, paneSize=[3,100,10])
		mc.paneLayout('vectorItemPane', e=True, paneSize=[4,100,24])
		
		#コンストレイントの種類の内訳をリストするパンの比率を変更します
		mc.paneLayout('listConstraintNodesPane', e=True, paneSize=[3,70,7])
		#コンストレイントの種類のリストするパンの比率を変更します
		mc.paneLayout('constraintTypeListPane', e=True, paneSize=[1,100,95])
		#コンストレイントの種類を収集してリストします
		self.listInConstraintType()
		
		
	#シーン内に存在するコンストレイントノードを分類して、コンストレイントタイプスクロールに記入
	def listInConstraintType(self, *args):
		mc.textScrollList('constraintTypeScroll', e=True, removeAll=True)
		global HA_constraintTypeDict
		HA_constraintTypeDict = {}
		constraintAllTypeList = []
		constrainItems = mc.ls( type='constraint' )
		for i in constrainItems:
			constraintAllTypeList.append(mc.nodeType(i))
		
		constraintTypeList = set(constraintAllTypeList)
		for i in constraintTypeList:
			mc.textScrollList('constraintTypeScroll', e=True, append=i)
			cNode = mc.ls(type=i)
			cParent = []
			cOut = []
			for e in cNode:
				parentList = mc.listRelatives(e, p=True, type='transform')
				shapes = mc.listRelatives(parentList, s=True)
				if shapes != None:
					mc.parent(e, world=True)
					cOut.append(e)
				#print parentList
				if parentList != None:
					cParent.extend(parentList)
				else:
					cOut.append(e)
			#print cOut
			
			if cOut != None:
				HA_constraintTypeDict[i] = [list(set(cParent)), list(set(cOut))]
			elif cOut == None:
				HA_constraintTypeDict[i] = list(set(cParent))
#コンストレイントノードを収集しました
#uiを作成します---------------------------------------------------------------------------------------
###############################################################################################################################################################################################################
#後ろのタブで任意のコンストレイントノードを選択したとき辞書の中身をリストします--------------------------------------------
	def listInConstrainGrp(self, *args):
		global HA_constraintTypeDict
		#self.listInConstraintType()
		type = mc.textScrollList('constraintTypeScroll', q=True, selectItem=True)
		mc.textScrollList('constraintGrpScrollList', e=True, removeAll=True)
		mc.textScrollList('constraintGrpInsideScrollList', e=True, removeAll=True)
		mc.textScrollList('constraintGrpOutsideScrollList', e=True, removeAll=True)
		cList = HA_constraintTypeDict[type[0]]
		#print cList
		cGrp = cList.pop(0)
		
		#print other
		if cGrp != None:
			mc.textScrollList('constraintGrpScrollList', e=True, append=cGrp)
		for i in cList:
			if i != [] and i != None:
				mc.textScrollList('constraintGrpOutsideScrollList', e=True, append=i)

#後ろのタブで任意のコンストレイントノードを選択したとき辞書の中身をリストします--------------------------------------------
#コンストレイントグループを選択したとき、グループ内の選択中のコンストレイントタイプを見gから二番目のリストにリストイン-------------------
	def listInConstrainContent(self, *args):
		global HA_constraintTypeDict
		type = mc.textScrollList('constraintTypeScroll', q=True, selectItem=True)
		grp = mc.textScrollList('constraintGrpScrollList', q=True, selectItem=True)
		mc.textScrollList('constraintGrpInsideScrollList', e=True, removeAll=True)
		cNodes = mc.ls((grp[0] + '|*'), type=type[0])
		mc.textScrollList('constraintGrpInsideScrollList', e=True, append=cNodes)
#コンストレイントグループを選択したとき、グループ内の選択中のコンストレイントタイプを見gから二番目のリストにリストイン-------------------
#後ろのタブで、listInボタンを押した時、コンストレイントに関係するすべてのノードを手前のタブのリストに書き込み
	def callingFromConstraint(self, *args):
		mc.textScrollList('parentItemScrollList', e=True, removeAll=True)
		mc.textScrollList('childrenItemScrollList', e=True, removeAll=True)
		mc.textScrollList('vectorItemScrollList', e=True, removeAll=True)
		
		trigger = 'constraintGrpInsideScrollList'	
		item = self.getSelectListItems(trigger)
		for i in item:
			cList = list(set( mc.listConnections(i + '.constraintParentInverseMatrix') ))
			pList = list(set( mc.listConnections(i + '.target', s=True, d=False) ))
			pList.remove(i)
			
			
			if len(cList) > len(pList):
				sub = len(cList) - len(pList)
				for i in range(0,sub):
					pList.append('LargeFamily')
			
			elif len(cList) < len(pList):
				sub = len(pList) - len(cList)
				for i in range(0,sub):
					cList.append('fChild')
				
			for e,v in enumerate(cList):
				mc.textScrollList('parentItemScrollList', e=True, append=pList[e])
				mc.textScrollList('childrenItemScrollList', e=True, append=cList[e])
				
			#アップベクターが存在した場合は、ベクターリストに書き込みます
			#複数の子オブジェクトをエイムする場合は個別にコンストレイントノードが作成されるので、考慮不要
			#ただ、複数の親が一つの子をエイムさせている場合は、その親の数だけ、アップベクターをリストする必要がある
			getUp = mc.listAttr(item[0], string='worldUpMatrix')
			getUpList = []
			if getUp != None:
				#print ''
				getUpList = mc.listConnections(item[0] + '.worldUpMatrix')
			if getUpList != None:	
				for i in pList:
					mc.textScrollList('vectorItemScrollList', e=True, append=getUpList)
		
		#リストの残数を数えなおします
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
		#ベクター数えなおし
		trigger = 'vectorItemScrollList'
		triggerInt = 'vectorAllNumber'
		selInt = 'vectorSelectNumber'
		self.counter(trigger, triggerInt, selInt)	
#後ろのタブで、listInボタンを押した時、コンストレイントに関係するすべてのノードを手前のタブのリストに書き込み
#後ろのタブで選択したコンストレイントを削除します
	def delListConstraint(self, *args):
		getGrp = mc.textScrollList('constraintGrpScrollList', q=True, selectItem=True)
		getItem = mc.textScrollList('constraintGrpOutsideScrollList', q=True, selectItem=True)
		mc.delete(getGrp)
		mc.delete(getItem)
		
		self.listInConstraintType()

		#リストの残数を数えなおします
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
		#ベクター数えなおし
		trigger = 'vectorItemScrollList'
		triggerInt = 'vectorAllNumber'
		selInt = 'vectorSelectNumber'
		self.counter(trigger, triggerInt, selInt)	
#後ろのタブで選択したコンストレイントを削除します
###############################################################################################################################################################################################################
#共用部分を作成します(リストリメンバー用のメモ、選択リストリターン、リストカウント、D&D)---------------------------------------------------------
	#選択するアイテムリストをシーン内でアイテムを選択します
	def selectScenesItems(self, trigger, *args):
		pick = self.getSelectListItems(trigger)
		getItems = []
		noneItems = []
		for i in pick:
			if mc.objExists(i) == True:
				getItems.append(i)
			else:
				noneItems.append(i)
		if noneItems != []:
			errorItems = '_'.join(noneItems)
			mc.confirmDialog(m='there items not found...\n' + errorItems)
		else:
			mc.select(getItems, r=True)
	
	#rimember用のリストを現在のリストで書き換えます
	def lastScrollList(self, trigger, *args):
		global HA_parentListRemember
		global HA_childrenListRemember
		global HA_vectorListRemember
		
		if trigger == 'parentItemScrollList':
			items = mc.textScrollList('parentItemScrollList', q=True, allItems=True)
			if items != None:
				HA_parentListRemember = items
			else:
				HA_parentListRemember = []
				
		if trigger == 'childrenItemScrollList':
			items = mc.textScrollList('childrenItemScrollList', q=True, allItems=True)
			if items != None:
				HA_childrenListRemember = items
			else:
				HA_childrenListRemember = []
				
		if trigger == 'vectorItemScrollList':
			items = mc.textScrollList('vectorItemScrollList', q=True, allItems=True)
			if items != None:
				HA_vectorListRemember = items
			else:
				HA_vectorListRemember = []
	#アイテム数をカウントします
	def counter(self, trigger, triggerInt, selInt, *args):
		allItems = mc.textScrollList(trigger, q=True, numberOfItems=True)
		selTtem = mc.textScrollList(trigger, q=True, numberOfSelectedItems=True)
		if allItems != None:
			mc.intField(triggerInt, e=True, value=allItems)
		else:
			mc.intField(triggerInt, e=True, value=0)
		if selTtem != None:
			mc.intField(selInt, e=True, value=selTtem)
		else:
			mc.intField(selInt, e=True, value=0)
		
	#それぞれのリストで、選択するべきアイテムを収集します
	def getSelectListItems(self, trigger, *args):
		selItems = mc.textScrollList(trigger, q=True, selectItem=True)
		if selItems == None or selItems == []:
			selItems = mc.textScrollList(trigger, q=True, allItems=True)		
		return selItems

#共用部分を作成します(リストリメンバー用のメモ、選択リストリターン、リストカウント、D&D)---------------------------------------------------------	
#リスト内アイテム選択時にシーン内同名アイテム選択
	#ペアレントリスト内のアイテムが選択されたとき、シーン内同名アイテムを選択
	def selectParentItem(self, *args):
		trigger = 'parentItemScrollList'
		self.selectScenesItems(trigger)
		
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'
		self.counter(trigger, triggerInt, selInt)#defの行数記入予定
		
		#アトリビュートリストを描きこみます
		self.listParentAttrKeyble()

	#チルドレンリスト内のアイテムが選択されたとき、シーン内同名アイテムを選択
	def selectChildrenItem(self, *args):
		trigger = 'childrenItemScrollList'
		self.selectScenesItems(trigger)
		
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'
		self.counter(trigger, triggerInt, selInt)#defの行数記入予定
		
		#アトリビュートリストを描きこみます
		self.listChildrenAttrKeyble()
		
	#ベクターリスト内のアイテムが選択されたとき、シーン内同名アイテムを選択
	def selectVectorItem(self, *args):
		trigger = 'vectorItemScrollList'
		self.selectScenesItems(trigger)
		
		triggerInt = 'vectorAllNumber'
		selInt = 'vectorSelectNumber'
		self.counter(trigger, triggerInt, selInt)#defの行数記入予定

#アイテムダブルクリック時にアイテム選択を解除します----------------------------------------------------------------------------------
	#ペアレントの選択を解除します
	def deselectParent(self, *args):
		trigger = 'parentItemScrollList'
		self.deselectScrollList(trigger)#defの行数記入予定
		
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'
		self.counter(trigger, triggerInt, selInt)#defの行数記入予定
		
	#チルドレンの選択を解除します		
	def deselectChildren(self, *args):
		trigger = 'childrenItemScrollList'
		self.deselectScrollList(trigger)#defの行数記入予定
		
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'
		self.counter(trigger, triggerInt, selInt)#defの行数記入予定
		
	#ヴェクターの選択を解除します		
	def deselectVector(self, *args):	
		trigger = 'vectorItemScrollList'
		self.deselectScrollList(trigger)#defの行数記入予定
				
		triggerInt = 'vectorAllNumber'
		selInt = 'vectorSelectNumber'
		self.counter(trigger, triggerInt, selInt)#defの行数記入予定
	#アイテムをディセレクトします
	def deselectScrollList(self, trigger, *args):
		mc.textScrollList(trigger, e=True, deselectAll=True)
		mc.select(clear=True)
#アイテムをディセレクトします--------------------------------------------------------------------------------------------
#リストインします----------------------------------------------------------------------------------------------------
	#ペアレントにリストインします
	def listInParent(self, *args):
		trigger = 'parentItemScrollList'
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'		
		
		self.listInSceneItem(trigger)
		self.lastScrollList(trigger)
		self.counter(trigger, triggerInt, selInt)

	#チルドレンにリストインします
	def listInChildren(self, *args):
		trigger = 'childrenItemScrollList'	
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'
		
		self.listInSceneItem(trigger)
		self.lastScrollList(trigger)
		self.counter(trigger, triggerInt, selInt)
		
	#ベクターにリストインします
	def listInVector(self, *args):
		trigger = 'vectorItemScrollList'
		triggerInt = 'vectorAllNumber'
		selInt = 'vectorSelectNumber'
		
		self.listInSceneItem(trigger)		
		self.lastScrollList(trigger)
		self.counter(trigger, triggerInt, selInt)
	
	#リストインします
	def listInSceneItem(self, trigger, *args):	
		listIn = mc.ls(sl=True)
		if listIn != None:
			mc.textScrollList(trigger, e=True, removeAll=True)
			mc.textScrollList(trigger, e=True, append=listIn)	
#リストインします----------------------------------------------------------------------------------------------------
#リストにアッドします--------------------------------------------------------------------------------------------------
	#ペアレントにアッドします
	def listAddParent(self, *args):
		trigger = 'parentItemScrollList'		
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'
		
		self.lastScrollList(trigger)
		self.listAddItem(trigger)
		self.counter(trigger, triggerInt, selInt)

	#チルドレンにアッドします
	def listAddChildren(self, *args):
		trigger = 'childrenItemScrollList'
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'
		
		self.lastScrollList(trigger)				
		self.listAddItem(trigger)
		self.counter(trigger, triggerInt, selInt)
		
	#ベクターにアッドします
	def listAddVector(self, *args):
		trigger = 'vectorItemScrollList'		
		triggerInt = 'vectorAllNumber'
		selInt = 'vectorSelectNumber'
		
		self.lastScrollList(trigger)		
		self.listAddItem(trigger)
		self.counter(trigger, triggerInt, selInt)
		
	#リストにアッドします
	def listAddItem(self, trigger, *args):
		listIn = mc.ls(sl=True)
		if listIn != None:
			mc.textScrollList(trigger, e=True, append=listIn)
#リストにアッドします--------------------------------------------------------------------------------------------------
#リムーブします-----------------------------------------------------------------------------------------------------	
	#ペアレントをリムーブします
	def removeParent(self, *args):
		trigger = 'parentItemScrollList'
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'
		
		self.lastScrollList(trigger)		
		self.removeItem(trigger)
		self.counter(trigger, triggerInt, selInt)
				
	#チルドレンをリムーブします
	def removeChildren(self, *args):
		trigger = 'childrenItemScrollList'		
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'
		
		self.lastScrollList(trigger)
		self.removeItem(trigger)
		self.counter(trigger, triggerInt, selInt)		
					
	#ベクターをリムーブします
	def removeVector(self, *args):
		trigger = 'vectorItemScrollList'
		triggerInt = 'vectorAllNumber'
		selInt = 'vectorSelectNumber'
		
		self.lastScrollList(trigger)
		self.removeItem(trigger)
		self.counter(trigger, triggerInt, selInt)
							
	#リムーブします
	def removeItem(self, trigger, *args):
		removeList = self.getSelectListItems(trigger)
		if removeList != None:
			mc.textScrollList(trigger, e=True, removeItem=removeList)
#リムーブします-----------------------------------------------------------------------------------------------------	
#左右のリストの内容を入れ替えます---------------------------------------------------------------------------------------	
	#右へ移動します
	def moveToChild(self, *args):
		#トリガーを指定します
		trigger ='parentItemScrollList'
		#セレクトアイテムを取得します
		memo = self.getSelectListItems(trigger)
		
		#チルドレンに追加します
		if memo != None:
			#ペアレントからリムーブします
			mc.textScrollList('parentItemScrollList', e=True, removeItem=memo)
			mc.textScrollList('childrenItemScrollList', e=True, append=memo)
			
		#ペアレントリストを記憶します
		trigger ='parentItemScrollList'
		self.lastScrollList(trigger)
		#チルドレンリストを記憶します		
		trigger ='childrenItemScrollList'
		self.lastScrollList(trigger)		
		
		#ペアレント数えなおし
		trigger = 'parentItemScrollList'
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
				
		#チルドレン数えなおし
		trigger ='childrenItemScrollList'
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'		
		self.counter(trigger, triggerInt, selInt)		
									
	#左へ移動します
	def moveToParent(self, *args):
		#トリガーを指定します
		trigger = 'childrenItemScrollList'
		#セレクトアイテムを取得します
		memo = self.getSelectListItems(trigger)
		
		#ペアレントに追加します
		if memo != None:
			#チルドレンからリムーブします		
			mc.textScrollList('childrenItemScrollList', e=True, removeItem=memo)
			mc.textScrollList('parentItemScrollList', e=True, append=memo)
		
		#ペアレントリストを記憶します
		trigger ='parentItemScrollList'
		self.lastScrollList(trigger)
		#チルドレンリストを記憶します		
		trigger ='childrenItemScrollList'
		self.lastScrollList(trigger)

		#ペアレント数えなおし
		trigger = 'parentItemScrollList'
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
				
		#チルドレン数えなおし
		trigger ='childrenItemScrollList'
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'		
		self.counter(trigger, triggerInt, selInt)				
						
	#左右入れ替え
	def swap(self, *args):
		#移動アイテムを収集します
		trigger ='parentItemScrollList'
		swapP = self.getSelectListItems(trigger)
			
		#移動アイテムを収集します
		trigger ='childrenItemScrollList'
		swapC = self.getSelectListItems(trigger)		
		
		if swapC != None:
			mc.textScrollList('childrenItemScrollList', e=True, removeItem=swapC)
			mc.textScrollList('parentItemScrollList', e=True, append=swapC)
			
		if swapP != None:
			mc.textScrollList('parentItemScrollList', e=True, removeItem=swapP)
			mc.textScrollList('childrenItemScrollList', e=True, append=swapP)
		
		#ペアレントリストを記憶します
		trigger ='parentItemScrollList'
		self.lastScrollList(trigger)
		#チルドレンリストを記憶します		
		trigger ='childrenItemScrollList'
		self.lastScrollList(trigger)
		#ベクターリストを記憶します		
		trigger ='vectorItemScrollList'
		self.lastScrollList(trigger)

		#ペアレント数えなおし
		trigger = 'parentItemScrollList'
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
				
		#チルドレン数えなおし
		trigger ='childrenItemScrollList'
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'		
		self.counter(trigger, triggerInt, selInt)				
		
	#思い出す
	def remenber(self, *args):
		global HA_parentListRemember
		global HA_childrenListRemember
		global HA_vectorListRemember		
		rememberP = HA_parentListRemember
		rememberC = HA_childrenListRemember
		rememberV = HA_vectorListRemember
		
		#ペアレントリストを記憶します
		trigger ='parentItemScrollList'
		self.lastScrollList(trigger)
		#チルドレンリストを記憶します		
		trigger ='childrenItemScrollList'
		self.lastScrollList(trigger)
		#ベクターリストを記憶します		
		trigger ='vectorItemScrollList'
		self.lastScrollList(trigger)
				
		mc.textScrollList('parentItemScrollList', e=True, removeAll=True)
		mc.textScrollList('childrenItemScrollList', e=True, removeAll=True)
		mc.textScrollList('vectorItemScrollList', e=True, removeAll=True)
		
		if HA_parentListRemember != None:
			mc.textScrollList('parentItemScrollList', e=True, append=rememberP)
		if HA_childrenListRemember != None:
			mc.textScrollList('childrenItemScrollList', e=True, append=rememberC)	
		if HA_vectorListRemember != None:
			mc.textScrollList('vectorItemScrollList', e=True, append=rememberV)			
		
		#ペアレント数えなおし
		trigger = 'parentItemScrollList'
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
				
		#チルドレン数えなおし
		trigger ='childrenItemScrollList'
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'		
		self.counter(trigger, triggerInt, selInt)		
		
		#ベクター数えなおし
		trigger = 'vectorItemScrollList'
		triggerInt = 'vectorAllNumber'
		selInt = 'vectorSelectNumber'
		self.counter(trigger, triggerInt, selInt)					
#左右のリストの内容を入れ替えます---------------------------------------------------------------------------------------	
#全選択
	#ペアレントリスト内のすべてのアイテムを選択します
	def selectAllParent(self, *args):
		trigger = 'parentItemScrollList'
		self.selectAll(trigger)
		
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
		
	#チルドレンリスト内のすべてのアイテムを選択します
	def selectAllChildren(self, *args):
		trigger = 'childrenItemScrollList'
		self.selectAll(trigger)
		
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'		
		self.counter(trigger, triggerInt, selInt)		
		
	#ベクターリスト内のすべてのアイテムを選択します
	def selectAllVector(self, *args):
		trigger = 'vectorItemScrollList'
		self.selectAll(trigger)
		
		triggerInt = 'vectorAllNumber'
		selInt = 'vectorSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
	#継承したスクロールアイテムを選択して選択します
	def selectAll(self, trigger, *args):
		all = mc.textScrollList(trigger, q=True, allItems=True)
		mc.textScrollList(trigger, e=True, selectItem=all)
		self.selectScenesItems(trigger)
				
#ヒエラルキーを選択します
	#ペアレントリストのアイテムを階層で選択します
	def parentHi(self, *args):
		trigger ='parentItemScrollList'
		self.listHierarchy(trigger)
		
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
		
	#チルドレンリストを記憶します	
	def childrenHi(self, *args):
		trigger ='childrenItemScrollList'
		self.listHierarchy(trigger)
		
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
	
	#ヴェクターリストを記憶します	
	def vectorHi(self, *args):
		trigger ='vectorItemScrollList'
		self.listHierarchy(trigger)
		
		triggerInt = 'vectorAllNumber'
		selInt = 'vectorSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
		
	#選択したアイテムが保持しているすべてのチルドレンを選択します
	def listHierarchy(self, trigger, *args):		
		items = self.getSelectListItems(trigger)
		selHi = []
		for i in items:
			mc.select(i,r=True, hi=True)	
			selHi.extend(mc.ls(sl=True, type='transform'))
			mc.select(clear=True)
		
		mc.select(selHi,r=True)
		
	
	#ペアレントリストのアイテムをシェイプノードで置き換えます
	def parentSwitchShape(self, *args):				
		trigger = 'parentItemScrollList'
		self.lastScrollList(trigger)
		
		self.listItemShape(trigger)
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
		
	#チルドレンリストのアイテムをシェイプノードで置き換えます
	def childrenSwitchShape(self, *args):				
		trigger = 'childrenItemScrollList'
		self.lastScrollList(trigger)
		
		self.listItemShape(trigger)
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
		
	#ヴェクターリストのアイテムをシェイプノードで置き換えます
	def vectorSwitchShape(self, *args):				
		trigger = 'vectorItemScrollList'
		self.lastScrollList(trigger)
		
		self.listItemShape(trigger)
		triggerInt = 'vectorAllNumber'
		selInt = 'vectorSelectNumber'		
		self.counter(trigger, triggerInt, selInt)

	#リストされているアイテムのシェイプノードを取得します
	def listItemShape(self, trigger, *args):
		transform = mc.textScrollList(trigger, q=True, allItems=True)
		shapeNodes = []
		flug = 0
		for i in transform:
			sh = mc.listRelatives(i, s=True)
			#print sh
			if sh != None:
				shapeNodes.extend(sh)
			else:
				flug = 1
		if flug == 1:
			mc.confirmDialog(m="!!list size down\nbecaue don't have shape inside!!")
		mc.textScrollList(trigger, e=True, removeAll=True)
		mc.textScrollList(trigger, e=True, append=shapeNodes)

#コンストレイントを呼び出します（双方全消しの上、書き直し）
	#ペアレント側からチルドレンを呼び出します
	def collingConstraintChildren(self, *args):		
		trigger = 'parentItemScrollList'
		self.lastScrollList(trigger)
		trigger = 'childrenItemScrollList'
		self.lastScrollList(trigger)			
		triggerA = 'parentItemScrollList'
		triggerB = 'childrenItemScrollList'
		plugS = '.parentMatrix[0]'
		plugA = '.target'
		plugB = '.constraintParentInverseMatrix'	
		
		self.collingOtherNodes(triggerA, triggerB, plugS, plugA, plugB)
		
		#リストを再カウントします
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'
		self.counter(trigger, triggerInt, selInt)#defの行数記入予定
		
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'
		self.counter(trigger, triggerInt, selInt)#defの行数記入予定
			
	#チルドレン側からペアレントを呼び出します
	def collingConstraintParent(self, *args):
		trigger = 'parentItemScrollList'
		self.lastScrollList(trigger)
		trigger = 'childrenItemScrollList'
		self.lastScrollList(trigger)
				
		triggerA = 'childrenItemScrollList'
		triggerB = 'parentItemScrollList'
		plugS = '.parentInverseMatrix'
		plugA = '.constraintParentInverseMatrix'
		plugB = '.target'
		
		self.collingOtherNodes(triggerA, triggerB, plugS, plugA, plugB)
		
		#リストを再カウントします
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'
		self.counter(trigger, triggerInt, selInt)#defの行数記入予定
		
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'
		self.counter(trigger, triggerInt, selInt)#defの行数記入予定
	
	def collingOtherNodes(self, triggerA, triggerB, plugS, plugA, plugB, *args):
		master = mc.textScrollList(triggerA, q=True, allItems=True)
		
		#コンストレイントノードを収集し
		constrainNode = []#コンストレインは一つのノードが複数持っている場合が存在するので、リストinリストで集めています。
		slaveDic = {}
		for i in master:
			cNode = mc.listConnections((i + plugS))
			if cNode != None:
				constrainNode.append(cNode)
			else:
				slaveDic[i] =[]
		
		for i in constrainNode:	
			for e in i:		
				masterNode = list(set(mc.listConnections(e + plugA)))
				#print masterNode
				if e in masterNode:
					masterNode.remove(e)
				
				slaveNode = list(set(mc.listConnections(e + plugB)))
				print slaveNode	
				if e in slaveNode:
					slaveNode.remove(e)
		
				masters = slaveDic.keys()#前回までのマスターを取得します
				for m in masterNode:
					if m not in masters:
						slaveDic[m] = slaveNode
					else:
						last = slaveDic[m]
						new = last + slaveNode
						slaveDic[m] = new
			
		#お互いのリストを初期化します
		mc.textScrollList('parentItemScrollList', e=True, removeAll=True)
		mc.textScrollList('childrenItemScrollList', e=True, removeAll=True)
		#作成した辞書の内容で双方のリストを書き直します
		masterkey = slaveDic.keys()
		for i in masterkey:
			slaves = slaveDic[i]
			for e in slaves:
				mc.textScrollList(triggerA, e=True, append=i)
				mc.textScrollList(triggerB, e=True, append=e)
#コンストレイントを呼び出します（双方全消しの上、書き直し）
#コネクションの呼び出しを行います（双方全消しの上、書き直し）
	#コネクションのチルドレンを呼び出します
	def collingConnectionChildren(self, *args):
		trigger = 'parentItemScrollList'
		self.lastScrollList(trigger)
		trigger = 'childrenItemScrollList'
		self.lastScrollList(trigger)
		
		triggerA = 'parentItemScrollList'
		triggerB = 'childrenItemScrollList'
		roots = False
		toe = True
		self.collingOtherConnections( triggerA, triggerB, roots, toe)
		
		#リストを再カウントします
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'
		self.counter(trigger, triggerInt, selInt)#defの行数記入予定
		
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'
		self.counter(trigger, triggerInt, selInt)#defの行数記入予定
		
	#コネクションのペアレントを呼び出します
	def collingConnectionParent(self, *args):
		trigger = 'parentItemScrollList'
		self.lastScrollList(trigger)
		trigger = 'childrenItemScrollList'
		self.lastScrollList(trigger)
		
		triggerA = 'childrenItemScrollList'
		triggerB = 'parentItemScrollList'
		roots = True
		toe = False
		self.collingOtherConnections( triggerA, triggerB, roots, toe)
		
		#リストを再カウントします
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'
		self.counter(trigger, triggerInt, selInt)#defの行数記入予定
		
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'
		self.counter(trigger, triggerInt, selInt)#defの行数記入予定
		
	#コネクションの呼び出しを管理します
	def collingOtherConnections(self, triggerA, triggerB, roots, toe, *args):
		master = mc.textScrollList(triggerA, q=True, allItems=True)
		slaveDict = {}
		for i in master:
			removeList = mc.listConnections(i, s=roots, d=toe, type='constraint')
			slaveList = mc.listConnections(i, s=roots, d=toe)
			if removeList != None:
				slaveList = set(slaveList) - set(removeList)
			
			if slaveList != None:
				slaveDict[i] = list(set(slaveList))
			else:
				slaveDict[i] = [' ']
		
		mc.textScrollList(triggerA, e=True, removeAll=True)
		mc.textScrollList(triggerB, e=True, removeAll=True)
		masterKeys = slaveDict.keys()
		for i in masterKeys:
			slaves = slaveDict[i]
			for v in slaves:
				mc.textScrollList(triggerA, e=True, append=i)
				mc.textScrollList(triggerB, e=True, append=v)
#コネクションの呼び出しを行います（双方全消しの上、書き直し）

#D&Dするべきアイテムとスクロールの情報をD&Ddefに渡します
	#ペアレントをD&Dします
	#ペアレントをドロップします
	def parentDrop(self, dragControl, dropControl, msgs, x, y, dragType, *args):		
		if mc.textScrollList('parentItemScrollList', q=True, allItems=True) != None:
			trigger = 'parentItemScrollList'
			self.lastScrollList(trigger)
			
		position = int(float(y)*0.1) +1
		for i, v in enumerate(msgs):
			mc.textScrollList(trigger, e=True, removeItem=v)
			mc.textScrollList(trigger, e=True, appendPosition=[(i+position), v])		
		
	#ペアレントをドラッグします
	def parentDrag(self, dragControl, x, y, mods, *args):
		msgs = []
		msgs = mc.textScrollList('parentItemScrollList', q=True, selectItem=True)
		return msgs	
	
	#チルドレンをD&Dします
	def childrenDrop(self, dragControl, dropControl, msgs, x, y, dragType, *args):
		if mc.textScrollList('childrenItemScrollList', q=True, allItems=True) != None:
			trigger = 'childrenItemScrollList'
			self.lastScrollList(trigger)
			
		position = int(float(y)*0.1) +1
		for i, v in enumerate(msgs):
			mc.textScrollList(trigger, e=True, removeItem=v)
			mc.textScrollList(trigger, e=True, appendPosition=[(i+position), v])
		
	def childrenDrag(self, dragControl, x, y, mods, *args):
		msgs = []
		msgs = mc.textScrollList('childrenItemScrollList', q=True, selectItem=True)
		return msgs
		
	#ベクターをD&Dします
	def vectorDrop(self, dragControl, dropControl, msgs, x, y, dragType, *args):
		if mc.textScrollList('vectorItemScrollList', q=True, allItems=True) != None:
			trigger = 'vectorItemScrollList'
			self.lastScrollList(trigger)
			
		position = int(float(y)*0.1) +1
		for i, v in enumerate(msgs):
			mc.textScrollList(trigger, e=True, removeItem=v)
			mc.textScrollList(trigger, e=True, appendPosition=[(i+position), v])
			
	def vectorDrag(self, dragControl, x, y, mods, *args):
		msgs = []
		msgs = mc.textScrollList('vectorItemScrollList', q=True, selectItem=True)
		return msgs

#アトリビュートリストの内容を変更します
	#allAttryが選択されたとき、リストアトリをすべて書き込みます(選択時にこのdefが実行されるように選択defに実行コマンド書き込み)
	#ペアレントの選択されているアイテムの一番上のノードのアトリビュートをすべて書き出します
	def listParentAttrAll(self,*args):
		trigger = 'parentItemScrollList'
		attrScroll = 'parentAttrScrollList'
		flug = 'all'
		self.listInAttr(trigger, attrScroll, flug)
	#チルドレンの選択されているアイテムの一番上のノードのアトリビュートをすべて書き出します
	def listChildrenAttrAll(self,*args):	
		trigger = 'childrenItemScrollList'
		attrScroll = 'childrenAttrScrollList'
		flug = 'all'
		self.listInAttr(trigger, attrScroll, flug)
	#ペアレントの選択されているアイテムの一番上のノードのアトリビュートをキーブルとマトリクスのみを書き出します
	def listParentAttrKeyble(self,*args):
		trigger = 'parentItemScrollList'
		attrScroll = 'parentAttrScrollList'
		flug = 'keyble'
		self.listInAttr(trigger, attrScroll, flug)
	#チルドレンの選択されているアイテムの一番上のノードのアトリビュートをキーブルとマトリクスのみを書き出します		
	def listChildrenAttrKeyble(self,*args):	
		trigger = 'childrenItemScrollList'
		attrScroll = 'childrenAttrScrollList'
		flug = 'keyble'
		self.listInAttr(trigger, attrScroll, flug)
	#フラグに従って、アトリビュートリストの内容を書き換えます
	def listInAttr(self, trigger, attrScroll, flug, *args):
		itemList = mc.textScrollList(trigger, q=True, selectItem=True)
		mc.textScrollList(attrScroll, e=True, removeAll=True)
		if flug == 'all':
			attrList = mc.listAttr(itemList[0])
			
			mc.textScrollList(attrScroll, e=True, append=attrList)
		else:
			attrList = mc.listAttr(itemList[0], keyable=True)
			worldMatrix = mc.listAttr(itemList[0] + '.worldMatrix')
			worldInverseMatrix = mc.listAttr(itemList[0] + '.worldInverseMatrix')
			matrix = mc.listAttr(itemList[0] + '.matrix')
			inverseMatrix = mc.listAttr(itemList[0] + '.inverseMatrix')
			parentMatrix =  mc.listAttr(itemList[0] + '.parentMatrix')
			parentInverseMatrix =  mc.listAttr(itemList[0] + '.parentInverseMatrix')
		
			mc.textScrollList(attrScroll, e=True, append=matrix)
			mc.textScrollList(attrScroll, e=True, append=worldMatrix)
			mc.textScrollList(attrScroll, e=True, append=parentMatrix)
			mc.textScrollList(attrScroll, e=True, append=inverseMatrix)
			mc.textScrollList(attrScroll, e=True, append=worldInverseMatrix)
			mc.textScrollList(attrScroll, e=True, append=parentInverseMatrix)	
#アトリビュートリストの内容を変更します
	
#コネクションを行います	
	#TRSコネクションを行います
	#TRSコネクションを行います
	#TRコネクションを行います	
	#TRコネクションを行います
	#Tコネクションを行います
	def connectTranslateChannels(self, *args):
		trigger = 'parentItemScrollList'
		self.lastScrollList(trigger)
	
		trigger = 'childrenItemScrollList'
		self.lastScrollList(trigger)
			
		trigger = 'parentItemScrollList'		
		pItem = self.getSelectListItems(trigger)
		trigger = 'childrenItemScrollList'
		cItem = self.getSelectListItems(trigger)
		
		pChannel = 'translate'
		cChannel = 'translate'
		self.connectAttrs(pItem, cItem, pChannel, cChannel)
			
		#ペアレント数えなおし
		trigger = 'parentItemScrollList'
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
				
		#チルドレン数えなおし
		trigger ='childrenItemScrollList'
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'		
		self.counter(trigger, triggerInt, selInt)	
	#Tコネクションを行います		
	#Rコネクションを行います		
	def connectRotateChannels(self, *args):
		trigger = 'parentItemScrollList'
		self.lastScrollList(trigger)
		
		trigger = 'childrenItemScrollList'
		self.lastScrollList(trigger)
			
		trigger = 'parentItemScrollList'		
		pItem = self.getSelectListItems(trigger)
		trigger = 'childrenItemScrollList'
		cItem = self.getSelectListItems(trigger)
		
		pChannel = 'rotate'
		cChannel = 'rotate'
		self.connectAttrs(pItem, cItem, pChannel, cChannel)
			
		#ペアレント数えなおし
		trigger = 'parentItemScrollList'
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
				
		#チルドレン数えなおし
		trigger ='childrenItemScrollList'
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'		
		self.counter(trigger, triggerInt, selInt)	
	#Rコネクションを行います
	#Sコネクションを行います		
	def connectScaleChannels(self, *args):
		trigger = 'parentItemScrollList'
		self.lastScrollList(trigger)
	
		trigger = 'childrenItemScrollList'
		self.lastScrollList(trigger)
			
		trigger = 'parentItemScrollList'		
		pItem = self.getSelectListItems(trigger)
		trigger = 'childrenItemScrollList'
		cItem = self.getSelectListItems(trigger)
		
		pChannel = 'scale'
		cChannel = 'scale'
		self.connectAttrs(pItem, cItem, pChannel, cChannel)
			
		#ペアレント数えなおし
		trigger = 'parentItemScrollList'
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
				
		#チルドレン数えなおし
		trigger ='childrenItemScrollList'
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'		
		self.counter(trigger, triggerInt, selInt)	
	
	#Sコネクションを行います
	
	#アトリビュートリストから選択したアイテムでコネクションします
	def connectSelectChannels(self, *args):
		trigger = 'parentItemScrollList'
		self.lastScrollList(trigger)
	
		trigger = 'childrenItemScrollList'
		self.lastScrollList(trigger)
		
		trigger = 'parentItemScrollList'		
		pItem = self.getSelectListItems(trigger)
		trigger = 'childrenItemScrollList'
		cItem = self.getSelectListItems(trigger)
		
		pChannelList = mc.textScrollList('parentAttrScrollList', q=True, selectItem=True)
		cChannelList = mc.textScrollList('childrenAttrScrollList', q=True, selectItem=True)
		pChannel = pChannelList[0]
		cChannel = cChannelList[0]
		self.connectAttrs(pItem, cItem, pChannel, cChannel)
			
		#ペアレント数えなおし
		trigger = 'parentItemScrollList'
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
				
		#チルドレン数えなおし
		trigger ='childrenItemScrollList'
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'		
		self.counter(trigger, triggerInt, selInt)	
	#アトリビュートリストから選択したアイテムでコネクションします
	
	#コネクションします
	def connectAttrs(self, pItem, cItem, pChannel, cChannel, *args):
		for i,v in enamerate(pItem):
			pAttr = mc.attributeQuery(pChannel, node=v, exists=True)
			cAttr = mc.attributeQuery(cChannel, node=cItem[i], exists=True)	
			if pAttr == True and cAttr == True:
				mc.connectAttr((v + '.' + pChannel), (cItem[i] + '.' + cChannel), f=True)
				mc.textScrollList('parentItemScrollList', e=True, removeIndexedItem=i)
				mc.textScrollList('childrenItemScrollList', e=True, removeIndexedItem=i)	
#コネクションします
#コネクションを行います
###############################################################################################################################################################################################################
#コンストレイントを行います
#コンシュトレイントが完了したら、コンストレイントノードをグループでまとめます。
	def collectionGrp(self, getConstraints, type, *args):
		gName = 'con_' + type + '#'
		mc.group(getConstraints, n=('con_' + type + '#'), world=True)
		mc.select(r=True)
#コンシュトレイントが完了したら、コンストレイントノードをグループでまとめます。
#作業終了後のリストを受け取ってリストからリムーブします。
	def removeList(self, constraintList, *args):
		cList = constraintList.keys()
		pList = []
		for i in cList:
			pList.append(constraintList[i])
		
		mc.textScrollList('parentItemScrollList', e=True, removeItem=pList)
		mc.textScrollList('childrenItemScrollList', e=True, removeItem=cList)	
#作業終了後のリストを受け取ってリストからリムーブします。
#作業終了後のリストを受け取ってリストからリムーブします。
	def removeVectorList(self, vectorList, *args):
		cList = vectorList.keys()
		vList = []
		for i in cList:
			vList.append(vectorList[i])
		
		#mc.textScrollList('parentItemScrollList', e=True, removeItem=pList)
		mc.textScrollList('vectorItemScrollList', e=True, removeItem=vList)	
#作業終了後のリストを受け取ってリストからリムーブします。

#コンストレイント用の辞書を作成して、リターンします
	def constraintDictReturn(self, *args):
		trigger = 'parentItemScrollList'		
		pItem = self.getSelectListItems(trigger)
		
		trigger = 'childrenItemScrollList'
		cItem = self.getSelectListItems(trigger)
		
		constraintList = {}
		if len(pItem) == len(cItem)*2:
			for i,v in enumerate(cItem):
				constraintList[v] = [ pItem[i] , pItem[i +1] ]
				
		elif len(pItem) >= len(cItem):
			for i,v in enumerate(cItem):
				constraintList[v] =  pItem[i]				
		else:
			for i,v in enumerate(cItem):
				constraintList[v] = pItem[0]
			if len(pItem) != 1:
				mc.confirmDialog(m=('ペアレントリストの一番目ですべてのチルドレンをコンストレイントします'))
				
		return constraintList
#コンストレイント用の辞書を作成して、リターンします
#ベクターをチルドレンと紐づいた辞書にしてリターンします
	def constraintVectorReturn(self, *args):
		trigger = 'vectorItemScrollList'
		vItem = self.getSelectListItems(trigger)
		
		trigger = 'childrenItemScrollList'
		cItem = self.getSelectListItems(trigger)
		
		constraintList = {}
		if len(vItem) == len(cItem)*2:
			for i,v in enumerate(cItem):
				constraintList[v] = [ vItem[i] , vItem[i +1] ]
				
		elif len(vItem) >= len(cItem):
			for i,v in enumerate(cItem):
				constraintList[v] =  vItem[i]				
		else:
			for i,v in enumerate(cItem):
				constraintList[v] = vItem[0]
			if len(vItem) != 1:
				mc.confirmDialog(m=('ペアレントリストの一番目ですべてのチルドレンをコンストレイントします'))
				
		return constraintList
#ベクターをチルドレンと紐づいた辞書にしてリターンします
#スキップチャンネルをリターンします
	def skipChannnelsReturn(self, cx,cy,cz, *args):
		xValue = mc.checkBox(cx, q=True, value=True)
		yValue = mc.checkBox(cy, q=True, value=True)
		zValue = mc.checkBox(cz, q=True, value=True)
		skipChannel = []
		if xValue == False:
			skipChannel.append('x')
		if yValue == False:
			skipChannel.append('y')
		if zValue == False:
			skipChannel.append('z')					
		return skipChannel
#スキップチャンネルをリターンします
#ペアレントコンストレイントを行います
	def parentC(self, *args):
		#現在リストされているアイテムでリメンバーを書き換えます
		trigger = 'parentItemScrollList'
		self.lastScrollList(trigger)
		trigger = 'childrenItemScrollList'
		self.lastScrollList(trigger)		
		
		#メインテインオフセットを確認します
		meinten = mc.checkBox('parentConstraintMaintainCheck', q=True, value=True)
		#スキップするチャンネルを確認します
		cx,cy,cz = 'parentTxCheck', 'parentTyCheck', 'parentTzCheck'
		skippingT = self.skipChannnelsReturn(cx,cy,cz)
		cx,cy,cz = 'parentRxCheck', 'parentRyCheck', 'parentRzCheck'
		skippingR = self.skipChannnelsReturn(cx,cy,cz)
				
		constraintList = self.constraintDictReturn()
		cLIst = constraintList.keys()
		
		getConstraints = []
		for i in cLIst:
			pItems = constraintList[i]
			if len(pItems) == 2:
				cn = pItems[0] + '_' + pItems[1] + '_to_' + i + '_parent'
				mc.parentConstraint(pItems, i, st=skippingT, sr=skippingR, maintainOffset=meinten, n=cn, weight=0.5)
				getConstraints.append(cn)
			else:
				cn = pItems + '_to_' + i + '_parent'
				mc.parentConstraint(pItems, i, st=skippingT, sr=skippingR, maintainOffset=meinten, n=cn, weight=1.0)
				getConstraints.append(cn)
						
		#作業が完了したリスト内のアイテムをリストからリムーブします
		self.removeList(constraintList)
		
		#グループノードを作成します
		type = 'parent_'
		self.collectionGrp(getConstraints, type)
				
		#リストの残数を数えなおします
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
		
#ペアレントコンストレイントを行います
#ポジションコンストレイントを行います
	def pointC(self, *args):
		#現在リストされているアイテムでリメンバーを書き換えます
		trigger = 'parentItemScrollList'
		self.lastScrollList(trigger)
		trigger = 'childrenItemScrollList'
		self.lastScrollList(trigger)		

		#メインテインオフセットを確認します		
		meinten = mc.checkBox('pointConstraintMaintainCheck', q=True, value=True)
		
		cx,cy,cz = 'pointTxCheck', 'pointTyCheck', 'pointTzCheck'
		skipping = self.skipChannnelsReturn(cx,cy,cz)
		
		constraintList = self.constraintDictReturn()
		cLIst = constraintList.keys()
		
		#コンストレイントノードを収集します
		getConstraints = []
		
		for i in cLIst:
			pItems = constraintList[i]
			if len(pItems) == 2:
				cn = pItems[0] + '_' + pItems[1] + '_to_' + i + '_position'
				mc.pointConstraint(pItems, i, skip=skipping, maintainOffset=meinten, n=cn, weight=0.5)
				getConstraints.append(cn)
			else:
				cn = pItems + '_to_' + i + '_position'
				mc.pointConstraint(pItems, i, skip=skipping, maintainOffset=meinten, n=cn, weight=1.0)#ポジションコンストレイントを行います
				getConstraints.append(cn)
						
		#作業が完了したリスト内のアイテムをリストからリムーブします
		self.removeList(constraintList)
		
		#グループノードを作成します
		type = 'point_'
		self.collectionGrp(getConstraints, type)
		
		#リストの残数を数えなおします
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
#ポジションコンストレイントを行います
#ローテーションコンストレイントを行います
	def rotateC(self, *args):
		#現在リストされているアイテムでリメンバーを書き換えます
		trigger = 'parentItemScrollList'
		self.lastScrollList(trigger)
		trigger = 'childrenItemScrollList'
		self.lastScrollList(trigger)		

		#メインテインオフセットを確認します		
		meinten = mc.checkBox('rotateConstraintMaintainCheck', q=True, value=True)
		
		cx,cy,cz = 'rotateTxCheck', 'rotateTyCheck', 'rotateTzCheck'
		skipping = self.skipChannnelsReturn(cx,cy,cz)
		
		constraintList = self.constraintDictReturn()
		cLIst = constraintList.keys()
			
		#コンストレイントノードを収集します		
		getConstraints = []
		
		for i in cLIst:
			pItems = constraintList[i]
			if len(pItems) == 2:
				cn = pItems[0] + '_' + pItems[1] + '_to_' + i + '_rotate'
				mc.orientConstraint(pItems, i, skip=skipping, maintainOffset=meinten, n=cn, weight=0.5)
				getConstraints.append(cn)
			else:
				cn = pItems + '_to_' + i + '_rotate'
				mc.orientConstraint(pItems, i, skip=skipping, maintainOffset=meinten, n=cn, weight=1.0)#ポジションコンストレイントを行います	
				getConstraints.append(cn)
						
		#作業が完了したリスト内のアイテムをリストからリムーブします
		self.removeList(constraintList)
		
		#グループノードを作成します
		type = 'rotate_'
		self.collectionGrp(getConstraints, type)		
				
		#リストの残数を数えなおします
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
#ローテーションコンストレイントを行います
#スケールコンストレイントを行います
	def scaleC(self, *args):
		#現在リストされているアイテムでリメンバーを書き換えます
		trigger = 'parentItemScrollList'
		self.lastScrollList(trigger)
		trigger = 'childrenItemScrollList'
		self.lastScrollList(trigger)		
		
		#メインテインオフセットを確認します		
		meinten = mc.checkBox('scaleConstraintMaintainCheck', q=True, value=True)
		
		cx,cy,cz = 'scaleTxCheck', 'scaleTyCheck', 'scaleTzCheck'
		skipping = self.skipChannnelsReturn(cx,cy,cz)
				
		constraintList = self.constraintDictReturn()
		cLIst = constraintList.keys()

		#コンストレイントノードを収集します		
		getConstraints = []
		
		for i in cLIst:
			pItems = constraintList[i]
			if len(pItems) == 2:
				cn = pItems[0] + '_' + pItems[1] + '_to_' + i + '_scale'
				mc.scaleConstraint(pItems, i, skip=skipping, maintainOffset=meinten, n=cn, weight=0.5)
				getConstraints.append(cn)
			else:
				cn = pItems + '_to_' + i + '_scale'
				mc.scaleConstraint(pItems, i, skip=skipping, maintainOffset=meinten, n=cn, weight=1.0)#ポジションコンストレイントを行います	
				getConstraints.append(cn)
				
		#作業が完了したリスト内のアイテムをリストからリムーブします
		self.removeList(constraintList)
		type = 'scale_'
		self.collectionGrp(getConstraints, type)		
		
		#リストの残数を数えなおします
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
#スケールコンストレイントを行います
#フォリクルなどの特殊コンストレイントを行います
#フォリクルコンストレイントを行います
	def follicleMeshC(self, *args):
		#現在リストされているアイテムでリメンバーを書き換えます
		trigger = 'parentItemScrollList'
		self.lastScrollList(trigger)
		trigger = 'childrenItemScrollList'
		self.lastScrollList(trigger)		
		
		#メインテインオフセットを確認します		
		meinten = mc.checkBox('meshFollicleOffsetCheck', q=True, value=True)
		
		cx,cy,cz = 'scaleTxCheck', 'scaleTyCheck', 'scaleTzCheck'
		skipping = self.skipChannnelsReturn(cx,cy,cz)
				
		constraintList = self.constraintDictReturn()
		cLIst = constraintList.keys()		
		
		for i in cLIst:
			closest = mc.createNode('closestPointOnMesh', n='pointOn_M_')
			mc.connectAttr(constraintList[i] + '.outMesh', closest + '.inMesh')
			translate = mc.xform(i, q=True, t=True)
			mc.setAttr(closest + '.inPositionX', translate[0])
			mc.setAttr(closest + '.inPositionY', translate[1])
			mc.setAttr(closest + '.inPositionZ', translate[2])
			
			folTrans = mc.createNode('transform', n='cnst_fol_M_')
			fol = mc.createNode('follicle', n='cnst_fol_MShape_', p=folTrans)
			mc.connectAttr(fol + '.outRotate', folTrans + '.rotate', f=True)
			mc.connectAttr(fol + '.outTranslate', folTrans + '.translate', f=True)
			mc.connectAttr(constraintList[i] + '.worldMatrix', fol + '.inputWorldMatrix', f=True)
			mc.connectAttr(constraintList[i] + '.outMesh', fol + '.inputMesh', f=True)
			mc.setAttr(fol + '.simulationMethod', 0)
			uPoint = mc.getAttr(closest + '.result.parameterU')
			vPoint = mc.getAttr(closest + '.result.parameterV')
			mc.setAttr(fol + '.parameterU', uPoint)
			mc.setAttr(fol + '.parameterV', vPoint)
			mc.parent(i, folTrans)
			if meinten == False:
				mc.setAttr((i + '.translate'), 0,0,0, type='float3')
				mc.setAttr((i + '.translate'), 0,0,0, type='float3')
			mc.delete(closest)
		
		#作業終了後、リストを初期化しノードをまとめます
		self.removeList(constraintList)		
		self.removeVectorList(vectorList)
		type = 'folM_'
		self.collectionGrp(getConstraints, type)
		
		#リストの残数を数えなおします
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
		
	#nuebisサーフェスでポイントスナップを行います(あまりうまくいっていません)
	def follicleSafaceC(self, *args):
		#現在リストされているアイテムでリメンバーを書き換えます
		trigger = 'parentItemScrollList'
		self.lastScrollList(trigger)
		trigger = 'childrenItemScrollList'
		self.lastScrollList(trigger)		
		
		#メインテインオフセットを確認します		
		meinten = mc.checkBox('nubFollicleOffsetCheck', q=True, value=True)		
		
		#コンストレイント辞書を作成します。
		constraintList = self.constraintDictReturn()
		cLIst = constraintList.keys()		
		#コンストレイントを行います。
		for i in cLIst:
			shapes = mc.listRelatives(constraintList[i],s=True)
			closest = mc.createNode('closestPointOnSurface', n='pointOn_S_')
			mc.connectAttr(constraintList[i] + '.create', closest + '.inputSurface')
			translate = mc.xform(i, q=True, t=True)
			mc.setAttr(closest + '.inPositionX', translate[0])
			mc.setAttr(closest + '.inPositionY', translate[1])
			mc.setAttr(closest + '.inPositionZ', translate[2])
			
			folTrans = mc.createNode('transform', n='cnst_fol_S_')
			fol = mc.createNode('follicle', n='cnst_fol_SShape_', p=folTrans)
			mc.connectAttr(fol + '.outRotate', folTrans + '.rotate', f=True)
			mc.connectAttr(fol + '.outTranslate', folTrans + '.translate', f=True)
			mc.connectAttr(shapes[0] + '.matrix', fol + '.inputWorldMatrix', f=True)
			mc.connectAttr(shapes[0] + '.worldSpace', fol + '.inputSurface', f=True)
			mc.setAttr(fol + '.simulationMethod', 0)
			uPoint = mc.getAttr(closest + '.result.parameterU')
			vPoint = mc.getAttr(closest + '.result.parameterV')
			mc.setAttr(fol + '.parameterU', uPoint)
			mc.setAttr(fol + '.parameterV', vPoint)
			mc.parent(i, folTrans)
			if meinten == False:
				mc.setAttr((i + '.translate'), 0,0,0, type='float3')
				mc.setAttr((i + '.translate'), 0,0,0, type='float3')
			mc.delete(closest)
		
		#作業終了後、リストを初期化し、ノードをまとめます
		self.removeList(constraintList)		
		self.removeVectorList(vectorList)
		type = 'folS_'
		self.collectionGrp(getConstraints, type)
		
		#リストの残数を数えなおします
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
		
#フォリクルコンストレイントを行います
#カーブインフォコンストレイントを行います
	def curveInfoC(self, *args):
		#現在リストされているアイテムでリメンバーを書き換えます
		trigger = 'parentItemScrollList'
		self.lastScrollList(trigger)
		trigger = 'childrenItemScrollList'
		self.lastScrollList(trigger)	
		trigger = 'vectorItemScrollList'
		self.lastScrollList(trigger)
		
		#場員とリストを取得します		           
		constraintList = self.constraintDictReturn()
		#vectorList = self.constraintVectorReturn()
		cList = constraintList.keys()
		
		for i in cList:
			mc.rebuildCurve(constraintList[i], ch=1, rpo=1, rt=0, end=1, kr=0, kcp=1, kep=1, kt=0, s=8, d=3, tol=0.01)
			mc.delete(constraintList[i], ch=True)
			pointCurve = mc.createNode('pointOnCurveInfo', n=(constraintList[i] + '_' + i + 'pointCurve_'))
			mc.setAttr((pointCurve + '.turnOnPercentage'), True)
			mc.connectAttr((constraintList[i] + '.worldSpace'), (pointCurve + '.inputCurve'), f=True)
			mc.connectAttr((pointCurve + '.position'), (i + '.translate'), f=True)
			mc.addAttr(i, shortName='lp', longName='loop', attributeType='float')
			mc.addAttr(i, shortName='po', longName='point', attributeType='float')
			mc.setAttr(i + '.loop', e=True, keyable=True)
			mc.setAttr(i + '.point', e=True, keyable=True)
			mc.connectAttr((i + '.point'), pointCurve + '.parameter', f=True)
			mc.expression(n=(i + '_loopEXP'), s='float $point,$pointInt,$act;$point='+ i +'.loop;$pointInt=int(' + i + '.loop);if(abs($point)>= 1){' + i + '.point=abs($point-$pointInt);}else{' + i + '.point=$point;}')
									
		#リストを初期化します
		self.removeList(constraintList)		
		#self.removeVectorList(vectorList)
		
		#リストの残数を数えなおします
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'		
		self.counter(trigger, triggerInt, selInt)		
#カーブインフォコンストレイントを行います
#ヴェクターノードを使用したコンストレイントを行います
#タンジェントコンストレイントを行います
	def tangentC(self, *args):
		#現在リストされているアイテムでリメンバーを書き換えます
		trigger = 'parentItemScrollList'
		self.lastScrollList(trigger)
		trigger = 'childrenItemScrollList'
		self.lastScrollList(trigger)	
		trigger = 'vectorItemScrollList'
		self.lastScrollList(trigger)		
		
		#ベクタータイプを確認します
		objRotate = mc.optionMenu('tangentConstraintUpVector', q=True, select=True)
		upVectSet = ''
		if objRotate == 1:
			upVectSet = 'object'
		else:
			upVectSet = 'objectrotation'
		
		
		#場員とリストを取得します		           
		constraintList = self.constraintDictReturn()
		vectorList = self.constraintVectorReturn()
		cList = constraintList.keys()
		
		#エイムする方向を決めます
		aimVect = mc.intFieldGrp('tangentConstraintAimVecto', q=True, v=True)
		#エイム時のup方向を決めます
		upVect = mc.intFieldGrp('tangentConstraintUpVecto',q=True, v=True)
		
		#コンストレイントノードを収集します		
		getConstraints = []		
		
		#コンストレイントを描けます
		for i in cList:
			pItems = constraintList[i]
			vList = vectorList[i]
			if len(pItems) == 2:
				cn = pItems[0] + '_' + pItems[1] + '_to_' + i + '_tan'
				mc.aimConstraint(pItems, i, maintainOffset=meinten, n=cn, worldUpObject=vList, worldUpType=upVectSet, worldUpVector=aimVect, upVector=upVect, weight=0.5)
				getConstraints.append(cn)
			else:
				cn = pItems + '_to_' + i + '_aim'
				mc.aimConstraint(pItems, i, n=cn, worldUpObject=vList, worldUpType=upVectSet, worldUpVector=aimVect, upVector=upVect, weight=1.0)
				getConstraints.append(cn)
		#リストを初期化します
		self.removeList(constraintList)		
		self.removeVectorList(vectorList)
		type = 'tan_'
		self.collectionGrp(getConstraints, type)
		
		#リストの残数を数えなおします
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
		#ベクター数えなおし		
		#ベクター数えなおし
		trigger = 'vectorItemScrollList'
		triggerInt = 'vectorAllNumber'
		selInt = 'vectorSelectNumber'
		self.counter(trigger, triggerInt, selInt)							
		
	
#タンジェントコンストレイントを行います
#エイムコンストレイントを行います
	def aimC(self, *args):
		#現在リストされているアイテムでリメンバーを書き換えます
		trigger = 'parentItemScrollList'
		self.lastScrollList(trigger)
		trigger = 'childrenItemScrollList'
		self.lastScrollList(trigger)	
		trigger = 'vectorItemScrollList'
		self.lastScrollList(trigger)	
				
		#メイン店を確認します
		meinten = mc.checkBox('scaleConstraintMaintainCheck', q=True, value=True)
		
		#ベクタータイプを確認します
		objRotate = mc.optionMenu('aimConstraintUpVector', q=True, select=True)
		upVectSet = ''
		if objRotate == 1:
			upVectSet = 'object'
		else:
			upVectSet = 'objectrotation'
		
		#スキップを確認します
		cx,cy,cz = 'aimRxCheck', 'aimRyCheck', 'aimRzCheck'
		skipping = self.skipChannnelsReturn(cx,cy,cz)
		#場員とリストを取得します		           
		constraintList = self.constraintDictReturn()
		vectorList = self.constraintVectorReturn()
		cList = constraintList.keys()
		
		#エイムする方向を決めます
		aimVect = mc.intFieldGrp('aimConstraintVectField', q=True, v=True)
		#エイム時のup方向を決めます
		upVect = mc.intFieldGrp('aimUpConstraintVectField',q=True, v=True)
		
		#コンストレイントノードを収集します		
		getConstraints = []		
		
		#コンストレイントを描けます
		for i in cList:
			pItems = constraintList[i]
			vList = vectorList[i]
			if len(pItems) == 2:
				cn = pItems[0] + '_' + pItems[1] + '_to_' + i + '_aim'
				mc.aimConstraint(pItems, i, skip=skipping, maintainOffset=meinten, n=cn, worldUpObject=vList, worldUpType=upVectSet, worldUpVector=aimVect, upVector=upVect, weight=0.5)
				getConstraints.append(cn)
			else:
				cn = pItems + '_to_' + i + '_aim'
				mc.aimConstraint(pItems, i, skip=skipping, maintainOffset=meinten, n=cn, worldUpObject=vList, worldUpType=upVectSet, worldUpVector=aimVect, upVector=upVect, weight=1.0)
				getConstraints.append(cn)
		#リストを初期化します
		self.removeList(constraintList)		
		self.removeVectorList(vectorList)
		type = 'aim_'
		self.collectionGrp(getConstraints, type)
		
		#リストの残数を数えなおします
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
		#ベクター数えなおし
		trigger = 'vectorItemScrollList'
		triggerInt = 'vectorAllNumber'
		selInt = 'vectorSelectNumber'
		self.counter(trigger, triggerInt, selInt)					
#エイムコンストレイントを行います
#ヴェクターノードを使用したコンストレイントを行います
#コンストレインします　
###############################################################################################################################################################################################################
###############################################################################################################################################################################################################
#スナップを行います
#ペアレンツコンストレイントを使用したスナップを行います
	def parentSConst(self, *args):
		#現在リストされているアイテムでリメンバーを書き換えます
		trigger = 'parentItemScrollList'
		self.lastScrollList(trigger)
		trigger = 'childrenItemScrollList'
		self.lastScrollList(trigger)	
		trigger = 'vectorItemScrollList'
		self.lastScrollList(trigger)
		
		#コンストレイント辞書を作成します。
		constraintList = self.constraintDictReturn()
		cLIst = constraintList.keys()
		
		getConstraints = []
		for i in cLIst:
			pItems = constraintList[i]
			if len(pItems) == 2:
				cn = pItems[0] + '_' + pItems[1] + '_to_' + i
				mc.parentConstraint(pItems, i, n=cn, weight=0.5)
				getConstraints.append(cn)
			else:
				cn = pItems[0] + '_to_' + i
				mc.parentConstraint(pItems, i, n=cn, weight=1.0)
				getConstraints.append(cn)
		#スナップ後にコンストレイントを削除します
		mc.delete(getConstraints)
		#リストを初期化します
		self.removeList(constraintList)		
		self.removeVectorList(vectorList)		
						
		#リストの残数を数えなおします
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
#ペアレンツコンストレイントを使用したスナップを行います
#ポイントコンストレイントを使用したスナップを行います
	def pointSConst(self, *args):
		#現在リストされているアイテムでリメンバーを書き換えます
		trigger = 'parentItemScrollList'
		self.lastScrollList(trigger)
		trigger = 'childrenItemScrollList'
		self.lastScrollList(trigger)	
		trigger = 'vectorItemScrollList'
		self.lastScrollList(trigger)
		
		#コンストレイント辞書を作成します。
		constraintList = self.constraintDictReturn()
		cLIst = constraintList.keys()
		
		getConstraints = []
		for i in cLIst:
			pItems = constraintList[i]
			if len(pItems) == 2:
				cn = pItems[0] + '_' + pItems[1] + '_to_' + i
				mc.pointConstraint(pItems, i, n=cn, weight=0.5)
				getConstraints.append(cn)
			else:
				cn = pItems[0] + '_to_' + i
				mc.pointConstraint(pItems, i, n=cn, weight=1.0)
				getConstraints.append(cn)
		#スナップ後にコンストレイントを削除します
		mc.delete(getConstraints)
		#リストを初期化します
		self.removeList(constraintList)		
		self.removeVectorList(vectorList)		
						
		#リストの残数を数えなおします
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
#ポイントコンストレイントを使用したスナップを行います
#ローテートコンストレイントを使用したスナップを行います
	def rotateSConst(self, *args):
		#現在リストされているアイテムでリメンバーを書き換えます
		trigger = 'parentItemScrollList'
		self.lastScrollList(trigger)
		trigger = 'childrenItemScrollList'
		self.lastScrollList(trigger)	
		trigger = 'vectorItemScrollList'
		self.lastScrollList(trigger)
		
		#コンストレイント辞書を作成します。
		constraintList = self.constraintDictReturn()
		cList = constraintList.keys()
		
		getConstraints = []
		for i in cList:
			pItems = constraintList[i]
			if len(pItems) == 2:
				cn = pItems[0] + '_' + pItems[1] + '_to_' + i
				mc.orientConstraint(pItems, i, n=cn, weight=0.5)
				getConstraints.append(cn)
			else:
				cn = pItems[0] + '_to_' + i
				mc.orientConstraint(pItems, i, n=cn, weight=1.0)
				getConstraints.append(cn)
		#スナップ後にコンストレイントを削除します
		mc.delete(getConstraints)
		#リストを初期化します
		self.removeList(constraintList)		
		self.removeVectorList(vectorList)		
						
		#リストの残数を数えなおします
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
#ローテートコンストレイントを使用したスナップを行います
#スケールコンストレイントを使用したスナップを行います
	def scaleSConst(self, *args):
		#現在リストされているアイテムでリメンバーを書き換えます
		trigger = 'parentItemScrollList'
		self.lastScrollList(trigger)
		trigger = 'childrenItemScrollList'
		self.lastScrollList(trigger)	
		trigger = 'vectorItemScrollList'
		self.lastScrollList(trigger)
		
		#コンストレイント辞書を作成します。
		constraintList = self.constraintDictReturn()
		cList = constraintList.keys()
		
		getConstraints = []
		for i in cList:
			pItems = constraintList[i]
			if len(pItems) == 2:
				cn = pItems[0] + '_' + pItems[1] + '_to_' + i
				mc.scaleConstraint(pItems, i, n=cn, weight=0.5)
				getConstraints.append(cn)
			else:
				cn = pItems[0] + '_to_' + i
				mc.scaleConstraint(pItems, i, n=cn, weight=1.0)
				getConstraints.append(cn)
		#スナップ後にコンストレイントを削除します
		mc.delete(getConstraints)
		#リストを初期化します
		self.removeList(constraintList)		
		self.removeVectorList(vectorList)		
						
		#リストの残数を数えなおします
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
#スケールコンストレイントを使用したスナップを行います
#ユーティリティのインサートを行います


connector().createUI()
connector().windowResize()

#手動でコンストレイントを行う場合のコネクションの組み方
"""constraintNodes = mc.createNode('parentConstraint', n='testPConstraint')
mc.connectAttr(('pCube4' + '.' + 'parentMatrix'), (constraintNodes + '.target[0].targetParentMatrix'))
mc.connectAttr(('pCube4' + '.' + 'translate'), (constraintNodes + '.target[0].targetTranslate'))
mc.connectAttr(('pCube4' + '.' + 'rotate'), (constraintNodes + '.target[0].targetRotate'))
mc.connectAttr(('pCube4' + '.' + 'scale'), (constraintNodes + '.target[0].targetScale'))
mc.connectAttr(('pCube4' + '.' + 'rotatePivot'), (constraintNodes + '.target[0].targetRotatePivot'))
mc.connectAttr(('pCube4' + '.' + 'rotatePivotTranslate'), (constraintNodes + '.target[0].targetRotateTranslate'))
mc.connectAttr(('pCube4' + '.' + 'rotateOrder'), (constraintNodes + '.target[0].targetRotateOrder'))

mc.connectAttr(('pCube5' + '.' + 'rotatePivotTranslate'), (constraintNodes + '.constraintRotateTranslate'))
mc.connectAttr(('pCube5' + '.' + 'rotatePivot'), (constraintNodes + '.constraintRotatePivot'))
mc.connectAttr(('pCube5' + '.' + 'rotateOrder'), (constraintNodes + '.constraintRotateOrder'))
mc.connectAttr(('pCube5' + '.' + 'parentInverseMatrix[0]'), (constraintNodes + '.constraintParentInverseMatrix'))

mc.connectAttr((constraintNodes + '.constraintRotateX'), ('pCube5' + '.' + 'rotateX'))
mc.connectAttr((constraintNodes + '.constraintRotateY'), ('pCube5' + '.' + 'rotateY'))
mc.connectAttr((constraintNodes + '.constraintRotateZ'), ('pCube5' + '.' + 'rotateZ'))
mc.connectAttr((constraintNodes + '.constraintTranslateX'), ('pCube5' + '.' + 'translateX'))
mc.connectAttr((constraintNodes + '.constraintTranslateY'), ('pCube5' + '.' + 'translateY'))
mc.connectAttr((constraintNodes + '.constraintTranslateZ'), ('pCube5' + '.' + 'translateZ'))

mc.addAttr(constraintNodes, ln='pCube4W0', at='float', min=0, max=1, dv=1)
mc.connectAttr((constraintNodes +'.pCube4W0'),(constraintNodes + '.target[0].targetWeight'))
"""
