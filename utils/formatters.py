from datetime import timedelta


def format_time(td):
    if not td:
        return "0h 0m"

    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60

    if hours > 0:
        return f"{hours}h {minutes}m"
    else:
        return f"{minutes}m"


def format_duration(seconds):
    return format_time(timedelta(seconds=seconds))


def format_user_mention(user_id):
    return f"<@{user_id}>"


def format_channel_mention(channel_id):
    return f"<#{channel_id}>"


def truncate_text(text, max_length=100):
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."
