class ShellProcess:
    def __init__(self, pid: int, name: str = "bash", local_vars: dict = None, env_vars: dict = None, history: list = None):
        self.pid = pid
        self.name = name
        self.local_vars = local_vars if local_vars is not None else {}
        self.env_vars = env_vars if env_vars is not None else {"USER": "ubuntu", "PWD": "/home/ubuntu"}
        # Track command history!
        self.history = history if history is not None else []

    def fork(self, child_pid: int):
        return ShellProcess(
            pid=child_pid,
            name=f"{self.name} (child)",
            local_vars=self.local_vars.copy(),
            env_vars=self.env_vars.copy(),
            history=self.history.copy()
        )

    def delete_local(self):
        self.local_vars = {}

    def exect(self, binary_name: str):
        self.name = binary_name
        self.delete_local()
        return self

    def fork_exect(self, child_pid: int, binary_name: str):
        child = self.fork(child_pid)
        return child.exect(binary_name)