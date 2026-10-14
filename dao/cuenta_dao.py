from typing import List, Optional
from dao.database import get_connection
from dao.cliente_dao import ClienteDAO
from model.cuenta import Cuenta
from model.cuenta_corriente import CuentaCorriente
from model.cuenta_ahorro import CuentaAhorro
from model.cuenta_vista import CuentaVista
from model.enums import TipoCuenta

class CuentaDAO:
    """
    Data Access Object (DAO) para las Cuentas Bancarias y sus subtipos polimórficos.
    Mapea registros SQLite a objetos CuentaCorriente, CuentaAhorro o CuentaVista.
    """
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path
        self.cliente_dao = ClienteDAO(db_path)

    def _mapear_fila_a_cuenta(self, row) -> Optional[Cuenta]:
        """Convierte una fila de la base de datos en una instancia del subtipo de Cuenta correspondiente."""
        rut_titular = row["rut_titular"]
        cliente = self.cliente_dao.obtener_por_rut(rut_titular)
        if not cliente:
            return None

        tipo_str = row["tipo"]
        numero = row["numero_cuenta"]
        saldo = float(row["saldo"])

        if tipo_str == TipoCuenta.CORRIENTE.value:
            cupo = int(row["cupo_sobregiro"])
            return CuentaCorriente(numero_cuenta=numero, titular=cliente, saldo=saldo, cupo_sobregiro=cupo)
        elif tipo_str == TipoCuenta.AHORRO.value:
            tasa = float(row["tasa_interes"])
            return CuentaAhorro(numero_cuenta=numero, titular=cliente, saldo=saldo, tasa_interes=tasa)
        elif tipo_str == TipoCuenta.VISTA.value:
            return CuentaVista(numero_cuenta=numero, titular=cliente, saldo=saldo)
        else:
            raise ValueError(f"Tipo de cuenta desconocido en base de datos: {tipo_str}")

    def crear(self, cuenta: Cuenta) -> bool:
        """
        Inserta una cuenta bancaria en la base de datos.
        """
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        sql = """
            INSERT INTO cuentas (numero_cuenta, rut_titular, tipo, saldo, cupo_sobregiro, tasa_interes)
            VALUES (?, ?, ?, ?, ?, ?);
        """
        cupo = getattr(cuenta, "cupo_sobregiro", 0.0)
        tasa = getattr(cuenta, "tasa_interes", 0.0)
        rut_titular = cuenta.titular.rut_cliente.getFormatedRut()

        try:
            cursor.execute(sql, (
                cuenta.numero_cuenta,
                rut_titular,
                cuenta.tipo.value,
                cuenta.saldo,
                cupo,
                tasa
            ))
            conn.commit()
            return True
        except Exception as ex:
            conn.rollback()
            raise ex
        finally:
            conn.close()

    def obtener_por_numero(self, numero_cuenta: str) -> Optional[Cuenta]:
        """
        Busca y retorna un objeto Cuenta por su número de cuenta.
        """
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        sql = """
            SELECT numero_cuenta, rut_titular, tipo, saldo, cupo_sobregiro, tasa_interes
            FROM cuentas
            WHERE numero_cuenta = ?;
        """
        cursor.execute(sql, (str(numero_cuenta).strip(),))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return None
        return self._mapear_fila_a_cuenta(row)

    def listar(self) -> List[Cuenta]:
        """
        Lista todas las cuentas bancarias de la base de datos.
        """
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        sql = """
            SELECT numero_cuenta, rut_titular, tipo, saldo, cupo_sobregiro, tasa_interes
            FROM cuentas
            ORDER BY numero_cuenta ASC;
        """
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.close()

        cuentas = []
        for row in rows:
            cuenta = self._mapear_fila_a_cuenta(row)
            if cuenta:
                cuentas.append(cuenta)
        return cuentas

    def listar_por_cliente(self, rut_str: str) -> List[Cuenta]:
        """
        Lista todas las cuentas pertenecientes a un cliente dado su RUT.
        """
        rut_norm = self.cliente_dao._normalizar_rut(rut_str)
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        sql = """
            SELECT numero_cuenta, rut_titular, tipo, saldo, cupo_sobregiro, tasa_interes
            FROM cuentas
            WHERE rut_titular = ?
            ORDER BY numero_cuenta ASC;
        """
        cursor.execute(sql, (rut_norm,))
        rows = cursor.fetchall()
        conn.close()

        cuentas = []
        for row in rows:
            cuenta = self._mapear_fila_a_cuenta(row)
            if cuenta:
                cuentas.append(cuenta)
        return cuentas

    def actualizar(self, cuenta: Cuenta) -> bool:
        """
        Actualiza el saldo, cupo de sobregiro y tasa de interés de la cuenta en la base de datos.
        """
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        sql = """
            UPDATE cuentas
            SET saldo = ?, cupo_sobregiro = ?, tasa_interes = ?
            WHERE numero_cuenta = ?;
        """
        cupo = getattr(cuenta, "cupo_sobregiro", 0.0)
        tasa = getattr(cuenta, "tasa_interes", 0.0)

        try:
            cursor.execute(sql, (cuenta.saldo, cupo, tasa, cuenta.numero_cuenta))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as ex:
            conn.rollback()
            raise ex
        finally:
            conn.close()

    def eliminar(self, numero_cuenta: str) -> bool:
        """
        Elimina una cuenta bancaria de la base de datos por su número.
        """
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        sql = "DELETE FROM cuentas WHERE numero_cuenta = ?;"

        try:
            cursor.execute(sql, (str(numero_cuenta).strip(),))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as ex:
            conn.rollback()
            raise ex
        finally:
            conn.close()
