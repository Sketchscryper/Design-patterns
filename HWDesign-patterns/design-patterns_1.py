# Задание 1. Создайте реализацию паттерна Builder.
# Протестируйте работу созданного класса.

print("Задание №1\n---------------------------------")
from typing import List

class Computer:
    """Продукт - компьютер, который мы будем строить"""

    def __init__(self):
        self.cpu: str = ""
        self.ram: int = 0
        self.storage: int = 0
        self.gpu: str = ""
        self.operating_system: str = ""
        self.peripherals: List[str] = []

    def __str__(self) -> str:
        return (f"Computer:\n"
                f"  CPU: {self.cpu}\n"
                f"  RAM: {self.ram}GB\n"
                f"  Storage: {self.storage}GB\n"
                f"  GPU: {self.gpu}\n"
                f"  OS: {self.operating_system}\n"
                f"  Peripherals: {', '.join(self.peripherals) if self.peripherals else 'None'}")


class ComputerBuilder:
    """Строитель компьютера"""

    def __init__(self):
        self.computer = Computer()

    def set_cpu(self, cpu: str) -> 'ComputerBuilder':
        """Установка процессора"""
        self.computer.cpu = cpu
        return self

    def set_ram(self, ram: int) -> 'ComputerBuilder':
        """Установка оперативной памяти"""
        if ram <= 0:
            raise ValueError("RAM must be positive")
        self.computer.ram = ram
        return self

    def set_storage(self, storage: int) -> 'ComputerBuilder':
        """Установка хранилища"""
        if storage <= 0:
            raise ValueError("Storage must be positive")
        self.computer.storage = storage
        return self

    def set_gpu(self, gpu: str) -> 'ComputerBuilder':
        """Установка видеокарты"""
        self.computer.gpu = gpu
        return self

    def set_operating_system(self, os: str) -> 'ComputerBuilder':
        """Установка операционной системы"""
        self.computer.operating_system = os
        return self

    def add_peripheral(self, peripheral: str) -> 'ComputerBuilder':
        """Добавление периферийного устройства"""
        self.computer.peripherals.append(peripheral)
        return self

    def build(self) -> Computer:
        """Построение компьютера и возврат результата"""
        # Можно добавить валидацию здесь
        if not self.computer.cpu:
            raise ValueError("CPU is required")
        if not self.computer.ram:
            raise ValueError("RAM is required")

        computer = self.computer
        self.computer = Computer()  # Сброс для возможного повторного использования
        return computer


class GamingComputerBuilder(ComputerBuilder):
    """Специализированный строитель для игровых компьютеров"""

    def __init__(self):
        super().__init__()

    def set_gpu(self, gpu: str) -> 'GamingComputerBuilder':
        """Переопределение для игровых видеокарт"""
        self.computer.gpu = f"Gaming {gpu}"
        return self

    def add_gaming_peripherals(self) -> 'GamingComputerBuilder':
        """Добавление игровой периферии"""
        self.add_peripheral("Gaming Mouse")
        self.add_peripheral("Mechanical Keyboard")
        self.add_peripheral("Gaming Headset")
        return self


class OfficeComputerBuilder(ComputerBuilder):
    """Специализированный строитель для офисных компьютеров"""

    def __init__(self):
        super().__init__()

    def set_cpu(self, cpu: str) -> 'OfficeComputerBuilder':
        """Переопределение для офисных процессоров"""
        self.computer.cpu = f"Office {cpu}"
        return self

    def add_office_peripherals(self) -> 'OfficeComputerBuilder':
        """Добавление офисной периферии"""
        self.add_peripheral("Office Mouse")
        self.add_peripheral("Standard Keyboard")
        self.add_peripheral("Printer")
        return self


