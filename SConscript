import os
Import('env')

env['OPENCVBUILDER_MODULE_DIR'] = 'opencv/modules'
env['OPENCVBUILDER_3RDPARTY_DIR'] = 'opencv/3rdparty'

env.configOpencv()

for entry in Glob('{path}/*'.format(path = env['OPENCVBUILDER_3RDPARTY_DIR'])):
	# Check if it is a dir
	if type(entry) == type(Dir('.')):
		# Generate module lib
		env['opencv_3rdparty'] = entry
		env.thirdpartyOpencv()

for entry in Glob('{path}/*'.format(path = env['OPENCVBUILDER_MODULE_DIR'])):
#	if(os.path.isdir('{module_dir}/{module}'.format(module_dir = env['OPENCVBUILDER_MODULE_DIR'], module = entry))):
	# Check if it is a dir
	if type(entry) == type(Dir('.')):
		# Generate module lib
		env['opencv_module'] = entry
		env.openclOpencv()
		env.buildOpencv()

env['LINKFLAGS'].extend(env['OPENCVBUILDER_ADDITIONAL_FLAGS'])
