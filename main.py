# dict : data ko store krne ke kaam aata hai, ismai data key : value pair mai store hote hai, or isko { iske andr apka data hoga }
# data = {
#     "a" : 1,
#     "b" : 2
# }
# print(data)

# # add c : 3
# data["c"] = 3
# print("After add value => ",data)

# # update 
# data["a"] = 10

# print("After update => ", data)

student1 = {
    "name" : "Neha das",
    "age" : 23
}
print(student1)
student1["name"] = "aman"

# deletion :- del, pop, popitem, clear
# del student1["age"] # delete toh krta hai lekin kuch return ni krta
# print(student1)

# val = student1.pop("age")
# print(val)
# print(student1)

# popitem
# val = student1.popitem() # jo bhi last element usko delete krna 
# print(student1)

# clear
student1.clear()
print(student1)