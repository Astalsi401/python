from os.path import dirname, abspath
pwd = dirname(abspath(__file__))

var = ['score', 'option', 'tempcode', 'usercode']
tmp = []
f = open(f"{pwd}/test.txt", "r")
Lines = f.readlines()

for i in range(0, len(Lines)):
    exec(f'{var[i]} = {Lines[i]}')

    # check type
    exec(f'print({var[i]}, type({var[i]}))')
