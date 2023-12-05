'''
'''
#!/usr/bin/env python
# -*- coding: shift_jis -*-
#HA = Hisakazu_Aoki
import maya.cmds as mc
class connector():
	def __init__(self):
		#�������o�[�ɂ��ẴO���[�o�����X�g��錾���܂�
		global HA_parentListRemember
		global HA_childrenListRemember
		global HA_vectorListRemember
		global HA_constraintTypeDict
		HA_parentListRemember = []
		HA_childrenListRemember = []
		HA_vectorListRemember = []
		HA_constraintTypeDict = {}
		

#UI���쐬���܂�
	def createUI(self, *args):
		if mc.window('connectorWindow', q=True, ex=True) == True:
			mc.deleteUI('connectorWindow')
		
		mc.window('connectorWindow',title='connector_1.0.0')
		#���C���^�u��ݒ肵�܂�
		mc.tabLayout('mainTab', p='connectorWindow')
		#�����[�V�������X�g�ƃ^�u�����C�A�E�g���܂�
		mc.paneLayout('relativePane', p='mainTab', configuration='vertical3')
		#���X�g�p����ݒ肵�܂�
		mc.paneLayout('allScrollListPane', p='relativePane', configuration='vertical3')
		
		#�y�A�����g�t���[�������C�A�E�g���܂�
		mc.paneLayout('parentItemPane', p='allScrollListPane', configuration='vertical2')
		#�y�A�����g�A�C�e���t���[�������C�A�E�g���܂�
		mc.frameLayout('parentItemFrame', p='parentItemPane', l='parent item')		
		mc.paneLayout('parentItemListPane', p='parentItemFrame', configuration='horizontal4')
		#�y�A�����g�A�C�e�����X�g�C�������C�A�E�g���܂�
		mc.paneLayout('parentItemListInAddPane', p='parentItemListPane', configuration='horizontal2')
		mc.button('parentItemListInButton', p='parentItemListInAddPane', l='List Replace', c=self.listInParent)
		mc.button('parentItemListAddButton', p='parentItemListInAddPane', l='List Add', c=self.listAddParent)
		#�y�A�����g�A�C�e�����X�g�C�������C�A�E�g���܂���
		mc.setParent('parentItemListInAddPane')		
		#�y�A�����g�A�C�e�����X�g�X�N���[�������C�A�E�g���܂���		
		mc.textScrollList('parentItemScrollList', p='parentItemListPane', ams=True, sc=self.selectParentItem, dcc=self.deselectParent, dgc=self.parentDrag, dpc=self.parentDrop)
		mc.popupMenu('parentItemScrollListPopMenu', p='parentItemScrollList', button=3)
		mc.menuItem('parentItemScrollListMenuSel', p='parentItemScrollListPopMenu', l='select all List', c=self.selectAllParent)
		mc.menuItem('parentItemScrollListMenuHi', p='parentItemScrollListPopMenu', l='select List Items Hi')
		mc.menuItem('parentItemScrollListMenuShape', p='parentItemScrollListPopMenu', l='shape list', c=self.parentSwitchShape)
		mc.menuItem('parentItemScrollListMenuColl_A', p='parentItemScrollListPopMenu', l='call constraint child', c=self.collingConstraintChildren)
		mc.menuItem('parentItemScrollListMenuColl_B', p='parentItemScrollListPopMenu', l='call connection child', c=self.collingConnectionChildren)

		#�y�A�����g�A�C�e�����X�g�J�E���g�����C�A�E�g���܂�
		mc.paneLayout('parentCountNumberPane', p='parentItemListPane', configuration='vertical2')
		mc.intField('parentAllNumber', p='parentCountNumberPane')
		mc.intField('parentSelectNumber', p='parentCountNumberPane')
		#�y�A�����g�A�C�e�����X�g�J�E���g�����C�A�E�g���܂���
		mc.setParent('parentCountNumberPane')		
		#�y�A�����g�A�C�e�����X�g�����[�u�����C�A�E�g���܂�
		mc.paneLayout('parentItemListRemovePane', p='parentItemListPane', configuration='horizontal3')
		mc.button('parentItemListRemoveButton', p='parentItemListRemovePane', l='remove', c=self.removeParent)
		mc.button('parentItemListMoveButton', p='parentItemListRemovePane', l='-->', c=self.moveToChild)
		mc.button('parentItemListSwapButton', p='parentItemListRemovePane', l='<-->', c=self.swap)
		#�y�A�����g�A�C�e�����X�g�����[�u�����C�A�E�g���܂���
		mc.setParent('parentItemListRemovePane')
		#�y�A�����g�A�C�e���t���[�������C�A�E�g���܂���
		mc.setParent('parentItemListPane')
		#�y�A�����g�A�C�e���t���[�������C�A�E�g���܂���
		mc.setParent('parentItemFrame')
		
		#�y�A�����g�A�g���r���[�g�����C�A�E�g���܂�
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
		#�y�A�����g�A�C�e���t���[�������C�A�E�g���܂���
		mc.setParent('parentAttrFrame')
		#�y�A�����g�t���[�������C�A�E�g���܂���
		mc.setParent('parentItemPane')
				
		#�`���h�����t���[�������C�A�E�g���܂�
		mc.paneLayout('childrenItemPane', p='allScrollListPane', configuration='vertical2')
		#�`���h�����A�g���r���[�g�����C�A�E�g���܂�
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
		#�`���h�����A�C�e���t���[�������C�A�E�g���܂���
		mc.setParent('childrenAttrFrame')
		
		#�`���h�����A�C�e���t���[�������C�A�E�g���܂�
		mc.frameLayout('childrenItemFrame', p='childrenItemPane', l='children item')		
		mc.paneLayout('childrenItemListPane', p='childrenItemFrame', configuration='horizontal4')
		#�`���h�����A�C�e�����X�g�C�������C�A�E�g���܂�
		mc.paneLayout('childrenItemListInAddPane', p='childrenItemListPane', configuration='horizontal2')
		mc.button('childrenItemListInButton', p='childrenItemListInAddPane', l='List Replace', c=self.listInChildren)
		mc.button('childrenItemListAddButton', p='childrenItemListInAddPane', l='List Add', c=self.listAddChildren)
		#�`���h�����A�C�e�����X�g�C�������C�A�E�g���܂���
		mc.setParent('parentItemListInAddPane')		
		#�`���h�����A�C�e�����X�g�X�N���[�������C�A�E�g���܂���		
		mc.textScrollList('childrenItemScrollList', p='childrenItemListPane', ams=True, sc=self.selectChildrenItem, dcc=self.deselectChildren, dgc=self.childrenDrag, dpc=self.childrenDrop)
		mc.popupMenu('childrenItemScrollListPopMenu', p='childrenItemScrollList', button=3)
		mc.menuItem('childrenItemScrollListMenuSel', p='childrenItemScrollListPopMenu', l='select all List', c=self.selectAllChildren)
		mc.menuItem('childrenItemScrollListMenuHi', p='childrenItemScrollListPopMenu', l='select List Items Hi', c=self.childrenHi)
		mc.menuItem('childrenItemScrollListMenuShape', p='childrenItemScrollListPopMenu', l='shape list', c=self.childrenSwitchShape)
		mc.menuItem('childrenItemScrollListMenuColl_A', p='childrenItemScrollListPopMenu', l='call constraint parent', c=self.collingConstraintParent)
		mc.menuItem('childrenItemScrollListMenuColl_B', p='childrenItemScrollListPopMenu', l='call connection parent', c=self.collingConnectionParent)
		
		#�`���h�����A�C�e�����X�g�J�E���g�����C�A�E�g���܂�
		mc.paneLayout('childrenCountNumberPane', p='childrenItemListPane', configuration='vertical2')
		mc.intField('childrenAllNumber', p='childrenCountNumberPane')
		mc.intField('childrenSelectNumber', p='childrenCountNumberPane')
		#�`���h�����A�C�e�����X�g�J�E���g�����C�A�E�g���܂���
		mc.setParent('childrenCountNumberPane')		
		#�`���h�����A�C�e�����X�g�����[�u�����C�A�E�g���܂�
		mc.paneLayout('childrenItemListRemovePane', p='childrenItemListPane', configuration='horizontal3')
		mc.button('childrenItemListRemoveButton', p='childrenItemListRemovePane', l='remove', c=self.removeChildren)
		mc.button('childrenItemListMoveButton', p='childrenItemListRemovePane', l='<--', c=self.moveToParent)
		mc.button('childrenItemListSwapButton', p='childrenItemListRemovePane', l='Remember', c=self.remenber)
		#�`���h�����A�C�e�����X�g�����[�u�����C�A�E�g���܂���
		mc.setParent('childrenItemListRemovePane')
		#�`���h�����A�C�e���t���[�������C�A�E�g���܂���
		mc.setParent('childrenItemListPane')
		#�`���h�����A�C�e���t���[�������C�A�E�g���܂���
		mc.setParent('childrenItemFrame')
		#�`���h�����t���[�������C�A�E�g���܂���
		mc.setParent('childrenItemPane')
		
		#�y�A�����g�ƃ`���h�����̃��X�g�����C�A�E�g���܂���
		mc.setParent('allScrollListPane')		
		
		#�x�N�^�[�A�C�e���t���[�������C�A�E�g���܂�
		mc.frameLayout('vectorItemFrame', p='relativePane', l='vector item')
		#�x�N�^�[�A�C�e������p�������C�A�E�g���܂�
		mc.paneLayout('vectorItemPane', p='vectorItemFrame', configuration='horizontal4')		
		#�x�N�^�[�A�C�e�������X�g�C�����邽�߂̐���p�������C�A�E�g���܂�
		mc.paneLayout('vectorItemListInAddPane',p='vectorItemPane', configuration='horizontal2')
		mc.button('vectorItemListInButton', p='vectorItemListInAddPane', l='List Replace', c=self.listInVector)
		mc.button('vectorItemListAddButton', p='vectorItemListInAddPane', l='List Add', c=self.listAddVector)
		#�x�N�^�[�A�C�e�������X�g�C�����邽�߂̐���p�������C�A�E�g���܂���
		mc.setParent('vectorItemListInAddPane')
		#�x�N�^�[�A�C�e�������X�g�X�N���[�������C�A�E�g���܂�
		mc.textScrollList('vectorItemScrollList', p='vectorItemPane', ams=True, sc=self.selectVectorItem, dcc=self.deselectVector, dgc=self.vectorDrag, dpc=self.vectorDrop)
		mc.popupMenu('vectorItemScrollListPopMenu', p='vectorItemScrollList', button=3)
		mc.menuItem('vectorItemScrollListMenuSel', p='vectorItemScrollListPopMenu', l='select List Items', c=self.selectAllVector)
		mc.menuItem('vectorItemScrollListMenuHi', p='vectorItemScrollListPopMenu', l='select List Items Hi', c=self.vectorHi)
		mc.menuItem('vectorItemScrollListMenuShape', p='vectorItemScrollListPopMenu', l='shape list', c=self.vectorSwitchShape)
		#mc.menuItem('vectorItemScrollListMenuColl', p='vectorItemScrollListPopMenu', l='coll others')
		
		#�x�N�^�[�A�C�e���̐���\������C���g�t�B�[���h�����C�A�E�g���܂�
		mc.paneLayout('vectorCountNumberPane',p='vectorItemPane', configuration='vertical2')
		mc.intField('vectorAllNumber', p='vectorCountNumberPane')
		mc.intField('vectorSelectNumber', p='vectorCountNumberPane')
		#�x�N�^�[�A�C�e���̐���\������C���g�t�B�[���h�����C�A�E�g���܂���
		mc.setParent('vectorCountNumberPane')
		#�x�N�^�[�A�C�e���������[�u���邽�߂̐���p�������C�A�E�g���܂�
		mc.paneLayout('vectorItemRemovePane',p='vectorItemPane', configuration='horizontal2')
		mc.button('vectorItemListRemoveButton', p='vectorItemRemovePane', l='Remove', c=self.removeVector)
		mc.button('vectorItemListClearButton', p='vectorItemRemovePane', l='All Clear')
		#�x�N�^�[�A�C�e���������[�u���邽�߂̐���p�������C�A�E�g���܂���
		mc.setParent('vectorItemRemovePane')
		#�x�N�^�[�A�C�e������p�������C�A�E�g���܂���
		mc.setParent('vectorItemPane')
		#�x�N�^�[�A�C�e���t���[�������C�A�E�g���܂���
		mc.setParent('vectorItemFrame')
		
		
		#�����[�V�����R���g���[���^�u�����C�A�E�g���܂�
		mc.tabLayout('relativeTab', p='relativePane')
		#�l�X�ȃR���X�g���C���g�̃t���[�����^�C�v�ʂɃ��C�A�E�g����y�C�������C�A�E�g���܂�
		mc.scrollLayout('constraintTypeScroll', p='relativeTab', childResizable=True)
		#�g�����X���[�g�R���X�g���C���g�i������x�[�V�b�N�ȃR���X�g���C���g�j���s���t���[�������C�A�E�g���܂�
