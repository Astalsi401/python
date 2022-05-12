import os
os.chdir(r'')

import base64
bs = ''
imgdata = base64.b64decode(bs)
file = open('.png','wb')
file.write(imgdata)
file.close()