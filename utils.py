

class shell_process:
    def __init__(self, local_vars=None, env_vars=None):
        #  Safe dictionary initialization
        self.local_vars = local_vars if local_vars is not None else {}
        self.env_vars = env_vars if env_vars is not None else {}        

    def fork(self):
        #  Break the memory reference link by copying
        return shell_process(self.local_vars.copy(), self.env_vars.copy())

    def delete_local(self):
        self.local_vars = {}
        
    def exect(self):
        self.delete_local()
        # To make fork_exect work seamlessly, exect should return self
        return self

    def fork_exect(self):

        return self.fork().exect()




def shell_script(source:str = None , process:shell_process = None):
    if source:
        """ script """
    else:
        sub_process = process.fork_exec()
        """ 
        script on sub process , then killed
 
        """

# no fork no exec()
def source(process:shell_process):
    return process

# no fork no exec()
def export(process:shell_process,var_name:str = None, var_value = None):
    return process.env_vars[{var_name}] = var_value


def change_directory(path:str = None,process:shell_process = None ):
    shell_process.env_vars["CURRENT_DIRECTORY"] = path

"""
regex_rules , if cd x --> change_directory








"""