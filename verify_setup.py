from collections import defaultdict

colours = (
    ('Yasoob', 'Yellow'),
    ('Ali', 'Blue'),
    ('Arham', 'Green'),
    ('Ali', 'Black'),
    ('Yasoob', 'Red'),
    ('Ahmed', 'Silver'),
)

favourite_colours = defaultdict(list)
'''
for name, colour in colours:
    favourite_colours[name].append(colour)
'''

#print(favourite_colours)

import sys
#Python imports work by searching the directories listed in sys.path
print (sys.path)

site_packages_path = next(p for p in sys.path if 'site-packages' in p)
print (site_packages_path)

import os

#set a environment variable
os.environ['DEBUSSY'] = '1'
someVariable = int(os.environ['DEBUSSY'])
print (someVariable)
print (os.environ['PYTHONPATH']) #contains project path

'''
# This won't work - there is no hi module
import hi
Traceback (most recent call last):
    File "<stdin>", line 1, in <module> 
ImportError: No module named hi
'''

# Create a hi module in your home directory.
home_dir = os.path.expanduser("~")
my_module_file = os.path.join(home_dir, "hi.py")
with open(my_module_file, 'w') as f:
    f.write('print ("hi")\n')
    f.write('a=10')

# Add the home directory to sys.path
sys.path.append(home_dir)

# Now this works, and prints hi!
import hi
print (hi.a)
