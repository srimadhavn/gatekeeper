# Tokyo Night inspired palette + a few presets

THEMES = {
    "tokyo": {
        "bg": "#1a1b26", "fg": "#a9b1d6", "accent": "#7dcfff",
        "success": "#9ece6a", "warning": "#e0af68", "error": "#f7768e",
        "header": "#bb9af7", "border": "#565f89"
    },
    "matrix": {
        "bg": "#000000", "fg": "#00ff9c", "accent": "#00ffaa",
        "success": "#00ff66", "warning": "#ccff00", "error": "#ff4d4d",
        "header": "#00ffd5", "border": "#007755"
    },
    "light": {
        "bg": "#f8f8f8", "fg": "#1f2335", "accent": "#0066ff",
        "success": "#2ea043", "warning": "#b08800", "error": "#d73a49",
        "header": "#4c2889", "border": "#aeb0b4"
    }
}

class Theme:
    _current = THEMES["tokyo"]

    @classmethod
    def set(cls, name: str):
        cls._current = THEMES.get(name, THEMES["tokyo"])

    @classmethod
    def C(cls, key: str) -> str:
        return f"[{cls._current[key]}]"