class ComputerDirector:
    """Директор для создания стандартных конфигураций"""

    @staticmethod
    def build_gaming_pc() -> Computer:
        """Создание стандартного игрового ПК"""
        return (GamingComputerBuilder()
                .set_cpu("Intel i7-12700K")
                .set_ram(32)
                .set_storage(1000)
                .set_gpu("NVIDIA RTX 4070")
                .set_operating_system("Windows 11")
                .add_gaming_peripherals()
                .build())

    @staticmethod
    def build_office_pc() -> Computer:
        """Создание стандартного офисного ПК"""
        return (OfficeComputerBuilder()
                .set_cpu("Intel i5-12400")
                .set_ram(16)
                .set_storage(512)
                .set_gpu("Integrated Graphics")
                .set_operating_system("Windows 10")
                .add_office_peripherals()
                .build())

    @staticmethod
    def build_budget_pc() -> Computer:
        """Создание бюджетного ПК"""
        return (ComputerBuilder()
                .set_cpu("AMD Ryzen 5 5600G")
                .set_ram(8)
                .set_storage(256)
                .set_gpu("Integrated Radeon Graphics")
                .set_operating_system("Linux Ubuntu")
                .build())


# Тестирование работы паттерна Builder
def test_builder_pattern():
    print("=== Тестирование паттерна Builder ===\n")

    # Тест 1: Базовое использование строителя
    print("1. Базовое использование ComputerBuilder:")
    computer = (ComputerBuilder()
                .set_cpu("Intel i5-12600K")
                .set_ram(16)
                .set_storage(512)
                .set_gpu("NVIDIA GTX 1660")
                .set_operating_system("Windows 10")
                .add_peripheral("Mouse")
                .add_peripheral("Keyboard")
                .build())
    print(computer)
    print()

    # Тест 2: Использование специализированного строителя
    print("2. Использование GamingComputerBuilder:")
    gaming_pc = (GamingComputerBuilder()
                 .set_cpu("AMD Ryzen 7 7800X3D")
                 .set_ram(32)
                 .set_storage(2000)
                 .set_gpu("AMD RX 7900 XT")
                 .set_operating_system("Windows 11")
                 .add_gaming_peripherals()
                 .add_peripheral("Webcam")
                 .build())
    print(gaming_pc)
    print()

    # Тест 3: Использование директора для стандартных конфигураций
    print("3. Стандартные конфигурации через Director:")

    print("Игровой ПК:")
    gaming_standard = ComputerDirector.build_gaming_pc()
    print(gaming_standard)
    print()

    print("Офисный ПК:")
    office_standard = ComputerDirector.build_office_pc()
    print(office_standard)
    print()

    print("Бюджетный ПК:")
    budget_standard = ComputerDirector.build_budget_pc()
    print(budget_standard)
    print()

    # Тест 4: Проверка валидации
    print("4. Проверка валидации:")
    try:
        invalid_computer = (ComputerBuilder()
                            .set_ram(-8)  # Неверное значение
                            .build())
    except ValueError as e:
        print(f"Ошибка валидации: {e}")

    try:
        incomplete_computer = (ComputerBuilder()
                               .set_ram(16)
                               .build())  # Нет CPU
    except ValueError as e:
        print(f"Ошибка валидации: {e}")
    print()

    # Тест 5: Fluent interface (цепочка вызовов)
    print("5. Fluent interface:")
    custom_pc = (ComputerBuilder()
                 .set_cpu("Intel i9-13900K")
                 .set_ram(64)
                 .set_storage(4000)
                 .set_gpu("NVIDIA RTX 4090")
                 .set_operating_system("Windows 11 Pro")
                 .add_peripheral("4K Monitor")
                 .add_peripheral("SSD NVMe")
                 .add_peripheral("Water Cooling")
                 .build())
    print(custom_pc)


if __name__ == "__main__":
    test_builder_pattern()
print()

# Задание 2. Создайте приложение для приготовления пасты.
# Приложение должно уметь создавать минимум три вида пасты.
# Классы различной пасты должны иметь следующие методы:
# ■ Тип пасты;
# ■ Соус;
# ■ Начинка;
# ■ Добавки.
# Для реализации используйте порождающие паттерны.

