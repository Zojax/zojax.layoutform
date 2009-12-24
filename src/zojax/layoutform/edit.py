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
""" 

$Id$
"""
from zope import interface, event
from zope.traversing.browser import absoluteURL
from zope.app.container.interfaces import IAdding
from zope.app.container.interfaces import IWriteContainer
from zope.app.container.interfaces import IContainerNamesContainer

from z3c.form import form, button
from zojax.statusmessage.interfaces import IStatusMessage

from form import PageletForm
from interfaces import _, IPageletEditForm, ISaveButton


class PageletEditForm(form.EditForm, PageletForm):
    interface.implements(IPageletEditForm)

    render = PageletForm.render
    __call__ = PageletForm.__call__

    @button.buttonAndHandler(
        _(u'Save'), name='save', provides=ISaveButton)
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            IStatusMessage(self.request).add(
                (self.formErrorsMessage,) + errors, 'formError')
        else:
            changes = self.applyChanges(data)
            if changes:
                IStatusMessage(self.request).add(self.successMessage)
            else:
                IStatusMessage(self.request).add(self.noChangesMessage)

            nextURL = self.nextURL()
            if nextURL:
                self.redirect(nextURL)

    def nextURL(self):
        return ''
