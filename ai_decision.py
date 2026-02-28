class AIDecisionEngine:
    """MRU-дың орталық AI миы"""
    
    # Энергия шектері
    CRITICAL_THRESHOLD = 20   # Қауіпті деңгей (%)
    LOW_THRESHOLD = 40        # Төмен деңгей (%)
    SAFE_THRESHOLD = 70       # Қауіпсіз деңгей (%)
    
    def __init__(self):
        self.mode = "SOLAR"           # Бастапқы режим
        self.autonomous = False       # Автономды режим
        self.decision_log = []        # Шешімдер журналы
    
    def decide(self, energy_data, comm_data):
        """Жағдайға қарай шешім қабылдау"""
        
        energy = energy_data["solar_energy"]
        methane = energy_data["methane_reserve"]
        comm_status = comm_data["status"]
        is_critical = energy_data["is_critical"]
        
        # Байланыс жоқ → автономды режим
        if comm_status == "DISCONNECTED":
            self.autonomous = True
        else:
            self.autonomous = False
        
        # AI шешім логикасы
        decision = {}
        
        if energy >= self.SAFE_THRESHOLD:
            # Энергия жеткілікті → күн режимі
            self.mode = "SOLAR"
            decision = {
                "mode": "☀️  КҮН РЕЖИМІ",
                "action": "Күн энергиясы жеткілікті. Метан генераторы өшірулі.",
                "priority": "LOW",
                "methane_needed": False
            }
        
        elif energy >= self.LOW_THRESHOLD:
            # Энергия төмендеп жатыр → аралас режим
            self.mode = "MIXED"
            decision = {
                "mode": "⚡ АРАЛАС РЕЖИМ",
                "action": "Энергия төмендеуде. Метан генераторы күту режимінде.",
                "priority": "MEDIUM",
                "methane_needed": False
            }
        
        elif is_critical:
            # Қауіпті деңгей → метан генераторын қос
            self.mode = "METHANE"
            
            if methane > 0:
                decision = {
                    "mode": "🔥 МЕТАН РЕЖИМІ",
                    "action": "ҚАУІП! Метан генераторы іске қосылды. Роботтар күту режимінде.",
                    "priority": "CRITICAL",
                    "methane_needed": True
                }
            else:
                decision = {
                    "mode": "🚨 АПАТ РЕЖИМІ",
                    "action": "АПАТ! Метан резерві таусылды! Жерден жедел жеткізілім керек!",
                    "priority": "EMERGENCY",
                    "methane_needed": False
                }
        
        else:
            # Энергия аз → метан режиміне дайындық
            self.mode = "METHANE_STANDBY"
            decision = {
                "mode": "🟡 МЕТАН КҮТУ РЕЖИМІ",
                "action": "Энергия аз. Метан генераторы дайын күйде.",
                "priority": "HIGH",
                "methane_needed": False
            }
        
        # Автономды режим белгісі
        decision["autonomous"] = self.autonomous
        decision["autonomous_msg"] = (
            "🤖 AI АВТОНОМДЫ РЕЖИМДЕ — Жер командасыз жұмыс істеуде"
            if self.autonomous else
            f"👨‍💻 Жермен байланыс бар ({comm_data['delay_minutes']} мин кешігу)"
        )
        
        # Журналға жазу
        self.decision_log.append(decision["mode"])
        
        return decision
