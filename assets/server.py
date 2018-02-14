#!/usr/bin/python2.7

import cgi
import json
import mimetypes
import os
import shutil
import subprocess
import time
import web
from types import ModuleType

mimetypes.init()
cgi.maxlen = 1073741824; # 1GB limit

class Main:
    def POST(self):
        # get post request json body
        try:
            data = json.loads(web.data())
        except:
            yield 'json is not formatted correctly'
        
        web.header('Transfer-Encoding', 'chunked')
        
        # execute
        try:
            cmd = 'unoconv '
            for arg in data['cmd']:
                if arg == 'INPUT':
                    cmd += " /var/www/tmp/" + data['input'] + " "
                elif arg == 'OUTPUT':
                    cmd += " /var/www/tmp/" + ''.join(random.choice(string.ascii_lowercase) for _ in range(10)) + " "
                else:
                    cmd += arg
            
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            line = process.stdout.readline()
            while line:
                yield str(line)
                line = process.stdout.readline()
            yield 'done'
        except Exception as e:
            yield cgi.escape(str(e))

class Upload:
    def PUT(self,path):
        try:
            with open("/var/www/tmp/" + path,"wb") as f:
                f.write(web.data())
        except ValueError:
            raise web.HTTPError.__init__(self, 413, {}, '')

class TestConnection:
    def GET(self):
        startTime = time.time()
        subprocess.call(["unoconv","--version"])
        totalTime = time.time() - startTime
        respdict = {'Exec Time':totalTime}
        return json.dumps(respdict)

if __name__ == "__main__":
    web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
    # symlink tmp directory for user generated files to static directory
    if os.path.exists('/var/www/static'):
        os.unlink('/var/www/static')
    try:
        os.symlink('/var/www/tmp','/var/www/static')
    except:
        pass
    
    urls = (
          '/service', 'Main',
          '/upload/(.+)', 'Upload',
          '/', 'TestConnection'
        )
    app = web.application(urls, globals())
    app.run()
