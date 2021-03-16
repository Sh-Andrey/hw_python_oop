import datetime as dt


class Record:
    """Создаем записи.

    Атрибуты класса:
    - число amount (денежная сумма или количество килокалорий);
    - комментарий comment, поясняющий, на что потрачены деньги
    или откуда взялись калории;
    - создания записи date (передаётся в явном виде в конструктор,
    либо присваивается значение по умолчанию — текущая дата).
    """
    def __init__(self, amount: float, comment: str, date=None) -> None:

        self.amount = amount
        self.comment = comment
        date_format: str = "%d.%m.%Y"
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, date_format).date()


class Calculator:

    def __init__(self, limit: float) -> None:
        """Общая функциональностью для классов
        CashCalculator и CaloriesCalculator.

        Атрибуты класса:
        - число limit (дневной лимит трат/калорий, который задал пользователь);
        - для хранение записей, создаем пустой список records.
        """
        self.limit = limit
        self.records: list = []

    def add_record(self, record: float) -> None:
        """
        Метод добавляет записи о деньгах/калориях в список records.
        """
        self.records.append(record)

    def get_today_stats(self) -> float:
        """
        Метод считает, сколько денег/калорий уже съедено сегодня.
        """
        date_now = dt.date.today()
        count = sum([record.amount for record in self.records
                     if record.date == date_now])
        return count

    def get_week_stats(self) -> float:
        """
        Метод считает, сколько денег/калорий потрачено за последние 7 дней.
        """
        date_now = dt.date.today()
        week = date_now - dt.timedelta(days=6)
        count = sum([record.amount for record in self.records
                     if date_now >= record.date >= week])
        return count

    def limit_today(self) -> float:
        """
        Метод считает, сколько денег/калорий осталось на день.
        """
        return self.limit - self.get_today_stats()


class CaloriesCalculator(Calculator):

    def get_calories_remained(self) -> str:
        """
        Метод определяет, сколько ещё калорий можно/нужно получить сегодня.
        """
        calories_today: float = self.limit_today()
        if calories_today > 0:
            return ("Сегодня можно съесть что-нибудь ещё,"
                    " но с общей калорийностью не более "
                    f"{calories_today} кКал")
        return "Хватит есть!"


class CashCalculator(Calculator):

    USD_RATE: float = 73.45
    EURO_RATE: float = 87.34
    RUB_RATE: float = 1.00

    def get_today_cash_remained(self, currency: str) -> str:
        """
        Метод возвращает сообщения о состоянии дневного баланса.
        """
        cash_sum: float = self.limit_today()
        cash_currency: str = currency.lower()
        cash_type: list = ["usd", "eur", "rub"]

        if cash_currency not in cash_type:
            return f"{currency} такой валюты нету!"

        if cash_sum == 0:
            return "Денег нет, держись"

        if cash_currency in cash_type:
            dict_currency = {
                "usd": (cash_sum / self.USD_RATE, "USD"),
                "eur": (cash_sum / self.EURO_RATE, "Euro"),
                "rub": (cash_sum / self.RUB_RATE, "руб"),
            }
            cash_dict: float = dict_currency[currency][0]
            type_dict: str = dict_currency[currency][1]
            cash_dict: float = abs(round(cash_dict, 2))

            if cash_sum < 0:
                return ("Денег нет, держись: "
                        f"твой долг - {cash_dict} {type_dict}")
            return f"На сегодня осталось {cash_dict} {type_dict}"
