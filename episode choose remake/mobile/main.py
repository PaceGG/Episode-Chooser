import requests
import json
import time
import sys
from datetime import datetime
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

FIREBASE_URL = "https://episode-chooser-a0459-default-rtdb.asia-southeast1.firebasedatabase.app/"
STATUS_PATH = "status.json"
COUNTER_PATH = "counter.json"

class Launcher:
    def __init__(self):
        self.running = True
        self.counter = 0
        
    def update_status(self, status):
        """Обновляет статус в Firebase"""
        data = {
            "status": status,
            "last_update": datetime.now().isoformat(),
            "counter": self.counter
        }
        try:
            response = requests.put(
                f"{FIREBASE_URL}{STATUS_PATH}",
                json=data
            )
            if response.status_code == 200:
                print(f"[✓] Статус обновлен: {status}")
            else:
                print(f"[✗] Ошибка обновления статуса: {response.status_code}")
        except Exception as e:
            print(f"[✗] Ошибка соединения: {e}")
    
    def increment_counter(self):
        """Увеличивает счетчик на 1"""
        self.counter += 1
        print(f"[+] Счетчик: {self.counter}")
        
        # Обновляем счетчик в Firebase
        try:
            response = requests.patch(
                f"{FIREBASE_URL}{COUNTER_PATH}",
                json={"value": self.counter}
            )
            if response.status_code == 200:
                print(f"[✓] Счетчик синхронизирован: {self.counter}")
            else:
                print("[✗] Ошибка синхронизации счетчика")
        except Exception as e:
            print(f"[✗] Ошибка соединения: {e}")
    
    def listen_for_commands(self):
        """Слушает команды из Firebase"""
        last_command = None
        
        while self.running:
            try:
                # Получаем команду из Firebase
                response = requests.get(
                    f"{FIREBASE_URL}command.json"
                )
                
                if response.status_code == 200:
                    command_data = response.json()
                    
                    if command_data:
                        command = command_data.get("action")
                        command_id = command_data.get("id")
                        
                        # Проверяем, не обработали ли уже эту команду
                        if command_id != last_command:
                            last_command = command_id
                            
                            if command == "increment":
                                print("[→] Получена команда: increment")
                                self.increment_counter()
                                # Очищаем команду после выполнения
                                requests.delete(f"{FIREBASE_URL}command.json")
                                
                            elif command == "exit":
                                print("[→] Получена команда: exit")
                                self.shutdown()
                                
            except Exception as e:
                print(f"[✗] Ошибка при получении команд: {e}")
            
            time.sleep(1)  # Проверяем каждую секунду
    
    def shutdown(self):
        """Завершает работу"""
        print("[!] Завершение работы...")
        self.running = False
        self.update_status("inactive")
        print("[✓] Статус обновлен на inactive")
        sys.exit(0)
    
    def run(self):
        """Запуск лаунчера"""
        print("[🚀] Запуск лаунчера...")
        
        # Устанавливаем статус active
        self.update_status("active")
        
        # Очищаем старые команды
        try:
            requests.delete(f"{FIREBASE_URL}command.json")
        except:
            pass
        
        print("[✓] Лаунчер запущен. Ожидание команд...")
        print("[ℹ] Нажмите Ctrl+C для остановки")
        
        # Запускаем прослушивание команд
        try:
            self.listen_for_commands()
        except KeyboardInterrupt:
            print("\n[!] Получен сигнал остановки")
            self.shutdown()

if __name__ == "__main__":
    launcher = Launcher()
    launcher.run()