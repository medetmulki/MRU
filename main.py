from energy_model import EnergyModel
from communication_delay import CommunicationSystem
from ai_decision import AIDecisionEngine

def print_separator():
    print("=" * 60)

def print_status(hour, energy_data, comm_data, decision, conditions):
    """Сағаттық есеп"""
    print_separator()
    print(f"⏱️  САҒАТ {hour:02d}:00 | {conditions}")
    print_separator()
    
    # Энергия күйі
    print(f"☀️  Күн шығысы:     {energy_data['solar_output']}%")
    print(f"🔋 Энергия деңгейі: {energy_data['solar_energy']}%")
    print(f"⛽ Метан резерві:   {energy_data['methane_reserve']}%")
    print()
    
    # Байланыс күйі
    print(f"🛰️  {comm_data['message']}")
    print()
    
    # AI шешімі
    print(f"🧠 AI РЕЖИМІ: {decision['mode']}")
    print(f"📋 ӘРЕКЕТ: {decision['action']}")
    print(f"⚡ БАСЫМДЫЛЫҚ: {decision['priority']}")
    print(f"🌍 {decision['autonomous_msg']}")
    print()

def run_simulation():
    """MRU симуляциясын іске қосу"""
    
    # Жүйелерді инициализациялау
    energy = EnergyModel()
    comm = CommunicationSystem()
    ai = AIDecisionEngine()
    
    print()
    print("=" * 60)
    print("   🚀 MRU — MARS RESEARCH UNIT")
    print("   AI Energy Management Simulation")
    print("   Команда: Мүлкі Медет & Шарикөрпе Ясин")
    print("   №24 мектеп, Ақтау | AEROO 2025")
    print("=" * 60)
    print()
    print("Симуляция басталуда: 24 сағаттық Марс циклі")
    print()
    input("Бастау үшін Enter басыңыз...")
    print()
    
    # 24 сағаттық симуляция
    scenarios = [
        # (сағат, түн_бе, шаңды_дауыл_ба, жағдай_сипаттамасы)
        (1,  False, False, "☀️  Күндіз — қалыпты жағдай"),
        (4,  False, False, "☀️  Күндіз — қалыпты жағдай"),
        (7,  False, True,  "🌪️  ШАҢДЫ ДАУЫЛ басталды!"),
        (10, False, True,  "🌪️  Шаңды дауыл жалғасуда"),
        (13, False, True,  "🌪️  Шаңды дауыл — 3-ші сағат"),
        (16, False, False, "☀️  Дауыл басылды — күн шықты"),
        (19, True,  False, "🌙  Марс түні басталды"),
        (22, True,  False, "🌙  Марс түні — терең"),
        (24, True,  False, "🌙  Марс түні аяқталуда"),
    ]
    
    for hour, is_night, is_dust_storm, condition in scenarios:
        # Жүйелерді жаңарту
        energy_data = energy.simulate_hour(is_night, is_dust_storm)
        comm_data = comm.get_status()
        decision = ai.decide(energy_data, comm_data)
        
        # Метан генераторын іске қосу
        if decision["methane_needed"]:
            success = energy.use_methane(15.0)
            if success:
                print(f"⛽ Метан генераторы іске қосылды! +15% энергия")
                energy_data["solar_energy"] = energy.solar_energy
                energy_data["methane_reserve"] = energy.methane_reserve
        
        # Нәтижені көрсету
        print_status(hour, energy_data, comm_data, decision, condition)
        input("Келесі сағатқа өту үшін Enter басыңыз...")
    
    # Қорытынды
    print_separator()
    print("📊 СИМУЛЯЦИЯ АЯҚТАЛДЫ — ҚОРЫТЫНДЫ")
    print_separator()
    print(f"✅ Соңғы энергия деңгейі: {energy.solar_energy:.1f}%")
    print(f"⛽ Қалған метан резерві:  {energy.methane_reserve:.1f}%")
    print(f"🧠 AI қабылдаған шешімдер саны: {len(ai.decision_log)}")
    print()
    print("🤖 AI шешімдер журналы:")
    for i, log in enumerate(ai.decision_log, 1):
        print(f"   {i}. {log}")
    print()
    print("🚀 MRU MVP симуляциясы сәтті аяқталды!")
    print("   Mars Research Unit | AEROO 2025")
    print_separator()

if _name_ == "_main_":
    run_simulation()
