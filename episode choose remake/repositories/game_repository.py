import json
from pathlib import Path
from typing import Dict, Any

class GameRepository:
    """Работа с данными игр в JSON"""
    
    def __init__(self, data_path: Path):
        self.data_path = data_path
        self._cache = None
    
    def load_all(self) -> Dict[int, Dict]:
        """Загружает все данные об играх"""
        if self._cache is None:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self._cache = data.get('game', {})
        return self._cache
    
    def load_game_data(self, game_id: int) -> Dict[str, Any]:
        """Загружает данные конкретной игры"""
        games = self.load_all()
        return games.get(str(game_id), {})
    
    def save_game_data(self, game_id: int, data: Dict[str, Any]) -> None:
        """Сохраняет данные игры"""
        games = self.load_all()
        games[str(game_id)] = data
        
        # Сохраняем в файл
        with open(self.data_path, 'r+', encoding='utf-8') as f:
            file_data = json.load(f)
            file_data['game'] = games
            f.seek(0)
            json.dump(file_data, f, indent=2, ensure_ascii=False)
            f.truncate()