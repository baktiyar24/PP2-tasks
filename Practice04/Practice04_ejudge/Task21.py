import importlib

for _ in range(int(input())):
    module_path, attr = input().split()
    try:
        mod = importlib.import_module(module_path)
        if not hasattr(mod, attr):
            print("ATTRIBUTE_NOT_FOUND")
        elif callable(getattr(mod, attr)):
            print("CALLABLE")
        else:
            print("VALUE")
    except ModuleNotFoundError:
        print("MODULE_NOT_FOUND")