import datetime as dt
from typing import Optional, Dict, List, Tuple

DATE_FORMAT: str = "%d.%m.%Y"


class Record:
    """Объект для хранения записей о расходах.

    Атрибуты класса:
    - число amount (денежная сумма или количество килокалорий);
    - комментарий comment, поясняющий, на что потрачены деньги
    или откуда взялись калории;
    - дата создания записи (передаётся в явном виде в конструктор,
    либо присваивается значение по умолчанию — текущая дата).
    """

    def __init__(self,
                 amount: float,
                 comment: str,
                 date: Optional[str] = None) -> None:
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, DATE_FORMAT).date()


class Calculator:
    """Общая функциональность для классов
    CashCalculator и CaloriesCalculator.

    Атрибуты класса:
    - число limit (дневной лимит трат/калорий, который задал пользователь);
    - для хранения записей, создаем пустой список records.
    """
    def __init__(self, limit: float) -> None:
        self.limit = limit
        self.records: List[Record] = []

    def add_record(self, record: Record) -> None:
        """
        Метод добавляет записи о деньгах/калориях в список records.
        """
        self.records.append(record)

    def get_today_stats(self) -> float:
        """
        Метод считает, сколько денег/калорий уже съедено сегодня.
        """
        today = dt.date.today()
        count = sum(record.amount for record in self.records
                    if record.date == today)
        return count

    def get_week_stats(self) -> float:
        """
        Метод считает, сколько денег/калорий потрачено за последние 7 дней.
        """
        today = dt.date.today()
        week_ago = today - dt.timedelta(days=7)
        count = sum(record.amount for record in self.records
                    if week_ago < record.date <= today)
        return count

    def remainder_today(self) -> float:
        """
        Метод считает, сколько денег/калорий осталось на день.
        """
        return self.limit - self.get_today_stats()


class CaloriesCalculator(Calculator):

    def get_calories_remained(self) -> str:
        """
        Метод определяет, сколько ещё калорий можно/нужно получить сегодня.
        """
        calories_today: float = self.remainder_today()
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
        Метод возвращает сообщения о состоянии дневного баланса
        в указанной валюте.
        """
        cash_sum: float = self.remainder_today()
        cash_currency: str = currency.lower()

        if cash_sum == 0:
            return "Денег нет, держись"

        currency_type: Dict[str, Tuple[float, str]] = {
            "usd": (self.USD_RATE, "USD"),
            "eur": (self.EURO_RATE, "Euro"),
            "rub": (self.RUB_RATE, "руб"),
        }

        if cash_currency not in currency_type:
            return f"{currency} такой валюты нету!"

        exchange_rate, cash_type = currency_type[currency]
        cash_sum: float = cash_sum / exchange_rate
        cash_sum = round(cash_sum, 2)

        if cash_sum < 0:
            amount_debt: float = abs(cash_sum)
            return ("Денег нет, держись: "
                    f"твой долг - {amount_debt} {cash_type}")
        return f"На сегодня осталось {cash_sum} {cash_type}"
