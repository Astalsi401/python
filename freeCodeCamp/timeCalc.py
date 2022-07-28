def add_time(start, duration, week=None):
    weekTable = {
        ', Sunday': 0,
        ', Monday': 1,
        ', Tuesday': 2,
        ', Wednesday': 3,
        ', Thursday': 4,
        ', Friday': 5,
        ', Saturday': 6,
    }
    rd, rw, twelvehc = '', '', ' AM'
    startime = start.split(' ')
    sh, sm = startime[0].split(':')
    ah, am = duration.split(':')
    sh = int(sh)
    sm = int(sm)
    ah = int(ah)
    am = int(am)
    if startime[1] == 'PM':
        sh += 12
    rh = sh + ah
    rm = sm + am
    rh += int(rm / 60)
    rm = rm % 60
    rd = int(rh / 24)
    rh = rh % 24
    if rh >= 12:
        twelvehc = ' PM'
        rh -= 12
    if rh == 0:
        rh = 12
    if week:
        week = week[0].upper() + week[1:].lower()
        rw = list(weekTable.keys())[list(weekTable.values()).index((weekTable[f', {week}'] + rd) % 7)]
    if rd == 0:
        rd = ''
    elif rd == 1:
        rd = ' (next day)'
    else:
        rd = f' ({rd} days later)'
    return '%d:%02d%s%s%s' % (rh, rm, twelvehc, rw, rd)


print(add_time("11:30 AM", "2:32", "Monday"))
