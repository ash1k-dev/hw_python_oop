from typing import Type, Dict
from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE: str = ('Тип тренировки: {training_type}; '
                    'Длительность: {duration:.3f} ч.; '
                    'Дистанция: {distance:.3f} км; '
                    'Ср. скорость: {speed:.3f} км/ч; '
                    'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    """Константа для перевода значений из метров в километры"""
    M_IN_KM = 1000
    """Количество минут в часе"""
    MINUTES_IN_HOUR = 60
    """Расстояние, которое спортсмен преодолевает за один шаг """
    LEN_STEP = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.action * self.LEN_STEP / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    """Не нашел значения этих коэффициентов для их осмысленного названия"""
    """Первый коэффициент для расчета каллорий."""
    COEFF_CALORIE_FOR_RUN_1 = 18
    """Второй коэффициент для расчета каллорий."""
    COEFF_CALORIE_FOR_RUN_2 = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.COEFF_CALORIE_FOR_RUN_1 * self.get_mean_speed()
                 - self.COEFF_CALORIE_FOR_RUN_2) * self.weight
                / self.M_IN_KM * (self.duration * self.MINUTES_IN_HOUR))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    """Первый коэффициент для расчета каллорий."""
    COEFF_CALORIE_FOR_WALK_1 = 0.035
    """Второй коэффициент для расчета каллорий."""
    COEFF_CALORIE_FOR_WALK_2 = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.COEFF_CALORIE_FOR_WALK_1 * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * self.COEFF_CALORIE_FOR_WALK_2 * self.weight) * (self.duration
                * self.MINUTES_IN_HOUR))


class Swimming(Training):
    """Тренировка: плавание."""

    """Расстояние, которое спортсмен преодолевает за один гребок."""
    LEN_STEP = 1.38
    """Первый коэффициент для расчета каллорий."""
    COEFF_CALORIE_FOR_SWIM_1 = 1.1
    """Второй коэффициент для расчета каллорий."""
    COEFF_CALORIE_FOR_SWIM_2 = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed()
                + self.COEFF_CALORIE_FOR_SWIM_1)
                * self.COEFF_CALORIE_FOR_SWIM_2 * self.weight)


def read_package(workout_type: str, data: list[int]):
    """Прочитать данные полученные от датчиков."""

    workout_types: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    try:
        if workout_type in workout_types:
            return workout_types[workout_type](*data)
    except ValueError:
        print("В списке нет подходящего значения")


def main(training: Training) -> None:
    """Главная функция."""

    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
