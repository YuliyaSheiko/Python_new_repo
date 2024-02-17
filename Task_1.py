import random


# list of 100 random numbers from 0 to 1000
# create function that will return array of numbers
def create_list():
    # using random.randint method start from 0 to 1000 and  put this numbers to array of length 100
    return [random.randint(0, 1000) for i in range(100)]
# assign result of function call to variable


my_list = create_list()
# function call
print("my list:", my_list)


# sort list from min to max (without using sort())
# create function for sorting that get list that should be sorted as argument
# use 'Bubble Sort' algorithm that was found in google

def my_sorting(lst):
    n = len(lst)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if lst[j] > lst[j + 1]:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
    # and return sorted list
    return lst

# assign result of function call to variable


sorted_list = my_sorting(my_list)
# function call
print("my sorted list:", sorted_list)

# calculate average for even and odd numbers
# create function for calculating average. It accepts  an array of numbers as argument


def calculate_average(my_sorted_list):
    # define variables, set default value to zero
    even_sum = 0
    even_count = 0
    odd_sum = 0
    odd_count = 0

    for num in my_sorted_list:
        # run for loop for list and check if the number is odd or even
        # In each case add this number to corresponding sum variable and increase the count
        if num % 2 == 0:
            even_sum += num
            even_count += 1
        else:
            odd_sum += num
            odd_count += 1
    # calculate average and assign the values to variables
    even_average = even_sum / even_count
    odd_average = odd_sum / odd_count
# return this variables
    return even_average, odd_average

# assign result of function call to variables


even_avg, odd_avg = calculate_average(sorted_list)

# print both average result in console
print("Average of even numbers:", even_avg)
print("Average of odd numbers:", odd_avg)