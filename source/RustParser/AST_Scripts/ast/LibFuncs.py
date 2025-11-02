
from RustParser.AST_Scripts.ast.common import *
from RustParser.AST_Scripts.ast.Expression import *

class LibFunction:
    def __init__(self, name: str):
        self.name = name

    def __call__(self, visitor, caller, args=None):
        """All library functions must implement this."""
        raise NotImplementedError(f"{self.name} must implement __call__")

class LibFuncUnwrap(LibFunction):
    def __init__(self):
        super().__init__("unwrap")

    def __call__(self, visitor, caller, args=None):
        val = caller.accept(visitor) if caller else None
        if val is None:
            raise ReturnSignal(value=Exception("called unwrap() on a None value"))
        return val

class LibFuncLen(LibFunction):
    def __init__(self):
        super().__init__("len")

    def __call__(self, visitor, caller, args=None):
        caller = caller.accept(visitor) if caller else None
        if isinstance(caller, ArrayLiteral):
            return caller.len()
        else:
            try:
                return len(caller)
            except Exception:
                raise Exception("len() called on non-iterable")
            
class LibFuncFrom(LibFunction):
    def __init__(self):
        super().__init__("from")

    def __call__(self, visitor, caller, args=None):
        caller = caller.accept(visitor) if caller else None
        arg = args[0].accept(visitor) if args and args[0] else None
        if isinstance(arg, str) and len(arg) == 1:
            return ord(arg)
        return int(arg)
        # TODO

class LibFuncIntoRaw(LibFunction):
    def __init__(self):
        super().__init__("into_raw")

    def __call__(self, visitor, caller, args=None):
        val = caller.accept(visitor) if caller else None
        if val is None:
            raise ReturnSignal(value=Exception("called into_raw() on a None value"))
        return val

class LibFuncNullMut(LibFunction):
    def __init__(self):
        super().__init__("null_mut")

    def __call__(self, visitor, caller, args=None):
        val = caller.accept(visitor) if caller else None
        if val is None:
            return None
        return None

class LibFuncAsRef(LibFunction):
    def __init__(self):
        super().__init__("as_ref")

    def __call__(self, visitor, caller, args=None):
        val = caller.accept(visitor) if caller else None
        if val is None:
            raise ReturnSignal(value=Exception("called as_ref() on a None value"))
        return val

class LibFuncIsEmpty(LibFunction):
    def __init__(self):
        super().__init__("is_empty")

    def __call__(self, visitor, caller, args=None):
        val = caller.accept(visitor) if caller else None
        if val is None:
            return True
        if isinstance(val, ArrayLiteral):
            if len(val) == 0:
                return True
        return False
    
class LibFuncIsNull(LibFunction):
    def __init__(self):
        super().__init__("is_null")

    def __call__(self, visitor, caller, args=None):
        val = caller.accept(visitor) if caller else None
        if val is None:
            return True
        return False
    
class LibFuncFetchAdd(LibFunction):
    def __init__(self):
        super().__init__("fetch_add")

    def __call__(self, visitor, caller, args=None):
        val = caller.accept(visitor) if caller else None
        if val is None:
            raise ReturnSignal(value=Exception("called push() with more than one argument"))
        to_be_added = args[0].accept(visitor)
        visitor.stack.update({caller.name: val + to_be_added})
        return val

class LibFuncPush(LibFunction):
    def __init__(self):
        super().__init__("push")

    def __call__(self, visitor, caller, args=None):
        caller = caller.accept(visitor) if caller else None
        if caller is None:
            raise ReturnSignal(value=Exception("called push() on a None value"))
        if len(args) > 1:
            raise ReturnSignal(value=Exception("called push() with more than one argument"))
        if isinstance(caller, ArrayLiteral):
            caller.elements.append(args[0].accept(visitor))

class LibFuncPop(LibFunction):
    def __init__(self):
        super().__init__("pop")

    def __call__(self, visitor, caller, args=None):
        caller = caller.accept(visitor) if caller else None
        if caller is None:
            raise ReturnSignal(value=Exception("called pop() on a None value"))
        if isinstance(caller, ArrayLiteral):
            if not caller.elements:
                raise ReturnSignal(value=Exception("called pop() on an empty ArrayLiteral"))
            last = caller.elements.pop()
            # visitor.stack.update({caller.name: caller})
            return last
        
class LibFuncIter(LibFunction):
    def __init__(self):
        super().__init__("iter")

    def __call__(self, visitor, caller, args=None):
        caller = caller.accept(visitor) if caller else None
        if caller is None:
            raise ReturnSignal(value=Exception("called iter() on a None value"))
        if isinstance(caller, ArrayLiteral):
            if not caller.elements:
                raise ReturnSignal(value=Exception("called iter() on an empty ArrayLiteral"))
            return len(caller.elements)
        if isinstance(caller, str):
            return len(caller)

class LibFuncAsBytes(LibFunction):
    def __init__(self):
        super().__init__("as_bytes")

    def __call__(self, visitor, caller, args=None):
        caller = caller.accept(visitor) if caller else None
        if caller is None:
            raise ReturnSignal(value=Exception("called as_bytes() on a None value"))
        if isinstance(caller, StrLiteral):
            return caller.encode('utf-8')
        return caller


class LibFuncIntoString(LibFunction):
    def __init__(self):
        super().__init__("into_string")

    def __call__(self, visitor, caller, args=None):
        caller = caller.accept(visitor) if caller else None
        if caller is None:
            raise ReturnSignal(value=Exception("called into_string() on a None value"))

        return str(caller)


class LibFuncAddrOfMut(LibFunction):
    def __init__(self):
        super().__init__("addr_of_mut!")

    def __call__(self, visitor, caller, args=None):
        expr = caller.accept(visitor) if caller else None
        if expr is None:
            raise ReturnSignal(value=Exception("called addr_of_mut!() on a None value"))

        return expr


class LibFuncFetchAdd(LibFunction):
    def __init__(self):
        super().__init__("fetch_add")

    def __call__(self, visitor, caller, args=None):
        val = caller.accept(visitor) if caller else None
        if val is None:
            raise ReturnSignal(value=Exception("called fetch_add() on a None value"))
        if len(args) < 1:
            raise ReturnSignal(value=Exception("called fetch_add() without an argument"))
        to_be_added = args[0].accept(visitor)
        new_val = val + to_be_added
        visitor.stack[caller.name] = new_val
        return val

class LibFuncByRef(LibFunction):
    def __init__(self):
        super().__init__("by_ref")

    def __call__(self, visitor, caller, args=None):
        iterator = caller.accept(visitor) if caller else None
        if iterator is None:
            raise ReturnSignal(value=Exception("called by_ref() on a None value"))

        return iterator


class LibFuncIntoBoxedSlice(LibFunction):
    def __init__(self):
        super().__init__("into_boxed_slice")

    def __call__(self, visitor, caller, args=None):
        vector = caller.accept(visitor) if caller else None
        if vector is None:
            raise ReturnSignal(value=Exception("called into_boxed_slice() on a None value"))

        return vector
