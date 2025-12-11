from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import statistics
import logging
from functools import wraps
import traceback

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('month_recap.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def handle_errors(func):
    """Декоратор для обработки ошибок."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Ошибка в функции {func.__name__}: {str(e)}")
            logger.error(traceback.format_exc())
            # Возвращаем базовую структуру с ошибкой
            return {
                'error': True,
                'error_message': str(e),
                'error_type': type(e).__name__,
                'function': func.__name__,
                'timestamp': datetime.now().isoformat()
            }
    return wrapper

def validate_session_data(session_id: str, session_data: Dict) -> bool:
    """Валидация данных сессии."""
    try:
        # Проверяем обязательные поля
        required_fields = ['game', 'datetime', 'episodes']
        for field in required_fields:
            if field not in session_data:
                logger.warning(f"Сессия {session_id}: отсутствует обязательное поле '{field}'")
                return False
        
        # Проверяем типы данных
        if not isinstance(session_data['datetime'], (int, float)):
            logger.warning(f"Сессия {session_id}: неверный тип datetime")
            return False
        
        if not isinstance(session_data['episodes'], list):
            logger.warning(f"Сессия {session_id}: episodes должен быть списком")
            return False
        
        # Валидация эпизодов
        for i, episode in enumerate(session_data['episodes']):
            if not isinstance(episode, dict):
                logger.warning(f"Сессия {session_id}: эпизод {i} должен быть словарем")
                continue
            
            # Проверяем обязательные поля эпизода
            episode_fields = ['number', 'title', 'duration', 'publishedAt']
            for field in episode_fields:
                if field not in episode:
                    logger.warning(f"Сессия {session_id}, эпизод {i}: отсутствует поле '{field}'")
        
        return True
        
    except Exception as e:
        logger.error(f"Ошибка при валидации сессии {session_id}: {str(e)}")
        return False

def safe_datetime_convert(timestamp) -> Optional[datetime]:
    """Безопасное преобразование timestamp в datetime."""
    try:
        if isinstance(timestamp, (int, float)):
            return datetime.fromtimestamp(timestamp)
        elif isinstance(timestamp, str):
            # Пробуем разные форматы
            for fmt in ['%Y-%m-%dT%H:%M:%SZ', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S']:
                try:
                    return datetime.strptime(timestamp, fmt)
                except:
                    continue
        return None
    except Exception as e:
        logger.warning(f"Ошибка преобразования даты: {timestamp}, ошибка: {str(e)}")
        return None

def safe_int_convert(value, default=0) -> int:
    """Безопасное преобразование в int."""
    try:
        return int(value)
    except (ValueError, TypeError):
        logger.debug(f"Не удалось преобразовать в int: {value}, используется значение по умолчанию: {default}")
        return default

def safe_float_convert(value, default=0.0) -> float:
    """Безопасное преобразование в float."""
    try:
        return float(value)
    except (ValueError, TypeError):
        logger.debug(f"Не удалось преобразовать в float: {value}, используется значение по умолчанию: {default}")
        return default

@handle_errors
def make_month_recap(target_month: str, sessions: Dict) -> Dict[str, Any]:
    """
    Создает подробную статистику за указанный месяц.
    
    Args:
        target_month: Месяц в формате "YY-MM" (например "25-12")
        sessions: Словарь с данными о сессиях
    
    Returns:
        Словарь с подробной статистикой
    """
    
    logger.info(f"Начинаем создание отчета за {target_month}")
    
    # Базовый объект отчета
    recap = {
        'target_month': target_month,
        'total_sessions': 0,
        'total_episodes': 0,
        'total_duration': 0,
        'games': {},
        'daily_stats': {},
        'time_stats': {},
        'episode_stats': {},
        'completion_stats': {},
        'game_rankings': {},
        'summary': {},
        'processing_info': {
            'start_time': datetime.now().isoformat(),
            'total_sessions_processed': 0,
            'sessions_skipped': 0,
            'sessions_with_errors': 0
        }
    }
    
    # Проверяем входные данные
    if not sessions:
        logger.warning("Передан пустой словарь sessions")
        recap['summary'] = {
            'message': 'Нет данных для обработки',
            'target_month': target_month
        }
        recap['processing_info']['end_time'] = datetime.now().isoformat()
        return recap
    
    # Проверяем формат месяца
    try:
        month_year = int("20" + target_month.split("-")[0])
        month = int(target_month.split("-")[1])
        if not 1 <= month <= 12:
            raise ValueError
        logger.debug(f"Формат месяца {target_month} корректен")
    except Exception as e:
        error_msg = f"Неверный формат месяца: {target_month}. Используйте YY-MM"
        logger.error(error_msg)
        recap['error'] = error_msg
        recap['processing_info']['end_time'] = datetime.now().isoformat()
        return recap
    
    all_episodes = []
    
    # Обрабатываем сессии
    for session_id, session_data in sessions.items():
        recap['processing_info']['total_sessions_processed'] += 1
        
        # Валидация данных сессии
        if not validate_session_data(session_id, session_data):
            recap['processing_info']['sessions_with_errors'] += 1
            logger.warning(f"Пропускаем сессию {session_id} из-за ошибок валидации")
            continue
        
        try:
            # Безопасное получение данных
            game_name = session_data.get('game', 'Неизвестная игра')
            timestamp = session_data.get('datetime')
            
            # Преобразуем дату
            session_date = safe_datetime_convert(timestamp)
            if not session_date:
                recap['processing_info']['sessions_skipped'] += 1
                logger.warning(f"Пропускаем сессию {session_id}: не удалось преобразовать дату")
                continue
            
            # Проверяем месяц
            session_month = f"{session_date.strftime('%y')}-{session_date.strftime('%m')}"
            if session_month != target_month:
                recap['processing_info']['sessions_skipped'] += 1
                logger.debug(f"Сессия {session_id} не в целевом месяце: {session_month}")
                continue
            
            # Основная статистика
            episodes = session_data.get('episodes', [])
            episode_count = len(episodes)
            
            recap['total_sessions'] += 1
            recap['total_episodes'] += episode_count
            
            # Инициализация статистики по игре
            if game_name not in recap['games']:
                recap['games'][game_name] = {
                    'session_count': 0,
                    'episode_count': 0,
                    'total_duration': 0,
                    'episodes': [],
                    'episode_numbers': [],
                    'titles': [],
                    'durations': []
                }
            
            game_stats = recap['games'][game_name]
            game_stats['session_count'] += 1
            game_stats['episode_count'] += episode_count
            
            # Обрабатываем эпизоды
            for episode in episodes:
                try:
                    # Безопасное получение данных эпизода
                    episode_duration = safe_int_convert(episode.get('duration', 0))
                    episode_title = episode.get('title', 'Без названия')
                    episode_number = safe_int_convert(episode.get('number', 0))
                    published_at = episode.get('publishedAt')
                    
                    # Обновляем статистику
                    recap['total_duration'] += episode_duration
                    game_stats['total_duration'] += episode_duration
                    
                    # Собираем данные эпизода
                    episode_data = {
                        'number': episode_number,
                        'title': episode_title,
                        'duration': episode_duration,
                        'published_at': published_at,
                        'game': game_name,
                        'session_id': session_id
                    }
                    
                    game_stats['episodes'].append(episode_data)
                    game_stats['episode_numbers'].append(episode_number)
                    game_stats['titles'].append(episode_title)
                    game_stats['durations'].append(episode_duration)
                    
                    all_episodes.append(episode_data)
                    
                    # Обработка даты публикации
                    if published_at:
                        try:
                            # Пробуем разные форматы даты
                            if 'T' in published_at:
                                episode_date = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                            else:
                                episode_date = datetime.strptime(published_at, '%Y-%m-%d %H:%M:%S')
                        except:
                            # Используем дату сессии как fallback
                            episode_date = session_date
                            logger.debug(f"Не удалось распарсить дату {published_at}, используем дату сессии")
                    else:
                        episode_date = session_date
                    
                    # Статистика по дням
                    date_str = episode_date.strftime('%Y-%m-%d')
                    
                    if date_str not in recap['daily_stats']:
                        recap['daily_stats'][date_str] = {
                            'episodes': 0,
                            'duration': 0,
                            'games': set(),
                            'session_ids': set(),
                            'episode_titles': []
                        }
                    
                    day_stats = recap['daily_stats'][date_str]
                    day_stats['episodes'] += 1
                    day_stats['duration'] += episode_duration
                    day_stats['games'].add(game_name)
                    day_stats['session_ids'].add(session_id)
                    day_stats['episode_titles'].append(episode_title)
                    
                    # Статистика по времени суток
                    hour = episode_date.hour
                    if hour < 6:
                        time_slot = "Ночь (0-5)"
                    elif hour < 12:
                        time_slot = "Утро (6-11)"
                    elif hour < 18:
                        time_slot = "День (12-17)"
                    else:
                        time_slot = "Вечер (18-23)"
                    
                    if time_slot not in recap['time_stats']:
                        recap['time_stats'][time_slot] = {'episodes': 0, 'duration': 0}
                    
                    recap['time_stats'][time_slot]['episodes'] += 1
                    recap['time_stats'][time_slot]['duration'] += episode_duration
                    
                except Exception as e:
                    logger.error(f"Ошибка при обработке эпизода в сессии {session_id}: {str(e)}")
                    recap['processing_info']['sessions_with_errors'] += 1
                    continue
                    
        except Exception as e:
            logger.error(f"Ошибка при обработке сессии {session_id}: {str(e)}")
            recap['processing_info']['sessions_with_errors'] += 1
            continue
    
    logger.info(f"Обработано {recap['total_sessions']} сессий, {recap['total_episodes']} эпизодов")
    
    # Если нет данных за месяц
    if recap['total_episodes'] == 0:
        recap['summary'] = {
            'message': f'Нет данных за {target_month}',
            'target_month': target_month,
            'sessions_processed': recap['processing_info']['total_sessions_processed']
        }
        recap['processing_info']['end_time'] = datetime.now().isoformat()
        return recap
    
    # Расчет статистики
    try:
        # 1. Основные средние значения
        recap['average_episodes_per_session'] = round(
            recap['total_episodes'] / recap['total_sessions'], 2
        ) if recap['total_sessions'] > 0 else 0
        
        recap['average_duration_per_episode'] = round(
            recap['total_duration'] / recap['total_episodes']
        ) if recap['total_episodes'] > 0 else 0
        
        recap['average_duration_per_session'] = round(
            recap['total_duration'] / recap['total_sessions']
        ) if recap['total_sessions'] > 0 else 0
        
        # Конвертируем длительность
        recap['total_duration_readable'] = _seconds_to_readable(recap['total_duration'])
        recap['average_duration_per_episode_readable'] = _seconds_to_readable(
            recap['average_duration_per_episode']
        )
        
        # 2. Статистика по играм
        for game_name, game_stats in recap['games'].items():
            try:
                game_stats['total_duration_readable'] = _seconds_to_readable(game_stats['total_duration'])
                
                # Средние значения
                game_stats['average_duration_per_episode'] = round(
                    game_stats['total_duration'] / game_stats['episode_count']
                ) if game_stats['episode_count'] > 0 else 0
                
                game_stats['average_episodes_per_session'] = round(
                    game_stats['episode_count'] / game_stats['session_count'], 2
                ) if game_stats['session_count'] > 0 else 0
                
                # Проценты
                game_stats['percentage_of_total_episodes'] = round(
                    (game_stats['episode_count'] / recap['total_episodes']) * 100, 1
                ) if recap['total_episodes'] > 0 else 0
                
                game_stats['percentage_of_total_duration'] = round(
                    (game_stats['total_duration'] / recap['total_duration']) * 100, 1
                ) if recap['total_duration'] > 0 else 0
                
                # Анализ эпизодов
                durations = game_stats.get('durations', [])
                if durations:
                    game_stats['duration_stats'] = {
                        'shortest_episode': min(durations),
                        'longest_episode': max(durations),
                        'average_episode_duration': game_stats['average_duration_per_episode'],
                        'total_duration_hours': round(game_stats['total_duration'] / 3600, 2)
                    }
                else:
                    game_stats['duration_stats'] = {
                        'shortest_episode': 0,
                        'longest_episode': 0,
                        'average_episode_duration': 0,
                        'total_duration_hours': 0
                    }
                
                # Дата начала и конца
                episodes = game_stats.get('episodes', [])
                if episodes:
                    dates = []
                    for ep in episodes:
                        if ep.get('published_at'):
                            try:
                                if 'T' in ep['published_at']:
                                    dt = datetime.fromisoformat(ep['published_at'].replace('Z', '+00:00'))
                                else:
                                    dt = datetime.strptime(ep['published_at'], '%Y-%m-%d %H:%M:%S')
                                dates.append(dt)
                            except:
                                continue
                    
                    if dates:
                        game_stats['date_range'] = {
                            'first': min(dates).strftime('%Y-%m-%d'),
                            'last': max(dates).strftime('%Y-%m-%d')
                        }
                    else:
                        game_stats['date_range'] = {'first': None, 'last': None}
                else:
                    game_stats['date_range'] = {'first': None, 'last': None}
                
                # Сортировка эпизодов
                game_stats['episodes'].sort(key=lambda x: safe_int_convert(x.get('number', 0)))
                
            except Exception as e:
                logger.error(f"Ошибка при обработке статистики игры {game_name}: {str(e)}")
                continue
        
        # 3. Статистика по дням
        daily_array = []
        for date_str, day_stats in recap['daily_stats'].items():
            try:
                episodes_count = day_stats.get('episodes', 0)
                duration = day_stats.get('duration', 0)
                
                day_data = {
                    'date': date_str,
                    'episodes': episodes_count,
                    'duration': duration,
                    'duration_readable': _seconds_to_readable(duration),
                    'games': list(day_stats.get('games', set())),
                    'games_count': len(day_stats.get('games', set())),
                    'sessions_count': len(day_stats.get('session_ids', set())),
                    'average_duration_per_episode': round(duration / episodes_count) if episodes_count > 0 else 0,
                    'episode_titles': day_stats.get('episode_titles', [])
                }
                daily_array.append(day_data)
            except Exception as e:
                logger.error(f"Ошибка при обработке дня {date_str}: {str(e)}")
                continue
        
        daily_array.sort(key=lambda x: x.get('date', ''))
        recap['daily_stats_array'] = daily_array
        
        # 4. Временные слоты
        time_stats_array = []
        for slot, stats in recap['time_stats'].items():
            try:
                time_data = {
                    'slot': slot,
                    'episodes': stats.get('episodes', 0),
                    'duration': stats.get('duration', 0),
                    'duration_readable': _seconds_to_readable(stats.get('duration', 0)),
                    'percentage_of_total': round(
                        (stats.get('episodes', 0) / recap['total_episodes']) * 100, 1
                    ) if recap['total_episodes'] > 0 else 0
                }
                time_stats_array.append(time_data)
            except Exception as e:
                logger.error(f"Ошибка при обработке временного слота {slot}: {str(e)}")
                continue
        
        time_stats_array.sort(key=lambda x: x.get('episodes', 0), reverse=True)
        recap['time_stats_array'] = time_stats_array
        
        # 5. Дни недели
        day_names = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
        weekday_stats = {}
        
        for day in daily_array:
            try:
                date_str = day.get('date')
                if not date_str:
                    continue
                    
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                weekday = day_names[date_obj.weekday()]
                
                if weekday not in weekday_stats:
                    weekday_stats[weekday] = {'episodes': 0, 'duration': 0, 'days': 0}
                
                weekday_stats[weekday]['episodes'] += day.get('episodes', 0)
                weekday_stats[weekday]['duration'] += day.get('duration', 0)
                weekday_stats[weekday]['days'] += 1
            except Exception as e:
                logger.error(f"Ошибка при обработке дня недели: {str(e)}")
                continue
        
        # Упорядочиваем по дням недели
        weekday_stats_array = []
        for day in day_names:
            if day in weekday_stats:
                stats = weekday_stats[day]
                try:
                    weekday_data = {
                        'day': day,
                        'episodes': stats['episodes'],
                        'duration': stats['duration'],
                        'duration_readable': _seconds_to_readable(stats['duration']),
                        'average_episodes_per_day': round(stats['episodes'] / stats['days'], 1) if stats['days'] > 0 else 0,
                        'average_duration_per_day': _seconds_to_readable(
                            round(stats['duration'] / stats['days']) if stats['days'] > 0 else 0
                        ),
                        'days_with_content': stats['days']
                    }
                    weekday_stats_array.append(weekday_data)
                except Exception as e:
                    logger.error(f"Ошибка при создании статистики дня недели {day}: {str(e)}")
                    continue
        
        recap['weekday_stats_array'] = weekday_stats_array
        
        # 6. Статистика эпизодов
        if all_episodes:
            try:
                durations = [safe_int_convert(ep.get('duration', 0)) for ep in all_episodes]
                valid_durations = [d for d in durations if d > 0]
                
                if valid_durations:
                    recap['episode_stats'] = {
                        'total_count': len(all_episodes),
                        'by_duration': {
                            'short': len([d for d in valid_durations if d < 1800]),
                            'medium': len([d for d in valid_durations if 1800 <= d < 3600]),
                            'long': len([d for d in valid_durations if 3600 <= d < 7200]),
                            'very_long': len([d for d in valid_durations if d >= 7200])
                        },
                        'shortest_episodes': sorted(all_episodes, key=lambda x: safe_int_convert(x.get('duration', 0)))[:5],
                        'longest_episodes': sorted(all_episodes, key=lambda x: safe_int_convert(x.get('duration', 0)), reverse=True)[:5],
                        'average_duration': round(sum(valid_durations) / len(valid_durations)) if valid_durations else 0,
                        'median_duration': int(statistics.median(valid_durations)) if valid_durations else 0
                    }
                    
                    # Добавляем читаемые форматы
                    for ep in recap['episode_stats']['shortest_episodes']:
                        ep['duration_readable'] = _seconds_to_readable(safe_int_convert(ep.get('duration', 0)))
                    for ep in recap['episode_stats']['longest_episodes']:
                        ep['duration_readable'] = _seconds_to_readable(safe_int_convert(ep.get('duration', 0)))
                    
                    recap['episode_stats']['average_duration_readable'] = _seconds_to_readable(
                        recap['episode_stats']['average_duration']
                    )
            except Exception as e:
                logger.error(f"Ошибка при расчете статистики эпизодов: {str(e)}")
                recap['episode_stats'] = {'error': str(e)}
        
        # 7. Статистика завершения
        try:
            recap['completion_stats'] = {
                'games_count': len(recap['games']),
                'average_daily_episodes': round(
                    recap['total_episodes'] / len(daily_array), 1
                ) if daily_array else 0,
                'days_with_content': len(daily_array),
                'content_density': round((len(daily_array) / 30) * 100, 1)  # Предполагаем 30 дней
            }
            
            # Только если есть данные
            if recap['games']:
                recap['completion_stats']['most_active_game_by_episodes'] = max(
                    recap['games'].items(), 
                    key=lambda x: x[1].get('episode_count', 0)
                )[0]
            
            if daily_array:
                recap['completion_stats']['busiest_day'] = max(
                    daily_array, 
                    key=lambda x: x.get('episodes', 0)
                )
                
        except Exception as e:
            logger.error(f"Ошибка при расчете статистики завершения: {str(e)}")
            recap['completion_stats'] = {'error': str(e)}
        
        # 8. Рейтинги игр
        try:
            if recap['games']:
                recap['game_rankings'] = {
                    'by_episodes': sorted(
                        [
                            {
                                'game': game,
                                'episodes': stats.get('episode_count', 0),
                                'percentage': stats.get('percentage_of_total_episodes', 0)
                            }
                            for game, stats in recap['games'].items()
                        ],
                        key=lambda x: x.get('episodes', 0),
                        reverse=True
                    ),
                    'by_duration': sorted(
                        [
                            {
                                'game': game,
                                'duration': stats.get('total_duration', 0),
                                'duration_readable': _seconds_to_readable(stats.get('total_duration', 0))
                            }
                            for game, stats in recap['games'].items()
                        ],
                        key=lambda x: x.get('duration', 0),
                        reverse=True
                    )
                }
        except Exception as e:
            logger.error(f"Ошибка при создании рейтингов: {str(e)}")
            recap['game_rankings'] = {'error': str(e)}
        
        # 9. Прогресс
        try:
            if daily_array:
                dates = [datetime.strptime(day['date'], '%Y-%m-%d') for day in daily_array if 'date' in day]
                if dates:
                    recap['progress'] = {
                        'start_date': min(dates).strftime('%Y-%m-%d'),
                        'end_date': max(dates).strftime('%Y-%m-%d'),
                        'days_with_content': len(dates),
                        'streak_days': _calculate_longest_streak([d.strftime('%Y-%m-%d') for d in dates])
                    }
        except Exception as e:
            logger.error(f"Ошибка при расчете прогресса: {str(e)}")
            recap['progress'] = {'error': str(e)}
        
        # 10. Сводка
        recap['summary'] = {
            'month': target_month,
            'total_sessions': recap['total_sessions'],
            'total_episodes': recap['total_episodes'],
            'total_duration': recap['total_duration_readable'],
            'games_played': len(recap['games']),
            'processing_status': 'Успешно'
        }
        
    except Exception as e:
        logger.error(f"Критическая ошибка при расчете статистики: {str(e)}")
        recap['summary'] = {
            'month': target_month,
            'error': 'Ошибка при расчете статистики',
            'error_details': str(e),
            'processing_status': 'С ошибками'
        }
    
    # Завершаем обработку
    recap['processing_info']['end_time'] = datetime.now().isoformat()
    recap['processing_info']['duration_seconds'] = (
        datetime.fromisoformat(recap['processing_info']['end_time']) - 
        datetime.fromisoformat(recap['processing_info']['start_time'])
    ).total_seconds()
    
    logger.info(f"Отчет за {target_month} готов. Обработка заняла {recap['processing_info']['duration_seconds']:.2f} секунд")
    
    return recap


def _seconds_to_readable(seconds: int) -> str:
    """Конвертирует секунды в читаемый формат."""
    try:
        seconds = int(seconds)
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        
        parts = []
        if hours > 0:
            parts.append(f"{hours}ч")
        if minutes > 0:
            parts.append(f"{minutes}м")
        if secs > 0 and hours == 0:
            parts.append(f"{secs}с")
        
        return ' '.join(parts) if parts else '0с'
    except:
        return '0с'


def _calculate_longest_streak(dates: List[str]) -> int:
    """Рассчитывает самую длинную серию дней подряд с контентом."""
    if not dates:
        return 0
    
    try:
        dates_sorted = sorted([datetime.strptime(d, '%Y-%m-%d') for d in dates])
        longest_streak = 1
        current_streak = 1
        
        for i in range(1, len(dates_sorted)):
            if (dates_sorted[i] - dates_sorted[i-1]).days == 1:
                current_streak += 1
                longest_streak = max(longest_streak, current_streak)
            else:
                current_streak = 1
        
        return longest_streak
    except:
        return 0


# Пример тестирования с некорректными данными
def test_with_invalid_data():
    """Тест с некорректными данными."""
    logger.info("Запуск теста с некорректными данными")
    
    test_sessions = {
        "valid_session": {
            "game": "Test Game",
            "datetime": 1765300093,
            "episodes": [
                {
                    "number": 1,
                    "title": "Valid Episode",
                    "duration": 3600,
                    "publishedAt": "2025-12-11T15:39:00Z"
                }
            ]
        },
        "invalid_datetime": {
            "game": "Test Game 2",
            "datetime": "invalid_timestamp",  # Некорректный timestamp
            "episodes": []
        },
        "missing_episodes": {
            "game": "Test Game 3",
            "datetime": 1765300093
            # Нет поля episodes
        },
        "invalid_episode_data": {
            "game": "Test Game 4",
            "datetime": 1765300093,
            "episodes": [
                {
                    # Неполные данные
                    "title": "Invalid Episode"
                }
            ]
        },
        "wrong_month": {
            "game": "Test Game 5",
            "datetime": 1609459200,  # 2021-01-01
            "episodes": [
                {
                    "number": 1,
                    "title": "Wrong Month",
                    "duration": 1800,
                    "publishedAt": "2021-01-01T12:00:00Z"
                }
            ]
        }
    }
    
    result = make_month_recap("25-12", test_sessions)
    
    print("\n=== РЕЗУЛЬТАТЫ ТЕСТА ===")
    print(f"Статус: {result.get('summary', {}).get('processing_status', 'Неизвестно')}")
    print(f"Обработано сессий: {result['processing_info']['total_sessions_processed']}")
    print(f"Пропущено сессий: {result['processing_info']['sessions_skipped']}")
    print(f"Сессий с ошибками: {result['processing_info']['sessions_with_errors']}")
    print(f"Успешных сессий: {result.get('total_sessions', 0)}")
    
    return result


if __name__ == "__main__":
    # Пример корректных данных
    sessions = {
        "1197": {
            "game": "Assassin’s Creed: Brotherhood",
            "datetime": 1765300093,
            "episodes": [
                {
                    "number": 16,
                    "title": "Ад на колесах",
                    "description": "• Шафер\n• План кампании\n• Ад на колесах\n• Линия огня\n• Волк в овечьей шкуре",
                    "publishedAt": "2025-12-11T15:39:00Z",
                    "videoId": "zY6phYvxcLs",
                    "duration": 3648
                },
                {
                    "number": 17,
                    "title": "Задания куртизанок",
                    "description": "• Спасаясь бегством\n• Врачебная ошибка\n• Сжимая кольцо\n• На живца\n• Смутьяны\n• Подделка документов\n• Неудачная политика\n• Persona non grata",
                    "publishedAt": "2025-12-11T15:44:01Z",
                    "videoId": "jGSIJdrRapo",
                    "duration": 2566
                },
                {
                    "number": 18,
                    "title": "Cento Occhi",
                    "description": "• Стремление к цели\n• Классовая борьба\n• Вечная молодость\n• Интриги\n• Сокращение штатов\n• Для поклонников\n• Полный финиш",
                    "publishedAt": "2025-12-11T15:47:01Z",
                    "videoId": "szcxlL95u_M",
                    "duration": 2812
                }
            ]
        }
    }
    
    # Тестируем с корректными данными
    print("Тест 1: Корректные данные")
    result1 = make_month_recap("25-12", sessions)
    print(f"Результат: {result1['summary']}")
    
    # Тестируем с некорректными данными
    print("\nТест 2: Некорректные данные")
    result2 = test_with_invalid_data()
    
    # Тестируем с пустыми данными
    print("\nТест 3: Пустые данные")
    result3 = make_month_recap("25-12", {})
    print(f"Результат: {result3['summary']}")
    
    # Тестируем с неверным форматом месяца
    print("\nТест 4: Неверный формат месяца")
    result4 = make_month_recap("25-13", sessions)  # Несуществующий месяц
    print(f"Результат: {result4.get('error', 'Нет ошибки')}")

def print_recap(recap):
    """
    Красивый вывод статистики за месяц в формате рекапа
    """
    
    # Основная статистика месяца
    print("═" * 60)
    print(f"📊 ИГРОВОЙ РЕКАП: СЕНТЯБРЬ 2025".center(60))
    print("═" * 60)
    
    print("\n📈 ОБЩАЯ СТАТИСТИКА МЕСЯЦА")
    print("-" * 40)
    
    # Основные цифры
    summary = recap['summary']
    print(f"🎮 Игр сыграно: {summary['games_played']}")
    print(f"🎥 Серий выпущено: {summary['total_episodes']}")
    print(f"⏱️ Общее время: {summary['total_duration']}")
    print(f"🕹️ Игровых сессий: {summary['total_sessions']}")
    
    # Процент дней с контентом
    completion = recap['completion_stats']
    density = completion['content_density']
    print(f"📅 Дней с контентом: {completion['days_with_content']} из 30 ({density}%)")
    
    # Самый активный день
    busiest = completion['busiest_day']
    print(f"🔥 Самый активный день: {busiest['date'][8:10]} сентября")
    print(f"   → {busiest['episodes']} серий ({busiest['duration_readable']})")
    
    print("\n🏆 ТОП ИГР ПО ВРЕМЕНИ")
    print("-" * 40)
    
    # Топ игр по времени
    for i, game in enumerate(recap['game_rankings']['by_duration'][:5], 1):
        medal = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"][i-1]
        game_name = game['game']
        if len(game_name) > 25:
            game_name = game_name[:22] + "..."
        print(f"{medal} {game_name:<25} {game['duration_readable']:>10}")
    
    print("\n📊 СТАТИСТИКА ПО ДНЯМ НЕДЕЛИ")
    print("-" * 40)
    
    # Статистика по дням недели
    weekdays = recap['weekday_stats_array']
    for day in weekdays:
        if day['episodes'] > 0:
            episodes_str = f"{day['episodes']} серий"
            duration_str = day['duration_readable']
            print(f"📅 {day['day']:<2} → {episodes_str:<15} ({duration_str:>8})")
    
    print("\n⏰ РАСПРЕДЕЛЕНИЕ ПО ВРЕМЕНИ СУТОК")
    print("-" * 40)
    
    # Время суток
    time_slots = recap['time_stats_array']
    for slot in time_slots:
        if slot['episodes'] > 0:
            name = slot['slot'].split(' ')[0]
            percent = slot['percentage_of_total']
            print(f"🌅 {name:<4} → {slot['episodes']:>2} серий ({percent:>4.1f}%)")
    
    print("\n🎬 САМЫЕ ДЛИННЫЕ СЕРИИ")
    print("-" * 40)
    
    # Самые длинные серии
    longest = recap['episode_stats']['longest_episodes'][:3]
    for i, ep in enumerate(longest, 1):
        game_name = ep['game']
        if len(game_name) > 20:
            game_name = game_name[:17] + "..."
        title = ep['title']
        if len(title) > 20:
            title = title[:17] + "..."
        print(f"{i}. {title:<20} ({game_name:<15}) {ep['duration_readable']:>8}")
    
    print("\n📅 ДЕТАЛИЗАЦИЯ ПО ДНЯМ")
    print("-" * 40)
    
    # Показываем несколько самых активных дней
    daily_stats = recap['daily_stats_array']
    active_days = sorted(daily_stats, key=lambda x: x['episodes'], reverse=True)[:3]
    
    for day in active_days:
        date_str = f"{day['date'][8:10]}.09"
        print(f"🗓️  {date_str} → {day['episodes']:>2} серий, {day['duration_readable']:>8}")
        print(f"   Игры: {', '.join(day['games'])}")
        if day['episodes'] > 0:
            avg_duration = day['duration'] / day['episodes'] / 60
            print(f"   Средняя длина серии: {avg_duration:.0f} мин")
        print()
    
    # Быстрые факты
    print("✨ БЫСТРЫЕ ФАКТЫ")
    print("-" * 40)
    
    ep_stats = recap['episode_stats']
    avg_duration = recap['average_duration_per_episode_readable']
    
    print(f"📏 Средняя длина серии: {avg_duration}")
    print(f"📊 Всего разных игр: {completion['games_count']}")
    print(f"⚡ Самая популярная игра: {completion['most_active_game_by_episodes']}")
    print(f"🎯 Максимальная серия: {ep_stats['longest_episodes'][0]['duration_readable']}")
    
    print("\n" + "═" * 60)
    print(f"🎉 Спасибо за просмотр! До следующего месяца!".center(60))
    print("═" * 60)


# Дополнительная функция для более компактного вывода
def print_recap_compact(recap):
    """
    Компактная версия рекапа
    """
    print("╔" + "═" * 58 + "╗")
    print(f"║{'🎮 ИГРОВОЙ РЕКАП • СЕНТЯБРЬ 2025 🎮'.center(58)}║")
    print("╠" + "═" * 58 + "╣")
    
    summary = recap['summary']
    completion = recap['completion_stats']
    
    # Первая строка: основные метрики
    print(f"║ {'🎥 Серий:':<12} {summary['total_episodes']:<5}", end="")
    print(f"{'⏱️ Время:':<10} {summary['total_duration']:<12}", end="")
    print(f"{'🎮 Игр:':<8} {summary['games_played']:<3} ║")
    
    # Вторая строка: дни
    print(f"║ {'📅 Активных дней:':<16} {completion['days_with_content']:<3}", end="")
    print(f"{'🔥 Пик:':<8} {completion['busiest_day']['date'][8:10]}.09", end="")
    print(f"{'({} серий)'.format(completion['busiest_day']['episodes']):<12} ║")
    
    # Топ-3 игры
    print("╠" + "─" * 58 + "╣")
    print(f"║ {'🏆 ТОП-3 ИГРЫ ПО ВРЕМЕНИ:'.center(58)}║")
    print("╠" + "─" * 58 + "╣")
    
    for i, game in enumerate(recap['game_rankings']['by_duration'][:3], 1):
        medal = ["🥇", "🥈", "🥉"][i-1]
        game_name = game['game']
        if len(game_name) > 25:
            game_name = game_name[:22] + "..."
        line = f"{medal} {game_name:<30} {game['duration_readable']:>10}"
        print(f"║ {line:<56} ║")
    
    print("╚" + "═" * 58 + "╝")


# Функция для вывода в формате инфографики ASCII
def print_recap_ascii(recap):
    """
    Вывод в виде ASCII инфографики
    """
    print("\n" + "▄" * 70)
    print("█" + " СТАТИСТИКА ИГР • СЕНТЯБРЬ 2025 ".center(68) + "█")
    print("▀" * 70)
    
    # Барчарт для топ игр по времени
    print("\n📊 Топ игр по времени (часы):")
    print("-" * 50)
    
    games = recap['game_rankings']['by_duration'][:5]
    max_hours = max(g['duration'] for g in games) / 3600
    
    for game in games:
        hours = game['duration'] / 3600
        bar_length = int((hours / max_hours) * 40)
        bar = "█" * bar_length
        
        # Сокращаем название игры если нужно
        name = game['game']
        if len(name) > 20:
            name = name[:17] + "..."
        
        print(f"{name:<20} {bar:40} {hours:5.1f}ч")
    
    # Дни недели активность
    print("\n📅 Активность по дням недели:")
    print("-" * 50)
    
    weekdays = recap['weekday_stats_array']
    max_episodes = max(w['episodes'] for w in weekdays)
    
    for day in weekdays:
        episodes = day['episodes']
        if max_episodes > 0:
            bar_length = int((episodes / max_episodes) * 30)
        else:
            bar_length = 0
        bar = "▓" * bar_length
        
        print(f"{day['day']:<2} {bar:30} {episodes:2} серий")
    
    # Быстрая статистика
    print("\n" + "─" * 50)
    stats = recap['completion_stats']
    ep_stats = recap['episode_stats']
    
    quick_stats = [
        f"🎯 Сред. длина: {recap['average_duration_per_episode_readable']}",
        f"📈 Лучший день: {stats['busiest_day']['episodes']} серий",
        f"⚡ Самая длинная: {ep_stats['longest_episodes'][0]['duration_readable']}",
        f"🏆 Лидер: {recap['game_rankings']['by_duration'][0]['game']}"
    ]
    
    # Вывод в 2 колонки
    for i in range(0, len(quick_stats), 2):
        if i + 1 < len(quick_stats):
            print(f"{quick_stats[i]:<30} {quick_stats[i+1]}")
        else:
            print(quick_stats[i])
    
    print("─" * 50)
    print("🎉 Отличный месяц! Продолжаем в том же духе!".center(50))
    print("▄" * 70)


@handle_errors
def make_year_recap(target_year: str, sessions: Dict) -> Dict[str, Any]:
    """
    Создает подробную статистику за указанный год.
    
    Args:
        target_year: Год в формате "YY" (например "25")
        sessions: Словарь с данными о сессиях
    
    Returns:
        Словарь с подробной статистикой за год
    """
    
    logger.info(f"Начинаем создание отчета за 20{target_year} год")
    
    # Базовый объект отчета
    recap = {
        'target_year': target_year,
        'total_sessions': 0,
        'total_episodes': 0,
        'total_duration': 0,
        'games': {},
        'monthly_stats': {},
        'seasonal_stats': {},
        'quarterly_stats': {},
        'game_rankings': {},
        'top_months': {},
        'summary': {},
        'processing_info': {
            'start_time': datetime.now().isoformat(),
            'total_sessions_processed': 0,
            'sessions_skipped': 0,
            'sessions_with_errors': 0
        }
    }
    
    # Проверяем входные данные
    if not sessions:
        logger.warning("Передан пустой словарь sessions")
        recap['summary'] = {
            'message': 'Нет данных для обработки',
            'target_year': f"20{target_year}"
        }
        recap['processing_info']['end_time'] = datetime.now().isoformat()
        return recap
    
    # Проверяем формат года
    try:
        full_year = int(f"20{target_year}")
        if not 2000 <= full_year <= 2100:
            raise ValueError
        logger.debug(f"Формат года 20{target_year} корректен")
    except Exception as e:
        error_msg = f"Неверный формат года: {target_year}. Используйте YY"
        logger.error(error_msg)
        recap['error'] = error_msg
        recap['processing_info']['end_time'] = datetime.now().isoformat()
        return recap
    
    all_episodes = []
    all_sessions = []
    monthly_data = {}
    
    # Обрабатываем сессии
    for session_id, session_data in sessions.items():
        recap['processing_info']['total_sessions_processed'] += 1
        
        # Валидация данных сессии
        if not validate_session_data(session_id, session_data):
            recap['processing_info']['sessions_with_errors'] += 1
            logger.warning(f"Пропускаем сессию {session_id} из-за ошибок валидации")
            continue
        
        try:
            # Безопасное получение данных
            game_name = session_data.get('game', 'Неизвестная игра')
            timestamp = session_data.get('datetime')
            
            # Преобразуем дату
            session_date = safe_datetime_convert(timestamp)
            if not session_date:
                recap['processing_info']['sessions_skipped'] += 1
                logger.warning(f"Пропускаем сессию {session_id}: не удалось преобразовать дату")
                continue
            
            # Проверяем год
            session_year = session_date.strftime('%y')
            if session_year != target_year:
                recap['processing_info']['sessions_skipped'] += 1
                logger.debug(f"Сессия {session_id} не в целевом годе: 20{session_year}")
                continue
            
            # Основная статистика
            episodes = session_data.get('episodes', [])
            episode_count = len(episodes)
            
            recap['total_sessions'] += 1
            recap['total_episodes'] += episode_count
            
            # Инициализация статистики по игре
            if game_name not in recap['games']:
                recap['games'][game_name] = {
                    'session_count': 0,
                    'episode_count': 0,
                    'total_duration': 0,
                    'monthly_activity': {},
                    'episodes': [],
                    'titles': [],
                    'durations': []
                }
            
            game_stats = recap['games'][game_name]
            game_stats['session_count'] += 1
            game_stats['episode_count'] += episode_count
            
            # Месяц сессии
            session_month = session_date.strftime('%m')
            session_month_name = session_date.strftime('%b')
            
            # Статистика по месяцам
            if session_month not in monthly_data:
                monthly_data[session_month] = {
                    'name': session_month_name,
                    'episodes': 0,
                    'duration': 0,
                    'sessions': 0,
                    'games': set(),
                    'total_games': 0
                }
            
            month_stats = monthly_data[session_month]
            month_stats['episodes'] += episode_count
            month_stats['sessions'] += 1
            month_stats['games'].add(game_name)
            
            # Обновляем статистику игры по месяцам
            if session_month not in game_stats['monthly_activity']:
                game_stats['monthly_activity'][session_month] = {
                    'episodes': 0,
                    'duration': 0
                }
            
            # Обрабатываем эпизоды
            for episode in episodes:
                try:
                    # Безопасное получение данных эпизода
                    episode_duration = safe_int_convert(episode.get('duration', 0))
                    episode_title = episode.get('title', 'Без названия')
                    episode_number = safe_int_convert(episode.get('number', 0))
                    published_at = episode.get('publishedAt')
                    
                    # Обновляем статистику
                    recap['total_duration'] += episode_duration
                    game_stats['total_duration'] += episode_duration
                    month_stats['duration'] += episode_duration
                    game_stats['monthly_activity'][session_month]['duration'] += episode_duration
                    game_stats['monthly_activity'][session_month]['episodes'] += 1
                    
                    # Собираем данные эпизода
                    episode_data = {
                        'number': episode_number,
                        'title': episode_title,
                        'duration': episode_duration,
                        'published_at': published_at,
                        'game': game_name,
                        'session_id': session_id,
                        'month': session_month,
                        'month_name': session_month_name
                    }
                    
                    game_stats['episodes'].append(episode_data)
                    game_stats['titles'].append(episode_title)
                    game_stats['durations'].append(episode_duration)
                    
                    all_episodes.append(episode_data)
                    
                except Exception as e:
                    logger.error(f"Ошибка при обработке эпизода в сессии {session_id}: {str(e)}")
                    recap['processing_info']['sessions_with_errors'] += 1
                    continue
            
            all_sessions.append({
                'id': session_id,
                'game': game_name,
                'date': session_date,
                'episode_count': episode_count,
                'month': session_month
            })
                    
        except Exception as e:
            logger.error(f"Ошибка при обработке сессии {session_id}: {str(e)}")
            recap['processing_info']['sessions_with_errors'] += 1
            continue
    
    logger.info(f"Обработано {recap['total_sessions']} сессий, {recap['total_episodes']} эпизодов за 20{target_year} год")
    
    # Если нет данных за год
    if recap['total_episodes'] == 0:
        recap['summary'] = {
            'message': f'Нет данных за 20{target_year} год',
            'target_year': f"20{target_year}",
            'sessions_processed': recap['processing_info']['total_sessions_processed']
        }
        recap['processing_info']['end_time'] = datetime.now().isoformat()
        return recap
    
    # Расчет статистики
    try:
        # 1. Основные средние значения
        recap['average_episodes_per_session'] = round(
            recap['total_episodes'] / recap['total_sessions'], 2
        ) if recap['total_sessions'] > 0 else 0
        
        recap['average_duration_per_episode'] = round(
            recap['total_duration'] / recap['total_episodes']
        ) if recap['total_episodes'] > 0 else 0
        
        recap['average_duration_per_session'] = round(
            recap['total_duration'] / recap['total_sessions']
        ) if recap['total_sessions'] > 0 else 0
        
        # Конвертируем длительность
        recap['total_duration_readable'] = _seconds_to_readable(recap['total_duration'])
        recap['average_duration_per_episode_readable'] = _seconds_to_readable(
            recap['average_duration_per_episode']
        )
        recap['total_duration_hours'] = round(recap['total_duration'] / 3600, 2)
        recap['total_duration_days'] = round(recap['total_duration'] / 86400, 2)
        
        # 2. Статистика по месяцам
        monthly_stats_array = []
        for month_num in range(1, 13):
            month_str = f"{month_num:02d}"
            month_name = datetime(2000, month_num, 1).strftime('%b')
            
            if month_str in monthly_data:
                data = monthly_data[month_str]
                monthly_stats = {
                    'month': month_str,
                    'month_name': month_name,
                    'episodes': data['episodes'],
                    'duration': data['duration'],
                    'duration_readable': _seconds_to_readable(data['duration']),
                    'sessions': data['sessions'],
                    'games': list(data['games']),
                    'games_count': len(data['games']),
                    'average_episodes_per_session': round(data['episodes'] / data['sessions'], 2) if data['sessions'] > 0 else 0,
                    'average_duration_per_episode': round(data['duration'] / data['episodes']) if data['episodes'] > 0 else 0
                }
                
                # Проценты от общего
                monthly_stats['percentage_of_year_episodes'] = round(
                    (data['episodes'] / recap['total_episodes']) * 100, 1
                ) if recap['total_episodes'] > 0 else 0
                
                monthly_stats['percentage_of_year_duration'] = round(
                    (data['duration'] / recap['total_duration']) * 100, 1
                ) if recap['total_duration'] > 0 else 0
            else:
                monthly_stats = {
                    'month': month_str,
                    'month_name': month_name,
                    'episodes': 0,
                    'duration': 0,
                    'duration_readable': '0с',
                    'sessions': 0,
                    'games': [],
                    'games_count': 0,
                    'average_episodes_per_session': 0,
                    'average_duration_per_episode': 0,
                    'percentage_of_year_episodes': 0,
                    'percentage_of_year_duration': 0
                }
            
            monthly_stats_array.append(monthly_stats)
        
        recap['monthly_stats'] = monthly_stats_array
        recap['active_months'] = len([m for m in monthly_stats_array if m['episodes'] > 0])
        
        # Топ месяцев
        recap['top_months'] = {
            'by_episodes': sorted(
                [m for m in monthly_stats_array if m['episodes'] > 0],
                key=lambda x: x['episodes'],
                reverse=True
            )[:3],
            'by_duration': sorted(
                [m for m in monthly_stats_array if m['duration'] > 0],
                key=lambda x: x['duration'],
                reverse=True
            )[:3],
            'by_games_count': sorted(
                [m for m in monthly_stats_array if m['games_count'] > 0],
                key=lambda x: x['games_count'],
                reverse=True
            )[:3]
        }
        
        # 3. Статистика по временам года
        seasons = {
            'Зима': ['12', '01', '02'],
            'Весна': ['03', '04', '05'],
            'Лето': ['06', '07', '08'],
            'Осень': ['09', '10', '11']
        }
        
        seasonal_stats = []
        for season_name, months in seasons.items():
            season_data = {
                'name': season_name,
                'episodes': 0,
                'duration': 0,
                'sessions': 0,
                'games': set(),
                'months_active': 0
            }
            
            for month in months:
                month_data = next((m for m in monthly_stats_array if m['month'] == month), None)
                if month_data and month_data['episodes'] > 0:
                    season_data['episodes'] += month_data['episodes']
                    season_data['duration'] += month_data['duration']
                    season_data['sessions'] += month_data['sessions']
                    season_data['games'].update(month_data['games'])
                    season_data['months_active'] += 1
            
            if season_data['episodes'] > 0:
                season_data['duration_readable'] = _seconds_to_readable(season_data['duration'])
                season_data['games_count'] = len(season_data['games'])
                season_data['games'] = list(season_data['games'])
                season_data['average_episodes_per_session'] = round(
                    season_data['episodes'] / season_data['sessions'], 2
                ) if season_data['sessions'] > 0 else 0
                
                seasonal_stats.append(season_data)
        
        recap['seasonal_stats'] = seasonal_stats
        
        # 4. Статистика по кварталам
        quarters = {
            'Q1': ['01', '02', '03'],
            'Q2': ['04', '05', '06'],
            'Q3': ['07', '08', '09'],
            'Q4': ['10', '11', '12']
        }
        
        quarterly_stats = []
        for quarter_name, months in quarters.items():
            quarter_data = {
                'name': quarter_name,
                'episodes': 0,
                'duration': 0,
                'sessions': 0,
                'games': set()
            }
            
            for month in months:
                month_data = next((m for m in monthly_stats_array if m['month'] == month), None)
                if month_data:
                    quarter_data['episodes'] += month_data['episodes']
                    quarter_data['duration'] += month_data['duration']
                    quarter_data['sessions'] += month_data['sessions']
                    quarter_data['games'].update(month_data['games'])
            
            quarter_data['duration_readable'] = _seconds_to_readable(quarter_data['duration'])
            quarter_data['games_count'] = len(quarter_data['games'])
            quarter_data['games'] = list(quarter_data['games'])
            quarterly_stats.append(quarter_data)
        
        recap['quarterly_stats'] = quarterly_stats
        
        # 5. Статистика по играм
        for game_name, game_stats in recap['games'].items():
            try:
                game_stats['total_duration_readable'] = _seconds_to_readable(game_stats['total_duration'])
                
                # Средние значения
                game_stats['average_duration_per_episode'] = round(
                    game_stats['total_duration'] / game_stats['episode_count']
                ) if game_stats['episode_count'] > 0 else 0
                
                game_stats['average_episodes_per_session'] = round(
                    game_stats['episode_count'] / game_stats['session_count'], 2
                ) if game_stats['session_count'] > 0 else 0
                
                # Проценты
                game_stats['percentage_of_total_episodes'] = round(
                    (game_stats['episode_count'] / recap['total_episodes']) * 100, 1
                ) if recap['total_episodes'] > 0 else 0
                
                game_stats['percentage_of_total_duration'] = round(
                    (game_stats['total_duration'] / recap['total_duration']) * 100, 1
                ) if recap['total_duration'] > 0 else 0
                
                # Месячная активность
                active_months = [m for m, data in game_stats['monthly_activity'].items() if data['episodes'] > 0]
                game_stats['active_months_count'] = len(active_months)
                game_stats['monthly_activity_percentage'] = round((len(active_months) / 12) * 100, 1)
                
                # Дата начала и конца
                episodes = game_stats.get('episodes', [])
                if episodes:
                    dates = []
                    for ep in episodes:
                        if ep.get('published_at'):
                            try:
                                if 'T' in ep['published_at']:
                                    dt = datetime.fromisoformat(ep['published_at'].replace('Z', '+00:00'))
                                else:
                                    dt = datetime.strptime(ep['published_at'], '%Y-%m-%d %H:%M:%S')
                                dates.append(dt)
                            except:
                                continue
                    
                    if dates:
                        game_stats['date_range'] = {
                            'first': min(dates).strftime('%Y-%m-%d'),
                            'last': max(dates).strftime('%Y-%m-%d'),
                            'days_active': (max(dates) - min(dates)).days
                        }
                    else:
                        game_stats['date_range'] = {'first': None, 'last': None, 'days_active': 0}
                else:
                    game_stats['date_range'] = {'first': None, 'last': None, 'days_active': 0}
                
                # Сортировка эпизодов
                game_stats['episodes'].sort(key=lambda x: safe_int_convert(x.get('number', 0)))
                
            except Exception as e:
                logger.error(f"Ошибка при обработке статистики игры {game_name}: {str(e)}")
                continue
        
        # 6. Рейтинги игр
        try:
            if recap['games']:
                recap['game_rankings'] = {
                    'by_episodes': sorted(
                        [
                            {
                                'game': game,
                                'episodes': stats.get('episode_count', 0),
                                'percentage': stats.get('percentage_of_total_episodes', 0),
                                'active_months': stats.get('active_months_count', 0)
                            }
                            for game, stats in recap['games'].items()
                        ],
                        key=lambda x: x.get('episodes', 0),
                        reverse=True
                    ),
                    'by_duration': sorted(
                        [
                            {
                                'game': game,
                                'duration': stats.get('total_duration', 0),
                                'duration_readable': _seconds_to_readable(stats.get('total_duration', 0)),
                                'duration_hours': round(stats.get('total_duration', 0) / 3600, 2)
                            }
                            for game, stats in recap['games'].items()
                        ],
                        key=lambda x: x.get('duration', 0),
                        reverse=True
                    ),
                    'by_sessions': sorted(
                        [
                            {
                                'game': game,
                                'sessions': stats.get('session_count', 0),
                                'average_episodes': stats.get('average_episodes_per_session', 0)
                            }
                            for game, stats in recap['games'].items()
                        ],
                        key=lambda x: x.get('sessions', 0),
                        reverse=True
                    )
                }
        except Exception as e:
            logger.error(f"Ошибка при создании рейтингов игр: {str(e)}")
            recap['game_rankings'] = {'error': str(e)}
        
        # 7. Статистика серий
        if all_sessions:
            try:
                recap['session_stats'] = {
                    'total': len(all_sessions),
                    'average_episodes_per_session': recap['average_episodes_per_session'],
                    'average_duration_per_session': recap['average_duration_per_session'],
                    'sessions_by_month': {},
                    'longest_break': _calculate_longest_break([s['date'] for s in all_sessions])
                }
                
                # Сессии по месяцам
                for session in all_sessions:
                    month = session['month']
                    if month not in recap['session_stats']['sessions_by_month']:
                        recap['session_stats']['sessions_by_month'][month] = 0
                    recap['session_stats']['sessions_by_month'][month] += 1
                
            except Exception as e:
                logger.error(f"Ошибка при расчете статистики сессий: {str(e)}")
                recap['session_stats'] = {'error': str(e)}
        
        # 8. Анализ эпизодов
        if all_episodes:
            try:
                durations = [safe_int_convert(ep.get('duration', 0)) for ep in all_episodes]
                valid_durations = [d for d in durations if d > 0]
                
                if valid_durations:
                    recap['episode_analysis'] = {
                        'total_count': len(all_episodes),
                        'average_duration': round(sum(valid_durations) / len(valid_durations)),
                        'average_duration_readable': _seconds_to_readable(
                            round(sum(valid_durations) / len(valid_durations))
                        ),
                        'median_duration': int(statistics.median(valid_durations)) if valid_durations else 0,
                        'duration_categories': {
                            'short': len([d for d in valid_durations if d < 1800]),
                            'medium': len([d for d in valid_durations if 1800 <= d < 3600]),
                            'long': len([d for d in valid_durations if 3600 <= d < 7200]),
                            'very_long': len([d for d in valid_durations if d >= 7200])
                        },
                        'longest_episodes': sorted(
                            all_episodes, 
                            key=lambda x: safe_int_convert(x.get('duration', 0)), 
                            reverse=True
                        )[:5]
                    }
                    
                    # Добавляем читаемые форматы для самых длинных эпизодов
                    for ep in recap['episode_analysis']['longest_episodes']:
                        ep['duration_readable'] = _seconds_to_readable(safe_int_convert(ep.get('duration', 0)))
                    
                    # Проценты категорий
                    total_valid = sum(recap['episode_analysis']['duration_categories'].values())
                    if total_valid > 0:
                        for category in recap['episode_analysis']['duration_categories']:
                            count = recap['episode_analysis']['duration_categories'][category]
                            recap['episode_analysis']['duration_categories'][f'{category}_percentage'] = round(
                                (count / total_valid) * 100, 1
                            )
            except Exception as e:
                logger.error(f"Ошибка при анализе эпизодов: {str(e)}")
                recap['episode_analysis'] = {'error': str(e)}
        
        # 9. Сводка
        recap['summary'] = {
            'year': f"20{target_year}",
            'total_sessions': recap['total_sessions'],
            'total_episodes': recap['total_episodes'],
            'total_duration': recap['total_duration_readable'],
            'total_duration_hours': recap['total_duration_hours'],
            'games_played': len(recap['games']),
            'active_months': recap['active_months'],
            'most_active_month': recap['top_months']['by_episodes'][0]['month_name'] if recap['top_months']['by_episodes'] else 'Нет данных',
            'most_played_game': recap['game_rankings']['by_episodes'][0]['game'] if recap['game_rankings']['by_episodes'] else 'Нет данных',
            'processing_status': 'Успешно'
        }
        
    except Exception as e:
        logger.error(f"Критическая ошибка при расчете статистики за год: {str(e)}")
        recap['summary'] = {
            'year': f"20{target_year}",
            'error': 'Ошибка при расчете статистики',
            'error_details': str(e),
            'processing_status': 'С ошибками'
        }
    
    # Завершаем обработку
    recap['processing_info']['end_time'] = datetime.now().isoformat()
    recap['processing_info']['duration_seconds'] = (
        datetime.fromisoformat(recap['processing_info']['end_time']) - 
        datetime.fromisoformat(recap['processing_info']['start_time'])
    ).total_seconds()
    
    logger.info(f"Отчет за 20{target_year} год готов. Обработка заняла {recap['processing_info']['duration_seconds']:.2f} секунд")
    
    return recap


@handle_errors
def make_all_time_recap(sessions: Dict) -> Dict[str, Any]:
    """
    Создает подробную статистику за все время.
    
    Args:
        sessions: Словарь с данными о сессиях
    
    Returns:
        Словарь с подробной статистикой за все время
    """
    
    logger.info(f"Начинаем создание отчета за все время")
    
    # Базовый объект отчета
    recap = {
        'period': 'all_time',
        'total_sessions': 0,
        'total_episodes': 0,
        'total_duration': 0,
        'games': {},
        'yearly_stats': {},
        'monthly_trends': {},
        'game_rankings': {},
        'milestones': {},
        'records': {},
        'summary': {},
        'processing_info': {
            'start_time': datetime.now().isoformat(),
            'total_sessions_processed': 0,
            'sessions_skipped': 0,
            'sessions_with_errors': 0
        }
    }
    
    # Проверяем входные данные
    if not sessions:
        logger.warning("Передан пустой словарь sessions")
        recap['summary'] = {
            'message': 'Нет данных для обработки',
            'period': 'all_time'
        }
        recap['processing_info']['end_time'] = datetime.now().isoformat()
        return recap
    
    all_episodes = []
    all_sessions = []
    yearly_data = {}
    monthly_trend_data = {}
    
    # Обрабатываем сессии
    for session_id, session_data in sessions.items():
        recap['processing_info']['total_sessions_processed'] += 1
        
        # Валидация данных сессии
        if not validate_session_data(session_id, session_data):
            recap['processing_info']['sessions_with_errors'] += 1
            logger.warning(f"Пропускаем сессию {session_id} из-за ошибок валидации")
            continue
        
        try:
            # Безопасное получение данных
            game_name = session_data.get('game', 'Неизвестная игра')
            timestamp = session_data.get('datetime')
            
            # Преобразуем дату
            session_date = safe_datetime_convert(timestamp)
            if not session_date:
                recap['processing_info']['sessions_skipped'] += 1
                logger.warning(f"Пропускаем сессию {session_id}: не удалось преобразовать дату")
                continue
            
            # Основная статистика
            episodes = session_data.get('episodes', [])
            episode_count = len(episodes)
            
            recap['total_sessions'] += 1
            recap['total_episodes'] += episode_count
            
            # Год и месяц
            session_year = session_date.strftime('%Y')
            session_year_short = session_date.strftime('%y')
            session_month = session_date.strftime('%m')
            year_month_key = f"{session_year}-{session_month}"
            
            # Статистика по годам
            if session_year not in yearly_data:
                yearly_data[session_year] = {
                    'year': session_year,
                    'year_short': session_year_short,
                    'episodes': 0,
                    'duration': 0,
                    'sessions': 0,
                    'games': set(),
                    'months': set()
                }
            
            year_stats = yearly_data[session_year]
            year_stats['episodes'] += episode_count
            year_stats['sessions'] += 1
            year_stats['games'].add(game_name)
            year_stats['months'].add(session_month)
            
            # Статистика по месяцам (для трендов)
            if year_month_key not in monthly_trend_data:
                monthly_trend_data[year_month_key] = {
                    'year': session_year,
                    'month': session_month,
                    'month_name': session_date.strftime('%b'),
                    'episodes': 0,
                    'duration': 0,
                    'sessions': 0,
                    'games': set()
                }
            
            month_trend_stats = monthly_trend_data[year_month_key]
            month_trend_stats['episodes'] += episode_count
            month_trend_stats['sessions'] += 1
            month_trend_stats['games'].add(game_name)
            
            # Инициализация статистики по игре
            if game_name not in recap['games']:
                recap['games'][game_name] = {
                    'session_count': 0,
                    'episode_count': 0,
                    'total_duration': 0,
                    'years_active': set(),
                    'first_session': None,
                    'last_session': None,
                    'episodes': [],
                    'durations': []
                }
            
            game_stats = recap['games'][game_name]
            game_stats['session_count'] += 1
            game_stats['episode_count'] += episode_count
            game_stats['years_active'].add(session_year)
            
            # Обновляем даты сессий для игры
            if not game_stats['first_session'] or session_date < game_stats['first_session']:
                game_stats['first_session'] = session_date
            if not game_stats['last_session'] or session_date > game_stats['last_session']:
                game_stats['last_session'] = session_date
            
            # Обрабатываем эпизоды
            for episode in episodes:
                try:
                    # Безопасное получение данных эпизода
                    episode_duration = safe_int_convert(episode.get('duration', 0))
                    episode_title = episode.get('title', 'Без названия')
                    episode_number = safe_int_convert(episode.get('number', 0))
                    published_at = episode.get('publishedAt')
                    
                    # Обновляем статистику
                    recap['total_duration'] += episode_duration
                    game_stats['total_duration'] += episode_duration
                    year_stats['duration'] += episode_duration
                    month_trend_stats['duration'] += episode_duration
                    
                    # Собираем данные эпизода
                    episode_data = {
                        'number': episode_number,
                        'title': episode_title,
                        'duration': episode_duration,
                        'published_at': published_at,
                        'game': game_name,
                        'session_id': session_id,
                        'year': session_year,
                        'month': session_month
                    }
                    
                    game_stats['episodes'].append(episode_data)
                    game_stats['durations'].append(episode_duration)
                    
                    all_episodes.append(episode_data)
                    
                except Exception as e:
                    logger.error(f"Ошибка при обработке эпизода в сессии {session_id}: {str(e)}")
                    recap['processing_info']['sessions_with_errors'] += 1
                    continue
            
            all_sessions.append({
                'id': session_id,
                'game': game_name,
                'date': session_date,
                'episode_count': episode_count,
                'year': session_year,
                'month': session_month
            })
                    
        except Exception as e:
            logger.error(f"Ошибка при обработке сессии {session_id}: {str(e)}")
            recap['processing_info']['sessions_with_errors'] += 1
            continue
    
    logger.info(f"Обработано {recap['total_sessions']} сессий, {recap['total_episodes']} эпизодов за все время")
    
    # Если нет данных
    if recap['total_episodes'] == 0:
        recap['summary'] = {
            'message': 'Нет данных для обработки',
            'period': 'all_time',
            'sessions_processed': recap['processing_info']['total_sessions_processed']
        }
        recap['processing_info']['end_time'] = datetime.now().isoformat()
        return recap
    
    # Расчет статистики
    try:
        # 1. Основные средние значения
        recap['average_episodes_per_session'] = round(
            recap['total_episodes'] / recap['total_sessions'], 2
        ) if recap['total_sessions'] > 0 else 0
        
        recap['average_duration_per_episode'] = round(
            recap['total_duration'] / recap['total_episodes']
        ) if recap['total_episodes'] > 0 else 0
        
        recap['average_duration_per_session'] = round(
            recap['total_duration'] / recap['total_sessions']
        ) if recap['total_sessions'] > 0 else 0
        
        # Конвертируем длительность
        recap['total_duration_readable'] = _seconds_to_readable(recap['total_duration'])
        recap['average_duration_per_episode_readable'] = _seconds_to_readable(
            recap['average_duration_per_episode']
        )
        recap['total_duration_hours'] = round(recap['total_duration'] / 3600, 2)
        recap['total_duration_days'] = round(recap['total_duration'] / 86400, 2)
        
        # 2. Статистика по годам
        yearly_stats_array = []
        all_years = sorted(yearly_data.keys())
        
        for year in all_years:
            data = yearly_data[year]
            yearly_stats = {
                'year': year,
                'year_short': data['year_short'],
                'episodes': data['episodes'],
                'duration': data['duration'],
                'duration_readable': _seconds_to_readable(data['duration']),
                'sessions': data['sessions'],
                'games': list(data['games']),
                'games_count': len(data['games']),
                'months_active': len(data['months']),
                'average_episodes_per_session': round(data['episodes'] / data['sessions'], 2) if data['sessions'] > 0 else 0,
                'average_duration_per_episode': round(data['duration'] / data['episodes']) if data['episodes'] > 0 else 0
            }
            
            # Проценты от общего
            yearly_stats['percentage_of_total_episodes'] = round(
                (data['episodes'] / recap['total_episodes']) * 100, 1
            ) if recap['total_episodes'] > 0 else 0
            
            yearly_stats['percentage_of_total_duration'] = round(
                (data['duration'] / recap['total_duration']) * 100, 1
            ) if recap['total_duration'] > 0 else 0
            
            yearly_stats_array.append(yearly_stats)
        
        recap['yearly_stats'] = yearly_stats_array
        
        # 3. Месячные тренды
        monthly_trends_array = []
        sorted_months = sorted(monthly_trend_data.keys())
        
        for month_key in sorted_months:
            data = monthly_trend_data[month_key]
            trend_stats = {
                'year_month': month_key,
                'year': data['year'],
                'month': data['month'],
                'month_name': data['month_name'],
                'episodes': data['episodes'],
                'duration': data['duration'],
                'sessions': data['sessions'],
                'games_count': len(data['games'])
            }
            
            monthly_trends_array.append(trend_stats)
        
        recap['monthly_trends'] = monthly_trends_array
        
        # 4. Статистика по играм
        for game_name, game_stats in recap['games'].items():
            try:
                game_stats['total_duration_readable'] = _seconds_to_readable(game_stats['total_duration'])
                game_stats['total_duration_hours'] = round(game_stats['total_duration'] / 3600, 2)
                
                # Средние значения
                game_stats['average_duration_per_episode'] = round(
                    game_stats['total_duration'] / game_stats['episode_count']
                ) if game_stats['episode_count'] > 0 else 0
                
                game_stats['average_episodes_per_session'] = round(
                    game_stats['episode_count'] / game_stats['session_count'], 2
                ) if game_stats['session_count'] > 0 else 0
                
                # Проценты
                game_stats['percentage_of_total_episodes'] = round(
                    (game_stats['episode_count'] / recap['total_episodes']) * 100, 1
                ) if recap['total_episodes'] > 0 else 0
                
                game_stats['percentage_of_total_duration'] = round(
                    (game_stats['total_duration'] / recap['total_duration']) * 100, 1
                ) if recap['total_duration'] > 0 else 0
                
                # Активность по годам
                game_stats['years_active'] = sorted(list(game_stats['years_active']))
                game_stats['years_active_count'] = len(game_stats['years_active'])
                
                # Продолжительность активности
                if game_stats['first_session'] and game_stats['last_session']:
                    days_active = (game_stats['last_session'] - game_stats['first_session']).days
                    game_stats['active_period'] = {
                        'first': game_stats['first_session'].strftime('%Y-%m-%d'),
                        'last': game_stats['last_session'].strftime('%Y-%m-%d'),
                        'days': days_active,
                        'years': round(days_active / 365, 1)
                    }
                else:
                    game_stats['active_period'] = {'first': None, 'last': None, 'days': 0, 'years': 0}
                
                # Статистика по продолжительности эпизодов
                durations = game_stats.get('durations', [])
                if durations:
                    game_stats['duration_stats'] = {
                        'shortest': min(durations),
                        'longest': max(durations),
                        'average': game_stats['average_duration_per_episode'],
                        'total_hours': round(game_stats['total_duration'] / 3600, 2)
                    }
                
                # Сортировка эпизодов
                game_stats['episodes'].sort(key=lambda x: (
                    x.get('year', '0000'),
                    x.get('month', '00'),
                    safe_int_convert(x.get('number', 0))
                ))
                
            except Exception as e:
                logger.error(f"Ошибка при обработке статистики игры {game_name}: {str(e)}")
                continue
        
        # 5. Рейтинги и рекорды
        try:
            # Рейтинги игр
            recap['game_rankings'] = {
                'by_episodes': sorted(
                    [
                        {
                            'game': game,
                            'episodes': stats.get('episode_count', 0),
                            'percentage': stats.get('percentage_of_total_episodes', 0),
                            'years_active': stats.get('years_active_count', 0)
                        }
                        for game, stats in recap['games'].items()
                    ],
                    key=lambda x: x.get('episodes', 0),
                    reverse=True
                ),
                'by_duration': sorted(
                    [
                        {
                            'game': game,
                            'duration': stats.get('total_duration', 0),
                            'duration_readable': _seconds_to_readable(stats.get('total_duration', 0)),
                            'duration_hours': round(stats.get('total_duration', 0) / 3600, 2)
                        }
                        for game, stats in recap['games'].items()
                    ],
                    key=lambda x: x.get('duration', 0),
                    reverse=True
                ),
                'by_sessions': sorted(
                    [
                        {
                            'game': game,
                            'sessions': stats.get('session_count', 0),
                            'average_episodes': stats.get('average_episodes_per_session', 0)
                        }
                        for game, stats in recap['games'].items()
                    ],
                    key=lambda x: x.get('sessions', 0),
                    reverse=True
                ),
                'by_longevity': sorted(
                    [
                        {
                            'game': game,
                            'years_active': stats.get('years_active_count', 0),
                            'active_period': stats.get('active_period', {}).get('days', 0),
                            'first_year': stats.get('active_period', {}).get('first', '')[:4]
                        }
                        for game, stats in recap['games'].items()
                        if stats.get('active_period', {}).get('days', 0) > 0
                    ],
                    key=lambda x: x.get('years_active', 0),
                    reverse=True
                )
            }
            
            # Рекорды
            if all_episodes:
                recap['records'] = {
                    'longest_episode': max(all_episodes, key=lambda x: safe_int_convert(x.get('duration', 0))),
                    'most_episodes_in_year': max(yearly_stats_array, key=lambda x: x.get('episodes', 0)),
                    'most_games_in_year': max(yearly_stats_array, key=lambda x: x.get('games_count', 0)),
                    'best_month': max(monthly_trends_array, key=lambda x: x.get('episodes', 0)) if monthly_trends_array else None,
                    'longest_streak': _calculate_longest_streak([s['date'].strftime('%Y-%m-%d') for s in all_sessions])
                }
                
                # Добавляем читаемые форматы для рекордов
                if recap['records']['longest_episode']:
                    recap['records']['longest_episode']['duration_readable'] = _seconds_to_readable(
                        safe_int_convert(recap['records']['longest_episode'].get('duration', 0))
                    )
                
        except Exception as e:
            logger.error(f"Ошибка при создании рейтингов и рекордов: {str(e)}")
            recap['game_rankings'] = {'error': str(e)}
            recap['records'] = {'error': str(e)}
        
        # 6. Вехи и достижения
        try:
            recap['milestones'] = {
                'total_episodes': recap['total_episodes'],
                'total_duration_hours': recap['total_duration_hours'],
                'total_games': len(recap['games']),
                'total_years': len(yearly_stats_array),
                'first_year': all_years[0] if all_years else None,
                'latest_year': all_years[-1] if all_years else None,
                'average_episodes_per_year': round(recap['total_episodes'] / len(yearly_stats_array)) if yearly_stats_array else 0,
                'average_games_per_year': round(len(recap['games']) / len(yearly_stats_array), 1) if yearly_stats_array else 0
            }
            
            # Статистика по десятилетиям если есть
            if len(all_years) > 5:
                decades = {}
                for year_stats in yearly_stats_array:
                    decade = f"{year_stats['year'][:3]}0-е"
                    if decade not in decades:
                        decades[decade] = {'episodes': 0, 'duration': 0, 'years': 0}
                    
                    decades[decade]['episodes'] += year_stats['episodes']
                    decades[decade]['duration'] += year_stats['duration']
                    decades[decade]['years'] += 1
                
                # Рассчитываем средние
                for decade in decades:
                    decades[decade]['average_episodes_per_year'] = round(
                        decades[decade]['episodes'] / decades[decade]['years']
                    )
                    decades[decade]['duration_readable'] = _seconds_to_readable(decades[decade]['duration'])
                
                recap['milestones']['decades'] = decades
            
        except Exception as e:
            logger.error(f"Ошибка при расчете вех: {str(e)}")
            recap['milestones'] = {'error': str(e)}
        
        # 7. Анализ трендов
        try:
            if len(yearly_stats_array) >= 2:
                recap['trend_analysis'] = {
                    'episodes_growth': [],
                    'duration_growth': [],
                    'games_growth': []
                }
                
                # Рассчитываем рост по годам
                for i in range(1, len(yearly_stats_array)):
                    prev_year = yearly_stats_array[i-1]
                    curr_year = yearly_stats_array[i]
                    
                    episodes_growth = curr_year['episodes'] - prev_year['episodes']
                    episodes_growth_percent = (episodes_growth / prev_year['episodes']) * 100 if prev_year['episodes'] > 0 else 0
                    
                    recap['trend_analysis']['episodes_growth'].append({
                        'from': prev_year['year'],
                        'to': curr_year['year'],
                        'growth': episodes_growth,
                        'growth_percent': round(episodes_growth_percent, 1),
                        'direction': 'up' if episodes_growth > 0 else 'down' if episodes_growth < 0 else 'stable'
                    })
                
                # Находим лучший год
                best_year = max(yearly_stats_array, key=lambda x: x['episodes'])
                recap['trend_analysis']['best_year'] = {
                    'year': best_year['year'],
                    'episodes': best_year['episodes'],
                    'duration': best_year['duration_readable']
                }
                
                # Находим самый продуктивный месяц в году
                if monthly_trends_array:
                    recap['trend_analysis']['most_productive_month'] = max(
                        monthly_trends_array,
                        key=lambda x: x['episodes']
                    )
                    
        except Exception as e:
            logger.error(f"Ошибка при анализе трендов: {str(e)}")
            recap['trend_analysis'] = {'error': str(e)}
        
        # 8. Сводка
        start_year = all_years[0] if all_years else 'Н/Д'
        end_year = all_years[-1] if all_years else 'Н/Д'
        
        recap['summary'] = {
            'period': f'{start_year}-{end_year}',
            'total_sessions': recap['total_sessions'],
            'total_episodes': recap['total_episodes'],
            'total_duration': recap['total_duration_readable'],
            'total_duration_days': recap['total_duration_days'],
            'total_games': len(recap['games']),
            'total_years': len(yearly_stats_array),
            'average_episodes_per_year': round(recap['total_episodes'] / len(yearly_stats_array)) if yearly_stats_array else 0,
            'most_productive_year': recap['trend_analysis'].get('best_year', {}).get('year', 'Н/Д') if recap.get('trend_analysis') else 'Н/Д',
            'most_played_game': recap['game_rankings']['by_episodes'][0]['game'] if recap['game_rankings'].get('by_episodes') else 'Н/Д',
            'processing_status': 'Успешно'
        }
        
    except Exception as e:
        logger.error(f"Критическая ошибка при расчете статистики за все время: {str(e)}")
        recap['summary'] = {
            'period': 'all_time',
            'error': 'Ошибка при расчете статистики',
            'error_details': str(e),
            'processing_status': 'С ошибками'
        }
    
    # Завершаем обработку
    recap['processing_info']['end_time'] = datetime.now().isoformat()
    recap['processing_info']['duration_seconds'] = (
        datetime.fromisoformat(recap['processing_info']['end_time']) - 
        datetime.fromisoformat(recap['processing_info']['start_time'])
    ).total_seconds()
    
    logger.info(f"Отчет за все время готов. Обработка заняла {recap['processing_info']['duration_seconds']:.2f} секунд")
    
    return recap


def _calculate_longest_break(dates: List[datetime]) -> Dict:
    """Рассчитывает самый длинный перерыв между активностями."""
    if not dates or len(dates) < 2:
        return {'days': 0, 'from': None, 'to': None}
    
    try:
        dates_sorted = sorted(dates)
        longest_break = 0
        break_start = None
        break_end = None
        
        for i in range(1, len(dates_sorted)):
            break_days = (dates_sorted[i] - dates_sorted[i-1]).days - 1
            if break_days > longest_break:
                longest_break = break_days
                break_start = dates_sorted[i-1]
                break_end = dates_sorted[i]
        
        return {
            'days': longest_break,
            'from': break_start.strftime('%Y-%m-%d') if break_start else None,
            'to': break_end.strftime('%Y-%m-%d') if break_end else None,
            'readable': f"{longest_break} дней" if longest_break > 0 else "Нет перерывов"
        }
    except Exception as e:
        logger.error(f"Ошибка при расчете перерыва: {str(e)}")
        return {'days': 0, 'from': None, 'to': None, 'error': str(e)}


# Функции для вывода рекапов в красивом формате
def print_year_recap(recap):
    """
    Красивый вывод статистики за год
    """
    year = recap['target_year']
    
    print("═" * 70)
    print(f"📊 ИГРОВОЙ ГОДОВОЙ ОТЧЕТ: 20{year}".center(70))
    print("═" * 70)
    
    print("\n📈 ОБЩАЯ СТАТИСТИКА ЗА ГОД")
    print("-" * 50)
    
    summary = recap['summary']
    print(f"🎮 Сыграно игр: {summary['games_played']}")
    print(f"🎥 Всего серий: {summary['total_episodes']}")
    print(f"⏱️ Общее время: {summary['total_duration']}")
    print(f"🕹️ Игровых сессий: {summary['total_sessions']}")
    print(f"📅 Активных месяцев: {summary['active_months']}")
    print(f"🔥 Самый активный месяц: {summary['most_active_month']}")
    
    print("\n🏆 ТОП-5 ИГР ГОДА")
    print("-" * 50)
    
    for i, game in enumerate(recap['game_rankings']['by_episodes'][:5], 1):
        medal = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"][i-1]
        game_name = game['game']
        if len(game_name) > 25:
            game_name = game_name[:22] + "..."
        
        episodes = game['episodes']
        percent = game['percentage']
        print(f"{medal} {game_name:<25} {episodes:>3} серий ({percent:>4.1f}%)")
    
    print("\n📊 АКТИВНОСТЬ ПО МЕСЯЦАМ")
    print("-" * 50)
    
    months = recap['monthly_stats']
    for month in months:
        if month['episodes'] > 0:
            episodes_str = f"{month['episodes']} серий"
            duration_str = month['duration_readable']
            percent = month['percentage_of_year_episodes']
            print(f"📅 {month['month_name']:<3} → {episodes_str:<12} {duration_str:>10} ({percent:>4.1f}%)")
    
    print("\n🌦️  СЕЗОННАЯ СТАТИСТИКА")
    print("-" * 50)
    
    seasons = recap['seasonal_stats']
    for season in seasons:
        if season['episodes'] > 0:
            episodes = season['episodes']
            duration = season['duration_readable']
            games = season['games_count']
            print(f"❄️ {season['name']:<5} → {episodes:>3} серий, {duration:>10}, {games:>2} игр")
    
    print("\n🎬 РЕКОРДЫ ГОДА")
    print("-" * 50)
    
    # Самый продуктивный месяц
    best_month = recap['top_months']['by_episodes'][0]
    print(f"📈 Лучший месяц: {best_month['month_name']}")
    print(f"   → {best_month['episodes']} серий ({best_month['duration_readable']})")
    
    # Самая длинная серия
    if 'episode_analysis' in recap:
        longest_ep = recap['episode_analysis']['longest_episodes'][0]
        print(f"⏱️  Самая длинная серия: {longest_ep['duration_readable']}")
        print(f"   → {longest_ep['game']}: {longest_ep['title']}")
    
    print("\n📅 КВАРТАЛЬНАЯ СТАТИСТИКА")
    print("-" * 50)
    
    quarters = recap['quarterly_stats']
    for q in quarters:
        if q['episodes'] > 0:
            print(f"📊 {q['name']:<3} → {q['episodes']:>3} серий, {q['duration_readable']:>10}, {q['games_count']:>2} игр")
    
    print("\n✨ ГОД В ЦИФРАХ")
    print("-" * 50)
    
    stats = [
        f"📏 Сред. длина серии: {recap['average_duration_per_episode_readable']}",
        f"📈 Сред. серий в месяц: {round(recap['total_episodes'] / recap['active_months'], 1)}",
        f"🎯 Игр в лучшем месяце: {best_month['games_count']}",
        f"⚡ Всего времени в часах: {recap['total_duration_hours']:.1f}ч"
    ]
    
    for i in range(0, len(stats), 2):
        if i + 1 < len(stats):
            print(f"{stats[i]:<35} {stats[i+1]}")
        else:
            print(stats[i])
    
    print("\n" + "═" * 70)
    print(f"🎉 Отличный год! Увидимся в следующем!".center(70))
    print("═" * 70)


def print_all_time_recap(recap):
    """
    Красивый вывод статистики за все время
    """
    print("═" * 80)
    print(f"🏆 ИГРОВАЯ ИСТОРИЯ: ВСЁ ВРЕМЯ 🏆".center(80))
    print("═" * 80)
    
    print("\n📊 ВСЕОБЩАЯ СТАТИСТИКА")
    print("-" * 60)
    
    summary = recap['summary']
    print(f"📅 Период: {summary['period']}")
    print(f"🎮 Всего игр: {summary['total_games']}")
    print(f"🎥 Всего серий: {summary['total_episodes']:,}".replace(',', ' '))
    print(f"⏱️ Общее время: {summary['total_duration']} ({summary['total_duration_days']:.1f} дней!)")
    print(f"🕹️ Всего сессий: {summary['total_sessions']:,}".replace(',', ' '))
    print(f"📈 Среднее в год: {summary['average_episodes_per_year']} серий")
    print(f"🏆 Лучший год: {summary['most_productive_year']}")
    
    print("\n🥇 ЛЕГЕНДАРНЫЕ ИГРЫ (ТОП-5 ВСЕГО ВРЕМЕНИ)")
    print("-" * 60)
    
    for i, game in enumerate(recap['game_rankings']['by_episodes'][:5], 1):
        medal = ["🏆", "🥈", "🥉", "4️⃣", "5️⃣"][i-1]
        game_name = game['game']
        if len(game_name) > 30:
            game_name = game_name[:27] + "..."
        
        episodes = game['episodes']
        years = game['years_active']
        percent = game['percentage']
        print(f"{medal} {game_name:<30} {episodes:>5} серий, {years} лет ({percent:>4.1f}%)")
    
    print("\n📊 ИСТОРИЯ ПО ГОДАМ")
    print("-" * 60)
    
    years = recap['yearly_stats']
    for year in years[-8:]:  # Показываем последние 8 лет
        if year['episodes'] > 0:
            episodes = year['episodes']
            games = year['games_count']
            percent = year['percentage_of_total_episodes']
            bar = "█" * int(percent / 2)  # Визуализация процента
            print(f"📅 20{year['year_short']:<3} → {episodes:>4} серий, {games:>2} игр {bar:<50}")
    
    print("\n🌟 ВЕХИ И РЕКОРДЫ")
    print("-" * 60)
    
    milestones = recap['milestones']
    records = recap['records']
    
    if records.get('longest_episode'):
        longest = records['longest_episode']
        print(f"⏱️  Абсолютный рекорд длины: {longest['duration_readable']}")
        print(f"   → {longest['game']}: {longest['title'][:40]}{'...' if len(longest['title']) > 40 else ''}")
    
    if records.get('best_month'):
        best_month = records['best_month']
        print(f"📈 Лучший месяц в истории: {best_month['month_name']} {best_month['year']}")
        print(f"   → {best_month['episodes']} серий за месяц!")
    
    print(f"📅 Самая длинная серия дней подряд: {records.get('longest_streak', 0)} дней")
    
    if milestones.get('decades'):
        print(f"\n📊 СТАТИСТИКА ПО ДЕСЯТИЛЕТИЯМ")
        print("-" * 60)
        
        for decade, data in milestones['decades'].items():
            if data['episodes'] > 0:
                avg = data['average_episodes_per_year']
                duration = data['duration_readable']
                print(f"🕰️  {decade:<7} → {data['episodes']:>5} серий ({avg:>3}/год, {duration:>10})")
    
    print("\n📈 ТРЕНДЫ И АНАЛИЗ")
    print("-" * 60)
    
    if 'trend_analysis' in recap:
        trends = recap['trend_analysis']
        
        if trends.get('best_year'):
            best = trends['best_year']
            print(f"📊 Пиковый год: {best['year']}")
            print(f"   → {best['episodes']} серий ({best['duration']})")
        
        if trends.get('most_productive_month'):
            month = trends['most_productive_month']
            print(f"📅 Рекордный месяц: {month['month_name']} {month['year']}")
            print(f"   → {month['episodes']} серий, {month['games_count']} игр")
        
        # Показываем динамику последних лет
        if trends.get('episodes_growth'):
            recent_growth = trends['episodes_growth'][-3:]  # Последние 3 года
            for growth in recent_growth:
                arrow = "↗️" if growth['direction'] == 'up' else "↘️" if growth['direction'] == 'down' else "➡️"
                sign = "+" if growth['growth'] > 0 else ""
                print(f"   {arrow} {growth['from']}-{growth['to']}: {sign}{growth['growth']} серий ({sign}{growth['growth_percent']:.1f}%)")
    
    print("\n🎯 БЫСТРЫЕ ФАКТЫ")
    print("-" * 60)
    
    facts = [
        f"📏 Средняя длина серии: {recap['average_duration_per_episode_readable']}",
        f"📊 Всего месяцев активности: {len(recap['monthly_trends'])}",
        f"🎮 Уникальных игр: {len(recap['games'])}",
        f"⏱️  Время в играх: {milestones.get('total_duration_hours', 0):.0f} часов"
    ]
    
    # Самые старые и новые игры
    if recap['game_rankings'].get('by_longevity'):
        oldest = recap['game_rankings']['by_longevity'][0]
        print(f"🏛️  Самая долгая история: {oldest['game']} ({oldest['years_active']} лет, с {oldest['first_year']})")
    
    print("\n" + "═" * 80)
    print(f"🎮 БОЛЬШОЕ СПАСИБО ЗА ВСЕ ЭТИ ГОДЫ ИГР! 🎮".center(80))
    print("═" * 80)


# Компактные версии выводов
def print_year_recap_compact(recap):
    """Компактная версия годового отчета"""
    year = recap['target_year']
    
    print("╔" + "═" * 68 + "╗")
    print(f"║{'📊 20' + year + ' ГОД В ЦИФРАХ 📊'.center(68)}║")
    print("╠" + "═" * 68 + "╣")
    
    # Первая строка
    s = recap['summary']
    print(f"║ {'🎥 Серий:':<10} {s['total_episodes']:<6}", end="")
    print(f"{'⏱️ Время:':<10} {s['total_duration']:<15}", end="")
    print(f"{'🎮 Игр:':<8} {s['games_played']:<3} ║")
    
    # Вторая строка
    print(f"║ {'📅 Активных мес:':<14} {s['active_months']:<3}", end="")
    best_month = recap['top_months']['by_episodes'][0]['month_name'] if recap['top_months']['by_episodes'] else 'Н/Д'
    print(f"{'🔥 Лучший:':<10} {best_month:<10}", end="")
    avg_month = round(s['total_episodes'] / s['active_months'], 1) if s['active_months'] > 0 else 0
    print(f"{'📈 Сред/мес:':<12} {avg_month:<4} ║")
    
    # Топ-3 игры
    print("╠" + "─" * 68 + "╣")
    print(f"║ {'🏆 ТОП-3 ИГРЫ ГОДА:'.center(68)}║")
    print("╠" + "─" * 68 + "╣")
    
    for i, game in enumerate(recap['game_rankings']['by_episodes'][:3], 1):
        medal = ["🥇", "🥈", "🥉"][i-1]
        game_name = game['game']
        if len(game_name) > 25:
            game_name = game_name[:22] + "..."
        episodes = game['episodes']
        percent = game['percentage']
        line = f"{medal} {game_name:<28} {episodes:>3} серий ({percent:>4.1f}%)"
        print(f"║ {line:<66} ║")
    
    print("╚" + "═" * 68 + "╝")


def print_all_time_recap_compact(recap):
    """Компактная версия отчета за все время"""
    print("╔" + "═" * 78 + "╗")
    print(f"║{'🌟 ИГРОВАЯ ИСТОРИЯ • ВСЁ ВРЕМЯ 🌟'.center(78)}║")
    print("╠" + "═" * 78 + "╣")
    
    s = recap['summary']
    
    # Основные метрики
    print(f"║ {'📅 Период:':<12} {s['period']:<15}", end="")
    print(f"{'🎮 Игр:':<8} {s['total_games']:<4}", end="")
    print(f"{'🎥 Серий:':<10} {s['total_episodes']:<6} ║")
    
    print(f"║ {'⏱️  Общее время:':<16} {s['total_duration']:<20}", end="")
    print(f"{'🕹️ Сессий:':<10} {s['total_sessions']:<6}", end="")
    print(f"{'📈 Ср/год:':<10} {s['average_episodes_per_year']:<4} ║")
    
    # Лучшая игра
    if recap['game_rankings'].get('by_episodes'):
        best_game = recap['game_rankings']['by_episodes'][0]
        print(f"║ {'🏆 Лучшая игра:':<14} {best_game['game'][:30]:<30}", end="")
        print(f"{best_game['episodes']:>5} серий ({best_game['percentage']:.1f}%){' ' * 5} ║")
    
    print("╚" + "═" * 78 + "╝")


# ASCII инфографика
def print_year_recap_ascii(recap):
    """ASCII инфографика для годового отчета"""
    year = recap['target_year']
    
    print("\n" + "▄" * 60)
    print("█" + f" 20{year} • ГОДОВОЙ ОТЧЕТ ".center(58) + "█")
    print("▀" * 60)
    
    # Топ игр по эпизодам (график)
    print("\n📊 Топ игр по сериям:")
    print("-" * 50)
    
    games = recap['game_rankings']['by_episodes'][:6]
    if games:
        max_episodes = max(g['episodes'] for g in games)
        
        for game in games:
            episodes = game['episodes']
            percent = game['percentage']
            bar_length = int((episodes / max_episodes) * 35)
            bar = "█" * bar_length
            
            # Сокращаем название
            name = game['game']
            if len(name) > 20:
                name = name[:17] + "..."
            
            print(f"{name:<20} {bar:35} {episodes:>4} ({percent:4.1f}%)")
    
    # Месячная активность
    print("\n📅 Активность по месяцам:")
    print("-" * 50)
    
    months = recap['monthly_stats']
    for month in months:
        if month['episodes'] > 0:
            episodes = month['episodes']
            bar = "▓" * min(episodes // 5, 30)  # Один блок = 5 серий
            print(f"{month['month_name']:<3} {bar:30} {episodes:>3} серий")
    
    # Статистика в две колонки
    print("\n" + "─" * 50)
    stats = [
        f"📈 Всего серий: {recap['summary']['total_episodes']}",
        f"⏱️ Общее время: {recap['summary']['total_duration']}",
        f"🎮 Сыграно игр: {recap['summary']['games_played']}",
        f"📅 Активных месяцев: {recap['summary']['active_months']}",
        f"🔥 Лучший месяц: {recap['summary']['most_active_month']}",
        f"📏 Сред. длина: {recap['average_duration_per_episode_readable']}"
    ]
    
    for i in range(0, len(stats), 2):
        if i + 1 < len(stats):
            print(f"{stats[i]:<30} {stats[i+1]}")
        else:
            print(stats[i])
    
    print("─" * 50)
    print(f"🎮 Отличный год!".center(50))
    print("▄" * 60)


def print_all_time_recap_ascii(recap):
    """ASCII инфографика для отчета за все время"""
    print("\n" + "▄" * 70)
    print("█" + " ИГРОВАЯ ИСТОРИЯ • ВСЁ ВРЕМЯ ".center(68) + "█")
    print("▀" * 70)
    
    # Топ игр за все время
    print("\n🏆 Легендарные игры (топ по сериям):")
    print("-" * 60)
    
    games = recap['game_rankings']['by_episodes'][:8]
    if games:
        max_episodes = max(g['episodes'] for g in games)
        
        for i, game in enumerate(games, 1):
            episodes = game['episodes']
            years = game.get('years_active', 1)
            bar_length = int((episodes / max_episodes) * 40)
            bar = "█" * bar_length
            
            # Сокращаем название
            name = game['game']
            if len(name) > 25:
                name = name[:22] + "..."
            
            rank = f"{i}.".rjust(3)
            print(f"{rank} {name:<25} {bar:40} {episodes:>5} серий")
    
    # Годовая активность
    print("\n📊 Активность по годам:")
    print("-" * 60)
    
    years = recap['yearly_stats'][-10:]  # Последние 10 лет
    if years:
        max_episodes = max(y['episodes'] for y in years)
        
        for year in years:
            if year['episodes'] > 0:
                episodes = year['episodes']
                bar = "▓" * int((episodes / max_episodes) * 30)
                print(f"20{year['year_short']:<4} {bar:30} {episodes:>4} серий")
    
    # Рекорды
    print("\n🌟 Абсолютные рекорды:")
    print("-" * 60)
    
    records = recap['records']
    if records.get('longest_episode'):
        longest = records['longest_episode']
        print(f"⏱️  Самая длинная серия: {longest['duration_readable']}")
        print(f"   → {longest['game']}")
    
    if records.get('best_month'):
        best = records['best_month']
        print(f"📈 Лучший месяц: {best['month_name']} {best['year']}")
        print(f"   → {best['episodes']} серий!")
    
    print(f"📅 Самая длинная серия дней: {records.get('longest_streak', 0)} дней")
    
    # Быстрые факты
    print("\n📈 Ключевые показатели:")
    print("-" * 60)
    
    facts = [
        f"🎯 Всего уникальных игр: {recap['summary']['total_games']}",
        f"📊 Всего серий: {recap['summary']['total_episodes']:,}".replace(',', ' '),
        f"⏱️  Общее время: {recap['summary']['total_duration_days']:.1f} дней",
        f"📅 Лет активности: {recap['summary']['total_years']}",
        f"📏 Средняя длина: {recap['average_duration_per_episode_readable']}"
    ]
    
    for fact in facts:
        print(f"   {fact}")
    
    print("\n" + "─" * 60)
    print("🎮 Спасибо за все эти годы игр!".center(60))
    print("▄" * 70)


# Тестирование функций
def test_recap_functions():
    """Тестирование всех функций рекапов"""
    print("=" * 80)
    print("ТЕСТИРОВАНИЕ ФУНКЦИЙ РЕКАПОВ".center(80))
    print("=" * 80)
    
    # Создаем тестовые данные
    test_sessions = {
        "session_2023_01": {
            "game": "The Legend of Zelda",
            "datetime": 1672531200,  # 2023-01-01
            "episodes": [
                {
                    "number": 1,
                    "title": "Начало приключения",
                    "duration": 4200,
                    "publishedAt": "2023-01-01T12:00:00Z"
                }
            ]
        },
        "session_2024_06": {
            "game": "Elden Ring",
            "datetime": 1717200000,  # 2024-06-01
            "episodes": [
                {
                    "number": 1,
                    "title": "Lands Between",
                    "duration": 5600,
                    "publishedAt": "2024-06-01T14:30:00Z"
                },
                {
                    "number": 2,
                    "title": "Stormveil Castle",
                    "duration": 7200,
                    "publishedAt": "2024-06-02T15:45:00Z"
                }
            ]
        },
        "session_2025_12": {
            "game": "Assassin’s Creed: Brotherhood",
            "datetime": 1765300093,  # 2025-12-11
            "episodes": [
                {
                    "number": 16,
                    "title": "Ад на колесах",
                    "duration": 3648,
                    "publishedAt": "2025-12-11T15:39:00Z"
                }
            ]
        }
    }
    
    # Тестируем месячный рекап
    print("\n1. ТЕСТ МЕСЯЧНОГО РЕКАПА:")
    print("-" * 40)
    month_recap = make_month_recap("25-12", test_sessions)
    print(f"Статус: {month_recap['summary'].get('processing_status', 'Н/Д')}")
    print(f"Сессий: {month_recap['total_sessions']}")
    print(f"Эпизодов: {month_recap['total_episodes']}")
    
    # Тестируем годовой рекап
    print("\n2. ТЕСТ ГОДОВОГО РЕКАПА:")
    print("-" * 40)
    year_recap = make_year_recap("25", test_sessions)
    print(f"Статус: {year_recap['summary'].get('processing_status', 'Н/Д')}")
    print(f"Сессий: {year_recap['total_sessions']}")
    print(f"Эпизодов: {year_recap['total_episodes']}")
    print(f"Игр: {len(year_recap['games'])}")
    
    # Тестируем рекап за все время
    print("\n3. ТЕСТ РЕКАПА ЗА ВСЕ ВРЕМЯ:")
    print("-" * 40)
    all_time_recap = make_all_time_recap(test_sessions)
    print(f"Статус: {all_time_recap['summary'].get('processing_status', 'Н/Д')}")
    print(f"Сессий: {all_time_recap['total_sessions']}")
    print(f"Эпизодов: {all_time_recap['total_episodes']}")
    print(f"Лет активности: {len(all_time_recap['yearly_stats'])}")
    
    # Демонстрация выводов
    print("\n4. ДЕМОНСТРАЦИЯ ВЫВОДОВ:")
    print("-" * 40)
    
    print("Годовой отчет (компактный):")
    print_year_recap_compact(year_recap)
    
    print("\nОтчет за все время (компактный):")
    print_all_time_recap_compact(all_time_recap)
    
    print("\n" + "=" * 80)
    print("ТЕСТИРОВАНИЕ ЗАВЕРШЕНО УСПЕШНО".center(80))
    print("=" * 80)
    
    return {
        'month': month_recap,
        'year': year_recap,
        'all_time': all_time_recap
    }


if __name__ == "__main__":
    # Запуск тестирования
    results = test_recap_functions()
    
    # Показать полные отчеты
    print("\n" + "=" * 80)
    print("ПОЛНЫЕ ОТЧЕТЫ ДЛЯ ОБЗОРА".center(80))
    print("=" * 80)
    
    # print("\n1. МЕСЯЧНЫЙ ОТЧЕТ (ASCII):")
    # print_month_recap_ascii(results['month'])
    
    print("\n2. ГОДОВОЙ ОТЧЕТ (ASCII):")
    print_year_recap_ascii(results['year'])
    
    print("\n3. ОТЧЕТ ЗА ВСЁ ВРЕМЯ (ASCII):")
    print_all_time_recap_ascii(results['all_time'])