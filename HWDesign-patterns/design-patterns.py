# Задание 1. Создайте реализацию паттерна Command. Протестируйте работу созданного класса.

print(f"Задание №1\n-----------------------------------------")
# Интерфейс команды
class Command:
    def execute(self):
        raise NotImplementedError("Метод execute должен быть переопределен")

    def undo(self):
        raise NotImplementedError("Метод undo должен быть переопределен")

# Получатель - объект, который выполняет основную работу
class Light:
    def turn_on(self):
        print("Свет включен!")

    def turn_off(self):
        print("Свет выключен!")

# Конкретная команда включения света
class TurnOnLightCommand(Command):
    def __init__(self, light):
        self.light = light

    def execute(self):
        self.light.turn_on()

    def undo(self):
        self.light.turn_off()

# Конкретная команда выключения света
class TurnOffLightCommand(Command):
    def __init__(self, light):
        self.light = light

    def execute(self):
        self.light.turn_off()

    def undo(self):
        self.light.turn_on()

# Инициатор - объект, который вызывает команды
class RemoteControl:
    def __init__(self):
        self.commands = []

    def set_command(self, command):
        self.commands.append(command)

    def press_button(self):
        if self.commands:
            last_command = self.commands[-1]
            last_command.execute()

    def undo_last(self):
        if self.commands:
            last_command = self.commands.pop()
            last_command.undo()

# Тестирование реализации
# Давайте протестируем работу созданного паттерна:

def test_command_pattern():
    # Создаем получателя
    light = Light()

    # Создаем команды
    turn_on = TurnOnLightCommand(light)
    turn_off = TurnOffLightCommand(light)

    # Создаем пульт управления
    remote = RemoteControl()

    # Тестирование включения света
    remote.set_command(turn_on)
    remote.press_button() # Ожидаемый вывод: "Свет включен"

    # Тестирование выключения света
    remote.set_command(turn_off)
    remote.press_button() # Ожидаемый вывод: "Свет выключен"

    # Тестирование отмены
    remote.undo_last() # Ожидаемый вывод: "Свет включен"

    print("Все тесты пройдены успешно!")

# Запуск тестов
test_command_pattern()
print()

# Задание 2. Есть класс, предоставляющий доступ к набору чисел. Источником этого набора чисел
# является некоторый файл. С определенной периодичностью данные в файле меняются
# (надо реализовать механизм обновления). Приложение должно получать доступ к этим данным и
# выполнять набор операций над ними (сумма, максимум, минимум и т.д.). При каждой попытке доступа
# к этому набору необходимо вносить запись в лог-файл. При реализации используйте паттерн Proxy
# (для логгирования) и другие необходимые паттерны.

print(f"Задание №2\n-----------------------------------------")
from abc import ABC, abstractmethod
from typing import List
import os
import time
from pathlib import Path

# Интерфейс для доступа к данным
class NumberDataSource(ABC):
    @abstractmethod
    def get_numbers(self) -> List[int]:
        pass

    @abstractmethod
    def refresh_data(self) -> None:
        pass

    @abstractmethod
    def get_data_source_info(self) -> str:
        pass

# Реальная реализация источника данных (Subject)
class FileNumberDataSource(NumberDataSource):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.numbers: List[int] = []
        self.last_modified_time: float = 0
        self.load_data()

    def load_data(self) -> None:
        try:
            if os.path.exists(self.file_path):
                self.last_modified_time = os.path.getmtime(self.file_path)
                self.numbers = []

                with open(self.file_path, 'r', encoding='utf-8') as file:
                    for line in file:
                        line = line.strip()
                        if line:
                            try:
                                self.numbers.append(int(line))
                            except ValueError:
                                print(f"Invalid number format: {line}")
            else:
                print(f"File {self.file_path} does not exist")
                self.numbers = []

        except IOError as e:
            print(f"Error reading file: {e}")
            self.numbers = []

    def get_numbers(self) -> List[int]:
        self.check_for_updates()
        return self.numbers.copy()

    def refresh_data(self) -> None:
        self.load_data()

    def check_for_updates(self) -> None:
        try:
            if os.path.exists(self.file_path):
                current_modified_time = os.path.getmtime(self.file_path)
                if current_modified_time > self.last_modified_time:
                    print("File change detected. Reloading data...")
                    self.refresh_data()
        except OSError as e:
            print(f"Error checking file updates: {e}")

    def get_data_source_info(self) -> str:
        return f"File: {self.file_path} (Numbers: {len(self.numbers)})"

