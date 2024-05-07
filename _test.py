import PresetNotes
import inspect

# get all classes from PresetNotes
classes = inspect.getmembers(PresetNotes, inspect.isclass)
# print the class names
for c in classes:
    print(c[0])
