import os

import opencvBuilderUtils
import opencv_config

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
    @staticmethod
    def optionToSources(option, sources,falseSource):
        if not ccmake[option]:
            sources = modulesToFilterFunctions.removeFromList(sources, source)
        return sources,None,None
    @staticmethod
    def libjpeg(env, sources, modulePath):
        sources = modulesToFilterFunctions.optionToSources('WITH_IOS', sources, 'jmemansi.c')
        if ccmake['WITH_IOS']:
            sources = modulesToFilterFunctions.removeFromList(sources, 'jmemnobs.c')
        return sources

modulesToFilter = {
    'libjpeg' : modulesToFilterFunctions.libjpeg
}

class moduleDefines:
    @staticmethod
    def all():
        defines,options = opencv_config.getDefinesAndCompileOptions()
        return defines

getDefines = {
    'libjpeg' : moduleDefines.all,
    'zlib' : moduleDefines.all
}

class moduleCompileFlags:
    @staticmethod
    def all():
        defines,options = opencv_config.getDefinesAndCompileOptions()
        return options

getCompileFlags = {
    'libjpeg' : moduleCompileFlags.all,
    'zlib' : moduleCompileFlags.all
}
