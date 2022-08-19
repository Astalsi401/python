from datetime import datetime

# Specifying some date and time values
dateTimeInstance1 = datetime(2021, 8, 1, 00, 00, 00)
dateTimeInstance2 = datetime(2021, 8, 2, 00, 00, 00)
dateTimeInstance3 = datetime(2021, 8, 3, 00, 00, 00)
dateTimeInstance4 = datetime(2022, 7, 10, 00, 00, 00)

# Calling the weekday() functions over the
# above dateTimeInstances
dayOfTheWeek1 = dateTimeInstance1.weekday()
dayOfTheWeek2 = dateTimeInstance2.weekday()
dayOfTheWeek3 = dateTimeInstance3.weekday()
dayOfTheWeek4 = dateTimeInstance4.weekday()

# Getting the integer value corresponding
# to the specified day of the week
print(dayOfTheWeek1)
print(dayOfTheWeek2)
print(dayOfTheWeek3)
print(dayOfTheWeek4)
