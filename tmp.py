from datetime import *

d1 = datetime(2022, 2, 7, 8, 43)
d2 = datetime(2022, 2, 7, 12, 3)
d3 = datetime(2022, 2, 7, 13, 30)
d4 = datetime(2022, 2, 7, 16, 40)
dayCount = (d2 - d1) + (d4 - d3)
print(dayCount)
