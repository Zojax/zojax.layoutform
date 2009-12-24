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
from zope import interface, event
from zope.traversing.browser import absoluteURL
from zope.app.container.interfaces import IAdding
from zope.app.container.interfaces import IWriteContainer
from zope.app.container.interfaces import IContainerNamesContainer

from z3c.form import form, button
from zojax.statusmessage.interfaces import IStatusMessage

from form import PageletForm
from interfaces import _, IPageletEditForm, ISaveAction


class PageletEditForm(PageletForm, form.EditForm):
    interface.implements(IPageletEditForm)

    @button.buttonAndHandler(_(u'Save'), name='save', provides=ISaveAction)
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
                changed = False
                for subform in self.subforms:
                    if subform.changesApplied:
                        IStatusMessage(self.request).add(self.successMessage)
                        self.changed = True
                        break

                if not changed:
                    IStatusMessage(self.request).add(self.noChangesMessage)

            nextURL = self.nextURL()
            if nextURL:
                self.redirect(nextURL)

    def nextURL(self):
        return ''
