class MarsAtmosphereAI:
    """
    MRU (Mars Rover Unit) Орталық миы.
    Марс атмосферасының экстремалды жағдайларын басқаруға арналған.
    """
    
    def __init__(self):
        # Қауіпсіздік шектері
        self.CRITICAL_TEMP = -100  # Цельсий (Марс түні)
        self.STORM_THRESHOLD = 75  # Шаң деңгейі (%)
        self.LOW_ENERGY = 30       # Энергия резерві (%)
        
        self.current_mode = "STANDBY"
        self.logs = []

    def analyze_environment(self, telemetry: dict) -> dict:
        """
        Марс телетметриясын талдау және шешім шығару.
        :param telemetry: {'temp', 'dust_opacity', 'solar_gain', 'methane_level'}
        """
        
        temp = telemetry.get('temp', -60)
        dust = telemetry.get('dust_opacity', 0)
        energy = telemetry.get('solar_gain', 100)
        methane = telemetry.get('methane_level', 0)
        
        decision = {
            "status": "OPERATIONAL",
            "heaters": "OFF",
            "power_source": "SOLAR",
            "alert": "NONE"
        }

        # 1. ШАҢДЫ ДАУЫЛДЫ ТЕКСЕРУ (Ең жоғарғы басымдық)
        if dust > self.STORM_THRESHOLD:
            self.current_mode = "STORM_PROTECTION"
            decision.update({
                "status": "EMERGENCY",
                "power_source": "METHANE" if methane > 10 else "BATTERY_SAVE",
                "alert": "🌪️ ШАҢДЫ ДАУЫЛ: Панельдер жабылды!"
            })

        # 2. ТЕРМАЛДЫҚ БАҚЫЛАУ (Түнде қатып қалмау үшін)
        elif temp < self.CRITICAL_TEMP:
            self.current_mode = "THERMAL_KEEP_ALIVE"
            decision["heaters"] = "MAXIMUM"
            decision["alert"] = "❄️ ЭКСТРЕМАЛДЫ СУЫҚ: Жылыту қосылды."
            if energy < self.LOW_ENERGY:
                 decision["power_source"] = "METHANE_HYBRID"

        # 3. ЭНЕРГИЯ ТАПШЫЛЫҒЫ
        elif energy < self.LOW_ENERGY and methane > 5:
            self.current_mode = "METHANE_SUPPORT"
            decision["power_source"] = "METHANE"
            decision["alert"] = "⚡ ЭНЕРГИЯ АЗ: Метан генераторы қосылды."

        # 4. ҚАЛЫПТЫ ЖАҒДАЙ
        else:
            self.current_mode = "OPTIMAL"
            decision["alert"] = "✅ ЖАҒДАЙ ТҰРАҚТЫ"

        self._log_event(decision["alert"])
        return decision

    def _log_event(self, message: str):
        """Оқиғаларды журналға жазу"""
        self.logs.append(message)
        if len(self.logs) > 50:
            self.logs.pop(0)

# --- ПАЙДАЛАНУ МЫСАЛЫ ---
mru_ai = MarsAtmosphereAI()

# Марстан келген деректер (Мысалы: түн және шаңды дауыл)
mars_data = {
    'temp': -110, 
    'dust_opacity': 85, 
    'solar_gain': 5, 
    'methane_level': 40
}

result = mru_ai.analyze_environment(mars_data)
print(f"РЕЖИМ: {result['alert']}")
print(f"ҚУАТ КӨЗІ: {result['power_source']}")
