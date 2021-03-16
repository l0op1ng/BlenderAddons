# single file
filename = "../scripts_test/op_boolean.py"
exec(compile(open(filename).read(), filename, 'exec'))

# script in a module
"""
import myscript
import importlib

importlib.reload(myscript)
myscript.main()
"""