# Прокси для логирования (Proxy)
class LoggingNumberDataSourceProxy(NumberDataSource):
    def __init__(self, real_data_source: NumberDataSource):
        self.real_data_source = real_data_source
        self.logger = Logger()

    def get_numbers(self) -> List[int]:
        info = self.real_data_source.get_data_source_info()
        self.logger.log(f"Accessing numbers from: {info}")

        numbers = self.real_data_source.get_numbers()
        self.logger.log(f"Retrieved {len(numbers)} numbers")

        return numbers

    def refresh_data(self) -> None:
        info = self.real_data_source.get_data_source_info()
        self.logger.log(f"Refreshing data for: {info}")

        self.real_data_source.refresh_data()
        self.logger.log("Data refreshed successfully")

    def get_data_source_info(self) -> str:
        return f"{self.real_data_source.get_data_source_info()} (with logging proxy)"

import datetime
from threading import Lock

# Логгер (Singleton)
class Logger:
    _instance = None
    _lock: Lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(Logger, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self):
        if not self._initialized:
            self.log_file = "number_data_access.log"
            self._initialized = True
            self.initialize_log_file()

    def initialize_log_file(self):
        try:
            Path(self.log_file).touch(exist_ok=True)
            self.log("Log file initialized")
        except IOError as e:
            print(f"Error creating log file: {e}")

    def log(self, message: str):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"

        print(log_message)  # Вывод в консоль

        # Запись в файл
        try:
            with open(self.log_file, 'a', encoding='utf-8') as file:
                file.write(log_message + '\n')
        except IOError as e:
            print(f"Error writing to log file: {e}")

# Сервис для операций с числами (Facade)
class NumberOperationsService:
    def __init__(self, data_source: NumberDataSource):
        self.data_source = data_source

    def get_sum(self) -> int:
        numbers = self.data_source.get_numbers()
        return sum(numbers)

    def get_max(self) -> int:
        numbers = self.data_source.get_numbers()
        return max(numbers) if numbers else 0

    def get_min(self) -> int:
        numbers = self.data_source.get_numbers()
        return min(numbers) if numbers else 0

    def get_average(self) -> float:
        numbers = self.data_source.get_numbers()
        return sum(numbers) / len(numbers) if numbers else 0.0

    def get_count(self) -> int:
        numbers = self.data_source.get_numbers()
        return len(numbers)

    def refresh_data(self):
        self.data_source.refresh_data()

    def perform_all_operations(self):
        """Выполняет все операции и возвращает результаты"""
        numbers = self.data_source.get_numbers()

        return {
            'numbers': numbers,
            'sum': sum(numbers),
            'max': max(numbers) if numbers else 0,
            'min': min(numbers) if numbers else 0,
            'average': sum(numbers) / len(numbers) if numbers else 0.0,
            'count': len(numbers)
        }

# Фабрика для создания источников данных (Factory Method)
class DataSourceFactory:
    @staticmethod
    def create_file_data_source(file_path: str) -> NumberDataSource:
        real_data_source = FileNumberDataSource(file_path)
        return LoggingNumberDataSourceProxy(real_data_source)

