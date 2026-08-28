local FRemap = require('foundation_remapping')
local remapper = FRemap.new()

remapper:remap('ralt', 'f18') -- for mac / leopold / ducky
--remapper:remap('rcmd', 'f18') -- for varmilo

--remapper:remap('lalt', 'lcmd') -- for ducky 	
--remapper:remap('lcmd', 'lalt') -- for ducky 

remapper:register()