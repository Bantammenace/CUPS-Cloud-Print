#! /usr/bin/python
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

import mimetools, base64, time, httplib, logging, urllib, urllib2, string, mimetypes, sys, os, json
from config import Config
from auth import Auth

try:
  configuration = Config()
except IOError:
  print "ERROR: Unable to load configuration from", Config.configfile,", create one from cloudprint.conf.example"
  sys.exit(1)
except Exception as error:
  print "ERROR: Unknown error when reading configuration file - ", error
  sys.exit(1)

email = configuration.get("Google", "Username")
password = configuration.get("Google", "Password")

CRLF = '\r\n'
BOUNDARY = mimetools.choose_boundary()

# The following are used for authentication functions.
FOLLOWUP_HOST = 'www.google.com/cloudprint'
FOLLOWUP_URI = 'select%2Fgaiaauth'
GAIA_HOST = 'www.google.com'
LOGIN_URI = '/accounts/ServiceLoginAuth'

# The following are used for general backend access.
CLOUDPRINT_URL = 'http://www.google.com/cloudprint'

logger = logging


def ReadFile(pathname):
  """Read contents of a file and return content.

  Args:
    pathname: string, (path)name of file.
  Returns:
    string: contents of file.
  """
  try:
    f = open(pathname, 'rb')
    try:
      s = f.read()
    except IOError, e:
      logger('Error reading %s\n%s', pathname, e)
    finally:
      f.close()
      return s
  except IOError, e:
    logger.error('Error opening %s\n%s', pathname, e)
    return None

def WriteFile(file_name, data):
  """Write contents of data to a file_name.

  Args:
    file_name: string, (path)name of file.
    data: string, contents to write to file.
  Returns:
    boolean: True = success, False = errors.
  """
  status = True

  try:
    f = open(file_name, 'wb')
    try:
      f.write(data)
    except IOError, e:
      logger.error('Error writing %s\n%s', file_name, e)
      status = False
    finally:
      f.close()
  except IOError, e:
    logger.error('Error opening %s\n%s', file_name, e)
    status = False

  return status

def Base64Encode(pathname):
  """Convert a file to a base64 encoded file.

  Args:
    pathname: path name of file to base64 encode..
  Returns:
    string, name of base64 encoded file.
  For more info on data urls, see:
    http://en.wikipedia.org/wiki/Data_URI_scheme
  """
  b64_pathname = pathname + '.b64'
  file_type = mimetypes.guess_type(pathname)[0] or 'application/octet-stream'
  data = ReadFile(pathname)

  # Convert binary data to base64 encoded data.
  header = 'data:%s;base64,' % file_type
  b64data = header + base64.b64encode(data)

  if WriteFile(b64_pathname, b64data):
    return b64_pathname
  else:
    return None


tokens = Auth.GetAuthTokens(email, password)
if tokens == None:
  print "ERROR: Invalid username/password"
  sys.exit(1)


def EncodeMultiPart(fields, files, file_type='application/xml'):
    """Encodes list of parameters and files for HTTP multipart format.

    Args:
      fields: list of tuples containing name and value of parameters.
      files: list of tuples containing param name, filename, and file contents.
      file_type: string if file type different than application/xml.
    Returns:
      A string to be sent as data for the HTTP post request.
    """
    lines = []
    for (key, value) in fields:
      lines.append('--' + BOUNDARY)
      lines.append('Content-Disposition: form-data; name="%s"' % key)
      lines.append('')  # blank line
      lines.append(value)
    for (key, filename, value) in files:
      lines.append('--' + BOUNDARY)
      lines.append(
          'Content-Disposition: form-data; name="%s"; filename="%s"'
          % (key, filename))
      lines.append('Content-Type: %s' % file_type)
      lines.append('')  # blank line
      lines.append(value)
    lines.append('--' + BOUNDARY + '--')
    lines.append('')  # blank line
    return CRLF.join(lines)
    
    
