import os
Import('env')

env['OPENCVBUILDER_MODULE_DIR'] = '{opencv_dir}/opencv/modules'.format(opencv_dir = env['openCV_DIR'])
env['OPENCVBUILDER_3RDPARTY_DIR'] = '{opencv_dir}/opencv/3rdparty'.format(opencv_dir = env['openCV_DIR'])
env.configOpencv()

for entry in os.listdir(env['OPENCVBUILDER_3RDPARTY_DIR']):
	if(os.path.isdir('{module_dir}/{module}'.format(module_dir = env['OPENCVBUILDER_3RDPARTY_DIR'], module = entry))):
		# Generate module lib
		env['opencv_3rdparty'] = Dir('{module_dir}/{module}'.format(module_dir = env['OPENCVBUILDER_3RDPARTY_DIR'], module = entry)).abspath
		env.thirdpartyOpencv()

for entry in os.listdir(env['OPENCVBUILDER_MODULE_DIR']):
	if(os.path.isdir('{module_dir}/{module}'.format(module_dir = env['OPENCVBUILDER_MODULE_DIR'], module = entry))):
		# Generate module lib
		env['opencv_module'] = Dir('{module_dir}/{module}'.format(module_dir = env['OPENCVBUILDER_MODULE_DIR'], module = entry)).abspath
		env.openclOpencv()
		env.buildOpencv()

env['LINKFLAGS'] = env['OPENCVBUILDER_ADDITIONAL_FLAGS']
