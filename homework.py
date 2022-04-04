from typing import Dict, List, Callable, ClassVar
from dataclasses import dataclass, asdict


SWM: str = 'SWM'
RUN: str = 'RUN'
WLK: str = 'WLK'


@dataclass()
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    TEMPLATE_MESSAGE: ClassVar[str] = ("Тип тренировки: {training_type}; "
                                       "Длительность: {duration:.3f} ч.; "
                                       "Дистанция: {distance:.3f} км; "
                                       "Ср. скорость: {speed:.3f} км/ч; "
                                       "Потрачено ккал: {calories:.3f}.")

    def get_message(self) -> str:
        """Создаст сообщение для выода."""
        return self.TEMPLATE_MESSAGE.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""

    action: int
    duration: float
    weight: float

    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[float] = 1000
    HOURS_PER_MINUTE: ClassVar[float] = 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(f'Исключение в {self.__class__.__name__}.')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message = InfoMessage(self.__class__.__name__,
                              self.duration,
                              self.get_distance(),
                              self.get_mean_speed(),
                              self.get_spent_calories())
        return message


@dataclass
class Running(Training):
    """Тренировка: бег."""

    COEFF_CALORIE_1: ClassVar[float] = 18
    COEFF_CALORIE_2: ClassVar[float] = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий для бега."""
        return ((self.COEFF_CALORIE_1 * self.get_mean_speed()
                 - self.COEFF_CALORIE_2) * self.weight / self.M_IN_KM
                * self.duration * self.HOURS_PER_MINUTE)


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    height: float

    IN_SQUARE: ClassVar[float] = 2
    COEFF_CALORIE_1: ClassVar[float] = 0.035
    COEFF_CALORIE_2: ClassVar[float] = 0.029

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий для бега."""
        return (self.COEFF_CALORIE_1 * self.weight
                + (self.get_mean_speed() ** self.IN_SQUARE
                   // self.height) * self.COEFF_CALORIE_2
                * self.weight) * self.duration * self.HOURS_PER_MINUTE


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    length_pool: float
    count_pool: int

    LEN_STEP: ClassVar[float] = 1.38
    COEF_ONE_FOR_CAL: ClassVar[float] = 1.1
    COEF_TWO_FOR_CAL: ClassVar[float] = 2

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения в бассейне."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.COEF_ONE_FOR_CAL)
                * self.COEF_TWO_FOR_CAL * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_of_training: Dict[str, Callable[[float], Training]] = {
        SWM: Swimming,
        RUN: Running,
        WLK: SportsWalking
    }

    if workout_type in type_of_training:
        return type_of_training[workout_type](*data)

    raise KeyError(f'Поданы неправильные входные данные. {workout_type}'
                   f'Правильные данные: {list(type_of_training.keys())}')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: List = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
