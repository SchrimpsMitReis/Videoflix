import subprocess
import sys
from pathlib import Path


PROJECT_DIR = Path(
    r"C:\Users\TheSu\OneDrive\Dokumente\Coding\Developer Akademie\Backend 11 - Backend für Businessapps\Videoflix")
WEB_SERVICE = "web"
QUEUE_NAME = "default"


def run_command(command: list[str], check: bool = True) -> subprocess.CompletedProcess:
    print(f"\n>> {' '.join(command)}")
    return subprocess.run(
        command,
        cwd=PROJECT_DIR,
        text=True,
        capture_output=True,
        check=check,
    )


def kill_rqworker() -> None:
    try:
        result = run_command(
            ["docker", "compose", "exec", WEB_SERVICE, "pkill", "-f", "rqworker"],
            check=False,
        )
        if result.returncode == 0:
            print("RQ-Worker beendet.")
        else:
            print("Kein laufender RQ-Worker gefunden oder bereits beendet.")
            if result.stderr.strip():
                print("stderr:", result.stderr.strip())
    except Exception as exc:
        print(f"Fehler beim Killen des Workers: {exc}")


def clear_queue_and_failed_jobs() -> None:
    python_code = f"""
    import django_rq
    
    queue = django_rq.get_queue("{QUEUE_NAME}")
    queue.empty()
    
    failed = queue.failed_job_registry
    for job_id in failed.get_job_ids():
        failed.remove(job_id, delete_job=True)
    
    print("Queue geleert.")
    print("Failed Jobs gelöscht.")
    """

    result = run_command(
        ["docker", "compose", "exec", WEB_SERVICE, "python",
            "manage.py", "shell", "-c", python_code]
    )
    print(result.stdout.strip())
    if result.stderr.strip():
        print("stderr:", result.stderr.strip())


def start_rqworker() -> None:
    # Startet den Worker im Hintergrund im Container
    command = (
        f"nohup python manage.py rqworker {QUEUE_NAME} "
        f"> /tmp/rqworker.log 2>&1 &"
    )

    result = run_command(
        ["docker", "compose", "exec", WEB_SERVICE, "sh", "-c", command]
    )
    print("RQ-Worker neu gestartet.")
    if result.stdout.strip():
        print(result.stdout.strip())
    if result.stderr.strip():
        print("stderr:", result.stderr.strip())


def show_worker_processes() -> None:
    result = run_command(
        ["docker", "compose", "exec", WEB_SERVICE,
            "sh", "-c", "ps aux | grep rqworker"],
        check=False,
    )
    print("\nAktuelle rqworker-Prozesse:")
    print(result.stdout.strip() or "(nichts gefunden)")
    if result.stderr.strip():
        print("stderr:", result.stderr.strip())


def main() -> int:
    try:
        kill_rqworker()
        clear_queue_and_failed_jobs()
        start_rqworker()
        show_worker_processes()
        print("\nFertig.")
        return 0
    except subprocess.CalledProcessError as exc:
        print("\nEin Befehl ist fehlgeschlagen.")
        print("Returncode:", exc.returncode)
        if exc.stdout:
            print("stdout:\n", exc.stdout)
        if exc.stderr:
            print("stderr:\n", exc.stderr)
        return 1
    except Exception as exc:
        print(f"\nUnerwarteter Fehler: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
