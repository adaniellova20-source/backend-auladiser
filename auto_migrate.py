from pathlib import Path
import logging
import argparse
import sys
from flask_migrate import Migrate, init, migrate, upgrade
from app import create_app
from app.extensions import db

logging.basicConfig(level=logging.INFO, format="[auto_migrate] %(message)s")
logger = logging.getLogger("auto_migrate")


def _list_versions(migrations_dir: Path) -> set:
    versions_dir = migrations_dir / "versions"
    return {p.name for p in versions_dir.iterdir() if p.is_file()} if versions_dir.exists() else set()


def _safe_run(command, *args, **kwargs) -> bool:
    try:
        command(*args, **kwargs)
        return True
    except Exception:
        logger.exception("Error al ejecutar el comando:")
        return False


def run_auto_migration(message: str = "auto migration", dry_run: bool = False) -> int:
    app = create_app()
    with app.app_context():
        Migrate(app, db)
        migrations_dir = Path("migrations")

        if not migrations_dir.exists():
            logger.info("Inicializando `migrations/`...")
            if dry_run:
                logger.info("dry-run: omitiendo init, migrate y upgrade.")
                return 0
            return 1 if not (_safe_run(init) and _safe_run(migrate, message=message) and _safe_run(upgrade)) else 0

        logger.info("Aplicando migraciones pendientes...")
        if not _safe_run(upgrade):
            return 1

        before = _list_versions(migrations_dir)
        logger.info("Generando nueva migración...")
        if dry_run:
            logger.info("dry-run: omitiendo migrate y upgrade.")
            return 0
        if not _safe_run(migrate, message=message):
            return 1

        new_files = sorted(_list_versions(migrations_dir) - before)
        if not new_files:
            logger.info("Sin nuevas migraciones.")
            return 0

        logger.info("Nuevas migraciones: %s", ", ".join(new_files))
        return 1 if not _safe_run(upgrade) else 0


def _parse_args(argv):
    parser = argparse.ArgumentParser(description="Auto migrador para Flask-Migrate")
    parser.add_argument("-m", "--message", default="auto migration", help="Mensaje de la migración")
    parser.add_argument("--dry-run", action="store_true", help="No modificar la DB o archivos")
    return parser.parse_args(argv)


if __name__ == "__main__":
    args = _parse_args(sys.argv[1:])
    sys.exit(run_auto_migration(message=args.message, dry_run=args.dry_run))
