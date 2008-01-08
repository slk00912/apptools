#------------------------------------------------------------------------------
# Copyright (c) 2005, Enthought, Inc.
# All rights reserved.
# 
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
# 
# Author: Enthought, Inc.
# Description: <Enthought resource package component>
#------------------------------------------------------------------------------
""" Returns a resource path based on the call stack.

This type of resource path is normally requested from the constructor for an
object whose resources are relative to the module constructing the object.
"""

# Standard library imports.
import sys

from os.path import dirname, exists
from os      import getcwd
    
def resource_path ( level = 2 ):
    """Returns a resource path calculated from the caller's stack.
    """
    module = sys._getframe( level ).f_globals.get( '__name__', '__main__' )
    
    if module != '__main__':
        # Return the path to the module:
        try:
            return dirname( getattr( sys.modules.get( module ), '__file__' ) )
        except:
            # Apparently 'module' is not a registered module...treat it like 
            # '__main__':
            pass
        
    # '__main__' is not a real module, so we need a work around:
    for path in [ dirname( sys.argv[0] ), getcwd() ]:
        if exists( path ):
            break
            
    return path
    
#### EOF ######################################################################
