from SCons.Builder import Builder
import os

# This module import
import opencvBuilderUtils
import thirdpartyConfig
import opencv_config

configDirectory = 'opencv'

def build_opencv_emitter(target, source, env):
    ''' Emitter for openCV builder '''
    module = os.path.basename(env['opencv_module'].rstr())
    try:
        thirdpartySource,thirdpartyTarget = opencv_config.moduleToEmitterValues[module](module)
    except KeyError:
        # This means we can call the default action
        thirdpartySource,thirdpartyTarget = opencv_config.moduleToEmitterValues['default'](module)

    source.extend(thirdpartySource)
    target.extend(thirdpartyTarget)

    # Search additional library dependencies
    try:
	addLibs,addLinkFlags = opencv_config.getAdditionalLibs[str(module)]()
	try:
        	env['OPENCVBUILDER_ADDITIONAL_LIBRARIES'].extend(addLibs)
	except KeyError:
		env['OPENCVBUILDER_ADDITIONAL_LIBRARIES'] = addLibs
	try:
		env['OPENCVBUILDER_ADDITIONAL_FLAGS'].extend(addLinkFlags)
	except KeyError:
		env['OPENCVBUILDER_ADDITIONAL_FLAGS'] = addLinkFlags
    except KeyError:
        pass
    return target,source

def build_opencv_generator(source, target, env, for_signature):
    ''' Generator for openCV builder '''
    module = os.path.basename(env['opencv_module'].rstr())

    # Install the required header files
    env.Install('{includeDir}/opencv2'.format(includeDir=env['OPENCVBUILDER_INCLUDE_DIR']), source[0])
    env.Install('{includeDir}/opencv2/{module}'.format(module = module, includeDir = env['OPENCVBUILDER_INCLUDE_DIR']), source[1])
    try:
        additionalHeaders = opencv_config.moduleToAdditionalHeaders[str(module)](module, env)
    except KeyError:
        # This means we can call the default handler
        additionalHeaders = opencv_config.moduleToAdditionalHeaders['default'](module, env)

    env.Install('{includeDir}/opencv2/{module}'.format(module = module, includeDir = env['OPENCVBUILDER_INCLUDE_DIR']), additionalHeaders)

    # Configure build environment for opencv
    env_opencv = env.Clone()
    # Empty defines to avoid unnecessary rebuilding of the library
    env_opencv['CPPDEFINES'] = []
    defines,options = opencv_config.getDefinesAndCompileOptions()
    env_opencv['CPPDEFINES'].extend(defines)
    env_opencv['CXXFLAGS'].extend(options)
    env_opencv['CPPPATH'].append('{module}/src'.format(module = env['opencv_module']))

    if module == 'core':
        # TODO: generate these properly
        env.Install('{includeDir}'.format(includeDir=env['OPENCVBUILDER_INCLUDE_DIR']), 'version_string.inc')
        env.Install('{includeDir}/opencv2'.format(includeDir=env['OPENCVBUILDER_INCLUDE_DIR']), 'opencv_modules.hpp')
    
    # Build module
    sources = list()
    sources.extend(opencvBuilderUtils.getFilesInFolder(env,'{module}/src'.format(module = env['opencv_module']), ['*.c', '*.cpp', '*.mm']))
    sources.append('{module}/src/opencl_kernels.cpp'.format(module = env['opencv_module']))
    try:
        sources,additionalIncludes,additionalLibs = opencv_config.modulesToFilter[str(module)](env, sources, env['opencv_module'])
        env_opencv['CPPPATH'].extend(additionalIncludes)
    except KeyError:
        pass

    env_opencv['CPPPATH'].extend(env['OPENCVBUILDER_INCLUDE_PATHS'])   
	
    lib = env_opencv.Library('{lib}'.format(lib = target[0]), sources)
    installed_lib = env_opencv.Install("{libs_dir}".format(libs_dir=env['OPENCVBUILDER_LIBS_DIR']), lib)
    env_opencv.Alias("buildAllLibs", installed_lib)
    return installed_lib

def config_opencv_emitter(target, source, env):
    ''' Emitter for opencv config '''
    # Check if these values exist in env, add them otherwise
    if not 'CPPPATH' in env:
        env['CPPPATH'] = []
    directory = os.getcwd()
    source.append('cvconfig.in')
    target.append('{includeDir}/cvconfig.h'.format(includeDir = env['OPENCVBUILDER_INCLUDE_DIR']))

    # Store ccmake values for building 
    for configParam,value in env['opencv_config'].iteritems():
        opencv_config.ccmake[configParam] = value

    # Check if configDirectory exists. If not, we are building in a variantDir and the entire directory structure should be copied
    if not os.path.isdir(configDirectory):
        print('VariantDir detected. Copying directory structure...')
        opencvBuilderUtils.copyDirectoryTree('{opencvDir}/{opencv_source}'.format(opencvDir=env['openCV_DIR'], opencv_source = configDirectory), configDirectory)

    # Add additional include paths
    opencv_config.opencvBuilderAdditionalIncludePaths = env['OPENCVBUILDER_INCLUDE_PATHS']
    return target,source

def config_opencv_generator(source, target, env, for_signature):
    ''' Generator for openCV builder '''
    # Check if target folder exists
    if not os.path.isdir(env['OPENCVBUILDER_INCLUDE_DIR']):
        os.popen('mkdir -p "{dir}"'.format(dir = env['OPENCVBUILDER_INCLUDE_DIR']))
    # write config file
    with open('{includeDir}/{configFile}'.format(includeDir=env['OPENCVBUILDER_INCLUDE_DIR'], configFile = opencv_config.configFile), 'w') as f:
        print "creating cvconfig.h"
        generateConfigFile(f, opencv_config.ccmake)
    return target

