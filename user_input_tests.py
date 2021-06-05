#For future testing purposes
import pyinputplus as pyip

#To test various inputs with no user prompts:
number = pyip.inputNum()
email = pyip.inputEmail() 
filepath = pyip.inputFilepath()
password = pyip.inputPassword()
#date_time = pyip.inputDatetime()

#To test various inputs with user prompts:
number_min = pyip.inputNum('Enter Number: ', min=4)
number_gt = pyip.inputNum('Enter Number: ', greaterThan=4)
number_multiple = pyip.inputNum('Enter Number: ', min=4, lessThan=6)

#Blank=True to make the input optional for the user
number_blank = pyip.inputNum('Enter Number: ', blank=True)

#limit=n tries
try:
    number_limit = pyip.inputNum('Enter Number: ', limit=3)
except:
    print("To many input attempts!")

#timeout=n seconds
try:
    number_timeout = pyip.inputNum('Enter Number: ', timeout=5)
except:
    print("Too much time to input!")

#limit = n tries & default which can be a string/number etc and thus doesnt return an exception and traceback
number_default = pyip.inputNum('Enter Number: ', limit=3, default=0)
print(number_default)

#Prints the help page for the module
#print(help(pyip))