#�y�A�����g�R���X�g���C���g�̃��C�A�E�g���s���܂�
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
#�y�A�����g�R���X�g���C���g�̃��C�A�E�g���s���܂���
#�|�C���g�R���X�g���C���g�̃��C�A�E�g���s���܂�
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
#�|�C���g�R���X�g���C���g�̃��C�A�E�g���s���܂�
#��]�R���X�g���C���g�̃��C�A�E�g���s���܂�
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
#��]�R���X�g���C���g�̃��C�A�E�g���s���܂�
#�L�k�R���X�g���C���g�̃��C�A�E�g���s���܂�
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
#�L�k�R���X�g���C���g�̃��C�A�E�g���s���܂�
		#�g�����X���[�g�R���X�g���C���g�i������x�[�V�b�N�ȃR���X�g���C���g�j���s���t���[�������C�A�E�g���܂���		
		#mc.setParent('transformConstrainFrame')
		
		#�V�F�C�v���g�p�����R���X�g���C���g�m�[�h�̍\�z���s���t���[�������C�A�E�g���܂�
#�t�H���N���R���X�g���C���g�̃��C�A�E�g���s���܂�				
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
#�t�H���N���R���X�g���C���g�̃��C�A�E�g���s���܂�		
#�J�[�u�C���t�H�R���X�g���C���g�̃��C�A�E�g���s���܂�		
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		mc.frameLayout('curveShapeConstraintFrame', p='constraintTypeScroll', l='curveShape constraint', bgc=[0,0,0], collapsable=True, collapse=True)
		mc.button('curveInfoConstraintButton', p='curveShapeConstraintFrame', l='curveInfo constraint', c=self.curveInfoC)
		mc.setParent('curveShapeConstraintFrame')		
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#�J�[�u�C���t�H�R���X�g���C���g�̃��C�A�E�g���s���܂�
#�^���W�F���g�R���X�g���C���g�̃��C�A�E�g���s���܂�------------------------------------------------------------------------------------------------------------------------------------------------------
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
#�^���W�F���g�R���X�g���C���g�̃��C�A�E�g���s���܂�------------------------------------------------------------------------------------------------------------------------------------------------------
		#�V�F�C�v���g�p�����R���X�g���C���g�m�[�h�̍\�z���s���t���[�������C�A�E�g���܂���
		#mc.setParent('shapeConstraintFrame')
		
		#����R���X�g���C���g���\�z����t���[�������C�A�E�g���܂�
