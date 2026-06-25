class Product:
    def __init__(self, name, demand_score):
        self.name = name
        self.demand_score = demand_score

    def __str__(self):
        return f"{self.name}: {self.demand_score}"
