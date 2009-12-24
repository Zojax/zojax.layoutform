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
from zope import interface


class IForm(interface.Interface):
    """ form view """


class IViewspace(interface.Interface):
    """ form viewspace """


class IExtraViewspaceInfo(interface.Interface):
    """ extra widget information """


class IWidget(interface.Interface):
    """ widget view """


class IFormButtons(interface.Interface):
    """ form buttons """


class IErrorView(interface.Interface):
    """ Error view snippet view """
