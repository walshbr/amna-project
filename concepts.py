class Coffee:
    # pass


#     def __init__(self):
#         # print("Coffee is created")
#         self.temperature = 0
#         self.flavour = 'sweet, smoky, sumatran'
    

# c = Coffee()
# # print(c)


# myCoffee = Coffee()
# print(myCoffee.flavour)
# print(c.temperature)

    def __init__(self, temp=0, flavour='bland', origin='yemen'):
        # above attributes default?
        self.temperature = temp
        self.flavour = flavour
        self.origin = origin

        self.dangerous = "no"
    
    def change_temp(self, temp):
        self.temperature = temp

ethans_coffee = Coffee(80, 'spicy')
# print(ethans_coffee.flavour)

brandons_coffee = Coffee(origin='brazil')
# print(brandons_coffee.temperature)
# print(brandons_coffee.flavour)
print(brandons_coffee.origin)

brandons_coffee.change_temp(120)
# print(brandons_coffee.temperature)

amnas_coffee = Coffee(100, 'fruity', 'ethiopia')
# print(amnas_coffee.origin)