from pathlib import Path
import re
 
p = Path.cwd() / 'input.csv'

# Part 1
numbers_simple_regex = re.compile(r'\d')
calibration_sum_simple = 0
with p.open() as src:
    for line in src:
        digits = numbers_simple_regex.findall(line)
        calibration_val = digits[0] + digits[-1]
        calibration_sum_simple += int(calibration_val)

print(calibration_sum_simple)
# -> correct

# Part 2
# input does not contain 'zero' or 'ten'
numbers = {
    'one': '1', 'two': '2', 'three': '3',
    'four': '4', 'five': '5', 'six': '6',
    'seven': '7', 'eight': '8', 'nine': '9'}

# either a word or a string digit
numbers.update({str(i+1): str(i+1) for i in range(9)})
# overlapping regex:
# https://junli.netlify.app/…on/
numbers_regex = re.compile(f"(?=({'|'.join(numbers)}))")
# translate words to digits line by line, concat and sum
calibration_sum = 0
with p.open() as src:
    for line in src:
        digits = [numbers[x] for x in numbers_regex.findall(line)]
        calibration_val = digits[0] + digits[-1]
        calibration_sum += int(calibration_val)

print(calibration_sum)
# -> correct