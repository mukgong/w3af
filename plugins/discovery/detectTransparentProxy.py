'''
detectTransparentProxy.py

Copyright 2006 Andres Riancho

This file is part of w3af, w3af.sourceforge.net .

w3af is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

w3af is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with w3af; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

'''

import core.controllers.outputManager as om

# options
from core.data.options.option import option
from core.data.options.optionList import optionList

from core.controllers.basePlugin.baseDiscoveryPlugin import baseDiscoveryPlugin
from core.controllers.w3afException import w3afRunOnce
from core.controllers.w3afException import w3afException

import core.data.kb.knowledgeBase as kb
import core.data.kb.info as info

import socket


class detectTransparentProxy(baseDiscoveryPlugin):
    '''
    Find out if your ISP has a transparent proxy installed.
    @author: Andres Riancho ( andres.riancho@gmail.com )
    '''
    
    def __init__(self):
        baseDiscoveryPlugin.__init__(self)
        self._run = True
        
    def discover(self, fuzzableRequest ):
        '''
        @parameter fuzzableRequest: A fuzzableRequest instance that contains (among other things) the URL to test.
        '''
        if not self._run:
            # This will remove the plugin from the discovery plugins to be run.
            raise w3afRunOnce()
        else:
            # I will only run this one time. All calls to detectTransparentProxy
            # return the same url's
            self._run = False
            
            if self._is_proxyed_conn( fuzzableRequest ):
                i = info.info()
                i.setPluginName(self.getName())
                i.setName( 'Transparent proxy detected' )
                i.setURL( fuzzableRequest.getURL() )
                msg = 'Your ISP seems to have a transparent proxy installed, this can influence'
                msg += ' w3af results.'
                i.setDesc( msg )
                kb.kb.append( self, 'detectTransparentProxy', i )
                om.out.information( i.getDesc() )
            else:
                om.out.information( 'Your ISP has no transparent proxy.' )
            
        return []
    
    def _is_proxyed_conn( self, fuzzableRequest ):
        '''
        Make a connection to a "random" IP to port 80 and make a request for the URL we are interested in.
        @return: True if proxy is present.
        '''
        random_ips = [ '1.2.3.4', '5.6.7.8', '9.8.7.6', '1.2.1.2', '1.0.0.1', \
        '60.60.60.60', '44.44.44.44', '11.22.33.44', '11.22.33.11', '7.99.7.99',\
        '87.78.87.78']
        
        for ip_address in random_ips:
            sock_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                sock_obj.connect( ( ip_address , 80) )
            except:
                return False
            else:
                continue
                
        return True

    def getOptions( self ):
        '''
        @return: A list of option objects for this plugin.
        '''    
        ol = optionList()
        return ol

    def setOptions( self, OptionList ):
        '''
        This method sets all the options that are configured using the user interface 
        generated by the framework using the result of getOptions().
        
        @parameter OptionList: A dictionary with the options for the plugin.
        @return: No value is returned.
        ''' 
        pass
        
    def getPluginDeps( self ):
        '''
        @return: A list with the names of the plugins that should be run before the
        current one.
        '''
        return []

    def getLongDesc( self ):
        '''
        @return: A DETAILED description of the plugin functions and features.
        '''
        return '''
        This plugin tries to detect transparent proxies.
        
        The procedure for detecting transparent proxies is simple, I try to connect to a series of IP
        addresses, to the port 80, if all of them return an opened socket, then it's the proxy server
        responding.
        '''
