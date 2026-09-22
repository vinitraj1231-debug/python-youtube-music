'''
Module containing the utility function: include
'''

import pkgutil
import importlib
import os
import sys
from typing import Callable
from importlib.machinery import ModuleSpec

def include(spec: ModuleSpec, func: Callable = None) -> dict:
    '''
    Include relative libraries, or an object they contain.

    If a relative library exists with an object of the same name inside,
    it returns that object, otherwise, it returns the library. Libraries
    or objects are only returned if func(library or object) is true.

    Args:
        spec: The specification of the module to import from
            Example: utils.__spec__
        func: A function to filter items by
            Example: lambda object: object.__name__ in ('foo',)

    Returns:
        A dictionary of imported libraries or objects

    Example:
        Package named utils containing foo.py, with a function inside named foo:
            >>> include(utils.__spec__)
            {'foo': <function foo at 0x0000027A533CE790>}
            >>>
        Package named utils containing foo.py with a function inside named bar:
            >>> include(utils.__spec__)
            <module 'utils.foo' from '/path/to/utils/foo.py'>
            >>>
    '''

    if not spec or not getattr(spec, 'submodule_search_locations', None):
        return {}

    if not func:
        func = lambda module_name: True

    try:
        importlib.util.module_from_spec(spec)
    except Exception:
        pass

    module = sys.modules.get(spec.name)

    sub_module_names = []
    try:
        sub_modules = pkgutil.iter_modules(spec.submodule_search_locations)
        for sub_module in sub_modules:
            if sub_module.name and not sub_module.name.startswith('__'):
                sub_module_names.append(sub_module.name)
    except Exception:
        pass

    # Fallback to os.listdir if pkgutil.iter_modules didn't find modules in virtual filesystem
    if not sub_module_names:
        for loc in spec.submodule_search_locations:
            try:
                for fname in os.listdir(loc):
                    if fname.startswith('__') or fname.startswith('.'):
                        continue
                    if fname.endswith('.py'):
                        sub_module_names.append(fname[:-3])
                    elif os.path.isdir(os.path.join(loc, fname)) and os.path.exists(os.path.join(loc, fname, '__init__.py')):
                        sub_module_names.append(fname)
            except Exception:
                pass

    # Deduplicate module names while preserving order
    seen = set()
    unique_names = []
    for name in sub_module_names:
        if name not in seen:
            seen.add(name)
            unique_names.append(name)

    imported = {}

    for sub_module_name in unique_names:
        try:
            sub_module = importlib.import_module(
                name=f'.{sub_module_name}',
                package=spec.name,
            )
        except Exception:
            continue

        obj = getattr(sub_module, sub_module_name, None) or sub_module

        if not func(obj):
            continue

        if module:
            setattr(module, sub_module_name, obj)

        imported[sub_module_name] = obj

    return imported