print("Задание №2\n---------------------------------")
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from enum import Enum


# Паттерн: Factory Method
class PastaType(Enum):
    CARBONARA = "Карбонара"
    BOLOGNESE = "Болоньезе"
    ALFREDO = "Альфредо"
    MARINARA = "Маринара"


class Pasta(ABC):
    """Абстрактный класс пасты"""

    def __init__(self):
        self._type: str = ""
        self._sauce: str = ""
        self._filling: str = ""
        self._additives: List[str] = []
        self._pasta_type: str = "спагетти"  # тип макарон

    @abstractmethod
    def get_type(self) -> str:
        pass

    @abstractmethod
    def get_sauce(self) -> str:
        pass

    @abstractmethod
    def get_filling(self) -> str:
        pass

    @abstractmethod
    def get_additives(self) -> List[str]:
        pass

    def set_pasta_type(self, pasta_type: str) -> None:
        self._pasta_type = pasta_type

    def get_pasta_type(self) -> str:
        return self._pasta_type

    def __str__(self) -> str:
        return (f"Паста: {self.get_type()}\n"
                f"Тип макарон: {self.get_pasta_type()}\n"
                f"Соус: {self.get_sauce()}\n"
                f"Начинка: {self.get_filling()}\n"
                f"Добавки: {', '.join(self.get_additives()) if self.get_additives() else 'нет'}\n"
                f"---")

    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': self.get_type(),
            'pasta_type': self.get_pasta_type(),
            'sauce': self.get_sauce(),
            'filling': self.get_filling(),
            'additives': self.get_additives()
        }


# Конкретные классы пасты
class CarbonaraPasta(Pasta):
    def get_type(self) -> str:
        return "Карбонара"

    def get_sauce(self) -> str:
        return "Сырно-яичный соус с гуанчиале"

    def get_filling(self) -> str:
        return "Гуанчиале, яичные желтки, пармезан"

    def get_additives(self) -> List[str]:
        return ["Черный перец", "Соль", "Оливковое масло"]


class BolognesePasta(Pasta):
    def get_type(self) -> str:
        return "Болоньезе"

    def get_sauce(self) -> str:
        return "Томатный соус с мясом"

    def get_filling(self) -> str:
        return "Говяжий фарш, свиной фарш, овощи"

    def get_additives(self) -> List[str]:
        return ["Базилик", "Чеснок", "Лук", "Морковь", "Сельдерей"]


class AlfredoPasta(Pasta):
    def get_type(self) -> str:
        return "Альфредо"

    def get_sauce(self) -> str:
        return "Сливочный соус с пармезаном"

    def get_filling(self) -> str:
        return "Курица, грибы"

    def get_additives(self) -> List[str]:
        return ["Пармезан", "Сливочное масло", "Чеснок", "Петрушка"]


class MarinaraPasta(Pasta):
    def get_type(self) -> str:
        return "Маринара"

    def get_sauce(self) -> str:
        return "Томатный соус с травами"

    def get_filling(self) -> str:
        return "Морепродукты (креветки, мидии, кальмары)"

    def get_additives(self) -> List[str]:
        return ["Чеснок", "Базилик", "Орегано", "Белое вино"]


# Паттерн: Factory Method
class PastaFactory(ABC):
    """Фабрика для создания пасты"""

    @abstractmethod
    def create_pasta(self) -> Pasta:
        pass

    def prepare_pasta(self) -> Pasta:
        pasta = self.create_pasta()
        print(f"Готовим {pasta.get_type()}...")
        return pasta


class CarbonaraFactory(PastaFactory):
    def create_pasta(self) -> Pasta:
        return CarbonaraPasta()


class BologneseFactory(PastaFactory):
    def create_pasta(self) -> Pasta:
        return BolognesePasta()


class AlfredoFactory(PastaFactory):
    def create_pasta(self) -> Pasta:
        return AlfredoPasta()


class MarinaraFactory(PastaFactory):
    def create_pasta(self) -> Pasta:
        return MarinaraPasta()


