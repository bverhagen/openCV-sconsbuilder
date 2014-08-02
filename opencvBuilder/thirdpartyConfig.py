import os

import opencvBuilderUtils

class thirdpartyEmitterFunctions:
    @staticmethod
    def libjpeg():
        sourceList = ['jpeglib.h', 'jerror.h']
        targetList = ['jpeg']
        return sourceList,targetList
    @staticmethod
    def zlib():
        sourceList = ['zlib.h']
        targetList = ['zlib']
        return sourceList,targetList

thirdpartyToEmitterValues = {
    'libjpeg' : thirdpartyEmitterFunctions.libjpeg,
    'zlib' : thirdpartyEmitterFunctions.zlib
}

class thirdpartyGeneratorFunction:
    @staticmethod
    def zlib(env, path):
        sourceFile = env.Glob('{path}/zconf.h.cmakein'.format(path = path))
        targetFile = '{path}/zconf.h'.format(path = path)
        
        if not os.path.isdir(path.rstr()):
            os.popen('mkdir -p "{dir}"'.format(dir = path.rstr()))
 
        # Read cmake file
        with open(sourceFile[0].rstr(), 'r') as f:
            with open(targetFile, 'w') as g:
                for contentLine in f:
                    # Process
                    contentLine = opencvBuilderUtils.processCmakeDefine(contentLine, 'Z_PREFIX', False)
                    # TODO: Check somehow on unistd.h
                    contentLine = opencvBuilderUtils.processCmakeDefine(contentLine, 'Z_HAVE_UNISTD_H', True)

                    # Write
                    g.write(contentLine)

        env.Install('{includeDir}/opencv2'.format(includeDir=env['OPENCVBUILDER_INCLUDE_DIR']), targetFile)
        return None

thirdpartyToGeneratorFunctions = {
    'zlib' : thirdpartyGeneratorFunction.zlib
}

class modulesToFilterFunctions:
    pass

modulesToFilter = {
}

class moduleDefines:
    @staticmethod
    def all():
        return ['-DNDEBUG']

getDefines = {
    'libjpeg' : moduleDefines.all,
    'zlib' : moduleDefines.all
}

class moduleCompileFlags:
    @staticmethod
    def all():
        return ['-fPIC']

getCompileFlags = {
    'libjpeg' : moduleCompileFlags.all,
    'zlib' : moduleCompileFlags.all
}
