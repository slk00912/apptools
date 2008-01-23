#------------------------------------------------------------------------------
# Copyright (c) 2008, Riverbank Computing Limited
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
#
# Author: Riverbank Computing Limited
# Description: <Enthought permissions package component>
#------------------------------------------------------------------------------


# Enthought library imports.
from enthought.pyface.action.api import Action
from enthought.traits.api import HasTraits, implements, Instance, List

# Local imports.
from enthought.permissions.i_policy_manager import IPolicyManager
from enthought.permissions.permission import Permission
from enthought.permissions.permissions_manager import PermissionsManager
from enthought.permissions.secure_proxy import SecureProxy
from i_policy_storage import IPolicyStorage
from role_definition import role_definition


class PolicyManager(HasTraits):
    """The default policy manager implementation.  This policy enforces the use
    of roles.  Permissions are associated with roles rather than directly with
    users.  Users are then associated with one or more roles."""

    implements(IPolicyManager)

    #### 'IPolicyManager' interface ###########################################

    management_actions = List(Instance(Action))

    user_permissions = List(Instance(Permission))

    #### 'PolicyManager' interface ############################################

    # The policy data storage.
    policy_storage = Instance(IPolicyStorage)

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, **traits):
        """Initialise the object."""

        super(PolicyManager, self).__init__(**traits)

        # Load the user permissions when they become authenticated.
        PermissionsManager.user_manager.on_trait_event(self._load_user_perms,
                'user_authenticated')

    ###########################################################################
    # 'IPolicyManager' interface.
    ###########################################################################

    def bootstrapping(self):
        """Return True if we are bootstrapping, ie. no roles have been defined
        or assigned."""

        try:
            bootstrap = self.policy_storage.is_empty()
        except UserStorageError:
            # Suppress the error and assume it isn't empty.
            bootstrap = False

        return bootstrap

    ###########################################################################
    # Trait handlers.
    ###########################################################################

    def _management_actions_default(self):
        """Return the management actions to manage the policy."""

        actions = []

        perm = Permission(name='ets.permissions.management.define_roles',
                description=u"Define roles", bootstrap=True)
        act = Action(name='&Role Definitions...',
                on_perform=lambda: role_definition(self))

        actions.append(SecureProxy(act, permissions=[perm], show=False))

        perm = Permission(name='ets.permissions.management.assign_roles',
                description=u"Assignment Roles", bootstrap=True)
        act = Action(name='&Role Assignments...', on_perform=self._assign_role)

        actions.append(SecureProxy(act, permissions=[perm], show=False))

        return actions

    def _policy_storage_default(self):
        """Return the default storage for the policy data."""

        from pickled_policy_storage import PickledPolicyStorage

        return PickledPolicyStorage()

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _load_user_perms(self, user):
        """Invoked when the user's authentication state changes."""

        # FIXME
        print "ZZZZZZZZZZZZZZZ", user

    def _assign_role(self):
        """Assign the roles."""

        from enthought.pyface.api import information

        information(None, "This will eventually implement a TraitsUI based GUI for assigning roles.")