# Паттерн: Builder
class PastaBuilder:
    """Строитель для кастомной пасты"""

    def __init__(self):
        self.pasta = None
        self.reset()

    def reset(self) -> None:
        self.pasta = CustomPasta()

    def set_type(self, pasta_type: str) -> 'PastaBuilder':
        self.pasta._type = pasta_type
        return self

    def set_sauce(self, sauce: str) -> 'PastaBuilder':
        self.pasta._sauce = sauce
        return self

    def set_filling(self, filling: str) -> 'PastaBuilder':
        self.pasta._filling = filling
        return self

    def set_pasta_type(self, pasta_type: str) -> 'PastaBuilder':
        self.pasta.set_pasta_type(pasta_type)
        return self

    def add_additive(self, additive: str) -> 'PastaBuilder':
        self.pasta._additives.append(additive)
        return self

    def build(self) -> Pasta:
        pasta = self.pasta
        self.reset()
        return pasta


class CustomPasta(Pasta):
    """Кастомная паста, создаваемая через Builder"""

    def get_type(self) -> str:
        return self._type or "Кастомная паста"

    def get_sauce(self) -> str:
        return self._sauce or "Без соуса"

    def get_filling(self) -> str:
        return self._filling or "Без начинки"

    def get_additives(self) -> List[str]:
        return self._additives


# Паттерн: Singleton для меню пасты
class PastaMenu:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._menu = {
                PastaType.CARBONARA: CarbonaraFactory(),
                PastaType.BOLOGNESE: BologneseFactory(),
                PastaType.ALFREDO: AlfredoFactory(),
                PastaType.MARINARA: MarinaraFactory()
            }
        return cls._instance

    def get_factory(self, pasta_type: PastaType) -> PastaFactory:
        return self._menu[pasta_type]

    def get_available_types(self) -> List[PastaType]:
        return list(self._menu.keys())


# Приложение для приготовления пасты
class PastaCookingApp:
    def __init__(self):
        self.menu = PastaMenu()
        self.builder = PastaBuilder()

    def show_menu(self) -> None:
        print("🍝 МЕНЮ ПАСТЫ 🍝")
        print("=" * 30)
        for i, pasta_type in enumerate(self.menu.get_available_types(), 1):
            print(f"{i}. {pasta_type.value}")
        print("5. Создать кастомную пасту")
        print("=" * 30)

    def cook_standard_pasta(self, choice: int) -> Pasta:
        types = self.menu.get_available_types()
        if 1 <= choice <= len(types):
            pasta_type = types[choice - 1]
            factory = self.menu.get_factory(pasta_type)
            return factory.prepare_pasta()
        else:
            raise ValueError("Неверный выбор")

    def cook_custom_pasta(self) -> Pasta:
        print("\nСоздание кастомной пасты:")
        print("Выберите тип макарон:")
        pasta_types = ["спагетти", "феттучини", "пенне", "фарфалле", "равиоли"]
        for i, pt in enumerate(pasta_types, 1):
            print(f"{i}. {pt}")

        choice = int(input("Ваш выбор: "))
        pasta_type = pasta_types[choice - 1] if 1 <= choice <= len(pasta_types) else "спагетти"

        print("\nВведите тип пасты (например: 'Моя особенная паста'):")
        type_name = input("Тип: ") or "Кастомная паста"

        print("\nВведите соус:")
        sauce = input("Соус: ") or "Стандартный соус"

        print("\nВведите начинку:")
        filling = input("Начинка: ") or "Стандартная начинка"

        print("\nДобавьте добавки (через запятую):")
        additives_input = input("Добавки: ") or ""
        additives = [additive.strip() for additive in additives_input.split(",") if additive.strip()]

        custom_pasta = (self.builder
                        .set_type(type_name)
                        .set_sauce(sauce)
                        .set_filling(filling)
                        .set_pasta_type(pasta_type)
                        .build())

        for additive in additives:
            custom_pasta._additives.append(additive)

        print("Кастомная паста создана!")
        return custom_pasta

    def run(self) -> None:
        print("Добро пожаловать в приложение для приготовления пасты!")

        while True:
            print("\n" + "=" * 40)
            self.show_menu()

            try:
                choice = int(input("\nВыберите вариант (0 для выхода): "))

                if choice == 0:
                    print("До свидания! Приятного аппетита! 🍝")
                    break
                elif 1 <= choice <= 4:
                    pasta = self.cook_standard_pasta(choice)
                    print("\nВаша паста готова!")
                    print(pasta)
                elif choice == 5:
                    pasta = self.cook_custom_pasta()
                    print("\nВаша кастомная паста готова!")
                    print(pasta)
                else:
                    print("Неверный выбор. Попробуйте снова.")

            except ValueError:
                print("Пожалуйста, введите число.")
            except Exception as e:
                print(f"Произошла ошибка: {e}")


