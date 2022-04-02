from typing import Dict, List, Callable


class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def __init__(self, training_type, duration, distance,
                 speed, calories) -> None:
        """Создаст новый эеземпляр класса и
        определит начальные значения объекта."""
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Создаст сообщение для выода."""
        message: str = f"Тип тренировки: {self.training_type}; " \
                       f"Длительность: {self.duration:.3f} ч.; " \
                       f"Дистанция: {self.distance:.3f} км; " \
                       f"Ср. скорость: {self.speed:.3f} км/ч; " \
                       f"Потрачено ккал: {self.calories:.3f}."
        return message


class Training:
    """Базовый класс тренировки."""

    NAME_OF_TRAINING: str = 'Training'
    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    HOURS_PER_MINUTE: float = 60

    action: int
    duration: float
    weight: float

    def __init__(self, action, duration, weight) -> None:
        """Создаст новый эеземпляр класса и
        определит начальные значения объекта."""
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message = InfoMessage(self.NAME_OF_TRAINING,
                              self.duration,
                              self.get_distance(),
                              self.get_mean_speed(),
                              self.get_spent_calories())
        return message


class Running(Training):
    """Тренировка: бег."""

    NAME_OF_TRAINING: str = 'Running'
    COEFF_CALORIE_1: float = 18
    COEFF_CALORIE_2: float = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий для бега."""
        return ((self.COEFF_CALORIE_1 * self.get_mean_speed()
                 - self.COEFF_CALORIE_2) * self.weight / self.M_IN_KM
                * self.duration * self.HOURS_PER_MINUTE)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    NAME_OF_TRAINING: str = 'SportsWalking'
    IN_SQUARE: float = 2
    COEFF_CALORIE_1: float = 0.035
    COEFF_CALORIE_2: float = 0.029

    action: int
    duration: float
    weight: float
    height: float

    def __init__(self, action, duration, weight, height) -> None:
        """Создаст новый эеземпляр класса и
        определит начальные значения объекта."""
        super().__init__(action, duration, weight)
        self.height = height

    def get_distance(self) -> float:
        """Получить дистанцию в км для ходьбы."""
        return super().get_distance()

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий для бега."""
        return (self.COEFF_CALORIE_1 * self.weight
                + (self.get_mean_speed() ** self.IN_SQUARE
                   // self.height) * self.COEFF_CALORIE_2
                * self.weight) * self.duration * self.HOURS_PER_MINUTE


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    NAME_OF_TRAINING: str = 'Swimming'
    COEF_ONE_FOR_CAL: float = 1.1
    COEF_TWO_FOR_CAL: float = 2

    action: int
    duration: float
    weight: float
    length_pool: float
    count_pool: float

    def __init__(self, action, duration, weight,
                 length_pool, count_pool) -> None:
        """Создаст новый эеземпляр класса и
        определит начальные значения объекта."""
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Получить дистанцию в км для плавания."""
        return super().get_distance()

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

    SWM: str = 'SWM'
    RUN: str = 'RUN'
    WLK: str = 'WLK'

    type_of_training: Dict[str, Callable] = {
        SWM: Swimming,
        RUN: Running,
        WLK: SportsWalking
    }

    if workout_type in type_of_training:
        return type_of_training[workout_type](*data)


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