#�G�C���R���X�g���C���g�̃��C�A�E�g���s���܂�		
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
#�G�C���R���X�g���C���g�̃��C�A�E�g���s���܂�		
		#����R���X�g���C���g���\�z����t���[�������C�A�E�g���܂���
		#mc.setParent('shapeConstraintFrame')		
		#�l�X�ȃR���X�g���C���g�̃t���[�����^�C�v�ʂɃ��C�A�E�g����y�C�������C�A�E�g���܂���
		mc.setParent('constraintTypeScroll')
		
		#�R�l�N�V�������ɃC���T�[�g���郆�[�e�B���e�B�[�̎�ނ̃��X�g�����C�A�E�g���܂�
		mc.paneLayout('insertUtirilyListPane', p='relativeTab')
		#�R�l�N�V�������ɃC���T�[�g���郆�[�e�B���e�B�[�̎�ނ̃��X�g�����C�A�E�g���܂���
		mc.setParent('insertUtirilyListPane')		
		#�����[�V�����R���g���[���^�u�����C�A�E�g���܂���
		mc.setParent('relativeTab')
		
		#�����[�V���������郊�X�g�ƃ����[�V�����̃^�C���ɂ��ă^�u�����C�A�E�g���܂���
		mc.setParent('relativePane')
		
		#�R���X�g���C���g�m�[�h�̃��X�g�𕪗ނ��ă��C�A�E�g���܂�
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
		#�R���X�g���C���g�m�[�h�̃��X�g�𕪗ނ��ă��C�A�E�g���܂���
		mc.setParent('listConstraintNodesPane')

		
		mc.setParent('relativePane')
		#���C���^�u��ݒ肵�܂�
		mc.setParent('mainTab')
		mc.showWindow('connectorWindow')
		
	#�E�B���h�E�����T�C�Y���܂�
	def windowResize(self, *args):
		#�R���X�g���C���g���쐬���X�g�̃^�u����ύX���܂�
		mc.tabLayout('mainTab', e=True, tabLabel=['relativePane', 'Conect list'])
		#�R���X�g���C���g�̎�ނ����X�g����^�u����ύX���܂�
		mc.tabLayout('mainTab', e=True, tabLabel=['listConstraintNodesPane', 'Constraint Type'])
		
		#�R���X�g���C���g�̃^�C�v�����X�g����^�u�����l�[�����܂�
		mc.tabLayout('relativeTab', e=True, tabLabel=['constraintTypeScroll', 'Constraint list'])
		#�R�l�N�V�������쐬����Ƃ��̕⏕���s�����[�e�B���e�B�[�m�[�h���쐬����^�u�����l�[�����܂�
		mc.tabLayout('relativeTab', e=True, tabLabel=['insertUtirilyListPane', 'Utirily list'])
		
		#�R���X�g���C���g���쐬����p�����C�A�E�g�̔䗦��ύX���܂�
		mc.paneLayout('relativePane', e=True, paneSize=[1,70,100])
		mc.paneLayout('relativePane', e=True, paneSize=[2,0,100])
		
		#�R���X�g���C���g���쐬���邻�ꂼ��̃A�g���r���[�g�p�����C�A�E�g�̔䗦��ύX���܂�
		mc.paneLayout('parentAttrPane', e=True, paneSize=[1,100,98])
		mc.paneLayout('childrenAttrPane', e=True, paneSize=[1,100,98])
		
		#�R���X�g���C���g���쐬���邻�ꂼ��̃��X�g�p�����C�A�E�g�̍��E�䗦��ύX���܂�		
		mc.paneLayout('parentItemPane', e=True, paneSize=[1,100,100])
		mc.paneLayout('childrenItemPane', e=True, paneSize=[2,100,100])
		
		#���X�g����Ă���A�C�e���̐���\��int�t�B�[���h�̔䗦��ύX���܂�
		mc.paneLayout('parentCountNumberPane', e=True, paneSize=[1,50,100])
		mc.paneLayout('childrenCountNumberPane', e=True, paneSize=[1,50,100])
		
		#�R���X�g���C���g���쐬���邻�ꂼ��̃��X�g�p�������̃��C�A�E�g�̔䗦��ύX���܂�		
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
		
		#�R���X�g���C���g�̎�ނ̓�������X�g����p���̔䗦��ύX���܂�
		mc.paneLayout('listConstraintNodesPane', e=True, paneSize=[3,70,7])
		#�R���X�g���C���g�̎�ނ̃��X�g����p���̔䗦��ύX���܂�
		mc.paneLayout('constraintTypeListPane', e=True, paneSize=[1,100,95])
		#�R���X�g���C���g�̎�ނ����W���ă��X�g���܂�
		self.listInConstraintType()
		
		
	#�V�[�����ɑ��݂���R���X�g���C���g�m�[�h�𕪗ނ��āA�R���X�g���C���g�^�C�v�X�N���[���ɋL��
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
#�R���X�g���C���g�m�[�h�����W���܂���
#ui���쐬���܂�---------------------------------------------------------------------------------------
###############################################################################################################################################################################################################
#���̃^�u�ŔC�ӂ̃R���X�g���C���g�m�[�h��I�������Ƃ������̒��g�����X�g���܂�--------------------------------------------
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

#���̃^�u�ŔC�ӂ̃R���X�g���C���g�m�[�h��I�������Ƃ������̒��g�����X�g���܂�--------------------------------------------
#�R���X�g���C���g�O���[�v��I�������Ƃ��A�O���[�v���̑I�𒆂̃R���X�g���C���g�^�C�v����g�����Ԗڂ̃��X�g�Ƀ��X�g�C��-------------------
	def listInConstrainContent(self, *args):
		global HA_constraintTypeDict
		type = mc.textScrollList('constraintTypeScroll', q=True, selectItem=True)
		grp = mc.textScrollList('constraintGrpScrollList', q=True, selectItem=True)
		mc.textScrollList('constraintGrpInsideScrollList', e=True, removeAll=True)
		cNodes = mc.ls((grp[0] + '|*'), type=type[0])
		mc.textScrollList('constraintGrpInsideScrollList', e=True, append=cNodes)
#�R���X�g���C���g�O���[�v��I�������Ƃ��A�O���[�v���̑I�𒆂̃R���X�g���C���g�^�C�v����g�����Ԗڂ̃��X�g�Ƀ��X�g�C��-------------------
#���̃^�u�ŁAlistIn�{�^�������������A�R���X�g���C���g�Ɋ֌W���邷�ׂẴm�[�h����O�̃^�u�̃��X�g�ɏ�������
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
				
			#�A�b�v�x�N�^�[�����݂����ꍇ�́A�x�N�^�[���X�g�ɏ������݂܂�
			#�����̎q�I�u�W�F�N�g���G�C������ꍇ�͌ʂɃR���X�g���C���g�m�[�h���쐬�����̂ŁA�l���s�v
			#�����A�����̐e����̎q���G�C�������Ă���ꍇ�́A���̐e�̐������A�A�b�v�x�N�^�[�����X�g����K�v������
			getUp = mc.listAttr(item[0], string='worldUpMatrix')
			getUpList = []
			if getUp != None:
				#print ''
				getUpList = mc.listConnections(item[0] + '.worldUpMatrix')
			if getUpList != None:	
				for i in pList:
					mc.textScrollList('vectorItemScrollList', e=True, append=getUpList)
		
		#���X�g�̎c���𐔂��Ȃ����܂�
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
		#�x�N�^�[�����Ȃ���
		trigger = 'vectorItemScrollList'
		triggerInt = 'vectorAllNumber'
		selInt = 'vectorSelectNumber'
		self.counter(trigger, triggerInt, selInt)	
#���̃^�u�ŁAlistIn�{�^�������������A�R���X�g���C���g�Ɋ֌W���邷�ׂẴm�[�h����O�̃^�u�̃��X�g�ɏ�������
#���̃^�u�őI�������R���X�g���C���g���폜���܂�
	def delListConstraint(self, *args):
		getGrp = mc.textScrollList('constraintGrpScrollList', q=True, selectItem=True)
		getItem = mc.textScrollList('constraintGrpOutsideScrollList', q=True, selectItem=True)
		mc.delete(getGrp)
		mc.delete(getItem)
		
		self.listInConstraintType()

		#���X�g�̎c���𐔂��Ȃ����܂�
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
		#�x�N�^�[�����Ȃ���
		trigger = 'vectorItemScrollList'
		triggerInt = 'vectorAllNumber'
		selInt = 'vectorSelectNumber'
		self.counter(trigger, triggerInt, selInt)	
#���̃^�u�őI�������R���X�g���C���g���폜���܂�
###############################################################################################################################################################################################################
#���p�������쐬���܂�(���X�g�������o�[�p�̃����A�I�����X�g���^�[���A���X�g�J�E���g�AD&D)---------------------------------------------------------
	#�I������A�C�e�����X�g���V�[�����ŃA�C�e����I�����܂�
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
	
	#rimember�p�̃��X�g�����݂̃��X�g�ŏ��������܂�
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
	#�A�C�e�������J�E���g���܂�
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
		
	#���ꂼ��̃��X�g�ŁA�I������ׂ��A�C�e�������W���܂�
	def getSelectListItems(self, trigger, *args):
		selItems = mc.textScrollList(trigger, q=True, selectItem=True)
		if selItems == None or selItems == []:
			selItems = mc.textScrollList(trigger, q=True, allItems=True)		
		return selItems

#���p�������쐬���܂�(���X�g�������o�[�p�̃����A�I�����X�g���^�[���A���X�g�J�E���g�AD&D)---------------------------------------------------------	
#���X�g���A�C�e���I�����ɃV�[���������A�C�e���I��
	#�y�A�����g���X�g���̃A�C�e�����I�����ꂽ�Ƃ��A�V�[���������A�C�e����I��
	def selectParentItem(self, *args):
		trigger = 'parentItemScrollList'
		self.selectScenesItems(trigger)
		
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'
		self.counter(trigger, triggerInt, selInt)#def�̍s���L���\��
		
		#�A�g���r���[�g���X�g��`�����݂܂�
		self.listParentAttrKeyble()

	#�`���h�������X�g���̃A�C�e�����I�����ꂽ�Ƃ��A�V�[���������A�C�e����I��
	def selectChildrenItem(self, *args):
		trigger = 'childrenItemScrollList'
		self.selectScenesItems(trigger)
		
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'
		self.counter(trigger, triggerInt, selInt)#def�̍s���L���\��
		
		#�A�g���r���[�g���X�g��`�����݂܂�
		self.listChildrenAttrKeyble()
		
	#�x�N�^�[���X�g���̃A�C�e�����I�����ꂽ�Ƃ��A�V�[���������A�C�e����I��
	def selectVectorItem(self, *args):
		trigger = 'vectorItemScrollList'
		self.selectScenesItems(trigger)
		
		triggerInt = 'vectorAllNumber'
		selInt = 'vectorSelectNumber'
		self.counter(trigger, triggerInt, selInt)#def�̍s���L���\��

#�A�C�e���_�u���N���b�N���ɃA�C�e���I�����������܂�----------------------------------------------------------------------------------
	#�y�A�����g�̑I�����������܂�
	def deselectParent(self, *args):
		trigger = 'parentItemScrollList'
		self.deselectScrollList(trigger)#def�̍s���L���\��
		
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'
		self.counter(trigger, triggerInt, selInt)#def�̍s���L���\��
		
	#�`���h�����̑I�����������܂�		
	def deselectChildren(self, *args):
		trigger = 'childrenItemScrollList'
		self.deselectScrollList(trigger)#def�̍s���L���\��
		
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'
		self.counter(trigger, triggerInt, selInt)#def�̍s���L���\��
		
	#���F�N�^�[�̑I�����������܂�		
	def deselectVector(self, *args):	
		trigger = 'vectorItemScrollList'
		self.deselectScrollList(trigger)#def�̍s���L���\��
				
		triggerInt = 'vectorAllNumber'
		selInt = 'vectorSelectNumber'
		self.counter(trigger, triggerInt, selInt)#def�̍s���L���\��
	#�A�C�e�����f�B�Z���N�g���܂�
	def deselectScrollList(self, trigger, *args):
		mc.textScrollList(trigger, e=True, deselectAll=True)
		mc.select(clear=True)
#�A�C�e�����f�B�Z���N�g���܂�--------------------------------------------------------------------------------------------
#���X�g�C�����܂�----------------------------------------------------------------------------------------------------
	#�y�A�����g�Ƀ��X�g�C�����܂�
	def listInParent(self, *args):
		trigger = 'parentItemScrollList'
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'		
		
		self.listInSceneItem(trigger)
		self.lastScrollList(trigger)
		self.counter(trigger, triggerInt, selInt)

	#�`���h�����Ƀ��X�g�C�����܂�
	def listInChildren(self, *args):
		trigger = 'childrenItemScrollList'	
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'
		
		self.listInSceneItem(trigger)
		self.lastScrollList(trigger)
		self.counter(trigger, triggerInt, selInt)
		
	#�x�N�^�[�Ƀ��X�g�C�����܂�
	def listInVector(self, *args):
		trigger = 'vectorItemScrollList'
		triggerInt = 'vectorAllNumber'
		selInt = 'vectorSelectNumber'
		
		self.listInSceneItem(trigger)		
		self.lastScrollList(trigger)
		self.counter(trigger, triggerInt, selInt)
	
	#���X�g�C�����܂�
	def listInSceneItem(self, trigger, *args):	
		listIn = mc.ls(sl=True)
		if listIn != None:
			mc.textScrollList(trigger, e=True, removeAll=True)
			mc.textScrollList(trigger, e=True, append=listIn)	
#���X�g�C�����܂�----------------------------------------------------------------------------------------------------
#���X�g�ɃA�b�h���܂�--------------------------------------------------------------------------------------------------
	#�y�A�����g�ɃA�b�h���܂�
	def listAddParent(self, *args):
		trigger = 'parentItemScrollList'		
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'
		
		self.lastScrollList(trigger)
		self.listAddItem(trigger)
		self.counter(trigger, triggerInt, selInt)

	#�`���h�����ɃA�b�h���܂�
	def listAddChildren(self, *args):
		trigger = 'childrenItemScrollList'
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'
		
		self.lastScrollList(trigger)				
		self.listAddItem(trigger)
		self.counter(trigger, triggerInt, selInt)
		
	#�x�N�^�[�ɃA�b�h���܂�
	def listAddVector(self, *args):
		trigger = 'vectorItemScrollList'		
		triggerInt = 'vectorAllNumber'
		selInt = 'vectorSelectNumber'
		
		self.lastScrollList(trigger)		
		self.listAddItem(trigger)
		self.counter(trigger, triggerInt, selInt)
		
	#���X�g�ɃA�b�h���܂�
	def listAddItem(self, trigger, *args):
		listIn = mc.ls(sl=True)
		if listIn != None:
			mc.textScrollList(trigger, e=True, append=listIn)
#���X�g�ɃA�b�h���܂�--------------------------------------------------------------------------------------------------
#�����[�u���܂�-----------------------------------------------------------------------------------------------------	
	#�y�A�����g�������[�u���܂�
	def removeParent(self, *args):
		trigger = 'parentItemScrollList'
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'
		
		self.lastScrollList(trigger)		
		self.removeItem(trigger)
		self.counter(trigger, triggerInt, selInt)
				
	#�`���h�����������[�u���܂�
	def removeChildren(self, *args):
		trigger = 'childrenItemScrollList'		
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'
		
		self.lastScrollList(trigger)
		self.removeItem(trigger)
		self.counter(trigger, triggerInt, selInt)		
					
	#�x�N�^�[�������[�u���܂�
	def removeVector(self, *args):
		trigger = 'vectorItemScrollList'
		triggerInt = 'vectorAllNumber'
		selInt = 'vectorSelectNumber'
		
		self.lastScrollList(trigger)
		self.removeItem(trigger)
		self.counter(trigger, triggerInt, selInt)
							
	#�����[�u���܂�
	def removeItem(self, trigger, *args):
		removeList = self.getSelectListItems(trigger)
		if removeList != None:
			mc.textScrollList(trigger, e=True, removeItem=removeList)
#�����[�u���܂�-----------------------------------------------------------------------------------------------------	
#���E�̃��X�g�̓��e�����ւ��܂�---------------------------------------------------------------------------------------	
	#�E�ֈړ����܂�
	def moveToChild(self, *args):
		#�g���K�[���w�肵�܂�
		trigger ='parentItemScrollList'
		#�Z���N�g�A�C�e�����擾���܂�
		memo = self.getSelectListItems(trigger)
		
		#�`���h�����ɒǉ����܂�
		if memo != None:
			#�y�A�����g���烊���[�u���܂�
			mc.textScrollList('parentItemScrollList', e=True, removeItem=memo)
			mc.textScrollList('childrenItemScrollList', e=True, append=memo)
			
		#�y�A�����g���X�g���L�����܂�
		trigger ='parentItemScrollList'
		self.lastScrollList(trigger)
		#�`���h�������X�g���L�����܂�		
		trigger ='childrenItemScrollList'
		self.lastScrollList(trigger)		
		
		#�y�A�����g�����Ȃ���
		trigger = 'parentItemScrollList'
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
				
		#�`���h���������Ȃ���
		trigger ='childrenItemScrollList'
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'		
		self.counter(trigger, triggerInt, selInt)		
									
	#���ֈړ����܂�
	def moveToParent(self, *args):
		#�g���K�[���w�肵�܂�
		trigger = 'childrenItemScrollList'
		#�Z���N�g�A�C�e�����擾���܂�
		memo = self.getSelectListItems(trigger)
		
		#�y�A�����g�ɒǉ����܂�
		if memo != None:
			#�`���h�������烊���[�u���܂�		
			mc.textScrollList('childrenItemScrollList', e=True, removeItem=memo)
			mc.textScrollList('parentItemScrollList', e=True, append=memo)
		
		#�y�A�����g���X�g���L�����܂�
		trigger ='parentItemScrollList'
		self.lastScrollList(trigger)
		#�`���h�������X�g���L�����܂�		
		trigger ='childrenItemScrollList'
		self.lastScrollList(trigger)

		#�y�A�����g�����Ȃ���
		trigger = 'parentItemScrollList'
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
				
		#�`���h���������Ȃ���
		trigger ='childrenItemScrollList'
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'		
		self.counter(trigger, triggerInt, selInt)				
						
	#���E����ւ�
	def swap(self, *args):
		#�ړ��A�C�e�������W���܂�
		trigger ='parentItemScrollList'
		swapP = self.getSelectListItems(trigger)
			
		#�ړ��A�C�e�������W���܂�
		trigger ='childrenItemScrollList'
		swapC = self.getSelectListItems(trigger)		
		
		if swapC != None:
			mc.textScrollList('childrenItemScrollList', e=True, removeItem=swapC)
			mc.textScrollList('parentItemScrollList', e=True, append=swapC)
			
		if swapP != None:
			mc.textScrollList('parentItemScrollList', e=True, removeItem=swapP)
			mc.textScrollList('childrenItemScrollList', e=True, append=swapP)
		
		#�y�A�����g���X�g���L�����܂�
		trigger ='parentItemScrollList'
		self.lastScrollList(trigger)
		#�`���h�������X�g���L�����܂�		
		trigger ='childrenItemScrollList'
		self.lastScrollList(trigger)
		#�x�N�^�[���X�g���L�����܂�		
		trigger ='vectorItemScrollList'
		self.lastScrollList(trigger)

		#�y�A�����g�����Ȃ���
		trigger = 'parentItemScrollList'
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
				
		#�`���h���������Ȃ���
		trigger ='childrenItemScrollList'
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'		
		self.counter(trigger, triggerInt, selInt)				
		
	#�v���o��
	def remenber(self, *args):
		global HA_parentListRemember
		global HA_childrenListRemember
		global HA_vectorListRemember		
		rememberP = HA_parentListRemember
		rememberC = HA_childrenListRemember
		rememberV = HA_vectorListRemember
		
		#�y�A�����g���X�g���L�����܂�
		trigger ='parentItemScrollList'
		self.lastScrollList(trigger)
		#�`���h�������X�g���L�����܂�		
		trigger ='childrenItemScrollList'
		self.lastScrollList(trigger)
		#�x�N�^�[���X�g���L�����܂�		
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
		
		#�y�A�����g�����Ȃ���
		trigger = 'parentItemScrollList'
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
				
		#�`���h���������Ȃ���
		trigger ='childrenItemScrollList'
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'		
		self.counter(trigger, triggerInt, selInt)		
		
		#�x�N�^�[�����Ȃ���
		trigger = 'vectorItemScrollList'
		triggerInt = 'vectorAllNumber'
		selInt = 'vectorSelectNumber'
		self.counter(trigger, triggerInt, selInt)					