# Демонстрация работы приложения
def demonstrate_pasta_patterns():
    print("=== Демонстрация паттернов проектирования ===\n")

    # 1. Factory Method
    print("1. Factory Method:")
    factories = [CarbonaraFactory(), BologneseFactory(), AlfredoFactory()]

    for factory in factories:
        pasta = factory.create_pasta()
        print(f"Фабрика создала: {pasta.get_type()}")
        print(f"Соус: {pasta.get_sauce()}")
        print(f"Начинка: {pasta.get_filling()}")
        print(f"Добавки: {', '.join(pasta.get_additives())}")
        print()

    # 2. Builder
    print("2. Builder Pattern:")
    builder = PastaBuilder()
    custom_pasta = (builder
                    .set_type("Экспериментальная паста")
                    .set_sauce("Трюфельный соус")
                    .set_filling("Утка конфи, грибы")
                    .set_pasta_type("феттучини")
                    .add_additive("Трюфельное масло")
                    .add_additive("Пармезан")
                    .add_additive("Зеленый лук")
                    .build())

    print(custom_pasta)

    # 3. Singleton
    print("3. Singleton Pattern:")
    menu1 = PastaMenu()
    menu2 = PastaMenu()
    print(f"menu1 is menu2: {menu1 is menu2}")
    print(f"Доступные типы: {[t.value for t in menu1.get_available_types()]}")
    print()


# Тестирование
if __name__ == "__main__":
    # Демонстрация паттернов
    demonstrate_pasta_patterns()

    # Запуск приложения
    app = PastaCookingApp()
    app.run()
print()

# Задание 3. Создайте реализацию паттерна Prototype. Протестируйте работу созданного класса.

print("Задание №3\n---------------------------------")
from abc import ABC, abstractmethod
from typing import List, Dict, Any
import copy
import json

class Prototype(ABC):
    """Абстрактный класс прототипа"""

    @abstractmethod
    def clone(self):
        pass

    @abstractmethod
    def deep_clone(self):
        pass


class Person(Prototype):
    """Класс Person, реализующий паттерн Prototype"""

    def __init__(self, name: str, age: int, hobbies: List[str] = None, metadata: Dict[str, Any] = None):
        self.name = name
        self.age = age
        self.hobbies = hobbies if hobbies else []
        self.metadata = metadata if metadata else {}
        self._internal_data = {"created_at": "2024-01-01"}  # внутренние данные

    def clone(self):
        """Поверхностное копирование"""
        return copy.copy(self)

    def deep_clone(self):
        """Глубокое копирование"""
        return copy.deepcopy(self)

    def custom_clone(self, **kwargs):
        """Кастомное клонирование с возможностью изменения атрибутов"""
        cloned = self.deep_clone()
        for key, value in kwargs.items():
            if hasattr(cloned, key):
                setattr(cloned, key, value)
        return cloned

    def add_hobby(self, hobby: str):
        self.hobbies.append(hobby)

    def update_metadata(self, key: str, value: Any):
        self.metadata[key] = value

    def __str__(self):
        return (f"Person(name='{self.name}', age={self.age}, "
                f"hobbies={self.hobbies}, metadata={self.metadata})")

    def to_dict(self):
        return {
            'name': self.name,
            'age': self.age,
            'hobbies': self.hobbies.copy(),
            'metadata': self.metadata.copy()
        }

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)