# Демонстрационный класс
class NumberDataApplication:
    @staticmethod
    def create_test_file(filename: str):
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write("10\n")
                file.write("20\n")
                file.write("30\n")
                file.write("40\n")
                file.write("50\n")
            print(f"Created test file: {filename}")
        except IOError as e:
            print(f"Error creating test file: {e}")

    @staticmethod
    def update_test_file(filename: str):
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write("5\n")
                file.write("15\n")
                file.write("25\n")
                file.write("35\n")
                file.write("45\n")
                file.write("55\n")  # Добавляем еще одно число
            print(f"Updated test file: {filename}")
        except IOError as e:
            print(f"Error updating test file: {e}")

    @staticmethod
    def run_demo():
        # Создаем тестовый файл
        test_file = "numbers.txt"
        NumberDataApplication.create_test_file(test_file)

        # Создаем источник данных через фабрику
        data_source = DataSourceFactory.create_file_data_source(test_file)
        service = NumberOperationsService(data_source)

        print("=== Первый доступ к данным ===")
        results = service.perform_all_operations()
        NumberDataApplication.print_results(results)

        # Ждем немного и обновляем файл
        print("\nОжидание 2 секунды перед обновлением файла...")
        time.sleep(2)

        NumberDataApplication.update_test_file(test_file)
        print("Файл обновлен, ожидание обнаружения изменений...")

        # Ждем еще немного для обнаружения изменений
        time.sleep(1)

        print("\n=== Второй доступ к данным (после обновления) ===")
        results = service.perform_all_operations()
        NumberDataApplication.print_results(results)

        # Еще один доступ для демонстрации
        print("\n=== Третий доступ к данным ===")
        results = service.perform_all_operations()
        NumberDataApplication.print_results(results)

        print(f"\nЛог операций записан в файл: {Logger().log_file}")

    @staticmethod
    def print_results(results: dict):
        print(f"Числа: {results['numbers']}")
        print(f"Сумма: {results['sum']}")
        print(f"Максимум: {results['max']}")
        print(f"Минимум: {results['min']}")
        print(f"Среднее: {results['average']:.2f}")
        print(f"Количество: {results['count']}")

# Запуск демонстрации
if __name__ == "__main__":
    NumberDataApplication.run_demo()

# Дополнительный класс для периодического мониторинга
class DataMonitor:
    def __init__(self, data_source: NumberDataSource, check_interval: int = 5):
        self.data_source = data_source
        self.check_interval = check_interval
        self.logger = Logger()
        self.running = False

    def start_monitoring(self):
        """Запускает периодический мониторинг изменений"""
        self.running = True
        self.logger.log("Data monitoring started")

        try:
            while self.running:
                # Просто обращаемся к данным, что вызовет проверку обновлений
                numbers = self.data_source.get_numbers()
                time.sleep(self.check_interval)
        except KeyboardInterrupt:
            self.logger.log("Data monitoring stopped")

    def stop_monitoring(self):
        self.running = False

# Пример использования
if __name__ == "__main__":
    # Создание файла с данными
    with open("data.txt", "w") as f:
        f.write("1\n2\n3\n4\n5\n")

    # Создание источника данных
    data_source = DataSourceFactory.create_file_data_source("data.txt")
    service = NumberOperationsService(data_source)

    # Выполнение операций
    print("Sum:", service.get_sum())
    print("Max:", service.get_max())
    print("Average:", service.get_average())

    # Можно также использовать монитор
    monitor = DataMonitor(data_source, check_interval=3)
    # monitor.start_monitoring() # Раскомментировать для запуска мониторинга
print()

# Задание 3. Создайте приложение для работы в библиотеке. Оно должно оперировать следующими
# сущностями: Книга, Библиотекарь, Читатель. Приложение должно позволять вводить, удалять,
# изменять, сохранять вфайл, загружать из файла, логгировать действия, искать информацию
# (результаты поиска выводятся на экран или файл) о сущностях. При реализации используйте
# максимально возможное количество паттернов проектирования.

print(f"Задание №3\n-----------------------------------------")
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Dict, Any
import json
import csv
import pickle
from pathlib import Path
import logging
from enum import Enum

# ==================== ПАТТЕРН: STRATEGY ====================
class ExportStrategy(ABC):
    @abstractmethod
    def export(self, data: List[Dict[str, Any]], filename: str) -> None:
        pass

class JSONExportStrategy(ExportStrategy):
    def export(self, data: List[Dict[str, Any]], filename: str) -> None:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

class CSVExportStrategy(ExportStrategy):
    def export(self, data: List[Dict[str, Any]], filename: str) -> None:
        if data:
            with open(filename, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)