#���E�̃��X�g�̓��e�����ւ��܂�---------------------------------------------------------------------------------------	
#�S�I��
	#�y�A�����g���X�g���̂��ׂẴA�C�e����I�����܂�
	def selectAllParent(self, *args):
		trigger = 'parentItemScrollList'
		self.selectAll(trigger)
		
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
		
	#�`���h�������X�g���̂��ׂẴA�C�e����I�����܂�
	def selectAllChildren(self, *args):
		trigger = 'childrenItemScrollList'
		self.selectAll(trigger)
		
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'		
		self.counter(trigger, triggerInt, selInt)		
		
	#�x�N�^�[���X�g���̂��ׂẴA�C�e����I�����܂�
	def selectAllVector(self, *args):
		trigger = 'vectorItemScrollList'
		self.selectAll(trigger)
		
		triggerInt = 'vectorAllNumber'
		selInt = 'vectorSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
	#�p�������X�N���[���A�C�e����I�����đI�����܂�
	def selectAll(self, trigger, *args):
		all = mc.textScrollList(trigger, q=True, allItems=True)
		mc.textScrollList(trigger, e=True, selectItem=all)
		self.selectScenesItems(trigger)
				
#�q�G�����L�[��I�����܂�
	#�y�A�����g���X�g�̃A�C�e�����K�w�őI�����܂�
	def parentHi(self, *args):
		trigger ='parentItemScrollList'
		self.listHierarchy(trigger)
		
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
		
	#�`���h�������X�g���L�����܂�	
	def childrenHi(self, *args):
		trigger ='childrenItemScrollList'
		self.listHierarchy(trigger)
		
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
	
	#���F�N�^�[���X�g���L�����܂�	
	def vectorHi(self, *args):
		trigger ='vectorItemScrollList'
		self.listHierarchy(trigger)
		
		triggerInt = 'vectorAllNumber'
		selInt = 'vectorSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
		
	#�I�������A�C�e�����ێ����Ă��邷�ׂẴ`���h������I�����܂�
	def listHierarchy(self, trigger, *args):		
		items = self.getSelectListItems(trigger)
		selHi = []
		for i in items:
			mc.select(i,r=True, hi=True)	
			selHi.extend(mc.ls(sl=True, type='transform'))
			mc.select(clear=True)
		
		mc.select(selHi,r=True)
		
	
	#�y�A�����g���X�g�̃A�C�e�����V�F�C�v�m�[�h�Œu�������܂�
	def parentSwitchShape(self, *args):				
		trigger = 'parentItemScrollList'
		self.lastScrollList(trigger)
		
		self.listItemShape(trigger)
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
		
	#�`���h�������X�g�̃A�C�e�����V�F�C�v�m�[�h�Œu�������܂�
	def childrenSwitchShape(self, *args):				
		trigger = 'childrenItemScrollList'
		self.lastScrollList(trigger)
		
		self.listItemShape(trigger)
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
		
	#���F�N�^�[���X�g�̃A�C�e�����V�F�C�v�m�[�h�Œu�������܂�
	def vectorSwitchShape(self, *args):				
		trigger = 'vectorItemScrollList'
		self.lastScrollList(trigger)
		
		self.listItemShape(trigger)
		triggerInt = 'vectorAllNumber'
		selInt = 'vectorSelectNumber'		
		self.counter(trigger, triggerInt, selInt)

	#���X�g����Ă���A�C�e���̃V�F�C�v�m�[�h���擾���܂�
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

#�R���X�g���C���g���Ăяo���܂��i�o���S�����̏�A���������j
	#�y�A�����g������`���h�������Ăяo���܂�
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
		
		#���X�g���ăJ�E���g���܂�
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'
		self.counter(trigger, triggerInt, selInt)#def�̍s���L���\��
		
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'
		self.counter(trigger, triggerInt, selInt)#def�̍s���L���\��
			
	#�`���h����������y�A�����g���Ăяo���܂�
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
		
		#���X�g���ăJ�E���g���܂�
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'
		self.counter(trigger, triggerInt, selInt)#def�̍s���L���\��
		
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'
		self.counter(trigger, triggerInt, selInt)#def�̍s���L���\��
	
	def collingOtherNodes(self, triggerA, triggerB, plugS, plugA, plugB, *args):
		master = mc.textScrollList(triggerA, q=True, allItems=True)
		
		#�R���X�g���C���g�m�[�h�����W��
		constrainNode = []#�R���X�g���C���͈�̃m�[�h�����������Ă���ꍇ�����݂���̂ŁA���X�gin���X�g�ŏW�߂Ă��܂��B
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
		
				masters = slaveDic.keys()#�O��܂ł̃}�X�^�[���擾���܂�
				for m in masterNode:
					if m not in masters:
						slaveDic[m] = slaveNode
					else:
						last = slaveDic[m]
						new = last + slaveNode
						slaveDic[m] = new
			
		#���݂��̃��X�g�����������܂�
		mc.textScrollList('parentItemScrollList', e=True, removeAll=True)
		mc.textScrollList('childrenItemScrollList', e=True, removeAll=True)
		#�쐬���������̓��e�őo���̃��X�g�����������܂�
		masterkey = slaveDic.keys()
		for i in masterkey:
			slaves = slaveDic[i]
			for e in slaves:
				mc.textScrollList(triggerA, e=True, append=i)
				mc.textScrollList(triggerB, e=True, append=e)
#�R���X�g���C���g���Ăяo���܂��i�o���S�����̏�A���������j
#�R�l�N�V�����̌Ăяo�����s���܂��i�o���S�����̏�A���������j
	#�R�l�N�V�����̃`���h�������Ăяo���܂�
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
		
		#���X�g���ăJ�E���g���܂�
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'
		self.counter(trigger, triggerInt, selInt)#def�̍s���L���\��
		
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'
		self.counter(trigger, triggerInt, selInt)#def�̍s���L���\��
		
	#�R�l�N�V�����̃y�A�����g���Ăяo���܂�
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
		
		#���X�g���ăJ�E���g���܂�
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'
		self.counter(trigger, triggerInt, selInt)#def�̍s���L���\��
		
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'
		self.counter(trigger, triggerInt, selInt)#def�̍s���L���\��
		
	#�R�l�N�V�����̌Ăяo�����Ǘ����܂�
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
#�R�l�N�V�����̌Ăяo�����s���܂��i�o���S�����̏�A���������j

