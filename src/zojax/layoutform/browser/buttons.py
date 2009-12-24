##############################################################################
#
# Copyright (c) 2008 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
""" Castom Button Widget Implementation

$Id$
"""
__docformat__ = "reStructuredText"
from zope import interface, component

from z3c.form import interfaces, widget, action, button

from zojax.layoutform.interfaces import \
    IAddButton, ISaveButton, ICancelButton, ILayoutFormLayer


class ButtonAction(button.ButtonAction):
    interface.implements(interfaces.IButtonAction)
    component.adapts(ILayoutFormLayer, interfaces.IButton)

    klass="z-form-button"


class AddButtonAction(button.ButtonAction):
    interface.implements(interfaces.IButtonAction)
    component.adapts(ILayoutFormLayer, IAddButton)

    klass="z-form-addbutton"


class SaveButtonAction(button.ButtonAction):
    interface.implements(interfaces.IButtonAction)
    component.adapts(ILayoutFormLayer, ISaveButton)

    klass="z-form-savebutton"


class CancelButtonAction(button.ButtonAction):
    interface.implements(interfaces.IButtonAction)
    component.adapts(ILayoutFormLayer, ICancelButton)

    klass="z-form-cancelbutton"
