"""Проверка решения на тестах папки задачи.

Запуск из корня репозитория:
    python3 tools/check.py placement/01_top_words
    python3 tools/check.py placement/04_subarray --tl 3

Ожидает в папке задачи файл solution.py и папку tests/ с парами N.in / N.out.
Решение читает из stdin и пишет в stdout. Сравнение — по словам (лишние пробелы и переводы строк не важны).
"""
import argparse
import subprocess
import sys
import time
from pathlib import Path


def main():
    p = argparse.ArgumentParser()
    p.add_argument("task", help="папка задачи, например placement/01_top_words")
    p.add_argument("--tl", type=float, default=2.0, help="лимит времени на тест, секунд")
    args = p.parse_args()

    task = Path(args.task)
    sol = task / "solution.py"
    tests = sorted((task / "tests").glob("*.in"), key=lambda f: int(f.stem))
    if not sol.exists() or not tests:
        sys.exit(f"Нет {sol} или тестов в {task / 'tests'}")

    passed = 0
    for t in tests:
        expected = t.with_suffix(".out").read_text().split()
        start = time.perf_counter()
        try:
            r = subprocess.run([sys.executable, str(sol)], stdin=t.open(), capture_output=True,
                               text=True, timeout=args.tl)
        except subprocess.TimeoutExpired:
            print(f"тест {t.stem}: TL  (> {args.tl} с)")
            continue
        ms = (time.perf_counter() - start) * 1000
        if r.returncode != 0:
            print(f"тест {t.stem}: RE  {r.stderr.strip().splitlines()[-1] if r.stderr.strip() else ''}")
        elif r.stdout.split() == expected:
            passed += 1
            print(f"тест {t.stem}: OK  {ms:.0f} мс")
        else:
            got = " ".join(r.stdout.split())
            print(f"тест {t.stem}: WA  получено: {got[:80]}{'…' if len(got) > 80 else ''}")
    print(f"\nИтог: {passed}/{len(tests)}")


if __name__ == "__main__":
    main()
