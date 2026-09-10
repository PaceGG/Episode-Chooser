import functools
import json
import threading
from pathlib import Path
import requests
import paths
from thread_utils import in_thread

FAILED_TASKS_FILE = paths.root_dir / "failed_telegram_tasks.json"
MAX_ID_MAP_SIZE = 100
_file_lock = threading.Lock()


def _read_data() -> dict:
    default_structure = {"tasks": {}, "id_map": {}}
    if not FAILED_TASKS_FILE.exists():
        return default_structure
    try:
        with open(FAILED_TASKS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if "tasks" not in data or "id_map" not in data:
                return default_structure
            return data
    except Exception:
        return default_structure


def _clean_id_map(id_map: dict) -> dict:
    if len(id_map) <= MAX_ID_MAP_SIZE:
        return id_map

    keys_to_keep = list(id_map.keys())[-MAX_ID_MAP_SIZE:]
    return {k: id_map[k] for k in keys_to_keep}


def _write_data(data: dict):
    if "id_map" in data:
        data["id_map"] = _clean_id_map(data["id_map"])

    with open(FAILED_TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def _get_next_temp_id(tasks: dict) -> int:
    existing_ids = [int(k) for k in tasks.keys() if k.startswith("-") and int(k) <= -1000]
    if not existing_ids:
        return -1000
    return min(existing_ids) - 1


def serialize_args(args, kwargs):
    s_args = [str(a) if isinstance(a, Path) else a for a in args]
    s_kwargs = {
        k: (str(v) if isinstance(v, Path) else v) for k, v in kwargs.items()
    }
    return s_args, s_kwargs


def save_failed_send(func_name: str, args: list, kwargs: dict) -> int:
    with _file_lock:
        data = _read_data()
        temp_id = _get_next_temp_id(data["tasks"])

        data["tasks"][str(temp_id)] = {
            "func_name": func_name,
            "args": args,
            "kwargs": kwargs,
        }
        _write_data(data)
        return temp_id


def resolve_message_id(msg_id: int) -> int:
    if msg_id >= 0:
        return msg_id

    with _file_lock:
        data = _read_data()
        real_id = data["id_map"].get(str(msg_id))
        if real_id is not None:
            return int(real_id)

    return msg_id


def telegram_delay(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        func_name = func.__name__

        msg_id = None
        if func_name in ("edit_message", "edit_caption", "delete_message"):
            if "message_id" in kwargs:
                msg_id = kwargs["message_id"]
            elif len(args) >= 2 and func_name in ("edit_message", "edit_caption"):
                msg_id = args[1]
            elif len(args) >= 1 and func_name == "delete_message":
                msg_id = args[0]

        if msg_id is not None and int(msg_id) < 0:
            temp_id = int(msg_id)
            real_id = resolve_message_id(temp_id)

            if real_id > 0:
                if "message_id" in kwargs:
                    kwargs["message_id"] = real_id
                elif len(args) >= 2 and func_name in ("edit_message", "edit_caption"):
                    args = list(args)
                    args[1] = real_id
                elif len(args) >= 1 and func_name == "delete_message":
                    args = list(args)
                    args[0] = real_id
            else:
                with _file_lock:
                    data = _read_data()
                    key = str(temp_id)

                    if func_name == "delete_message":
                        data["tasks"].pop(key, None)
                        _write_data(data)
                        return {"ok": True, "result": True}

                    if key in data["tasks"]:
                        task = data["tasks"][key]
                        new_content = args[0] if args else kwargs.get("new_text") or kwargs.get("new_caption")

                        if task["func_name"] in ("send_message", "edit_message"):
                            if task["args"]:
                                task["args"][0] = new_content
                            else:
                                task["kwargs"]["text"] = new_content
                        elif task["func_name"] in ("send_image", "edit_caption"):
                            if len(task["args"]) > 1:
                                task["args"][1] = new_content
                            else:
                                task["kwargs"]["caption"] = new_content

                        _write_data(data)
                        return {"ok": True, "result": {"message_id": temp_id}}

        s_args, s_kwargs = serialize_args(args, kwargs)
        try:
            return func(*args, **kwargs)
        except (requests.exceptions.Timeout, requests.exceptions.RequestException) as e:
            if func_name in ("send_message", "send_image"):
                temp_id = save_failed_send(func_name, s_args, s_kwargs)
                return temp_id

            if func_name in ("edit_message", "edit_caption"):
                save_failed_send(func_name, s_args, s_kwargs)

            return None

    return wrapper

@in_thread
def retry_failed_tasks(module_namespace=None):
    if module_namespace is None:
        import telegram_utils
        module_namespace = telegram_utils.__dict__

    with _file_lock:
        data = _read_data()

    tasks = data.get("tasks", {})
    if not tasks:
        return

    for temp_id_str, task in list(tasks.items()):
        func_name = task["func_name"]
        args = task["args"]
        kwargs = task["kwargs"]

        func = module_namespace.get(func_name)
        if not func:
            continue

        try:
            real_func = getattr(func, "__wrapped__", func)
            res = real_func(*args, **kwargs)

            with _file_lock:
                current_data = _read_data()
                current_data["tasks"].pop(temp_id_str, None)

                if isinstance(res, int) and res > 0:
                    current_data["id_map"][temp_id_str] = res
                elif isinstance(res, dict) and res.get("result", {}).get("message_id"):
                    real_id = res["result"]["message_id"]
                    current_data["id_map"][temp_id_str] = real_id

                _write_data(current_data)

        except Exception as e:
            ...
retry_failed_tasks()