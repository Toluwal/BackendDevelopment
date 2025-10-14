class Pet:
    def __init__(self, name, species, age):
        self.name = name
        self.species = species
        self.age = age

    def display(self):
        print(f" The pet name is {self.name}  and of {self.species} specie and {self.age} years old. ")

    def celebrate(self):
        print(f" {self.name} is a lovely cat ")
cat = Pet("Pop", "felidae", 7)
cat.display()
cat.celebrate()