from typing import Dict, List


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return f"Тип тренировки: {self.training_type}; " \
               f"Длительность: {self.duration:.{3}f} ч.; " \
               f"Дистанция: {self.distance:.{3}f} км; " \
               f"Ср. скорость: {self.speed:.{3}f} км/ч; " \
               f"Потрачено ккал: {self.calories:.{3}f}."


class Training:
    """Базовый класс тренировки."""
    NAME_OF_TRAINING: str = 'Training'
    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    HOURS_PER_MINUTE: float = 60

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
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

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

    def get_distance(self) -> float:
        """Получить дистанцию в км для бега."""
        return super().get_distance()

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий для бега."""
        coeff_calorie_1 = 18
        coeff_calorie_2 = 20
        return (coeff_calorie_1 * self.get_mean_speed()
                - coeff_calorie_2) * self.weight / self.M_IN_KM *\
            self.duration * self.HOURS_PER_MINUTE

    def show_training_info(self) -> InfoMessage:
        return super().show_training_info()


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    NAME_OF_TRAINING: str = 'SportsWalking'

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_distance(self) -> float:
        """Получить дистанцию в км для ходьбы."""
        return super().get_distance()

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий для бега."""
        coeff_calorie_1: float = 0.035
        coeff_calorie_2: float = 0.029
        return (coeff_calorie_1 * self.weight
                + (self.get_mean_speed() ** 2
                   // self.height) * coeff_calorie_2
                * self.weight) * self.duration * self.HOURS_PER_MINUTE

    def show_training_info(self) -> InfoMessage:
        return super().show_training_info()


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    NAME_OF_TRAINING: str = 'Swimming'

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float,
                 ) -> None:
        """Добавить длину бассейна."""
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Получить дистанцию в км для плавания."""
        return super().get_distance()

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения в бассейне."""
        return self.length_pool * self.count_pool / \
            self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (self.get_mean_speed() + 1.1) * 2 * self.weight

    def show_training_info(self) -> InfoMessage:
        return super().show_training_info()


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_of_training: Dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
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
