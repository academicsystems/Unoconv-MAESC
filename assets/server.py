#!/usr/bin/python2.7

import cgi
import json
import mimetypes
import os
import random
import shutil
import string
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
            if not os.path.isfile("/var/www/tmp/" + data['input']):
                raise web.NotFound(data['input'] + " not found, did you upload it yet? or is your volume attached correctly?")
            
            output = ''
            
            cmd = 'unoconv '
            for arg in data['cmd']:
                if arg == 'INPUT':
                    cmd += " /var/www/tmp/" + data['input'] + " "
                elif arg[:6] == 'OUTPUT':
                    output = ''.join(random.choice(string.ascii_lowercase) for _ in range(10)) + arg[6:]
                    cmd += " /var/www/tmp/" + output + " "
                else:
                    cmd += arg
            
            yield cmd + "\n"
            
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            line = process.stdout.readline()
            while line:
                yield str(line)
                line = process.stdout.readline()
            yield 'DONE: ' + output
        except Exception as e:
            yield cgi.escape(str(e))

class Upload:
    def PUT(self,path):
        try:
            with open("/var/www/tmp/" + path,"wb") as f:
                f.write(web.data())
        except Exception as e:
            raise web.InternalError(str(e))

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
