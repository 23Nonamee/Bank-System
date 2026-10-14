from datetime import datetime
from typing import List, Optional
from dao.database import get_connection
from dao.cuenta_dao import CuentaDAO
from model.transaccion import Transaccion
from model.movimiento import Movimiento
from model.cartola import Cartola
from model.enums import TipoMovimiento

class TransaccionDAO:
    """
    Data Access Object (DAO) para la Transacción Bancaria y sus líneas de detalle (Movimientos).
    Cumple con el requisito de persistir cabecera y detalles en una sola operación atómica (commit/rollback).
    """
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path
        self.cuenta_dao = CuentaDAO(db_path)

    def crear_con_detalles(self, transaccion: Transaccion) -> int:
        """
        Inserta la cabecera de la transacción y todas sus líneas de detalle (Movimientos)
        de forma estrictamente ATÓMICA en una sola transacción de base de datos.
        """
        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        sql_tx = "INSERT INTO transacciones (numero_cuenta, fecha) VALUES (?, ?);"
        sql_mov = """
            INSERT INTO movimientos (transaccion_id, tipo, monto, descripcion, cuenta_origen, cuenta_destino)
            VALUES (?, ?, ?, ?, ?, ?);
        """

        try:
            fecha_iso = transaccion.fecha.isoformat()
            cursor.execute(sql_tx, (transaccion.cuenta.numero_cuenta, fecha_iso))
            transaccion_id = cursor.lastrowid

            for mov in transaccion.detalles:
                origen_num = mov.cuenta_origen.numero_cuenta if mov.cuenta_origen else transaccion.cuenta.numero_cuenta
                destino_num = mov.cuenta_destino.numero_cuenta if mov.cuenta_destino else None

                cursor.execute(sql_mov, (
                    transaccion_id,
                    mov.tipo.value,
                    mov.monto,
                    mov.descripcion,
                    origen_num,
                    destino_num
                ))

            conn.commit()
            return transaccion_id
        except Exception as ex:
            conn.rollback()
            raise ex
        finally:
            conn.close()

    def obtener_por_id(self, id_transaccion: int) -> Optional[Transaccion]:
        """
        Obtiene una transacción completa con sus líneas de detalle reconstruidas como objetos Movimiento.
        """
        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT id, numero_cuenta, fecha FROM transacciones WHERE id = ?;", (id_transaccion,))
        row_tx = cursor.fetchone()
        if not row_tx:
            conn.close()
            return None

        cuenta = self.cuenta_dao.obtener_por_numero(row_tx["numero_cuenta"])
        if not cuenta:
            conn.close()
            return None

        try:
            fecha_dt = datetime.fromisoformat(row_tx["fecha"])
        except Exception:
            fecha_dt = datetime.now()

        transaccion = Transaccion(cuenta=cuenta, fecha=fecha_dt)

        # Cargar líneas de detalle
        cursor.execute("""
            SELECT id, tipo, monto, descripcion, cuenta_origen, cuenta_destino
            FROM movimientos
            WHERE transaccion_id = ?
            ORDER BY id ASC;
        """, (id_transaccion,))
        rows_mov = cursor.fetchall()
        conn.close()

        for rm in rows_mov:
            tipo_mov = TipoMovimiento(rm["tipo"])
            c_origen = self.cuenta_dao.obtener_por_numero(rm["cuenta_origen"]) if rm["cuenta_origen"] else cuenta
            c_destino = self.cuenta_dao.obtener_por_numero(rm["cuenta_destino"]) if rm["cuenta_destino"] else None
            
            mov = Movimiento(
                tipo=tipo_mov,
                monto=float(rm["monto"]),
                descripcion=rm["descripcion"],
                cuenta_origen=c_origen,
                cuenta_destino=c_destino
            )
            transaccion.agregarDetalle(mov)

        return transaccion

    def listar_todos(self) -> List[Transaccion]:
        """Lista todas las transacciones registradas en el sistema."""
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM transacciones ORDER BY id ASC;")
        rows = cursor.fetchall()
        conn.close()

        transacciones = []
        for r in rows:
            tx = self.obtener_por_id(r["id"])
            if tx:
                transacciones.append(tx)
        return transacciones

    def listar_por_cuenta(self, numero_cuenta: str) -> List[Transaccion]:
        """Lista todas las transacciones asociadas a una cuenta específica."""
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id FROM transacciones WHERE numero_cuenta = ? ORDER BY id ASC;",
            (str(numero_cuenta).strip(),)
        )
        rows = cursor.fetchall()
        conn.close()

        transacciones = []
        for r in rows:
            tx = self.obtener_por_id(r["id"])
            if tx:
                transacciones.append(tx)
        return transacciones

    def eliminar(self, id_transaccion: int) -> bool:
        """Elimina una transacción y sus líneas de detalle asociadas."""
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM transacciones WHERE id = ?;", (id_transaccion,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as ex:
            conn.rollback()
            raise ex
        finally:
            conn.close()

    def obtener_cartola(
        self, 
        numero_cuenta: str, 
        fecha_inicio: Optional[datetime] = None, 
        fecha_fin: Optional[datetime] = None
    ) -> Optional[Cartola]:
        """
        Genera la Cartola Bancaria con todos los movimientos registrados para una cuenta.
        Cumple con las pruebas P12 y P13 del guion de pruebas.
        """
        cuenta = self.cuenta_dao.obtener_por_numero(numero_cuenta)
        if not cuenta:
            return None

        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        sql = """
            SELECT m.tipo, m.monto, m.descripcion, m.cuenta_origen, m.cuenta_destino, t.fecha
            FROM movimientos m
            JOIN transacciones t ON m.transaccion_id = t.id
            WHERE t.numero_cuenta = ?
            ORDER BY m.id ASC;
        """
        cursor.execute(sql, (numero_cuenta,))
        rows = cursor.fetchall()
        conn.close()

        movimientos = []
        fechas = []
        for r in rows:
            tipo_mov = TipoMovimiento(r["tipo"])
            c_origen = self.cuenta_dao.obtener_por_numero(r["cuenta_origen"]) if r["cuenta_origen"] else cuenta
            c_destino = self.cuenta_dao.obtener_por_numero(r["cuenta_destino"]) if r["cuenta_destino"] else None
            
            mov = Movimiento(
                tipo=tipo_mov,
                monto=float(r["monto"]),
                descripcion=r["descripcion"],
                cuenta_origen=c_origen,
                cuenta_destino=c_destino
            )
            movimientos.append(mov)
            try:
                fechas.append(datetime.fromisoformat(r["fecha"]))
            except Exception:
                pass

        f_ini = fecha_inicio if fecha_inicio else (min(fechas) if fechas else datetime.now())
        f_fin = fecha_fin if fecha_fin else (max(fechas) if fechas else datetime.now())

        return Cartola(cuenta=cuenta, fecha_inicio=f_ini, fecha_fin=f_fin, movimientos=movimientos)
