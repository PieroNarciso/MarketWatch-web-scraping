import numpy as np

dicty = {'Open': '$201.30',
         'Day Range': '199.29 - 202.76',
         '52 Week Range': '142.00 - 233.47',
         'Market Cap': '$908.31B',
         'Shares Outstanding': '4.6B',
         'Public Float': '4.71B',
         'Beta': '1.22',
         'Rev. per Employee': '$1.98M',
         'P/E Ratio': '17.13',
         'EPS': '$11.73',
         'Yield': '1.53%',
         'Dividend': '$0.77',
         'Ex-Dividend Date': 'Aug 9, 2019',
         'Short Interest': '43.01M',
         '% of Float Shorted': '0.91%',
         'Average Volume': '27.41M'}

example = list(dicty.values())

list_string = example[1].split()

list_of_list = []
for item in list_string:
    new_string = ''.join((ch if ch in '0123456789.-e' else ' ') for ch in item)
    # print('new string', new_string)
    try:
        list_of_numbers = [float(i) for i in new_string.split()]
        # print('list of numbers', list_of_numbers)
        list_of_list.append(list_of_numbers[0])

    except:
        pass

print(example[0])
print(list_of_list)

# new_string = ''.join((ch if ch in '0123456789.-e' else ' ') for ch in example[1])
#
# try:
#     list_of_numbers = [float(i) for i in new_string.split()]
#     print(list_of_numbers)
# except:
#     print("not a float")

