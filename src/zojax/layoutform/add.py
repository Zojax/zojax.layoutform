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
from zope.traversing.browser import absoluteURL
from zope.app.container.interfaces import IAdding
from zope.app.container.interfaces import IWriteContainer
from zope.app.container.interfaces import IContainerNamesContainer

from z3c.form import form, button
from zojax.statusmessage.interfaces import IStatusMessage

from form import PageletForm
from interfaces import _, IPageletAddForm, IAddButton, ICancelButton

from zope.proxy import removeAllProxies


class PageletAddForm(form.AddForm, PageletForm):
    interface.implements(IPageletAddForm)

    render = PageletForm.render
    __call__ = PageletForm.__call__

    _addedObject = None

    formCancelMessage = _(u'Action has been canceled.')

    @button.buttonAndHandler(_(u'Add'), name='add', provides=IAddButton)
    def handleAdd(self, action):
        data, errors = self.extractData()

        if errors:
            IStatusMessage(self.request).add(
                (self.formErrorsMessage,) + errors, 'formError')
        else:
            obj = self.createAndAdd(data)

            if obj is not None:
                self._addedObject = obj
                self._finishedAdd = True
                self.redirect(self.nextURL())

    @button.buttonAndHandler(
        _(u'Cancel'), name='cancel', provides=ICancelButton)
    def handleCancel(self, action):
        self._finishedAdd = True
        self.redirect(self.cancelURL())
        IStatusMessage(self.request).add(self.formCancelMessage)

    def createAndAdd(self, data):
        obj = self.create(data)
        addedObj = self.add(obj)
        if addedObj is not None:
            return addedObj
        return obj

    def nextURL(self):
        if self._addedObject is None:
            url = absoluteURL(self.context, self.request)
        else:
            url = absoluteURL(self._addedObject, self.request)

        return '%s/@@SelectedManagementView.html'%url

    def cancelURL(self):
        context = self.context

        if IAdding.providedBy(context):
            url = absoluteURL(context.context, self.request)
        else:
            url = absoluteURL(context, self.request)

        return '%s/@@SelectedManagementView.html'%url

    def nameAllowed(self):
        """Return whether names can be input by the user."""
        context = self.context

        if IAdding.providedBy(context):
            context = context.context

        if IWriteContainer.providedBy(context):
            return not IContainerNamesContainer.providedBy(context)
        else:
            return False
