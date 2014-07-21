import os
import string

headerExtensions = ['*.h', '*.hpp']
sourceExtensions = ['*.c', '*.cpp', '*.mm']

def processCmakeDefine(contentString, define, defineDefine):
        # Process
        if defineDefine:
            contentString = contentString.replace('#cmakedefine {define}'.format(define = define), '#define {define}'.format(define = define))
        else:
            contentString = contentString.replace('#cmakedefine {define}'.format(define = define), '/* #undef {define} */'.format(define = define))
        return contentString

def copyDirectoryTree(src, dst):
    print('Copying directory structure...')
    fread = os.popen('find {src} -type d -print'.format(src = src))
    folders = fread.read()
    fread.close()
    fnames = string.split(folders,"\n")
    startString = len(src)
    for f in fnames:
        os.popen('mkdir -p "{dst}/{dir}"'.format(dst = dst, dir = f[startString:]))

def getFilesInFolder(env, path = '.', extensions = ['*.c', '*.cpp']):
    files = list()
    for extension in extensions:
        files.extend(env.Glob('{path}/{extension}'.format(path = path, extension = extension)))

    return files

