from src.base_product import BaseProduct
from src.print_mixin import PrintMixin


class Product(BaseProduct, PrintMixin):
    name: str
    description: str
    price: float
    quantity: int

    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        self.name = name
        self.description = description
        self.__price = price
        if quantity > 0:
            self.quantity = quantity
        else:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")
        super().__init__()

    def __str__(self) -> str:
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт"

    def __add__(self, other: "Product") -> float:
        if not isinstance(other, Product):
            raise TypeError("Можно складывать только объекты Product")  # с помощью комментария увидим, где ошибка
        return (self.price * self.quantity) + (other.price * other.quantity)

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        # доп.задание при понижении цены (проверка цены)
        try:
            current_price = self.__price
            if new_price < current_price:
                confirmation = input(
                    f"Цена понижается с {current_price} до {new_price}."
                    f"Если хотите понизить цену введите 'y', либо вернуть текущую цену 'n': "
                )
                if confirmation.lower() != "y":
                    print("Изменение цены отменено")
                    return
        except AttributeError:
            pass

        self.__price = new_price

    @classmethod
    def new_product(cls, product_data: dict, products_list: list):
        """
        Создает новый товар с проверкой на дубликаты
        Параметры:
        - product_data: словарь с данными товара
        - products_list: список существующих товаров для проверки
        Возвращает: объект Product
        """
        if products_list is None:
            products_list = []

        name = product_data["name"]
        description = product_data["description"]
        price = float(product_data["price"])
        quantity = int(product_data["quantity"])

        for existing_product in products_list:
            if existing_product.name.lower() == name.lower():
                existing_product.quantity += quantity  # суммируем количество
                existing_product.price = max(existing_product.price, price)  # Берём максимальную цену продукта
                existing_product.description = description  # обновление описание товара
                print(f"Товар {name} уже существует. Объединено количество и выбрана наибольшая цена")
                return existing_product

        # Если дубликатов нет - создаем новый товар и добавляем в список
        created_product = cls(name, description, price, quantity)
        products_list.append(created_product)  # Добавляем новый товар в список
        return created_product


class Smartphone(Product):
    """
    Класс наследник "Смартфон" класса Product
    """

    def __init__(
        self, name, description, price, quantity, efficiency: float, model: str, memory: int, color: str
    ) -> None:
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

    def __add__(self, other):
        if type(other) is Smartphone:
            return (self.price * self.quantity) + (other.price * other.quantity)
        raise TypeError("Можно складывать только объекты Smartphone")  # с помощью комментария увидим, где ошибка


class LawnGrass(Product):
    """
    Класс наследник "Трава газонная" класса Product
    """

    def __init__(self, name, description, price, quantity, country: str, germination_period: str, color: str) -> None:
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def __add__(self, other):
        if type(other) is LawnGrass:
            return (self.price * self.quantity) + (other.price * other.quantity)
        raise TypeError("Можно складывать только объекты LawnGrass")  # с помощью комментария увидим, где ошибка
