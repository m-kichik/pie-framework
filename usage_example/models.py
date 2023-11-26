import orm


class Box(orm.Model):
    name = orm.TextField()
    width = orm.IntegerField()
    height = orm.IntegerField()


class Car(orm.Model):
    name = orm.TextField()
    power = orm.IntegerField()


# orm.Model.connect("/home/danisimo/VK_education/pie-framework/my_db.sqlite3")
Car.create_entity()
Box.create_entity()


car1 = Car("fera", 1000)
car1.save()
car2 = Car("ford", 555)
car2.save()

b1 = Box("Коробка от пылесоса", 100, 100)
b1.save()
b2 = Box("Коробка от Ифона", 500, 500)
b2.save()

print(Car.get())
print(Car.get(["name"]))
print(Car.get(["name", "power"]))
