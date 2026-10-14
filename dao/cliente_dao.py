from typing import List, Optional
from dao.database import get_connection
from model.cliente import Cliente
from model.rut import Rut
from model.mora import Mora

class ClienteDAO:
    """
    Data Access Object (DAO) para la entidad Cliente.
    Realiza operaciones CRUD completas en SQLite con consultas 100% parametrizadas.
    """
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path

    def _normalizar_rut(self, rut_str: str) -> str:
        """Normaliza el formato del RUT para consultas consistentes."""
        try:
            return Rut(rut_str).getFormatedRut()
        except Exception:
            return rut_str.strip()

    def crear(self, cliente: Cliente) -> bool:
        """
        Inserta un nuevo cliente en la base de datos.
        Consulta parametrizada para prevenir inyección SQL.
        """
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        sql = """
            INSERT INTO clientes (rut, nombre, direccion, is_mora, amount_mora)
            VALUES (?, ?, ?, ?, ?);
        """
        rut_fmt = cliente.rut_cliente.getFormatedRut()
        is_mora = 1 if cliente.mora_cliente.getIsMora() else 0
        amount_mora = cliente.mora_cliente.getAmountMora()

        try:
            cursor.execute(sql, (rut_fmt, cliente.nombre, cliente.direccion, is_mora, amount_mora))
            conn.commit()
            return True
        except Exception as ex:
            conn.rollback()
            raise ex
        finally:
            conn.close()

    def obtener_por_rut(self, rut_str: str) -> Optional[Cliente]:
        """
        Busca y retorna un Cliente por su RUT.
        Retorna una instancia de la clase Cliente o None si no existe.
        """
        rut_norm = self._normalizar_rut(rut_str)
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        sql = """
            SELECT rut, nombre, direccion, is_mora, amount_mora
            FROM clientes
            WHERE rut = ?;
        """
        cursor.execute(sql, (rut_norm,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return None

        rut_obj = Rut(row["rut"])
        mora_obj = Mora(is_mora=bool(row["is_mora"]), amount_mora=int(row["amount_mora"]))
        return Cliente(nombre=row["nombre"], rut=rut_obj, direccion=row["direccion"], mora=mora_obj)

    def listar(self) -> List[Cliente]:
        """
        Lista todos los clientes registrados en el sistema ordenados por nombre.
        Retorna una lista de objetos Cliente.
        """
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        sql = """
            SELECT rut, nombre, direccion, is_mora, amount_mora
            FROM clientes
            ORDER BY nombre ASC;
        """
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.close()

        clientes = []
        for row in rows:
            rut_obj = Rut(row["rut"])
            mora_obj = Mora(is_mora=bool(row["is_mora"]), amount_mora=int(row["amount_mora"]))
            clientes.append(Cliente(nombre=row["nombre"], rut=rut_obj, direccion=row["direccion"], mora=mora_obj))
        return clientes

    def actualizar(self, cliente: Cliente) -> bool:
        """
        Actualiza el nombre, dirección y estado de mora de un cliente existente.
        """
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        sql = """
            UPDATE clientes
            SET nombre = ?, direccion = ?, is_mora = ?, amount_mora = ?
            WHERE rut = ?;
        """
        rut_fmt = cliente.rut_cliente.getFormatedRut()
        is_mora = 1 if cliente.mora_cliente.getIsMora() else 0
        amount_mora = cliente.mora_cliente.getAmountMora()

        try:
            cursor.execute(sql, (cliente.nombre, cliente.direccion, is_mora, amount_mora, rut_fmt))
            conn.commit()
            actualizado = cursor.rowcount > 0
            return actualizado
        except Exception as ex:
            conn.rollback()
            raise ex
        finally:
            conn.close()

    def eliminar(self, rut_str: str) -> bool:
        """
        Elimina un cliente por su RUT de la base de datos.
        """
        rut_norm = self._normalizar_rut(rut_str)
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        sql = "DELETE FROM clientes WHERE rut = ?;"

        try:
            cursor.execute(sql, (rut_norm,))
            conn.commit()
            eliminado = cursor.rowcount > 0
            return eliminado
        except Exception as ex:
            conn.rollback()
            raise ex
        finally:
            conn.close()