#D&D����ׂ��A�C�e���ƃX�N���[���̏���D&Ddef�ɓn���܂�
	#�y�A�����g��D&D���܂�
	#�y�A�����g���h���b�v���܂�
	def parentDrop(self, dragControl, dropControl, msgs, x, y, dragType, *args):		
		if mc.textScrollList('parentItemScrollList', q=True, allItems=True) != None:
			trigger = 'parentItemScrollList'
			self.lastScrollList(trigger)
			
		position = int(float(y)*0.1) +1
		for i, v in enumerate(msgs):
			mc.textScrollList(trigger, e=True, removeItem=v)
			mc.textScrollList(trigger, e=True, appendPosition=[(i+position), v])		
		
	#�y�A�����g���h���b�O���܂�
	def parentDrag(self, dragControl, x, y, mods, *args):
		msgs = []
		msgs = mc.textScrollList('parentItemScrollList', q=True, selectItem=True)
		return msgs	
	
	#�`���h������D&D���܂�
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
		
	#�x�N�^�[��D&D���܂�
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

#�A�g���r���[�g���X�g�̓��e��ύX���܂�
	#allAttry���I�����ꂽ�Ƃ��A���X�g�A�g�������ׂď������݂܂�(�I�����ɂ���def�����s�����悤�ɑI��def�Ɏ��s�R�}���h��������)
	#�y�A�����g�̑I������Ă���A�C�e���̈�ԏ�̃m�[�h�̃A�g���r���[�g�����ׂď����o���܂�
	def listParentAttrAll(self,*args):
		trigger = 'parentItemScrollList'
		attrScroll = 'parentAttrScrollList'
		flug = 'all'
		self.listInAttr(trigger, attrScroll, flug)
	#�`���h�����̑I������Ă���A�C�e���̈�ԏ�̃m�[�h�̃A�g���r���[�g�����ׂď����o���܂�
	def listChildrenAttrAll(self,*args):	
		trigger = 'childrenItemScrollList'
		attrScroll = 'childrenAttrScrollList'
		flug = 'all'
		self.listInAttr(trigger, attrScroll, flug)
	#�y�A�����g�̑I������Ă���A�C�e���̈�ԏ�̃m�[�h�̃A�g���r���[�g���L�[�u���ƃ}�g���N�X�݂̂������o���܂�
	def listParentAttrKeyble(self,*args):
		trigger = 'parentItemScrollList'
		attrScroll = 'parentAttrScrollList'
		flug = 'keyble'
		self.listInAttr(trigger, attrScroll, flug)
	#�`���h�����̑I������Ă���A�C�e���̈�ԏ�̃m�[�h�̃A�g���r���[�g���L�[�u���ƃ}�g���N�X�݂̂������o���܂�		
	def listChildrenAttrKeyble(self,*args):	
		trigger = 'childrenItemScrollList'
		attrScroll = 'childrenAttrScrollList'
		flug = 'keyble'
		self.listInAttr(trigger, attrScroll, flug)
	#�t���O�ɏ]���āA�A�g���r���[�g���X�g�̓��e�����������܂�
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
#�A�g���r���[�g���X�g�̓��e��ύX���܂�
	
#�R�l�N�V�������s���܂�	
	#TRS�R�l�N�V�������s���܂�
	#TRS�R�l�N�V�������s���܂�
	#TR�R�l�N�V�������s���܂�	
	#TR�R�l�N�V�������s���܂�
	#T�R�l�N�V�������s���܂�
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
			
		#�y�A�����g�����Ȃ���
		trigger = 'parentItemScrollList'
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
				
		#�`���h���������Ȃ���
		trigger ='childrenItemScrollList'
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'		
		self.counter(trigger, triggerInt, selInt)	
	#T�R�l�N�V�������s���܂�		
	#R�R�l�N�V�������s���܂�		
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
			
		#�y�A�����g�����Ȃ���
		trigger = 'parentItemScrollList'
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
				
		#�`���h���������Ȃ���
		trigger ='childrenItemScrollList'
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'		
		self.counter(trigger, triggerInt, selInt)	
	#R�R�l�N�V�������s���܂�
	#S�R�l�N�V�������s���܂�		
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
			
		#�y�A�����g�����Ȃ���
		trigger = 'parentItemScrollList'
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
				
		#�`���h���������Ȃ���
		trigger ='childrenItemScrollList'
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'		
		self.counter(trigger, triggerInt, selInt)	
	
	#S�R�l�N�V�������s���܂�
	
	#�A�g���r���[�g���X�g����I�������A�C�e���ŃR�l�N�V�������܂�
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
			
		#�y�A�����g�����Ȃ���
		trigger = 'parentItemScrollList'
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
				
		#�`���h���������Ȃ���
		trigger ='childrenItemScrollList'
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'		
		self.counter(trigger, triggerInt, selInt)	
	#�A�g���r���[�g���X�g����I�������A�C�e���ŃR�l�N�V�������܂�
	
	#�R�l�N�V�������܂�
	def connectAttrs(self, pItem, cItem, pChannel, cChannel, *args):
		for i,v in enamerate(pItem):
			pAttr = mc.attributeQuery(pChannel, node=v, exists=True)
			cAttr = mc.attributeQuery(cChannel, node=cItem[i], exists=True)	
			if pAttr == True and cAttr == True:
				mc.connectAttr((v + '.' + pChannel), (cItem[i] + '.' + cChannel), f=True)
				mc.textScrollList('parentItemScrollList', e=True, removeIndexedItem=i)
				mc.textScrollList('childrenItemScrollList', e=True, removeIndexedItem=i)	
#�R�l�N�V�������܂�
#�R�l�N�V�������s���܂�
###############################################################################################################################################################################################################
#�R���X�g���C���g���s���܂�
#�R���V���g���C���g������������A�R���X�g���C���g�m�[�h���O���[�v�ł܂Ƃ߂܂��B
	def collectionGrp(self, getConstraints, type, *args):
		gName = 'con_' + type + '#'
		mc.group(getConstraints, n=('con_' + type + '#'), world=True)
		mc.select(r=True)
#�R���V���g���C���g������������A�R���X�g���C���g�m�[�h���O���[�v�ł܂Ƃ߂܂��B
#��ƏI����̃��X�g���󂯎���ă��X�g���烊���[�u���܂��B
	def removeList(self, constraintList, *args):
		cList = constraintList.keys()
		pList = []
		for i in cList:
			pList.append(constraintList[i])
		
		mc.textScrollList('parentItemScrollList', e=True, removeItem=pList)
		mc.textScrollList('childrenItemScrollList', e=True, removeItem=cList)	
#��ƏI����̃��X�g���󂯎���ă��X�g���烊���[�u���܂��B
#��ƏI����̃��X�g���󂯎���ă��X�g���烊���[�u���܂��B
	def removeVectorList(self, vectorList, *args):
		cList = vectorList.keys()
		vList = []
		for i in cList:
			vList.append(vectorList[i])
		
		#mc.textScrollList('parentItemScrollList', e=True, removeItem=pList)
		mc.textScrollList('vectorItemScrollList', e=True, removeItem=vList)	
#��ƏI����̃��X�g���󂯎���ă��X�g���烊���[�u���܂��B

#�R���X�g���C���g�p�̎������쐬���āA���^�[�����܂�
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
				mc.confirmDialog(m=('�y�A�����g���X�g�̈�Ԗڂł��ׂẴ`���h�������R���X�g���C���g���܂�'))
				
		return constraintList
#�R���X�g���C���g�p�̎������쐬���āA���^�[�����܂�
#�x�N�^�[���`���h�����ƕR�Â��������ɂ��ă��^�[�����܂�
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
				mc.confirmDialog(m=('�y�A�����g���X�g�̈�Ԗڂł��ׂẴ`���h�������R���X�g���C���g���܂�'))
				
		return constraintList
#�x�N�^�[���`���h�����ƕR�Â��������ɂ��ă��^�[�����܂�
#�X�L�b�v�`�����l�������^�[�����܂�
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
#�X�L�b�v�`�����l�������^�[�����܂�
#�y�A�����g�R���X�g���C���g���s���܂�
	def parentC(self, *args):
		#���݃��X�g����Ă���A�C�e���Ń������o�[�����������܂�
		trigger = 'parentItemScrollList'
		self.lastScrollList(trigger)
		trigger = 'childrenItemScrollList'
		self.lastScrollList(trigger)		
		
		#���C���e�C���I�t�Z�b�g���m�F���܂�
		meinten = mc.checkBox('parentConstraintMaintainCheck', q=True, value=True)
		#�X�L�b�v����`�����l�����m�F���܂�
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
						
		#��Ƃ������������X�g���̃A�C�e�������X�g���烊���[�u���܂�
		self.removeList(constraintList)
		
		#�O���[�v�m�[�h���쐬���܂�
		type = 'parent_'
		self.collectionGrp(getConstraints, type)
				
		#���X�g�̎c���𐔂��Ȃ����܂�
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
		