class Employee(Person):
    """Наследник Person с дополнительными атрибутами"""

    def __init__(self, name: str, age: int, position: str, salary: float, **kwargs):
        super().__init__(name, age, **kwargs)
        self.position = position
        self.salary = salary
        self.skills = []

    def clone(self):
        return copy.copy(self)

    def deep_clone(self):
        return copy.deepcopy(self)

    def add_skill(self, skill: str):
        self.skills.append(skill)

    def __str__(self):
        base_str = super().__str__()
        return (f"Employee({base_str[7:-1]}, "
                f"position='{self.position}', salary={self.salary}, "
                f"skills={self.skills})")

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'position': self.position,
            'salary': self.salary,
            'skills': self.skills.copy()
        })
        return data


class PrototypeRegistry:
    """Реестр прототипов (паттерн Registry)"""

    def __init__(self):
        self._prototypes: Dict[str, Prototype] = {}

    def register_prototype(self, key: str, prototype: Prototype):
        self._prototypes[key] = prototype

    def unregister_prototype(self, key: str):
        if key in self._prototypes:
            del self._prototypes[key]

    def get_prototype(self, key: str) -> Prototype:
        if key not in self._prototypes:
            raise ValueError(f"Прототип с ключом '{key}' не найден")
        return self._prototypes[key].clone()

    def get_deep_prototype(self, key: str) -> Prototype:
        if key not in self._prototypes:
            raise ValueError(f"Прототип с ключом '{key}' не найден")
        return self._prototypes[key].deep_clone()

    def list_prototypes(self) -> List[str]:
        return list(self._prototypes.keys())


# Тестирование паттерна Prototype
def test_prototype_pattern():
    print("=== Тестирование паттерна Prototype ===\n")

    # Создание оригинального объекта
    print("1. Создание оригинального объекта:")
    original_person = Person(
        name="Иван Иванов",
        age=30,
        hobbies=["чтение", "программирование"],
        metadata={"department": "IT", "level": "senior"}
    )
    print(f"Оригинал: {original_person}")
    print(f"ID оригинала: {id(original_person)}")
    print(f"ID hobbies: {id(original_person.hobbies)}")
    print()

    # Поверхностное копирование
    print("2. Поверхностное копирование (shallow copy):")
    shallow_copy = original_person.clone()
    print(f"Копия: {shallow_copy}")
    print(f"ID копии: {id(shallow_copy)}")
    print(f"ID hobbies копии: {id(shallow_copy.hobbies)}")
    print("Списки hobbies разделяются (same ID):", id(original_person.hobbies) == id(shallow_copy.hobbies))
    print()

    # Глубокое копирование
    print("3. Глубокое копирование (deep copy):")
    deep_copy = original_person.deep_clone()
    print(f"Глубокая копия: {deep_copy}")
    print(f"ID глубокой копии: {id(deep_copy)}")
    print(f"ID hobbies глубокой копии: {id(deep_copy.hobbies)}")
    print("Списки hobbies разные (different ID):", id(original_person.hobbies) != id(deep_copy.hobbies))
    print()

    # Изменение оригинального объекта
    print("4. Изменение оригинального объекта:")
    original_person.add_hobby("путешествия")
    original_person.update_metadata("level", "lead")
    print(f"Оригинал после изменений: {original_person}")
    print(f"Поверхностная копия после изменений оригинала: {shallow_copy}")
    print(f"Глубокая копия после изменений оригинала: {deep_copy}")
    print()

    # Кастомное клонирование
    print("5. Кастомное клонирование:")
    custom_clone = original_person.custom_clone(name="Петр Петров", age=25)
    print(f"Кастомная копия: {custom_clone}")
    print()

    # Тестирование наследования
    print("6. Тестирование наследования:")
    original_employee = Employee(
        name="Анна Сидорова",
        age=28,
        position="Разработчик",
        salary=100000,
        hobbies=["йога", "рисование"],
        metadata={"team": "backend"}
    )
    original_employee.add_skill("Python")
    original_employee.add_skill("Django")

    employee_copy = original_employee.deep_clone()
    print(f"Оригинальный сотрудник: {original_employee}")
    print(f"Копия сотрудника: {employee_copy}")
    print()

    # Изменение копии сотрудника
    employee_copy.add_skill("JavaScript")
    employee_copy.salary = 120000
    print("После изменения копии:")
    print(f"Оригинальный сотрудник: {original_employee}")
    print(f"Копия сотрудника: {employee_copy}")
    print()

    # Тестирование реестра прототипов
    print("7. Тестирование реестра прототипов:")
    registry = PrototypeRegistry()

    # Регистрация прототипов
    registry.register_prototype("default_person", Person("Default", 0))
    registry.register_prototype("senior_dev", original_person)
    registry.register_prototype("backend_dev", original_employee)

    print("Зарегистрированные прототипы:", registry.list_prototypes())

    # Получение прототипов из реестра
    default_person = registry.get_deep_prototype("default_person")
    senior_dev_copy = registry.get_deep_prototype("senior_dev")

    print(f"Прототип по умолчанию: {default_person}")
    print(f"Копия senior разработчика: {senior_dev_copy}")
    print()

    # JSON представление
    print("8. JSON представление объектов:")
    print("Оригинальный person JSON:")
    print(original_person.to_json())
    print("\nОригинальный employee JSON:")
    print(original_employee.to_json())


