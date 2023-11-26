import sqlite3
import pathlib


class BaseType:
    field_type: str

    def __init__(self, unique: bool = False, null: bool = True, default: int = None):
        self.unique = unique
        self.null = null
        self.default = default


class IntegerField(BaseType):
    field_type = 'INTEGER'


class TextField(BaseType):
    field_type = 'TEXT'


class RealField(BaseType):
    field_type = 'REAL'


class Model:
    __connection = None

    def __init__(self, *args, **kwargs):
        fields = [el for el in vars(self.__class__) if not el.startswith("__")]
        for i, value in enumerate(args):
            # задаем переменные переданные с помощью args
            setattr(self, fields[i], value)

        for field, value in kwargs.items():
            setattr(self, field, value)

    @classmethod
    def return_attr4create_table(cls):
        attributes = {}
        for key, value in vars(cls).items():
            # проверка на системные методы и поля
            if not key.startswith("__") and not callable(value):
                attributes[key] = value
        return attributes

    def return_attr4update_data(self):
        attributes = {}
        for key, value in vars(self).items():
            # проверка на системные методы и поля
            if not key.startswith("__") and not callable(value):
                attributes[key] = value
        return attributes

    @classmethod
    def connect(cls, path: str):
        path_db = pathlib.Path(path)

        try:
            cls.connection = sqlite3.connect(path_db)
        except Exception as e:
            print(f"Error connect to db {path_db}, {e}")

    @classmethod
    def create_entity(cls, update=False):

        cursor = cls.connection.cursor()

        fields = ""
        for key, val in cls.return_attr4create_table().items():
            fields += f"{key} {val.field_type}, "
        fields = fields[:-2]

        cursor.execute(f"CREATE TABLE IF NOT EXISTS {cls.__name__} ({fields})")

        cls.connection.commit()

    def save(self):
        cursor = self.connection.cursor()

        fields = ""
        data = list()
        for key, val in self.return_attr4update_data().items():
            fields += f"{key}, "
            data.append(val)
        fields = fields[:-2]

        count_q = "?," * len(self.return_attr4update_data().keys())
        sql = f"INSERT INTO {self.__class__.__name__} ({fields}) VALUES ({count_q[:-1]})"
        cursor.execute(sql, tuple(data))
        self.connection.commit()

    @classmethod
    def get(cls, fields=None):
        cursor = cls.connection.cursor()

        f = ""
        if fields == None:
            f = "*"
        else:
            f = ",".join(fields)

        sql = f"SELECT {f} FROM {cls.__name__}"
        cursor.execute(sql)
        data = cursor.fetchall()
        return data

    def delete(self):
        pass