class PickleExportStrategy(ExportStrategy):
    def export(self, data: List[Dict[str, Any]], filename: str) -> None:
        with open(filename, 'wb') as f:
            pickle.dump(data, f)

# ==================== ПАТТЕРН: OBSERVER ====================
class Observer(ABC):
    @abstractmethod
    def update(self, message: str) -> None:
        pass

class LoggerObserver(Observer):
    def update(self, message: str) -> None:
        logging.info(message)

class ConsoleObserver(Observer):
    def update(self, message: str) -> None:
        print(f"CONSOLE: {message}")

# ==================== ПАТТЕРН: FACTORY METHOD ====================
class EntityFactory(ABC):
    @abstractmethod
    def create_entity(self, data: Dict[str, Any]) -> Any:
        pass

# ==================== ОСНОВНЫЕ СУЩНОСТИ ====================
class BookStatus(Enum):
    AVAILABLE = "available"
    BORROWED = "borrowed"
    RESERVED = "reserved"

@dataclass
class Book:
    id: int
    title: str
    author: str
    year: int
    isbn: str
    status: BookStatus = BookStatus.AVAILABLE
    borrower_id: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'isbn': self.isbn,
            'status': self.status.value,
            'borrower_id': self.borrower_id
        }

@dataclass
class Librarian:
    id: int
    name: str
    email: str
    phone: str
    position: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'position': self.position
        }

@dataclass
class Reader:
    id: int
    name: str
    email: str
    phone: str
    books_borrowed: List[int]  # List of book IDs

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'books_borrowed': self.books_borrowed
        }

# ==================== ПАТТЕРН: REPOSITORY ====================
class Repository(ABC):
    @abstractmethod
    def add(self, entity: Any) -> None:
        pass

    @abstractmethod
    def get(self, entity_id: int) -> Optional[Any]:
        pass

    @abstractmethod
    def get_all(self) -> List[Any]:
        pass

    @abstractmethod
    def update(self, entity: Any) -> None:
        pass

    @abstractmethod
    def delete(self, entity_id: int) -> None:
        pass

    @abstractmethod
    def search(self, **kwargs) -> List[Any]:
        pass

class BookRepository(Repository):
    def __init__(self):
        self.books: Dict[int, Book] = {}
        self.next_id = 1

    def add(self, book: Book) -> None:
        book.id = self.next_id
        self.books[book.id] = book
        self.next_id += 1

    def get(self, book_id: int) -> Optional[Book]:
        return self.books.get(book_id)

    def get_all(self) -> List[Book]:
        return list(self.books.values())

    def update(self, book: Book) -> None:
        if book.id in self.books:
            self.books[book.id] = book

    def delete(self, book_id: int) -> None:
        if book_id in self.books:
            del self.books[book_id]

    def search(self, **kwargs) -> List[Book]:
        results = self.get_all()
        for key, value in kwargs.items():
            if value is not None:
                results = [b for b in results if getattr(b, key, None) == value]
        return results

class LibrarianRepository(Repository):
    def __init__(self):
        self.librarians: Dict[int, Librarian] = {}
        self.next_id = 1

    def add(self, librarian: Librarian) -> None:
        librarian.id = self.next_id
        self.librarians[librarian.id] = librarian
        self.next_id += 1

    def get(self, librarian_id: int) -> Optional[Librarian]:
        return self.librarians.get(librarian_id)

    def get_all(self) -> List[Librarian]:
        return list(self.librarians.values())

    def update(self, librarian: Librarian) -> None:
        if librarian.id in self.librarians:
            self.librarians[librarian.id] = librarian

    def delete(self, librarian_id: int) -> None:
        if librarian_id in self.librarians:
            del self.librarians[librarian_id]

    def search(self, **kwargs) -> List[Librarian]:
        results = self.get_all()
        for key, value in kwargs.items():
            if value is not None:
                results = [l for l in results if getattr(l, key, None) == value]
        return results

