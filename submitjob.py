#! /usr/bin/env python2
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

import sys
from auth import Auth
from printer import Printer

if len(sys.argv) == 2 and sys.argv[1] == 'version':
    # line below is replaced on commit
    CCPVersion = "20131017 220257"
    print "CUPS Cloud Print Submit Job Version " + CCPVersion
    sys.exit(0)
    
if ( len(sys.argv) < 6 ):
  sys.stderr.write("ERROR: Usage: " + sys.argv[0] + " pdf-file page-title printer-uri cups-printer-name options\n")
  sys.exit(1)

requestors, storage = Auth.SetupAuth(False)
printer = Printer(requestors)

printerid, requestor = printer.getPrinterIDByURI(sys.argv[3])
printer.requestor = requestor
if printerid == None:
  print("ERROR: Printer '" + sys.argv[3] + "' not found")
  sys.exit(1)

if printer.submitJob(printerid, 'pdf', sys.argv[1], sys.argv[2], sys.argv[4], sys.argv[5] ):
  print("INFO: Successfully printed")
  sys.exit(0)
else:
  print("ERROR: Failed to submit job to cloud print")
  sys.exit(1)
