class Mora:
    """
    Clase que representa el estado de morosidad de un cliente.
    Encapsulamiento con getters, setters y validaciones.
    """
    def __init__(self, is_mora: bool = False, amount_mora: int = 0):
        self._is_mora = False
        self._amount_mora = 0
        
        self.setIsMora(is_mora)
        self.setAmountMora(amount_mora)

    @property
    def is_mora(self) -> bool:
        return self._is_mora

    @property
    def amount_mora(self) -> int:
        return self._amount_mora

    def getIsMora(self) -> bool:
        return self._is_mora

    def getAmountMora(self) -> int:
        return self._amount_mora

    def setIsMora(self, status: bool) -> None:
        if not isinstance(status, bool):
            raise TypeError("El estado de mora debe ser un valor booleano (True/False).")
        self._is_mora = status
        if not status:
            self._amount_mora = 0

    def setAmountMora(self, amount: int) -> None:
        if not isinstance(amount, (int, float)) or amount < 0:
            raise ValueError("El monto de mora debe ser un número positivo mayor o igual a 0.")
        self._amount_mora = int(amount)
        if self._amount_mora > 0:
            self._is_mora = True

    def __str__(self) -> str:
        if self._is_mora:
            return f"Mora Vigente: ${self._amount_mora:,.0f}"
        return "Sin Mora"

    def __repr__(self) -> str:
        return f"Mora(is_mora={self._is_mora}, amount_mora={self._amount_mora})"
