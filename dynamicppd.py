#! /usr/bin/env python2
#    CUPS Cloudprint - Print via Google Cloud Print                          
#    Copyright (C) 2013 Simon Cadman
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

def showUsage():
    sys.stderr.write("ERROR: Usage: " + sys.argv[0] + " [list|cat drivername]\n")
    sys.exit(1)
        
requestors, storage = Auth.SetupAuth(False)
printer = Printer(requestors)
printers = printer.getPrinters(True)
if printers == None:
    print("ERROR: No Printers Found")
    sys.exit(1)

if ( len(sys.argv) < 2 ):
    showUsage()

if sys.argv[1] == 'list':
    for foundprinter in printers:
        print('"cupscloudprint:' + foundprinter['name'].encode('ascii', 'replace').replace(' ', '-') + '.ppd" en "Google" "' + foundprinter['name'].encode('ascii', 'replace') + ' (' + foundprinter['account'] + ')" "DRV:GCP;"')
        
elif sys.argv[1] == 'cat':
    if len(sys.argv) == 2 or sys.argv[2] == "":
        showUsage()
    else:
        ppdname = sys.argv[2]
        # find printer
        for foundprinter in printers:
            if ppdname == 'cupscloudprint:'+ foundprinter['name'].encode('ascii', 'replace').replace(' ', '-') + '.ppd':
                capabilities = []
                # generate and output ppd
                ppddetails = """*PPD-Adobe: "4.3"
*%%%% PPD file for Cloud Print with CUPS.
*%%%% Created by the CUPS PPD Compiler CUPS v1.6.1.
*FormatVersion: "4.3"
*FileVersion: "1.0"
*LanguageVersion: English
*LanguageEncoding: ISOLatin1
*PCFileName: "cloudprint.ppd"
*Product: "(Google Cloud Print)"
*Manufacturer: "Google"
*ModelName: "Google Cloud Print"
*ShortNickName: "Google Cloud Print"
*NickName: "Google Cloud Print, 1.0"
*PSVersion: "(1) 0"
*LanguageLevel: "3"
*ColorDevice: True
*DefaultColorSpace: RGB
*FileSystem: False
*Throughput: "1"
*LandscapeOrientation: Minus90
*TTRasterizer: Type42
*% Driver-defined attributes...
*1284DeviceID: "MFG:Google;MDL:Cloud Print;DES:GoogleCloudPrint;"
*cupsLanguages: "en"
*OpenUI *PageSize/Media Size: PickOne
*OrderDependency: 10 AnySetup *PageSize
*DefaultPageSize: Letter
*PageSize Letter/US Letter: "<</PageSize[612 792]/ImagingBBox null>>setpagedevice"
*PageSize Legal/US Legal: "<</PageSize[612 1008]/ImagingBBox null>>setpagedevice"
*PageSize A4/A4: "<</PageSize[595 842]/ImagingBBox null>>setpagedevice"
*CloseUI: *PageSize
*OpenUI *PageRegion/Media Size: PickOne
*OrderDependency: 10 AnySetup *PageRegion
*DefaultPageRegion: Letter
*PageRegion Letter/US Letter: "<</PageSize[612 792]/ImagingBBox null>>setpagedevice"
*PageRegion Legal/US Legal: "<</PageSize[612 1008]/ImagingBBox null>>setpagedevice"
*PageRegion A4/A4: "<</PageSize[595 842]/ImagingBBox null>>setpagedevice"
*CloseUI: *PageRegion
*DefaultImageableArea: Letter
*ImageableArea Letter/US Letter: "0 0 612 792"
*ImageableArea Legal/US Legal: "0 0 612 1008"
*ImageableArea A4/A4: "0 0 595 842"
*DefaultPaperDimension: Letter
*PaperDimension Letter/US Letter: "612 792"
*PaperDimension Legal/US Legal: "612 1008"
*PaperDimension A4/A4: "595 842"
*OpenUI *ColorModel/Color Mode: PickOne
*OrderDependency: 10 AnySetup *ColorModel
*DefaultColorModel: RGB
*ColorModel Gray/Grayscale: "<</cupsColorSpace 0/cupsColorOrder 0/cupsCompression 0>>setpagedevice"
*ColorModel RGB/Color: "<</cupsColorSpace 1/cupsColorOrder 0/cupsCompression 0>>setpagedevice"
*ColorModel CMYK/CMYK: "<</cupsColorSpace 6/cupsColorOrder 0/cupsCompression 0>>setpagedevice"
*CloseUI: *ColorModel
"""

                #print foundprinter['fulldetails']
                if 'capabilities' in foundprinter['fulldetails']:
                    for capability in foundprinter['fulldetails']['capabilities']:
                        if capability['type'] == 'Feature':
                            ppddetails += '*OpenUI *' + capability['name'].replace(':','_') + '/' + capability['displayName'] +': PickOne' + "\n"
                            for option in capability['options']:
                                ppddetails += '*' + capability['name'].replace(':','_') + ': ' + option['displayName'] + ' "' + option['name'] + '"' + "\n"
                            ppddetails += '*CloseUI: *' + capability['displayName'] + "\n"
                        elif capability['type'] == 'ParameterDef':
                            pass
                            #print option['displayName']
                            #print capability['psf:MinValue'], capability['psf:MaxValue']
                        
                ppddetails += """*DefaultFont: Courier
*Font AvantGarde-Book: Standard "(1.05)" Standard ROM
*Font AvantGarde-BookOblique: Standard "(1.05)" Standard ROM
*Font AvantGarde-Demi: Standard "(1.05)" Standard ROM
*Font AvantGarde-DemiOblique: Standard "(1.05)" Standard ROM
*Font Bookman-Demi: Standard "(1.05)" Standard ROM
*Font Bookman-DemiItalic: Standard "(1.05)" Standard ROM
*Font Bookman-Light: Standard "(1.05)" Standard ROM
*Font Bookman-LightItalic: Standard "(1.05)" Standard ROM
*Font Courier: Standard "(1.05)" Standard ROM
*Font Courier-Bold: Standard "(1.05)" Standard ROM
*Font Courier-BoldOblique: Standard "(1.05)" Standard ROM
*Font Courier-Oblique: Standard "(1.05)" Standard ROM
*Font Helvetica: Standard "(1.05)" Standard ROM
*Font Helvetica-Bold: Standard "(1.05)" Standard ROM
*Font Helvetica-BoldOblique: Standard "(1.05)" Standard ROM
*Font Helvetica-Narrow: Standard "(1.05)" Standard ROM
*Font Helvetica-Narrow-Bold: Standard "(1.05)" Standard ROM
*Font Helvetica-Narrow-BoldOblique: Standard "(1.05)" Standard ROM
*Font Helvetica-Narrow-Oblique: Standard "(1.05)" Standard ROM
*Font Helvetica-Oblique: Standard "(1.05)" Standard ROM
*Font NewCenturySchlbk-Bold: Standard "(1.05)" Standard ROM
*Font NewCenturySchlbk-BoldItalic: Standard "(1.05)" Standard ROM
*Font NewCenturySchlbk-Italic: Standard "(1.05)" Standard ROM
*Font NewCenturySchlbk-Roman: Standard "(1.05)" Standard ROM
*Font Palatino-Bold: Standard "(1.05)" Standard ROM
*Font Palatino-BoldItalic: Standard "(1.05)" Standard ROM
*Font Palatino-Italic: Standard "(1.05)" Standard ROM
*Font Palatino-Roman: Standard "(1.05)" Standard ROM
*Font Symbol: Special "(001.005)" Special ROM
*Font Times-Bold: Standard "(1.05)" Standard ROM
*Font Times-BoldItalic: Standard "(1.05)" Standard ROM
*Font Times-Italic: Standard "(1.05)" Standard ROM
*Font Times-Roman: Standard "(1.05)" Standard ROM
*Font ZapfChancery-MediumItalic: Standard "(1.05)" Standard ROM
*Font ZapfDingbats: Special "(001.005)" Special ROM
*% End of cloudprint.ppd, 04169 bytes."""
                print ppddetails
                sys.exit(0)
                
        # no printers found
        print("ERROR: PPD " + ppdname +" Not Found")
        sys.exit(1)