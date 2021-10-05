import os
os.chdir(r'D:\\Pictures\\Saved Pictures')
import base64
f=open('mail_icon.png','rb')
ls_f=base64.b64encode(f.read())
f.close()
print(ls_f)