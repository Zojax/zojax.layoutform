##############################################################################
#
# Copyright (c) 2007 Zope Foundation and Contributors.
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
"""Support for Layout Templates

$Id$
"""
from zope import interface
from zope.component import getMultiAdapter, queryMultiAdapter
from zope.pagetemplate.interfaces import IPageTemplate

from z3c.form import form
from zojax.layout.interfaces import IPagelet
from zojax.layout.pagelet import BrowserPagelet

from interfaces import IPageletForm, IPageletDisplayForm, IPageletFormView


class PageletForm(form.Form, BrowserPagelet):
    interface.implements(IPageletForm)

    __call__ = BrowserPagelet.__call__

    def render(self):
        # render content template 
        if self.template is None:
            view = queryMultiAdapter((self, self.request), IPageletFormView)
            if view is not None:
                view.update()
                return view.render()

            template = getMultiAdapter((self, self.request), IPageTemplate)
            return template(self)

        return self.template()


class PageletDisplayForm(form.DisplayForm, PageletForm):
    interface.implements(IPageletDisplayForm)

    render = PageletForm.render
    __call__ = PageletForm.__call__
