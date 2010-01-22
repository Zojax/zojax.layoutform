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
from zope.component import queryMultiAdapter
from zope.traversing.browser import absoluteURL
from zope.lifecycleevent import Attributes, ObjectModifiedEvent

from z3c.form import subform, button
from z3c.form.interfaces import ISubForm, IActionHandler

from zojax.statusmessage.interfaces import IStatusMessage

from utils import applyChanges
from form import PageletBaseForm
from interfaces import _, IPageletEditSubForm, IPageletSubform, ISaveAction, \
                          IPageletAddSubForm, IAddAction




class PageletEditSubForm(subform.EditSubForm, PageletBaseForm):
    interface.implements(IPageletEditSubForm)

    label = u''
    description = u''
    changesApplied = False

    render = PageletBaseForm.render
    __call__ = PageletBaseForm.__call__

    def __init__(self, context, parentForm, request):
        super(PageletEditSubForm, self).__init__(context, request, parentForm)

    def applyChanges(self, data):
        return applyChanges(self, self.getContent(), data)

    @button.handler(ISaveAction)
    def handleApply(self, action):
        data, errors = self.extractData()

        if not errors:
            changes = self.applyChanges(data)
            if changes:
                descriptions = []
                for interface, names in changes.items():
                    descriptions.append(Attributes(interface, *names))

                self.changesApplied = True
                event.notify(
                    ObjectModifiedEvent(self.getContent(), *descriptions))

    def executeActions(self, form):
        request = self.request
        content = self.getContent()

        if hasattr(form, 'actions'):
            for action in form.actions.executedActions:
                adapter = queryMultiAdapter(
                    (self, request, content, action), IActionHandler)
                if adapter:
                    adapter()

        if ISubForm.providedBy(form):
            self.executeActions(form.parentForm)

        elif IPageletSubform.providedBy(form) and form.managers:
            self.executeActions(form.managers[0])

    def update(self):
        self.updateWidgets()

        if not IPageletSubform.providedBy(self):
            self.executeActions(self.parentForm)

    def isAvailable(self):
        return True

    def postUpdate(self):
        self.executeActions(self.parentForm)


class PageletAddSubForm(PageletEditSubForm):
    interface.implements(IPageletAddSubForm)

    @button.handler(IAddAction)
    def handleApply(self, action):
        data, errors = self.extractData()
        if not errors:
            changes = self.applyChanges(data)
            if changes:
                descriptions = []
                for interface, names in changes.items():
                    descriptions.append(Attributes(interface, *names))

                self.changesApplied = True
                event.notify(
                    ObjectModifiedEvent(self.getContent(), *descriptions))