def additional_tests():
    print("\n=== Дополнительные тесты ===\n")

    # Тест вложенных объектов
    print("1. Тест с вложенными объектами:")
    complex_person = Person(
        name="Тестовый",
        age=99,
        hobbies=["сложное", "хобби"],
        metadata={
            "nested": {
                "level1": {
                    "level2": "глубокое значение"
                }
            },
            "list": [1, 2, 3, [4, 5]]
        }
    )

    complex_copy = complex_person.deep_clone()

    # Изменяем глубоко вложенные данные
    complex_person.metadata["nested"]["level1"]["level2"] = "измененное значение"
    complex_person.metadata["list"][3].append(6)

    print("Оригинал после глубоких изменений:")
    print(complex_person.metadata)
    print("Копия после глубоких изменений оригинала:")
    print(complex_copy.metadata)
    print("Разные объекты:", complex_person.metadata is not complex_copy.metadata)
    print()

    # Тест производительности
    print("2. Тест производительности (клонирование 1000 объектов):")
    import time

    test_person = Person("Test", 25, ["hobby1", "hobby2"])

    # Поверхностное копирование
    start_time = time.time()
    for _ in range(1000):
        test_person.clone()
    shallow_time = time.time() - start_time

    # Глубокое копирование
    start_time = time.time()
    for _ in range(1000):
        test_person.deep_clone()
    deep_time = time.time() - start_time

    print(f"Время 1000 поверхностных копий: {shallow_time:.4f} сек")
    print(f"Время 1000 глубоких копий: {deep_time:.4f} сек")
    print(f"Разница: {deep_time / shallow_time:.2f}x")
    print()

    # Тест исключений
    print("3. Тест обработки исключений:")
    registry = PrototypeRegistry()

    try:
        registry.get_prototype("nonexistent")
    except ValueError as e:
        print(f"Ожидаемая ошибка: {e}")

    # Тест с пустыми данными
    empty_person = Person("", 0, [], {})
    empty_copy = empty_person.deep_clone()
    print(f"Пустой оригинал: {empty_person}")
    print(f"Пустая копия: {empty_copy}")
    print("Разные объекты:", empty_person is not empty_copy)


if __name__ == "__main__":
    test_prototype_pattern()
    additional_tests()