#�y�A�����g�R���X�g���C���g���s���܂�
#�|�W�V�����R���X�g���C���g���s���܂�
	def pointC(self, *args):
		#���݃��X�g����Ă���A�C�e���Ń������o�[�����������܂�
		trigger = 'parentItemScrollList'
		self.lastScrollList(trigger)
		trigger = 'childrenItemScrollList'
		self.lastScrollList(trigger)		

		#���C���e�C���I�t�Z�b�g���m�F���܂�		
		meinten = mc.checkBox('pointConstraintMaintainCheck', q=True, value=True)
		
		cx,cy,cz = 'pointTxCheck', 'pointTyCheck', 'pointTzCheck'
		skipping = self.skipChannnelsReturn(cx,cy,cz)
		
		constraintList = self.constraintDictReturn()
		cLIst = constraintList.keys()
		
		#�R���X�g���C���g�m�[�h�����W���܂�
		getConstraints = []
		
		for i in cLIst:
			pItems = constraintList[i]
			if len(pItems) == 2:
				cn = pItems[0] + '_' + pItems[1] + '_to_' + i + '_position'
				mc.pointConstraint(pItems, i, skip=skipping, maintainOffset=meinten, n=cn, weight=0.5)
				getConstraints.append(cn)
			else:
				cn = pItems + '_to_' + i + '_position'
				mc.pointConstraint(pItems, i, skip=skipping, maintainOffset=meinten, n=cn, weight=1.0)#�|�W�V�����R���X�g���C���g���s���܂�
				getConstraints.append(cn)
						
		#��Ƃ������������X�g���̃A�C�e�������X�g���烊���[�u���܂�
		self.removeList(constraintList)
		
		#�O���[�v�m�[�h���쐬���܂�
		type = 'point_'
		self.collectionGrp(getConstraints, type)
		
		#���X�g�̎c���𐔂��Ȃ����܂�
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
#�|�W�V�����R���X�g���C���g���s���܂�
#���[�e�[�V�����R���X�g���C���g���s���܂�
	def rotateC(self, *args):
		#���݃��X�g����Ă���A�C�e���Ń������o�[�����������܂�
		trigger = 'parentItemScrollList'
		self.lastScrollList(trigger)
		trigger = 'childrenItemScrollList'
		self.lastScrollList(trigger)		

		#���C���e�C���I�t�Z�b�g���m�F���܂�		
		meinten = mc.checkBox('rotateConstraintMaintainCheck', q=True, value=True)
		
		cx,cy,cz = 'rotateTxCheck', 'rotateTyCheck', 'rotateTzCheck'
		skipping = self.skipChannnelsReturn(cx,cy,cz)
		
		constraintList = self.constraintDictReturn()
		cLIst = constraintList.keys()
			
		#�R���X�g���C���g�m�[�h�����W���܂�		
		getConstraints = []
		
		for i in cLIst:
			pItems = constraintList[i]
			if len(pItems) == 2:
				cn = pItems[0] + '_' + pItems[1] + '_to_' + i + '_rotate'
				mc.orientConstraint(pItems, i, skip=skipping, maintainOffset=meinten, n=cn, weight=0.5)
				getConstraints.append(cn)
			else:
				cn = pItems + '_to_' + i + '_rotate'
				mc.orientConstraint(pItems, i, skip=skipping, maintainOffset=meinten, n=cn, weight=1.0)#�|�W�V�����R���X�g���C���g���s���܂�	
				getConstraints.append(cn)
						
		#��Ƃ������������X�g���̃A�C�e�������X�g���烊���[�u���܂�
		self.removeList(constraintList)
		
		#�O���[�v�m�[�h���쐬���܂�
		type = 'rotate_'
		self.collectionGrp(getConstraints, type)		
				
		#���X�g�̎c���𐔂��Ȃ����܂�
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
#���[�e�[�V�����R���X�g���C���g���s���܂�
#�X�P�[���R���X�g���C���g���s���܂�
	def scaleC(self, *args):
		#���݃��X�g����Ă���A�C�e���Ń������o�[�����������܂�
		trigger = 'parentItemScrollList'
		self.lastScrollList(trigger)
		trigger = 'childrenItemScrollList'
		self.lastScrollList(trigger)		
		
		#���C���e�C���I�t�Z�b�g���m�F���܂�		
		meinten = mc.checkBox('scaleConstraintMaintainCheck', q=True, value=True)
		
		cx,cy,cz = 'scaleTxCheck', 'scaleTyCheck', 'scaleTzCheck'
		skipping = self.skipChannnelsReturn(cx,cy,cz)
				
		constraintList = self.constraintDictReturn()
		cLIst = constraintList.keys()

		#�R���X�g���C���g�m�[�h�����W���܂�		
		getConstraints = []
		
		for i in cLIst:
			pItems = constraintList[i]
			if len(pItems) == 2:
				cn = pItems[0] + '_' + pItems[1] + '_to_' + i + '_scale'
				mc.scaleConstraint(pItems, i, skip=skipping, maintainOffset=meinten, n=cn, weight=0.5)
				getConstraints.append(cn)
			else:
				cn = pItems + '_to_' + i + '_scale'
				mc.scaleConstraint(pItems, i, skip=skipping, maintainOffset=meinten, n=cn, weight=1.0)#�|�W�V�����R���X�g���C���g���s���܂�	
				getConstraints.append(cn)
				
		#��Ƃ������������X�g���̃A�C�e�������X�g���烊���[�u���܂�
		self.removeList(constraintList)
		type = 'scale_'
		self.collectionGrp(getConstraints, type)		
		
		#���X�g�̎c���𐔂��Ȃ����܂�
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
#�X�P�[���R���X�g���C���g���s���܂�
#�t�H���N���Ȃǂ̓���R���X�g���C���g���s���܂�
#�t�H���N���R���X�g���C���g���s���܂�
	def follicleMeshC(self, *args):
		#���݃��X�g����Ă���A�C�e���Ń������o�[�����������܂�
		trigger = 'parentItemScrollList'
		self.lastScrollList(trigger)
		trigger = 'childrenItemScrollList'
		self.lastScrollList(trigger)		
		
		#���C���e�C���I�t�Z�b�g���m�F���܂�		
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
		
		#��ƏI����A���X�g�����������m�[�h���܂Ƃ߂܂�
		self.removeList(constraintList)		
		self.removeVectorList(vectorList)
		type = 'folM_'
		self.collectionGrp(getConstraints, type)
		
		#���X�g�̎c���𐔂��Ȃ����܂�
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
		
	#nuebis�T�[�t�F�X�Ń|�C���g�X�i�b�v���s���܂�(���܂肤�܂������Ă��܂���)
	def follicleSafaceC(self, *args):
		#���݃��X�g����Ă���A�C�e���Ń������o�[�����������܂�
		trigger = 'parentItemScrollList'
		self.lastScrollList(trigger)
		trigger = 'childrenItemScrollList'
		self.lastScrollList(trigger)		
		
		#���C���e�C���I�t�Z�b�g���m�F���܂�		
		meinten = mc.checkBox('nubFollicleOffsetCheck', q=True, value=True)		
		
		#�R���X�g���C���g�������쐬���܂��B
		constraintList = self.constraintDictReturn()
		cLIst = constraintList.keys()		
		#�R���X�g���C���g���s���܂��B
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
		
		#��ƏI����A���X�g�����������A�m�[�h���܂Ƃ߂܂�
		self.removeList(constraintList)		
		self.removeVectorList(vectorList)
		type = 'folS_'
		self.collectionGrp(getConstraints, type)
		
		#���X�g�̎c���𐔂��Ȃ����܂�
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
		
#�t�H���N���R���X�g���C���g���s���܂�
#�J�[�u�C���t�H�R���X�g���C���g���s���܂�
	def curveInfoC(self, *args):
		#���݃��X�g����Ă���A�C�e���Ń������o�[�����������܂�
		trigger = 'parentItemScrollList'
		self.lastScrollList(trigger)
		trigger = 'childrenItemScrollList'
		self.lastScrollList(trigger)	
		trigger = 'vectorItemScrollList'
		self.lastScrollList(trigger)
		
		#����ƃ��X�g���擾���܂�		           
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
									
		#���X�g�����������܂�
		self.removeList(constraintList)		
		#self.removeVectorList(vectorList)
		
		#���X�g�̎c���𐔂��Ȃ����܂�
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'		
		self.counter(trigger, triggerInt, selInt)		
