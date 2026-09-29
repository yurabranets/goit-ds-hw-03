from pymongo.errors import PyMongoError
from filepath import path
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from functools import wraps


client=MongoClient(
    path,
            server_api=ServerApi('1')
)

db = client.HM


class CatNotFound(Exception):
    pass



def handler_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except CatNotFound:
            print("Кота з таким іменем не знайдено")
        except PyMongoError as e:
            print(f"Помилка {e}")
        except ValueError:
            print("Некоректне значення")
    return wrapper



def check(cat, message):
    if not cat:
        raise CatNotFound
    print(message)


#функція для виведення всіх записів із колекції.
@handler_error
def read_cats():
    cats = db.cats.find({})
    for el in cats:
        print(el)



#функція, яка дозволяє користувачеві ввести ім'я кота та виводить інформацію про цього кота.
@handler_error
def read_inf(name):
    cat=db.cats.find_one({"name":name})
    check(cat, cat)
   

#функція, яка дозволяє користувачеві оновити вік кота за ім'ям.
@handler_error
def update_age(name,age):
    cat=db.cats.update_one({"name":name}, {"$set":{"age":age}})
    check(cat.matched_count, "Вік оновлено")

#функція, яка дозволяє додати нову характеристику до списку features кота за ім'ям.
@handler_error
def update_features(name, features):
    cat=db.cats.update_one({"name":name}, {"$push":{"features":features}})
    check(cat.matched_count, "Додали нову характеристику")

@handler_error
def delete_cat(name):
    cat=db.cats.delete_one({"name":name})
    check(cat.deleted_count, "Запис видалено")

@handler_error
def delete_cats():
    db.cats.delete_many({})
    print("Колекцію очищено")

@handler_error
def create_cat(name, age, features):
    """Створює нового кота."""
    db.cats.insert_one({"name": name, "age": age, "features": features})
    print("Кота додано")



def menu():
    while True:
        cmd=input("Введіть команду:")

        try:
            if cmd == "all":
                read_cats()
            elif cmd == "find":
                read_inf(input("Ім'я: "))
            elif cmd == "age":
                update_age(input("Ім'я: "), int(input("Новий вік: ")))
            elif cmd == "feature":
                update_features(input("Ім'я: "), input("Характеристика: "))
            elif cmd == "delete":
                delete_cat(input("Ім'я: "))
            elif cmd == "clear":
                delete_cats()
            elif cmd=="exit":
                break
            elif cmd == "create":
                create_cat(input("Ім'я: "), int(input("Вік: ")), [f.strip() for f in input("Особливості (через кому): ").split(",")])
            else:
                print("Невідома команда")
        except ValueError:
            print("Некоректне значення")

    
    
if __name__=="__main__":
    menu()

