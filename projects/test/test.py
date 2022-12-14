from os.path import abspath, dirname
import re


print(re.sub(r'\\[^\\]*$', '', dirname(abspath(__file__))))
