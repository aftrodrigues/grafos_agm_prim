my_list = range(1,5)

List comprehension
'cria outra lista a partir de um método passado pelos valores de uma lista'
# Output: [1, 4, 9, 16]
[x**2 for x in my_list]


Iterator:
# object with 2 magic methods:'

""" Create the iterator object """
def __iter__(self):
	return self

""" make and return the next something ( integer, string, object )"""
def __next__(self):
	return <something>


Generator:
'object that produces or get an item at time from list'
# example:
(x**2 for x in my_list)


lambda function:
'Anonymous function, get the arguments e return the result fo the expresison'
# main used to set values to parameter of an function. ex.: filter, map, reduce
# syntax
lambda arguments: expression









in-built Functions:

filter( <functions that return True of False>, <list>)

map( <function that return an value> , <list> )

# reduce all the values of an list to only one
reduce( function(x, y), <list>)
reduce(lambda x, y: x+y, my_list) # sum all the values of the list

