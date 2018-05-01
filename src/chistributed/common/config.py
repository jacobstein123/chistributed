#  Copyright (c) 2016, The University of Chicago
#  All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are met:
#
#  - Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
#  - Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
#  - Neither the name of The University of Chicago nor the names of its
#    contributors may be used to endorse or promote products derived from this
#    software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
#  ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
#  LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
#  CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
#  SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
#  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
#  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
#  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#  POSSIBILITY OF SUCH DAMAGE.

import os.path
import yaml
from chistributed.common import ChistributedException


class Config(object):    
    OPTION_NODE_EXECUTABLE = "node-executable"
    OPTION_NODES = "nodes"
    
    VALID_OPTIONS = [OPTION_NODE_EXECUTABLE, OPTION_NODES]
    REQUIRED_OPTIONS = [OPTION_NODE_EXECUTABLE, OPTION_NODES]

    @staticmethod
    def get_config_file_values(config_file):
        if not os.path.exists(config_file):
            return {}
        
        with open(config_file, 'r') as f:
            config_file_values = yaml.safe_load(f)
    
        if type(config_file_values) != dict:
            raise ChistributedException("{} is not valid YAML".format(f))
        
        return config_file_values

    @classmethod
    def get_config(cls, config_file, config_overrides = {}):
        config = {}
                
        config_values = cls.get_config_file_values(config_file)
        config.update(config_values)
        config.update(config_overrides)
                
        for o in Config.REQUIRED_OPTIONS:
            if o not in config:
                raise ChistributedException("Configuration file %s does not include required option %s" % (config_file, o)) 
        
        return cls(config)

    def __init__(self, config_values):        
        self.config_values = {opt:config_values.get(opt) for opt in Config.VALID_OPTIONS}
        
    def get_node_executable(self):
        v = self.config_values[Config.OPTION_NODE_EXECUTABLE]
        
        if v is None or len(v) == 0:
            raise ChistributedException("Option {} must have a value".format(Config.OPTION_NODE_EXECUTABLE))
        
        return v 
    
    def get_nodes(self):
        nodes = self.config_values[Config.OPTION_NODES]

        if nodes is None or len(nodes) == 0:
            raise ChistributedException("Option {} must have a value".format(Config.OPTION_NODES))

        return nodes.split()
        
