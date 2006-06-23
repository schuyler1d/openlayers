#!/usr/bin/env python

"""This is a blind proxy that we use to get around browser
restrictions that prevent the Javascript from loading pages not on the
same server as the Javascript.  This has several problems: it's less
efficient, it might break some sites, and it's a security risk because
people can use this proxy to browse the web and possibly do bad stuff
with it.  If you can get your code signed (see:
http://trac.openlayers.org/wiki/HowToSignJavascript), then you should
modify Parameters.js so that this isn't used.  Otherwise, you're stuck
with it.  It only loads pages via http and https, but it can load any
content type. XML and HTML are both currently used by Openlayers."""

from mod_python import apache, util
import urllib, time, cgi, re
import memcache

is_xml_like         = re.compile( r'^\s*<?xml[^>]*?>', re.DOTALL )
is_tab_separated    = re.compile( r'^(?:(?:[^\t\n]+\t)+[^\t\n]*\n?)$)+', 
                                    re.DOTALL )

class Session (object):
    max_bad_requests = 6
    timeout = 86400

    def __init__ ():
        self.cache = memcache.Client(['127.0.0.1:11211'], debug=0)
        self.ip    = apache.mp_conn.remote_ip

    def made_bad_request ():
        self.cache.incr( self.ip )

    def made_good_request ():
        self.cache.decr( self.ip )

    def validate ():
        count = self.cache.get( self.ip )
        if count is None:
            self.cache.set( self.ip, "0", time.time() + self.timeout )
            return True
        else:
            return count < max_bad_requests

def authenhandler (req):
    client = Session()
    if client.validate():
        return apache.OK
    else:
        return apache.HTTP_SERVICE_UNAVAILABLE

def handler (req):
    fs = util.FieldStorage(req)
    url = fs.getvalue('url', "http://openlayers.org")
    client = Session()

    if url.startswith("http://") or url.startswith("https://"):
        proxy = urllib.urlopen(url)
        content = proxy.read()
        proxy.close()

        content_type = None
        if is_xml_like.match(content):
            content_type = "text/xml"
        elif is_tab_separated.match(content): 
            content_type = "text/plain"

        if content_type is not None:
            req.content_type = content_type
            req.write(content)
            client.made_good_request()
            return apache.OK
        else:
            client.made_bad_request()
            return apache.HTTP_BAD_REQUEST
    else:
        client.made_bad_request()
        return apache.HTTP_BAD_REQUEST
