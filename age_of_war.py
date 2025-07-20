from itertools import permutations

ADVANTAGE = {
    "Militia": ["Spearmen", "LightCavalry"],
    "Spearmen": ["LightCavalry", "HeavyCavalry"],
    "LightCavalry": ["FootArcher", "CavalryArcher"],
    "HeavyCavalry": ["Militia", "FootArcher", "LightCavalry"],
    "CavalryArcher": ["Spearmen", "HeavyCavalry"],
    "FootArcher": ["Militia", "CavalryArcher"]
}


class Platoon:
    def __init__(self, unit_class: str, count: int):
        self.unit_class = unit_class
        self.count = count

   
    def has_advantage_over(self, opponent: 'Platoon') -> bool:
        return opponent.unit_class in ADVANTAGE.get(self.unit_class, [])

 
    def effective_strength_against(self, opponent: 'Platoon') -> float:
        if self.has_advantage_over(opponent):
            return self.count * 2
        return self.count


    def battles_against(self, opponent: 'Platoon') -> str:
        my_effective = self.effective_strength_against(opponent)
        if my_effective > opponent.count:
            return "Win"
        elif my_effective == opponent.count:
            return "Draw"
        else:
            return "Loss"

    def __str__(self):
        return f"{self.unit_class}#{self.count}"


class Army:
    def __init__(self, platoons: list[Platoon]):
        self.platoons = platoons

    
    @staticmethod
    def from_string(data: str) -> 'Army':
        parts = data.strip().split(';')
        platoons = []
        for part in parts:
            cls, count = part.split('#')
            platoons.append(Platoon(cls.strip(), int(count)))
        return Army(platoons)

   
    def get_best_arrangement(self, opponent: 'Army') -> list[Platoon] | None:
        for arrangement in permutations(self.platoons):
            wins = 0
            for my_platoon, opp_platoon in zip(arrangement, opponent.platoons):
                if my_platoon.battles_against(opp_platoon) == "Win":
                    wins += 1
            if wins >= 3:
                return list(arrangement)
        return None

    def __str__(self):
        return ';'.join(str(p) for p in self.platoons)


def solve_age_of_war():
    try:
        my_input = input().strip()
        enemy_input = input().strip()
        my_army = Army.from_string(my_input)
        enemy_army = Army.from_string(enemy_input)
        best_arrangement = my_army.get_best_arrangement(enemy_army)
        if best_arrangement:
            print(';'.join(str(p) for p in best_arrangement))
        else:
            print("There is no chance of winning")
    except Exception as e:
        print(f"Error: {e}")

def test_with_sample():
    my_input = "Spearmen#10;Militia#30;FootArcher#20;LightCavalry#1000;HeavyCavalry#120"
    enemy_input = "Militia#10;Spearmen#10;FootArcher#1000;LightCavalry#120;CavalryArcher#100"
    my_army = Army.from_string(my_input)
    enemy_army = Army.from_string(enemy_input)
    best_arrangement = my_army.get_best_arrangement(enemy_army)

    if best_arrangement:
        print("Best arrangement found:")
        print(';'.join(str(p) for p in best_arrangement))
        print("\nBattle outcomes:")
        for i, (my_p, opp_p) in enumerate(zip(best_arrangement, enemy_army.platoons), 1):
            outcome = my_p.battles_against(opp_p)
            effective = my_p.effective_strength_against(opp_p)
            print(f"Battle {i}: {my_p} vs {opp_p} -> {outcome} (Effective: {effective} vs {opp_p.count})")
    else:
        print("There is no chance of winning")


if __name__ == "__main__":
    

    # Use this during testing
    test_with_sample()