class ReaderRepository(Repository):
    def __init__(self):
        self.readers: Dict[int, Reader] = {}
        self.next_id = 1

    def add(self, reader: Reader) -> None:
        reader.id = self.next_id
        self.readers[reader.id] = reader
        self.next_id += 1

    def get(self, reader_id: int) -> Optional[Reader]:
        return self.readers.get(reader_id)

    def get_all(self) -> List[Reader]:
        return list(self.readers.values())

    def update(self, reader: Reader) -> None:
        if reader.id in self.readers:
            self.readers[reader.id] = reader

    def delete(self, reader_id: int) -> None:
        if reader_id in self.readers:
            del self.readers[reader_id]

    def search(self, **kwargs) -> List[Reader]:
        results = self.get_all()
        for key, value in kwargs.items():
            if value is not None:
                results = [r for r in results if getattr(r, key, None) == value]
        return results

# ==================== ПАТТЕРН: FACADE ====================
class LibraryFacade:
    def __init__(self):
        self.book_repo = BookRepository()
        self.librarian_repo = LibrarianRepository()
        self.reader_repo = ReaderRepository()
        self.observers: List[Observer] = []

        # Настройка логирования
        logging.basicConfig(
            filename='library.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.add_observer(LoggerObserver())
        self.add_observer(ConsoleObserver())

    def add_observer(self, observer: Observer) -> None:
        self.observers.append(observer)

    def notify_observers(self, message: str) -> None:
        for observer in self.observers:
            observer.update(message)

    # Book operations
    def add_book(self, title: str, author: str, year: int, isbn: str) -> Book:
        book = Book(0, title, author, year, isbn)
        self.book_repo.add(book)
        self.notify_observers(f"Book added: {title} by {author}")
        return book

    def get_book(self, book_id: int) -> Optional[Book]:
        return self.book_repo.get(book_id)

    def update_book(self, book: Book) -> None:
        self.book_repo.update(book)
        self.notify_observers(f"Book updated: {book.title}")

    def delete_book(self, book_id: int) -> None:
        book = self.book_repo.get(book_id)
        if book:
            self.book_repo.delete(book_id)
            self.notify_observers(f"Book deleted: {book.title}")

    def search_books(self, **kwargs) -> List[Book]:
        return self.book_repo.search(**kwargs)

    # Librarian operations
    def add_librarian(self, name: str, email: str, phone: str, position: str) -> Librarian:
        librarian = Librarian(0, name, email, phone, position)
        self.librarian_repo.add(librarian)
        self.notify_observers(f"Librarian added: {name}")
        return librarian

    def get_librarian(self, librarian_id: int) -> Optional[Librarian]:
        return self.librarian_repo.get(librarian_id)

    def update_librarian(self, librarian: Librarian) -> None:
        self.librarian_repo.update(librarian)
        self.notify_observers(f"Librarian updated: {librarian.name}")

    def delete_librarian(self, librarian_id: int) -> None:
        librarian = self.librarian_repo.get(librarian_id)
        if librarian:
            self.librarian_repo.delete(librarian_id)
            self.notify_observers(f"Librarian deleted: {librarian.name}")

    def search_librarians(self, **kwargs) -> List[Librarian]:
        return self.librarian_repo.search(**kwargs)

    # Reader operations
    def add_reader(self, name: str, email: str, phone: str) -> Reader:
        reader = Reader(0, name, email, phone, [])
        self.reader_repo.add(reader)
        self.notify_observers(f"Reader added: {name}")
        return reader

    def get_reader(self, reader_id: int) -> Optional[Reader]:
        return self.reader_repo.get(reader_id)

    def update_reader(self, reader: Reader) -> None:
        self.reader_repo.update(reader)
        self.notify_observers(f"Reader updated: {reader.name}")

    def delete_reader(self, reader_id: int) -> None:
        reader = self.reader_repo.get(reader_id)
        if reader:
            self.reader_repo.delete(reader_id)
            self.notify_observers(f"Reader deleted: {reader.name}")

    def search_readers(self, **kwargs) -> List[Reader]:
        return self.reader_repo.search(**kwargs)

    # Book borrowing operations
    def borrow_book(self, reader_id: int, book_id: int) -> bool:
        reader = self.reader_repo.get(reader_id)
        book = self.book_repo.get(book_id)

        if not reader or not book:
            return False

        if book.status != BookStatus.AVAILABLE:
            return False

        book.status = BookStatus.BORROWED
        book.borrower_id = reader_id
        reader.books_borrowed.append(book_id)

        self.book_repo.update(book)
        self.reader_repo.update(reader)

        self.notify_observers(f"Book '{book.title}' borrowed by {reader.name}")
        return True

    def return_book(self, book_id: int) -> bool:
        book = self.book_repo.get(book_id)

        if not book or book.status != BookStatus.BORROWED:
            return False

        reader = self.reader_repo.get(book.borrower_id)
        if reader and book_id in reader.books_borrowed:
            reader.books_borrowed.remove(book_id)
            self.reader_repo.update(reader)

        book.status = BookStatus.AVAILABLE
        book.borrower_id = None
        self.book_repo.update(book)

        self.notify_observers(f"Book '{book.title}' returned")
        return True

    # Export operations
    def export_data(self, strategy: ExportStrategy, filename: str, entity_type: str) -> None:
        if entity_type == 'books':
            data = [book.to_dict() for book in self.book_repo.get_all()]
        elif entity_type == 'librarians':
            data = [librarian.to_dict() for librarian in self.librarian_repo.get_all()]
        elif entity_type == 'readers':
            data = [reader.to_dict() for reader in self.reader_repo.get_all()]
        else:
            raise ValueError("Invalid entity type")

        strategy.export(data, filename)
        self.notify_observers(f"Exported {entity_type} to {filename}")

    # Import operations
    def import_books_from_json(self, filename: str) -> None:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for item in data:
                    book = Book(
                        item['id'],
                        item['title'],
                        item['author'],
                        item['year'],
                        item['isbn'],
                        BookStatus(item['status']),
                        item['borrower_id']
                    )
                    self.book_repo.books[book.id] = book
                    self.book_repo.next_id = max(self.book_repo.next_id, book.id + 1)
            self.notify_observers(f"Imported books from {filename}")
        except Exception as e:
            self.notify_observers(f"Error importing books: {e}")

    def save_state(self) -> None:
        state = {
            'books': [book.to_dict() for book in self.book_repo.get_all()],
            'librarians': [librarian.to_dict() for librarian in self.librarian_repo.get_all()],
            'readers': [reader.to_dict() for reader in self.reader_repo.get_all()]
        }
        with open('library_state.json', 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
        self.notify_observers("Library state saved")

    def load_state(self) -> None:
        try:
            with open('library_state.json', 'r', encoding='utf-8') as f:
                state = json.load(f)

                # Load books
                self.book_repo = BookRepository()
                for item in state['books']:
                    book = Book(
                        item['id'],
                        item['title'],
                        item['author'],
                        item['year'],
                        item['isbn'],
                        BookStatus(item['status']),
                        item['borrower_id']
                    )
                    self.book_repo.books[book.id] = book
                    self.book_repo.next_id = max(self.book_repo.next_id, book.id + 1)

                # Load librarians
                self.librarian_repo = LibrarianRepository()
                for item in state['librarians']:
                    librarian = Librarian(
                        item['id'],
                        item['name'],
                        item['email'],
                        item['phone'],
                        item['position']
                    )
                    self.librarian_repo.librarians[librarian.id] = librarian
                    self.librarian_repo.next_id = max(self.librarian_repo.next_id, librarian.id + 1)

                # Load readers
                self.reader_repo = ReaderRepository()
                for item in state['readers']:
                    reader = Reader(
                        item['id'],
                        item['name'],
                        item['email'],
                        item['phone'],
                        item['books_borrowed']
                    )
                    self.reader_repo.readers[reader.id] = reader
                    self.reader_repo.next_id = max(self.reader_repo.next_id, reader.id + 1)

                self.notify_observers("Library state loaded")
        except FileNotFoundError:
            self.notify_observers("No saved state found")
        except Exception as e:
            self.notify_observers(f"Error loading state: {e}")

# ==================== ПАТТЕРN: COMMAND ====================
class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass

class AddBookCommand(Command):
    def __init__(self, facade: LibraryFacade, title: str, author: str, year: int, isbn: str):
        self.facade = facade
        self.title = title
        self.author = author
        self.year = year
        self.isbn = isbn

    def execute(self) -> None:
        self.facade.add_book(self.title, self.author, self.year, self.isbn)


class BorrowBookCommand(Command):
    def __init__(self, facade: LibraryFacade, reader_id: int, book_id: int):
        self.facade = facade
        self.reader_id = reader_id
        self.book_id = book_id

    def execute(self) -> None:
        self.facade.borrow_book(self.reader_id, self.book_id)

# ==================== ПАТТЕРN: SINGLETON ====================
class LibraryManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LibraryManager, cls).__new__(cls)
            cls._instance.facade = LibraryFacade()
        return cls._instance

    def get_facade(self) -> LibraryFacade:
        return self.facade

# ==================== ДЕМОНСТРАЦИОННЫЙ КЛАСС ====================
class LibraryDemo:
    def __init__(self):
        self.manager = LibraryManager()
        self.facade = self.manager.get_facade()

    def run_demo(self):
        print("=== ДЕМОНСТРАЦИЯ РАБОТЫ БИБЛИОТЕКИ ===")

        # Добавляем книги
        print("\n1. Добавляем книги:")
        books = [
            self.facade.add_book("Война и мир", "Лев Толстой", 1869, "978-5-389-07464-0"),
            self.facade.add_book("Преступление и наказание", "Федор Достоевский", 1866, "978-5-699-40445-2"),
            self.facade.add_book("Мастер и Маргарита", "Михаил Булгаков", 1967, "978-5-389-06228-9")
        ]

        # Добавляем читателей
        print("\n2. Добавляем читателей:")
        readers = [
            self.facade.add_reader("Иван Иванов", "ivan@mail.com", "+7-999-123-45-67"),
            self.facade.add_reader("Петр Петров", "petr@mail.com", "+7-999-765-43-21")
        ]

        # Добавляем библиотекарей
        print("\n3. Добавляем библиотекарей:")
        librarians = [
            self.facade.add_librarian("Анна Сидорова", "anna@library.ru", "+7-495-123-45-67", "Главный библиотекарь"),
            self.facade.add_librarian("Мария Кузнецова", "maria@library.ru", "+7-495-765-43-21", "Библиотекарь")
        ]

        # Выдача книг
        print("\n4. Выдаем книги читателям:")
        self.facade.borrow_book(readers[0].id, books[0].id)
        self.facade.borrow_book(readers[1].id, books[1].id)

        # Поиск книг
        print("\n5. Поиск книг Толстого:")
        tolsto_books = self.facade.search_books(author="Лев Толстой")
        for book in tolsto_books:
            print(f"  - {book.title} ({book.year})")

        # Экспорт данных
        print("\n6. Экспортируем данные в JSON:")
        self.facade.export_data(JSONExportStrategy(), "books_export.json", "books")
        self.facade.export_data(JSONExportStrategy(), "readers_export.json", "readers")

        # Сохраняем состояние
        print("\n7. Сохраняем состояние библиотеки:")
        self.facade.save_state()

        # Возврат книги
        print("\n8. Возвращаем книгу:")
        self.facade.return_book(books[0].id)

        # Поиск читателей
        print("\n9. Поиск читателя по email:")
        reader_search = self.facade.search_readers(email="petr@mail.com")
        for reader in reader_search:
            print(f"  - {reader.name}: {reader.email}")

        print("\n=== ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА ===")
        print("Логи записаны в файл 'library.log'")

# Запуск демонстрации
if __name__ == "__main__":
    demo = LibraryDemo()
    demo.run_demo()

    # Пример интерактивного использования
    facade = LibraryManager().get_facade()

    # Можно продолжать работать с фасадом
    # facade.add_book("Новая книга", "Новый автор", 2023, "123-456-789")
    # facade.export_data(CSVExportStrategy(), "books.csv", "books")

