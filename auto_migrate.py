
from pathlib import Path
import logging
import argparse
import sys

from flask_migrate import (
    Migrate,
    init as init_cmd,
    migrate as migrate_cmd,
    upgrade as upgrade_cmd,
)

from app import create_app
from app.extensions import db


logging.basicConfig(level=logging.INFO, format="[auto_migrate] %(message)s")
logger = logging.getLogger("auto_migrate")


def _list_versions(migrations_dir: Path) -> set:
    versions_dir = migrations_dir / "versions"
    if not versions_dir.exists() or not versions_dir.is_dir():
        return set()
    return {p.name for p in versions_dir.iterdir() if p.is_file()}


def _safe_run(cmd_fn, *args, **kwargs) -> bool:
    try:
        cmd_fn(*args, **kwargs)
        return True
    except Exception:
        logger.exception("Comando de migración falló:")
        return False


def run_auto_migration(message: str = "auto migration", dry_run: bool = False) -> int:
    """
    Genera y aplica migraciones de forma segura.

    Comportamiento:
    - Si no existe `migrations/`: init -> migrate -> upgrade
    - Si existe:
        1) upgrade (poner la DB al día)
        2) migrate (generar nueva migración si hay cambios)
        3) upgrade (solo si se generó una nueva migración)
    """
    app = create_app()

    with app.app_context():
        Migrate(app, db)
        migrations_dir = Path("migrations")

        # Caso inicial: no existe carpeta migrations
        if not migrations_dir.exists() or not migrations_dir.is_dir():
            logger.info("`migrations/` no existe, inicializando...")
            if dry_run:
                logger.info("dry-run: saltando init, migrate y upgrade.")
                return 0
            if not _safe_run(init_cmd):
                return 1
            if not _safe_run(migrate_cmd, message=message):
                return 1
            if not _safe_run(upgrade_cmd):
                return 1
            logger.info("Migración inicial generada y aplicada.")
            return 0

        # Caso existente: asegurar que la DB está al día
        logger.info("Aplicando migraciones pendientes (si las hay)...")
        if not _safe_run(upgrade_cmd):
            return 1

        # Generar nueva migración y detectar si se creó un archivo nuevo
        before = _list_versions(migrations_dir)
        logger.info("Generando nueva migración (si hay cambios en modelos)...")
        if dry_run:
            logger.info("dry-run: saltando migrate y posible upgrade.")
            return 0
        if not _safe_run(migrate_cmd, message=message):
            return 1
        after = _list_versions(migrations_dir)

        new_files = sorted(list(after - before))
        if not new_files:
            logger.info("No se generó ninguna nueva migración. Nada que aplicar.")
            return 0

        logger.info("Nueva(s) migración(es) generada(s): %s", ", ".join(new_files))
        logger.info("Aplicando nueva(s) migración(es)...")
        if not _safe_run(upgrade_cmd):
            return 1

        logger.info("Proceso de migración automático finalizado.")
        return 0


def _parse_args(argv):
    p = argparse.ArgumentParser(description="Auto migrator para Flask-Migrate")
    p.add_argument("-m", "--message", default="auto migration", help="Mensaje de la migración")
    p.add_argument("--dry-run", action="store_true", help="No ejecutar comandos que modifiquen la DB o archivos")
    return p.parse_args(argv)


if __name__ == "__main__":
    args = _parse_args(sys.argv[1:])
    sys.exit(run_auto_migration(message=args.message, dry_run=args.dry_run))
