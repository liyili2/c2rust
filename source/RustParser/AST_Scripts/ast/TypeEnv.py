from RustParser.AST_Scripts.ast.Func import *

class TypeEnv:
    def __init__(self):
        self.builtin_function_names = ["as_ref", "unwrap"]
        self.scopes = [{}]
        self.function_env = {} 
        for f in self.builtin_function_names:
            self.function_env[f] = {
            "kind": "function",
            "param_types": FunctionParamList(params=[]),
            "return_type": None
        }

    def enter_scope(self):
        self.scopes.append({})

    def exit_scope(self):
        self.scopes.pop()

    def declare(self, name, typ, mutable=False, isSafelyWrapped=False):
        self.scopes[-1][name] = {
            "type": typ,
            "owned": True,
            "borrowed": False,
            "mutable": mutable,
            "isSafelyWrapped": isSafelyWrapped,
        }

    def wrapSafe(self, name, isSafelyWrapped):
        self.scopes[-1][name]["isSafelyWrapped"] = isSafelyWrapped

    # def define(self, name, info):
    #     self.scopes[-1][name] = info

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

    def top(self):
        return self.scopes[-1]