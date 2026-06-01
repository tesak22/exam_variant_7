from abc import ABC, abstractmethod
from typing import List
from google.adk.agents import Agent


class Exercise(ABC):

    def __init__(self, name: str, duration_min: int):
        self.name = name
        self.duration_min = duration_min

    @abstractmethod
    def calories_burned(self) -> float:
        pass


class CardioExercise(Exercise):

    def __init__(self, name: str, duration_min: int, intensity: float):
        super().__init__(name, duration_min)
        self.intensity = intensity

    def calories_burned(self) -> float:
        return self.duration_min * 8 * self.intensity


class StrengthExercise(Exercise):

    def __init__(self, name: str, duration_min: int, weight_kg: float):
        super().__init__(name, duration_min)
        self.weight_kg = weight_kg

    def calories_burned(self) -> float:
        return self.duration_min * 5 + self.weight_kg * 0.5


class Workout:

    def __init__(self):
        self.__exercises: List[Exercise] = []

    def add(self, exercise: Exercise):
        self.__exercises.append(exercise)

    def total_calories(self) -> float:
        return sum(ex.calories_burned() for ex in self.__exercises)

    def summary(self) -> dict:
        return {
            "exercises": [
                {
                    "name": ex.name,
                    "duration_min": ex.duration_min,
                    "calories": round(ex.calories_burned(), 2)
                }
                for ex in self.__exercises
            ],
            "total_calories": round(self.total_calories(), 2)
        }


def calculate_workout(exercises: list) -> dict:
    workout = Workout()

    for item in exercises:

        if item["type"] == "cardio":
            exercise = CardioExercise(
                item["name"],
                item["duration_min"],
                item["intensity"]
            )

        elif item["type"] == "strength":
            exercise = StrengthExercise(
                item["name"],
                item["duration_min"],
                item["weight_kg"]
            )
        else:
            continue

        workout.add(exercise)

    result = workout.summary()

    total = result["total_calories"]

    if total < 200:
        recommendation = "Легке навантаження."
    elif total < 500:
        recommendation = "Помірне навантаження."
    else:
        recommendation = "Високе навантаження."

    result["recommendation"] = recommendation
    return result


root_agent = Agent(
    name="fitness_trainer_agent",
    model="gemini-2.0-flash",
    description="Фітнес-тренер",
    instruction="""
Ти персональний фітнес-тренер.
Розраховуй калорії тренування через calculate_workout.
Надавай рекомендації щодо навантаження.
Відповідай українською мовою.
""",
    tools=[calculate_workout]
)
