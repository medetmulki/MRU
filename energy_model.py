import random

class EnergyModel:
    """Марстағы энергия жүйесін симуляциялайды"""
    
    def _init_(self):
        self.solar_energy = 100.0      # Күн энергиясы (%)
        self.methane_reserve = 100.0   # Метан резерві (%)
        self.consumption = 10.0        # Энергия тұтыну (% / сағат)
    
    def simulate_hour(self, is_night=False, is_dust_storm=False):
        """Бір сағаттық энергия симуляциясы"""
        
        # Күн энергиясы жағдайы
        if is_dust_storm:
            solar_output = random.uniform(0, 5)    # Шаңды дауыл: 0-5%
        elif is_night:
            solar_output = 0                        # Түн: 0%
        else:
            solar_output = random.uniform(40, 80)  # Күндіз: 40-80%
        
        # Энергия балансы
        self.solar_energy = max(0, self.solar_energy + solar_output - self.consumption)
        
        return {
            "solar_output": round(solar_output, 1),
            "solar_energy": round(self.solar_energy, 1),
            "methane_reserve": round(self.methane_reserve, 1),
            "is_critical": self.solar_energy < 20
        }
    
    def use_methane(self, amount=15.0):
        """Метан генераторын іске қосу"""
        if self.methane_reserve >= amount:
            self.methane_reserve -= amount
            self.solar_energy = min(100, self.solar_energy + amount)
            return True
        return False
