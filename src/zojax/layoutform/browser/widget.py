##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
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
"""

$Id$
"""
from zope import interface, component
from zope.component import getMultiAdapter
from z3c.form.interfaces import IWidget
from zojax.layout.interfaces import IPageletContext

import interfaces


class WidgetRenderer(object):

    def render(self):
        renderer = getMultiAdapter(
            (self.context,) + self.contexts + (self.request,),
            interfaces.IWidget, name=self.context.mode)

        renderer.update()
        return renderer.render()


@component.adapter(IWidget)
@interface.implementer(IPageletContext)
def getWidgetManager(widget):
    return widget.field, widget.form
