from multiprocessing import cpu_count

MAX_THREADS = max(1, min(cpu_count() - 1, 4))

LANG = {
    'Auto-detect': 'auto',
    'English': 'en',
    'Korean': 'ko',
    'Indonesia': 'id',
    'Vietnamese': 'vi',
    'Chinese': 'zh',
    'Japanese': 'ja',
    'French': 'fr',
}

INSTRUCTION = """1. Press "Shift + X" to take a screenshot
2. Draw a rectangle by dragging mouse
3. Press "Space" to translate, "Esc" to cancel
"""

ZOOM_FACTOR = 1.2
