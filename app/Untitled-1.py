class Dog:
    def __init__(self, name, breed, age):  # Constructor
        self.name = name     # Initialize the 'name' attribute
        self.breed = breed   # Initialize the 'breed' attribute
        self.age = age       # Initialize the 'age' attribute

    def bark(self):
        print(f"{self.name} is barking!")

# Creating an object (instance) of the class Dog
my_dog = Dog("Buddy", "Golden Retriever", 3)
