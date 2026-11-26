from config import global_config
from telegram.filters import is_admin

__all__ = ["is_admin", "is_sudo"]


def is_sudo(user_id: int) -> bool:
    admin_id = global_config["admin_id"]
    return bool(admin_id) and admin_id == user_id
