class TypeEnv:
    def __init__(self):
        self.scopes = [{}]
        self.function_env = {} 

    def enter_scope(self):
        self.scopes.append({})

    def exit_scope(self):
        self.scopes.pop()

    def declare(self, name, typ):
        self.scopes[-1][name] = {
            "type": typ,
            "owned": True,
            "borrowed": False,
        }

    def define(self, name, info):
        self.scopes[-1][name] = info

    def lookup(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        raise Exception(f"Undefined variable '{name}'")

    def declare_function(self, name, param_types, return_type):
        self.function_env[name] = {
            "kind": "function",
            "param_types": param_types,
            "return_type": return_type
        }

    def lookup_function(self, name):
        if name in self.function_env:
            return self.function_env[name]
        raise Exception(f"Undefined function '{name}'")