def SubmitJob(printerid, jobtype, jobsrc, jobname):
  """Submit a job to printerid with content of dataUrl.

  Args:
    printerid: string, the printer id to submit the job to.
    jobtype: string, must match the dictionary keys in content and content_type.
    jobsrc: string, points to source for job. Could be a pathname or id string.
  Returns:
    boolean: True = submitted, False = errors.
  """
  if jobtype == 'pdf':
    
    if not os.path.exists(jobsrc):
      print "ERROR: PDF doesnt exist"
      return False
    b64file = Base64Encode(jobsrc)
    fdata = ReadFile(b64file)
    os.unlink(b64file)
    hsid = True
  elif jobtype in ['png', 'jpeg']:
    fdata = ReadFile(jobsrc)
  else:
    fdata = None

  title = jobname
  content = {'pdf': fdata,
             'jpeg': jobsrc,
             'png': jobsrc,
            }
  content_type = {'pdf': 'dataUrl',
                  'jpeg': 'image/jpeg',
                  'png': 'image/png',
                 }
  headers = [('printerid', printerid),
             ('title', title),
             ('content', content[jobtype]),
             ('contentType', content_type[jobtype])]
  files = [('capabilities', 'capabilities', '{"capabilities":[]}')]
  if jobtype in ['pdf', 'jpeg', 'png']:
    edata = EncodeMultiPart(headers, files, file_type=content_type[jobtype])
  else:
    edata = EncodeMultiPart(headers, files)

  response = GetUrl('%s/submit' % CLOUDPRINT_URL, tokens, data=edata,
                    cookies=False)
  try:
    responseobj = json.loads(response)
    if responseobj['success'] == True:
      return True
    else:
      logger.error('Print job %s failed with %s', jobtype, responseobj['message'])
      return False
      
  except Exception as error_msg:
    logger.error('Print job %s failed with %s', jobtype, error_msg)
    return False
  
def GetPrinter(printer, proxy=None):
    printer_id = None
    response = GetUrl('%s/search?q=%s' % (CLOUDPRINT_URL, printer), tokens)
    printer = urllib.unquote(printer)
    responseobj = json.loads(response)
    if 'printers' in responseobj and len(responseobj['printers']) > 0:
      for printerdetail in responseobj['printers']:
	if printer == printerdetail['name']:
	  return printerdetail['id']
    else:
      return None

def GetUrl(url, tokens, data=None, cookies=False, anonymous=False):
  """Get URL, with GET or POST depending data, adds Authorization header.

  Args:
    url: Url to access.
    tokens: dictionary of authentication tokens for specific user.
    data: If a POST request, data to be sent with the request.
    cookies: boolean, True = send authentication tokens in cookie headers.
    anonymous: boolean, True = do not send login credentials.
  Returns:
    String: response to the HTTP request.
  """
  request = urllib2.Request(url)
  request.add_header('X-CloudPrint-Proxy', 'api-prober')
  if not anonymous:
    if cookies:
      logger.debug('Adding authentication credentials to cookie header')
      request.add_header('Cookie', 'SID=%s; HSID=%s; SSID=%s' % (
          tokens['SID'], tokens['HSID'], tokens['SSID']))
    else:  # Don't add Auth headers when using Cookie header with auth tokens.   
      request.add_header('Authorization', 'GoogleLogin auth=%s' % tokens['Auth'])
  if data:
    request.add_data(data)
    request.add_header('Content-Length', str(len(data)))
    request.add_header('Content-Type', 'multipart/form-data;boundary=%s' % BOUNDARY)

  # In case the gateway is not responding, we'll retry.
  retry_count = 0
  while retry_count < 5:
    try:
      result = urllib2.urlopen(request).read()
      return result
    except urllib2.HTTPError, e:
      # We see this error if the site goes down. We need to pause and retry.
      err_msg = 'Error accessing %s\n%s' % (url, e)
      logger.error(err_msg)
      logger.info('Pausing %d seconds', 60)
      time.sleep(60)
      retry_count += 1
      if retry_count == 5:
        return err_msg

printername = sys.argv[2].replace('cloudprint://','')

printerid = GetPrinter(printername)
if printerid == None:
  print "ERROR: Printer '" + printername + "' not found"
  sys.exit(1)

name = sys.argv[1]
if len(sys.argv) > 3:
  name = sys.argv[3]

if SubmitJob(printerid, 'pdf', sys.argv[1], name):
  print "INFO: Successfully printed"
  sys.exit(0)
else:
  print "ERROR: Failed to submit job to cloud print"
  sys.exit(1)
