import random

class CommunicationSystem:
    """Жер-Марс байланыс жүйесін симуляциялайды"""
    
    def _init_(self):
        self.min_delay = 4    # Минималды кешігу (минут)
        self.max_delay = 24   # Максималды кешігу (минут)
        self.connection_probability = 0.85  # Байланыс мүмкіндігі 85%
    
    def get_status(self):
        """Байланыс күйін анықтау"""
        
        # Байланыс бар ма?
        connected = random.random() < self.connection_probability
        
        if not connected:
            return {
                "status": "DISCONNECTED",
                "delay_minutes": None,
                "message": "⚠️  Байланыс жоқ — AI автономды режимде"
            }
        
        delay = random.randint(self.min_delay, self.max_delay)
        
        if delay <= 8:
            status = "GOOD"
            msg = f"✅ Байланыс жақсы — кешігу {delay} мин"
        elif delay <= 16:
            status = "DELAYED"
            msg = f"🟡 Байланыс кешіккен — кешігу {delay} мин"
        else:
            status = "CRITICAL_DELAY"
            msg = f"🔴 Байланыс өте кешіккен — кешігу {delay} мин"
        
        return {
            "status": status,
            "delay_minutes": delay,
            "message": msg
        }
