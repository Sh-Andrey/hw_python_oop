import datetime as dt


class Record:
    """
    Создаем записи.
    Свойства класса:
    - число amount (денежная сумма или количество килокалорий);
    - комментарий comment, поясняющий, на что потрачены деньги
    или откуда взялись калории;
    - дату создания записи date (передаётся в явном виде в конструктор,
    либо присваивается значение по умолчанию — текущая дата).
    """

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.datetime.now().date()
        else:
            self.date = dt.datetime.strptime(date, "%d.%m.%Y").date()


class Calculator:
    def __init__(self, limit):
        """
        Общая функциональностью для классов CashCalories и Calories.
        - число limit (дневной лимит трат/калорий, который задал пользователь);
        - для хранение записей, создаем пустой список records.
        """

        self.limit = limit
        self.records = []

    def add_record(self, record):
        """
        Метод добавляет и сохраняет новые зиписи
        о деньгах/калориях в список records.
        """

        self.records.append(record)

    def get_today_stats(self):
        """
        Метод считает, сколько денег/калорий уже съедено сегодня.
        """

        count = 0
        for record in self.records:
            if record.date == dt.datetime.now().date():
                count += record.amount
        return count

    def get_week_stats(self):
        """
        Метод считает, сколько денег/калорий потрачено за последние 7 дней.
        """

        count = 0
        week = dt.datetime.now().date() - dt.timedelta(days=7)
        for record in self.records:
            if week <= record.date <= dt.datetime.now().date():
                count += record.amount
        return count


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        """
        Метод определяет, сколько ещё калорий можно/нужно получить сегодня.
        """

        calories_today = self.limit - self.get_today_stats()
        if calories_today > 0:
            return ("Сегодня можно съесть что-нибудь ещё,"
                    " но с общей калорийностью не более "
                    f"{calories_today} кКал")
        return "Хватит есть!"


class CashCalculator(Calculator):
    USD_RATE = 73.45
    EURO_RATE = 87.34
    RUB_RATE = 1.00

    def get_today_cash_remained(self, currency):
        """
        Метод возвращает сообщения о состоянии дневного баланса.
        """

        cash_sum = self.limit - self.get_today_stats()
        cash_type = ""

        if currency == "usd":
            cash_sum /= self.USD_RATE
            cash_type = "USD"
        elif currency == "eur":
            cash_sum /= self.EURO_RATE
            cash_type = "Euro"
        elif currency == "rub":
            cash_sum /= self.RUB_RATE
            cash_type = "руб"

        cash_sum = round(cash_sum, 2)
        if cash_sum == 0:
            return "Денег нет, держись"
        elif cash_sum < 0:
            return ("Денег нет, держись: твой долг - "
                    "{:.2f}".format(-cash_sum) + f" {cash_type}")
        return f"На сегодня осталось {cash_sum} {cash_type}"
