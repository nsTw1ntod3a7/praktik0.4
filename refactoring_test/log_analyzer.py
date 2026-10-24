"""
Модуль анализа серверных логов и выявления дубликатов запросов.
Оптимизировано с O(N^2) до O(N) при помощи set и Counter.
"""

from collections import Counter

BAD_STATUSES = frozenset({401, 403})


def find_duplicate_requests(logs):
    """Возвращает request_id, которые встречаются в логах более одного раза.

    Порядок результата: в порядке обнаружения первого повтора.
    """
    duplicates = []
    seen = set()
    already_reported = set()

    for log in logs:
        req_id = log['request_id']
        if req_id in seen:                      # поиск в set: O(1)
            if req_id not in already_reported:
                already_reported.add(req_id)
                duplicates.append(req_id)
        else:
            seen.add(req_id)

    return duplicates


def find_top_offenders(logs, threshold=3):
    """IP-адреса с числом ответов 401/403 >= threshold (в порядке первого появления)."""
    # один проход: считаем ошибки по каждому IP
    bad_counts = Counter(
        log.get('ip') for log in logs if log.get('status') in BAD_STATUSES
    )

    # второй проход: сохраняем порядок появления IP в логах
    bad_ips = []
    added = set()
    for log in logs:
        if log.get('status') in BAD_STATUSES:
            ip = log.get('ip')
            if bad_counts[ip] >= threshold and ip not in added:
                added.add(ip)
                bad_ips.append(ip)

    return bad_ips
