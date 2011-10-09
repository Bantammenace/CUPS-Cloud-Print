#    CUPS Cloudprint - Print via Google Cloud Print                          
#    Copyright (C) 2011 Simon Cadman
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License    
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import ConfigParser, os, pickle

class Config():
  
  configfile = "/etc/cloudprint.conf"
  
  def __init__( self ):
    self.config = ConfigParser.ConfigParser()
    self.config.readfp( open(self.configfile) )
    # verify we have needed params
    self.config.get("Google", "Username")
    self.config.get("Google", "Password")
    
  def get ( self, section, key ):
    return self.config.get(section, key)

  def save (self ):
    with open(self.configfile, 'wb') as configdetail:
      self.config.write(configdetail)
