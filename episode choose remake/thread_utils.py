import functools
import threading
import console_setup

_threads_lock = threading.Lock()
_active_threads = 0
_base_title = "Episode Chooser"


def _update_title():
    with _threads_lock:
        n = _active_threads
    console_setup.set_title(f"{_base_title} ⏳" if n > 0 else _base_title)


def in_thread(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        global _active_threads
        with _threads_lock:
            _active_threads += 1
        _update_title()

        def runner():
            global _active_threads
            try:
                func(*args, **kwargs)
            finally:
                with _threads_lock:
                    _active_threads -= 1
                _update_title()

        threading.Thread(target=runner, daemon=False).start()

    return wrapper