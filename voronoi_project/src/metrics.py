import math
from abc import ABC, abstractmethod

class DistanceMetric(ABC):
    @abstractmethod
    def calculate(self, p1, p2) -> float:
        pass

class EuclideanDistance(DistanceMetric):
    def calculate(self, p1, p2) -> float:
        return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

class ManhattanDistance(DistanceMetric):
    def calculate(self, p1, p2) -> float:
        return abs(p1.x - p2.x) + abs(p1.y - p2.y)