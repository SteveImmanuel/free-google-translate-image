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
