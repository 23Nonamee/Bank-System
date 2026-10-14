import sqlite3
import os
from typing import Optional

DB_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "banco.db")

def get_connection(db_path: Optional[str] = None) -> sqlite3.Connection:
    """
    Obtiene una conexión a la base de datos SQLite con claves foráneas activadas.
    """
    path = db_path if db_path else DB_FILE
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn


def inicializar_base_datos(db_path: Optional[str] = None) -> None:
    """
    Crea las tablas necesarias en la base de datos SQLite si no existen.
    Garantiza que el sistema corra de inmediato en un computador nuevo.
    """
    conn = get_connection(db_path)
    cursor = conn.cursor()

    # 1. Tabla Clientes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            rut TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            direccion TEXT NOT NULL,
            is_mora INTEGER NOT NULL DEFAULT 0,
            amount_mora INTEGER NOT NULL DEFAULT 0
        );
    """)

    # 2. Tabla Cuentas Bancarias
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cuentas (
            numero_cuenta TEXT PRIMARY KEY,
            rut_titular TEXT NOT NULL,
            tipo TEXT NOT NULL,
            saldo REAL NOT NULL DEFAULT 0.0,
            cupo_sobregiro REAL NOT NULL DEFAULT 0.0,
            tasa_interes REAL NOT NULL DEFAULT 0.0,
            FOREIGN KEY (rut_titular) REFERENCES clientes (rut) ON DELETE CASCADE
        );
    """)

    # 3. Tabla Transacciones (Cabecera)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transacciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_cuenta TEXT NOT NULL,
            fecha TEXT NOT NULL,
            FOREIGN KEY (numero_cuenta) REFERENCES cuentas (numero_cuenta) ON DELETE CASCADE
        );
    """)

    # 4. Tabla Movimientos (Líneas de detalle de la Transacción)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movimientos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaccion_id INTEGER NOT NULL,
            tipo TEXT NOT NULL,
            monto REAL NOT NULL,
            descripcion TEXT NOT NULL,
            cuenta_origen TEXT,
            cuenta_destino TEXT,
            FOREIGN KEY (transaccion_id) REFERENCES transacciones (id) ON DELETE CASCADE
        );
    """)

    conn.commit()
    conn.close()