#�J�[�u�C���t�H�R���X�g���C���g���s���܂�
#���F�N�^�[�m�[�h���g�p�����R���X�g���C���g���s���܂�
#�^���W�F���g�R���X�g���C���g���s���܂�
	def tangentC(self, *args):
		#���݃��X�g����Ă���A�C�e���Ń������o�[�����������܂�
		trigger = 'parentItemScrollList'
		self.lastScrollList(trigger)
		trigger = 'childrenItemScrollList'
		self.lastScrollList(trigger)	
		trigger = 'vectorItemScrollList'
		self.lastScrollList(trigger)		
		
		#�x�N�^�[�^�C�v���m�F���܂�
		objRotate = mc.optionMenu('tangentConstraintUpVector', q=True, select=True)
		upVectSet = ''
		if objRotate == 1:
			upVectSet = 'object'
		else:
			upVectSet = 'objectrotation'
		
		
		#����ƃ��X�g���擾���܂�		           
		constraintList = self.constraintDictReturn()
		vectorList = self.constraintVectorReturn()
		cList = constraintList.keys()
		
		#�G�C��������������߂܂�
		aimVect = mc.intFieldGrp('tangentConstraintAimVecto', q=True, v=True)
		#�G�C������up���������߂܂�
		upVect = mc.intFieldGrp('tangentConstraintUpVecto',q=True, v=True)
		
		#�R���X�g���C���g�m�[�h�����W���܂�		
		getConstraints = []		
		
		#�R���X�g���C���g��`���܂�
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
		#���X�g�����������܂�
		self.removeList(constraintList)		
		self.removeVectorList(vectorList)
		type = 'tan_'
		self.collectionGrp(getConstraints, type)
		
		#���X�g�̎c���𐔂��Ȃ����܂�
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
		#�x�N�^�[�����Ȃ���		
		#�x�N�^�[�����Ȃ���
		trigger = 'vectorItemScrollList'
		triggerInt = 'vectorAllNumber'
		selInt = 'vectorSelectNumber'
		self.counter(trigger, triggerInt, selInt)							
		
	
#�^���W�F���g�R���X�g���C���g���s���܂�
#�G�C���R���X�g���C���g���s���܂�
	def aimC(self, *args):
		#���݃��X�g����Ă���A�C�e���Ń������o�[�����������܂�
		trigger = 'parentItemScrollList'
		self.lastScrollList(trigger)
		trigger = 'childrenItemScrollList'
		self.lastScrollList(trigger)	
		trigger = 'vectorItemScrollList'
		self.lastScrollList(trigger)	
				
		#���C���X���m�F���܂�
		meinten = mc.checkBox('scaleConstraintMaintainCheck', q=True, value=True)
		
		#�x�N�^�[�^�C�v���m�F���܂�
		objRotate = mc.optionMenu('aimConstraintUpVector', q=True, select=True)
		upVectSet = ''
		if objRotate == 1:
			upVectSet = 'object'
		else:
			upVectSet = 'objectrotation'
		
		#�X�L�b�v���m�F���܂�
		cx,cy,cz = 'aimRxCheck', 'aimRyCheck', 'aimRzCheck'
		skipping = self.skipChannnelsReturn(cx,cy,cz)
		#����ƃ��X�g���擾���܂�		           
		constraintList = self.constraintDictReturn()
		vectorList = self.constraintVectorReturn()
		cList = constraintList.keys()
		
		#�G�C��������������߂܂�
		aimVect = mc.intFieldGrp('aimConstraintVectField', q=True, v=True)
		#�G�C������up���������߂܂�
		upVect = mc.intFieldGrp('aimUpConstraintVectField',q=True, v=True)
		
		#�R���X�g���C���g�m�[�h�����W���܂�		
		getConstraints = []		
		
		#�R���X�g���C���g��`���܂�
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
		#���X�g�����������܂�
		self.removeList(constraintList)		
		self.removeVectorList(vectorList)
		type = 'aim_'
		self.collectionGrp(getConstraints, type)
		
		#���X�g�̎c���𐔂��Ȃ����܂�
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
		#�x�N�^�[�����Ȃ���
		trigger = 'vectorItemScrollList'
		triggerInt = 'vectorAllNumber'
		selInt = 'vectorSelectNumber'
		self.counter(trigger, triggerInt, selInt)					
#�G�C���R���X�g���C���g���s���܂�
#���F�N�^�[�m�[�h���g�p�����R���X�g���C���g���s���܂�
#�R���X�g���C�����܂��@
###############################################################################################################################################################################################################
###############################################################################################################################################################################################################
#�X�i�b�v���s���܂�
#�y�A�����c�R���X�g���C���g���g�p�����X�i�b�v���s���܂�
	def parentSConst(self, *args):
		#���݃��X�g����Ă���A�C�e���Ń������o�[�����������܂�
		trigger = 'parentItemScrollList'
		self.lastScrollList(trigger)
		trigger = 'childrenItemScrollList'
		self.lastScrollList(trigger)	
		trigger = 'vectorItemScrollList'
		self.lastScrollList(trigger)
		
		#�R���X�g���C���g�������쐬���܂��B
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
		#�X�i�b�v��ɃR���X�g���C���g���폜���܂�
		mc.delete(getConstraints)
		#���X�g�����������܂�
		self.removeList(constraintList)		
		self.removeVectorList(vectorList)		
						
		#���X�g�̎c���𐔂��Ȃ����܂�
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
#�y�A�����c�R���X�g���C���g���g�p�����X�i�b�v���s���܂�
#�|�C���g�R���X�g���C���g���g�p�����X�i�b�v���s���܂�
	def pointSConst(self, *args):
		#���݃��X�g����Ă���A�C�e���Ń������o�[�����������܂�
		trigger = 'parentItemScrollList'
		self.lastScrollList(trigger)
		trigger = 'childrenItemScrollList'
		self.lastScrollList(trigger)	
		trigger = 'vectorItemScrollList'
		self.lastScrollList(trigger)
		
		#�R���X�g���C���g�������쐬���܂��B
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
		#�X�i�b�v��ɃR���X�g���C���g���폜���܂�
		mc.delete(getConstraints)
		#���X�g�����������܂�
		self.removeList(constraintList)		
		self.removeVectorList(vectorList)		
						
		#���X�g�̎c���𐔂��Ȃ����܂�
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
#�|�C���g�R���X�g���C���g���g�p�����X�i�b�v���s���܂�
#���[�e�[�g�R���X�g���C���g���g�p�����X�i�b�v���s���܂�
	def rotateSConst(self, *args):
		#���݃��X�g����Ă���A�C�e���Ń������o�[�����������܂�
		trigger = 'parentItemScrollList'
		self.lastScrollList(trigger)
		trigger = 'childrenItemScrollList'
		self.lastScrollList(trigger)	
		trigger = 'vectorItemScrollList'
		self.lastScrollList(trigger)
		
		#�R���X�g���C���g�������쐬���܂��B
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
		#�X�i�b�v��ɃR���X�g���C���g���폜���܂�
		mc.delete(getConstraints)
		#���X�g�����������܂�
		self.removeList(constraintList)		
		self.removeVectorList(vectorList)		
						
		#���X�g�̎c���𐔂��Ȃ����܂�
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
#���[�e�[�g�R���X�g���C���g���g�p�����X�i�b�v���s���܂�
#�X�P�[���R���X�g���C���g���g�p�����X�i�b�v���s���܂�
	def scaleSConst(self, *args):
		#���݃��X�g����Ă���A�C�e���Ń������o�[�����������܂�
		trigger = 'parentItemScrollList'
		self.lastScrollList(trigger)
		trigger = 'childrenItemScrollList'
		self.lastScrollList(trigger)	
		trigger = 'vectorItemScrollList'
		self.lastScrollList(trigger)
		
		#�R���X�g���C���g�������쐬���܂��B
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
		#�X�i�b�v��ɃR���X�g���C���g���폜���܂�
		mc.delete(getConstraints)
		#���X�g�����������܂�
		self.removeList(constraintList)		
		self.removeVectorList(vectorList)		
						
		#���X�g�̎c���𐔂��Ȃ����܂�
		triggerInt = 'parentAllNumber'
		selInt = 'parentSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
		triggerInt = 'childrenAllNumber'
		selInt = 'childrenSelectNumber'		
		self.counter(trigger, triggerInt, selInt)
#�X�P�[���R���X�g���C���g���g�p�����X�i�b�v���s���܂�
#���[�e�B���e�B�̃C���T�[�g���s���܂�


connector().createUI()
connector().windowResize()

#�蓮�ŃR���X�g���C���g���s���ꍇ�̃R�l�N�V�����̑g�ݕ�
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
