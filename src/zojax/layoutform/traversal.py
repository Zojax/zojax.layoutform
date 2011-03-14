from zope.interface import implements
from zope.interface import alsoProvides
from zope.interface import noLongerProvides
from zope.component import adapts

from zope.traversing.interfaces import ITraversable
from zope.traversing.interfaces import TraversalError

from zope.publisher.interfaces.browser import IBrowserRequest

from z3c.form.interfaces import IForm


class FormWidgetTraversal(object):
    """Allow traversal to widgets via the ++widget++ namespace. The context
    is the from itself (used when the layout wrapper view is not used).
    
    Note that to support security in Zope 2.10, the widget being traversed to
    must have an __of__ method, i.e. it must support acquisition. The easiest
    way to do that, is to mix in Acquisition.Explicit. The acquisition parent
    will be the layout form wrapper view.
    
    In Zope 2.12, this is not necessary, because we also set the __parent__
    pointer of the returned widget to be the traversal context.
    
    Unfortunately, if you mix in Acquisition.Explicit in Zope 2.12 *and* the
    class implements IAcquirer, Zope may complain because the view probably
    does *not* implement acquisition (in Zope 2.12, views no longer mix in
    Acquisiton.Explicit). To support both Zope 2.10 and Zope 2.12, you will
    need to cheat and mix in Acquisition.Explicit, but use implementsOnly()
    or some other mechanism to make sure the instance does not provide
    IAcquirer.
    """
    
    implements(ITraversable)
    adapts(IForm, IBrowserRequest)
    
    def __init__(self, context, request=None):
        self.context = context
        self.request = request
    
    def _prepareForm(self):
        return self.context
    
    def traverse(self, name, ignored):
        
        form = self._prepareForm()

        # Since we cannot check security during traversal,
        # we delegate the check to the widget view.
        form.update()
        
        # Find the widget - it may be in a group
        widget = None
        if name in form.widgets:
            widget = form.widgets.get(name)
        elif getattr(form, 'groups', None) is not None:
            for group in form.groups:
                if name in group.widgets:
                    widget = group.widgets.get(name)
        
        # Make the parent of the widget the traversal parent.
        # This is required for security to work in Zope 2.12
        print widget
        if widget is not None:
            widget.__parent__ = self.context
            return widget
        
        raise TraversalError(name)