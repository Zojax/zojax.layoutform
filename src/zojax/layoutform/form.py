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
from zope.component import getAdapters
from zope.component import getMultiAdapter, queryMultiAdapter
from zope.pagetemplate.interfaces import IPageTemplate

from z3c.form import form, util
from z3c.form.interfaces import IForm, IGroup, ISubForm

from zojax.layout.interfaces import IPagelet
from zojax.layout.pagelet import BrowserPagelet

from interfaces import _
from interfaces import IFormWrapper, IForms
from interfaces import IPageletForm, IPageletSubform
from interfaces import IPageletDisplayForm, IPageletFormView


class Views(util.SelectionManager):
    """Forms manager."""
    interface.implements(IForms)
    managerInterface = IForms

    def __init__(self, *args, **kw):
        super(Views, self).__init__()
        for view in args:
            self._data_values.append(view)
            self._data_keys.append(view.__name__)
            self._data[view.__name__] = view

    def __iter__(self):
        return iter(self._data_values)


class PageletBaseForm(form.BaseForm, BrowserPagelet):

    __call__ = BrowserPagelet.__call__

    def render(self):
        if self.template is not None:
            return self.template()
        else:
            view = queryMultiAdapter((self, self.request), IPageletFormView)
            if view is not None:
                view.update()
                return view.render()

        raise LookupError("Can't find IPageletFormView view for this form.")


class PageletForm(form.Form, PageletBaseForm):
    interface.implements(IPageletForm)

    label = u''
    description = u''

    forms = ()
    groups = ()
    subforms = ()
    views = ()

    render = PageletBaseForm.render
    __call__ = PageletBaseForm.__call__

    successMessage = _('Data successfully updated.')
    noChangesMessage = _('No changes were applied.')
    formErrorsMessage = _(u'Please fix indicated errors.')

    def extractData(self, setErrors=True):
        data, errors = super(PageletForm, self).extractData(setErrors=setErrors)
        for form in self.groups:
            formData, formErrors = form.extractData(setErrors=setErrors)
            data.update(formData)
            if formErrors:
                errors += formErrors

        for form in self.subforms:
            try:
                formData, formErrors = form.extractData(setErrors=setErrors)
            except Exception, e:
                raise Exception('Error', (form, e))
            if formErrors:
                errors += formErrors

        return data, errors

    def _loadSubforms(self):
        return [(name, form) for name, form in
                getAdapters((self.context,self,self.request), IPageletSubform)]

    def updateForms(self):
        wrapped = IFormWrapper.providedBy(self)

        forms = []
        groups = []
        subforms = []
        views = []
        for name, form in self._loadSubforms():
            form.__name__ = name
            form.update()
            if not form.isAvailable():
                continue

            if IGroup.providedBy(form):
                groups.append((form.weight, form.__name__, form))
            elif ISubForm.providedBy(form):
                subforms.append((form.weight, form.__name__, form))
            elif IPageletForm.providedBy(form):
                if wrapped:
                    interface.alsoProvides(form, IFormWrapper)
                forms.append((form.weight, form.__name__, form))
            else:
                views.append((form.weight, form.__name__, form))

        groups.sort()
        self.groups = Views(*[form for weight, name, form in groups])

        subforms.sort()
        self.subforms = Views(*[form for weight, name, form in subforms])

        forms.sort()
        self.forms = Views(*[form for weight, name, form in forms])

        views.sort()
        self.views = Views(*[view for weight, name, view in views])

    def update(self):
        self.updateWidgets()
        self.updateActions()
        self.updateForms()

        if not IPageletSubform.providedBy(self):
            self.actions.execute()

            for form in self.groups:
                form.postUpdate()
            for form in self.subforms:
                form.postUpdate()
            for form in self.forms:
                form.postUpdate()

    def postUpdate(self):
        for form in self.groups:
            form.postUpdate()
        for form in self.subforms:
            form.postUpdate()
        for form in self.forms:
            form.postUpdate()

        self.actions.execute()


class PageletDisplayForm(PageletForm, form.DisplayForm):
    interface.implements(IPageletDisplayForm)

    render = PageletForm.render
    __call__ = PageletForm.__call__