def generateConfigFile(configFile, config = {}):
    ''' Generate the config file '''
    for param,value in config.iteritems():
        string = opencv_config.ccmakeToCvconfig[str(param)](value)
        if string != None:
           configFile.write(string)

def opencl_opencv_emitter(target, source, env):
    ''' Opencl builder emitter '''
    source.append('{module}/src/opencl_kernels.hpp'.format(module = env['opencv_module']))
    source.append('{module}/src/opencl_kernels.cpp'.format(module = env['opencv_module']))
    return target, source

def opencl_opencv_generator(source, target, env, for_signature):
    ''' Opencl builder generator '''
    module = os.path.basename(env['opencv_module'].rstr())
    clmakePath = env.Glob('{path}/../../cmake/cl2cpp.cmake'.format(path = env['opencv_module']))
    clmakePath = clmakePath[0].srcnode()
    clfiles = env.Glob('{path}/src/opencl/*.cl'.format(path = env['opencv_module']))
    if clfiles:
        cldir =  os.path.dirname(os.path.realpath(clfiles[0].srcnode().rstr()))
    else:
        cldir = ''
    cmd = 'cmake -DMODULE_NAME="{module_name}" -DCL_DIR="{cldir}" -DOUTPUT=$TARGET -P {cmakeFile}'.format(module = env['opencv_module'], module_name = module, cmakeFile = clmakePath, cldir = cldir)
    # These two are for older versions of the builder
    opencl_files = env.Command("{module}/src/opencl_kernels.hpp".format(module = env['opencv_module']),'', cmd)
    opencl_files.append(env.Command("{module}/src/opencl_kernels.cpp".format(module = env['opencv_module']),'', cmd))
    # Do the same for the new opencl_kernels names
    opencl_files.append(env.Command("{modulePath}/src/opencl_kernels_{module}.hpp".format(modulePath = env['opencv_module'], module = module),'', cmd))
    opencl_files.append(env.Command("{modulePath}/src/opencl_kernels_{module}.cpp".format(modulePath = env['opencv_module'], module = module),'', cmd))
    return opencl_files

def thirdparty_opencv_emitter(target, source, env):
    ''' Emitter for 3rdparty openCV stuff '''
    module = os.path.basename(env['opencv_3rdparty'].rstr())
    try:
        thirdpartySource,thirdpartyTarget = thirdpartyConfig.thirdpartyToEmitterValues[module]()
        source.extend(thirdpartySource)
        target.extend(thirdpartyTarget)
    except KeyError:
        # This means the third party lib is not yet supported. Generated unique dummies
        source.append('{module}_dummy.h'.format(module = module))
        target.append('{module}_dummy'.format(module = module))
    return target,source

def thirdparty_opencv_generator(source, target, env, for_signature):
    ''' Generator for 3rdparty openCV stuff '''
    # Do a library specific preliminary step if necessary
    module = os.path.basename(env['opencv_3rdparty'].rstr())

    # Inherit as much as possible from the parent build environment but do not inherit its defines: this will cause the library to be rebuilt in unnecessary cases.
    env_opencv = env.Clone()
    env_opencv['CPPDEFINES'] = []
    try:
        env_opencv['CPPDEFINES'].extend(thirdpartyConfig.getDefines[module]())
    except KeyError:
        pass
    try:
        env_opencv['CPPFLAGS'].extend(thirdpartyConfig.getCompileFlags[module]())
    except KeyError:
        pass

    # Install header file
    env.Install('{includeDir}/opencv2'.format(includeDir=env['OPENCVBUILDER_INCLUDE_DIR']), source)

    try:
        thirdpartyConfig.thirdpartyToGeneratorFunctions[module](env_opencv, env['opencv_3rdparty'])
    except KeyError:
        pass

    # Build module
    sources = list()
    sources.extend(opencvBuilderUtils.getFilesInFolder(env,'{module}'.format(module = env['opencv_3rdparty']), ['*.c', '*.cpp']))

    # Filter module-specific files
    try:
        sources,additionalIncludes,additionalLibs = thirdpartyConfig.modulesToFilter[str(module)](env, sources, env['opencv_module'])
        env_opencv['CPPPATH'].extend(additionalIncludes)
    except KeyError:
        pass

    lib = env_opencv.Library('{lib}'.format(lib = target[0]), sources)
    installed_lib = env_opencv.Install("{libs_dir}".format(libs_dir=env['OPENCVBUILDER_LIBS_DIR']), lib)
    env_opencv.Alias("buildAllLibs", installed_lib)
    return installed_lib

def exists(env):
    return env.Detect('buildOpencv') and env.Detect('configOpencv')

def generate(env):
    configOpencvBuilder = Builder(emitter = config_opencv_emitter, generator = config_opencv_generator)
    env.Append(BUILDERS = {'configOpencv' : configOpencvBuilder})
    thirdpartyOpencvBuilder = Builder(emitter = thirdparty_opencv_emitter, generator = thirdparty_opencv_generator)
    env.Append(BUILDERS = {'thirdpartyOpencv' : thirdpartyOpencvBuilder})
    openclOpencvBuilder = Builder(emitter = opencl_opencv_emitter, generator = opencl_opencv_generator)
    env.Append(BUILDERS = {'openclOpencv' : openclOpencvBuilder})
    opencvBuilder = Builder(emitter = build_opencv_emitter, generator = build_opencv_generator)
    env.Append(BUILDERS = {'buildOpencv' : opencvBuilder})
