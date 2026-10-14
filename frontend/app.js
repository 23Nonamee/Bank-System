/**
 * ============================================================================
 * SOUTHPARK BANK - BANCA EN LÍNEA SEGURA
 * Lógica Frontend en JavaScript Puro (Vanilla JS)
 * Características: Validación defensiva, Módulo 11 chileno, SPA, Accesibilidad
 * ============================================================================
 */

(function () {
  "use strict";

  // ==========================================================================
  // ESTADO DE LA APLICACIÓN (DATOS DE EJEMPLO DE LA DEMO ACADÉMICA)
  // ==========================================================================

  const state = {
    isAuthenticated: false,
    user: {
      name: "Isaias Arancibia",
      rut: "12.345.678-5",
      passwordDemo: "123456"
    },
    accounts: {
      cc: {
        number: "CC-1001-9874",
        type: "Cuenta Corriente",
        balance: 1450000,
        overdraft: 300000
      },
      ca: {
        number: "CA-2001-4412",
        type: "Cuenta de Ahorro",
        balance: 500000,
        rate: 0.045
      }
    },
    movements: [
      {
        id: 105,
        date: "13/10/2026 14:32",
        description: "Abono Remuneración Mensual",
        type: "ABONO",
        amount: 1200000,
        balanceAfter: 1450000
      },
      {
        id: 104,
        date: "12/10/2026 19:15",
        description: "Compra Supermercado SouthPark",
        type: "CARGO",
        amount: 85400,
        balanceAfter: 250000
      },
      {
        id: 103,
        date: "10/10/2026 11:20",
        description: "Giro Cajero Automático Centro",
        type: "CARGO",
        amount: 50000,
        balanceAfter: 335400
      },
      {
        id: 102,
        date: "08/10/2026 09:45",
        description: "Pago de Servicios Básicos",
        type: "CARGO",
        amount: 42600,
        balanceAfter: 385400
      },
      {
        id: 101,
        date: "05/10/2026 16:10",
        description: "Transferencia Recibida de Terceros",
        type: "ABONO",
        amount: 128000,
        balanceAfter: 428000
      }
    ],
    rates: {
      dolar: 945.50,
      uf: 37850.20,
      lastUpdated: new Date().toLocaleDateString("es-CL")
    },
    converterDirection: "CLP_TO_USD", // Opciones: "CLP_TO_USD" | "USD_TO_CLP"
    pendingTransfer: null // Datos temporales para la confirmación
  };

  // ==========================================================================
  // ELEMENTOS DEL DOM
  // ==========================================================================

  const dom = {
    // Header & Sesión
    userSession: document.getElementById("user-session"),
    sessionUserName: document.getElementById("session-user-name"),
    sessionUserRut: document.getElementById("session-user-rut"),
    btnLogout: document.getElementById("btn-logout"),
    mainNav: document.getElementById("main-nav"),

    // Pestañas
    tabSummary: document.getElementById("tab-summary"),
    tabTransfer: document.getElementById("tab-transfer"),
    tabCurrency: document.getElementById("tab-currency"),

    // Vistas / Pantallas
    viewLogin: document.getElementById("view-login"),
    viewSummary: document.getElementById("view-summary"),
    viewTransfer: document.getElementById("view-transfer"),
    viewCurrency: document.getElementById("view-currency"),

    // Formulario de Login
    formLogin: document.getElementById("form-login"),
    loginRut: document.getElementById("login-rut"),
    loginRutError: document.getElementById("login-rut-error"),
    loginPass: document.getElementById("login-password"),
    loginPassError: document.getElementById("login-password-error"),
    loginAlert: document.getElementById("login-alert"),
    loginAlertText: document.getElementById("login-alert-text"),
    btnSubmitLogin: document.getElementById("btn-submit-login"),
    loginSpinner: document.getElementById("login-spinner"),
    loginBtnText: document.getElementById("login-btn-text"),
    btnTogglePassword: document.getElementById("btn-toggle-password"),
    togglePasswordIcon: document.getElementById("toggle-password-icon"),

    // Pantalla Resumen
    ccBalance: document.getElementById("cc-balance"),
    ccOverdraft: document.getElementById("cc-overdraft"),
    ccTotalAvailable: document.getElementById("cc-total-available"),
    btnQuickTransfer: document.getElementById("btn-quick-transfer"),
    filterMovementType: document.getElementById("filter-movement-type"),
    movementsTbody: document.getElementById("movements-tbody"),

    // Formulario de Transferencia
    formTransfer: document.getElementById("form-transfer"),
    transferSource: document.getElementById("transfer-source"),
    transferRut: document.getElementById("transfer-rut"),
    transferRutError: document.getElementById("transfer-rut-error"),
    transferName: document.getElementById("transfer-name"),
    transferNameError: document.getElementById("transfer-name-error"),
    transferBank: document.getElementById("transfer-bank"),
    transferBankError: document.getElementById("transfer-bank-error"),
    transferAccountType: document.getElementById("transfer-account-type"),
    transferAccountNum: document.getElementById("transfer-account-num"),
    transferAccountNumError: document.getElementById("transfer-account-num-error"),
    transferAmount: document.getElementById("transfer-amount"),
    transferAmountError: document.getElementById("transfer-amount-error"),
    transferAmountHint: document.getElementById("transfer-amount-hint"),
    transferMessage: document.getElementById("transfer-message"),
    btnResetTransfer: document.getElementById("btn-reset-transfer"),

    // Modal de Confirmación
    modalConfirm: document.getElementById("modal-confirm"),
    modalDestName: document.getElementById("modal-dest-name"),
    modalDestRut: document.getElementById("modal-dest-rut"),
    modalDestBank: document.getElementById("modal-dest-bank"),
    modalDestAccount: document.getElementById("modal-dest-account"),
    modalSourceAccount: document.getElementById("modal-source-account"),
    modalMessage: document.getElementById("modal-message"),
    modalAmount: document.getElementById("modal-amount"),
    btnModalCancel: document.getElementById("btn-modal-cancel"),
    btnModalConfirm: document.getElementById("btn-modal-confirm"),
    modalSpinner: document.getElementById("modal-spinner"),
    modalBtnText: document.getElementById("modal-btn-text"),

    // Modal Comprobante
    modalReceipt: document.getElementById("modal-receipt"),
    receiptAmount: document.getElementById("receipt-amount"),
    receiptTxId: document.getElementById("receipt-tx-id"),
    receiptDatetime: document.getElementById("receipt-datetime"),
    receiptDestName: document.getElementById("receipt-dest-name"),
    receiptDestRut: document.getElementById("receipt-dest-rut"),
    receiptBank: document.getElementById("receipt-bank"),
    receiptNewBalance: document.getElementById("receipt-new-balance"),
    btnReceiptClose: document.getElementById("btn-receipt-close"),

    // Divisas & Calculadora
    valDolar: document.getElementById("val-dolar"),
    dateDolar: document.getElementById("date-dolar"),
    valUf: document.getElementById("val-uf"),
    dateUf: document.getElementById("date-uf"),
    btnRefreshRates: document.getElementById("btn-refresh-rates"),
    ratesSpinner: document.getElementById("rates-spinner"),
    ratesBtnText: document.getElementById("rates-btn-text"),
    formConverter: document.getElementById("form-converter"),
    converterAmount: document.getElementById("converter-amount"),
    converterAmountLabel: document.getElementById("converter-amount-label"),
    converterPrefix: document.getElementById("converter-prefix"),
    converterResultLabel: document.getElementById("converter-result-label"),
    converterResultValue: document.getElementById("converter-result-value"),
    converterAppliedRate: document.getElementById("converter-applied-rate"),
    converterAmountError: document.getElementById("converter-amount-error"),
    btnSwapCurrency: document.getElementById("btn-swap-currency"),

    // Toast flotante
    toastNotification: document.getElementById("toast-notification"),
    toastIcon: document.getElementById("toast-icon"),
    toastText: document.getElementById("toast-text")
  };

  // ==========================================================================
  // UTILIDADES DE FORMATO Y VALIDACIÓN (MÓDULO 11 CHILENO)
  // ==========================================================================

  /**
   * Limpia y formatea un número como moneda chilena ($ 1.250.000).
   */
  function formatMoney(amount, currency = "CLP") {
    if (isNaN(amount)) return "$ 0 " + currency;
    const formatted = Math.round(amount)
      .toString()
      .replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    return `$ ${formatted} ${currency}`;
  }

  /**
   * Limpia un RUT eliminando puntos y espacios, manteniendo guion y dígito.
   */
  function cleanRut(rutRaw) {
    if (!rutRaw) return "";
    return rutRaw.replace(/[^0-9kK-]/g, "").toUpperCase();
  }

  /**
   * Da formato visual con puntos y guion a un RUT (ej: 12345678-5 -> 12.345.678-5).
   */
  function formatRut(rutRaw) {
    const cleaned = cleanRut(rutRaw).replace(/-/g, "");
    if (cleaned.length < 2) return cleaned;
    const body = cleaned.slice(0, -1);
    const dv = cleaned.slice(-1);
    const formattedBody = body.replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    return `${formattedBody}-${dv}`;
  }

  /**
   * Valida estrictamente un RUT chileno usando el Algoritmo Módulo 11 oficial.
   * Réplica exacta de la lógica de validación de backend en model/rut.py.
   */
  function isValidChileanRut(rutString) {
    const cleaned = cleanRut(rutString);
    if (!cleaned || !cleaned.includes("-")) return false;

    const parts = cleaned.split("-");
    if (parts.length !== 2) return false;

    const cuerpo = parts[0].replace(/\./g, "");
    const dv = parts[1].toUpperCase();

    // Debe tener al menos 7 dígitos en el cuerpo y solo dígitos numéricos
    if (!/^\d{7,8}$/.test(cuerpo)) return false;
    if (!/^[0-9K]$/.test(dv)) return false;

    // Cálculo Módulo 11
    let suma = 0;
    let multiplo = 2;

    for (let i = cuerpo.length - 1; i >= 0; i--) {
      suma += parseInt(cuerpo[i], 10) * multiplo;
      multiplo = multiplo === 7 ? 2 : multiplo + 1;
    }

    const resto = 11 - (suma % 11);
    let dvEsperado;
    if (resto === 11) {
      dvEsperado = "0";
    } else if (resto === 10) {
      dvEsperado = "K";
    } else {
      dvEsperado = resto.toString();
    }

    return dv === dvEsperado;
  }

  /**
   * Muestra mensaje de error inline junto a un campo de formulario y actualiza ARIA.
   */
  function setFieldError(inputEl, errorEl, message) {
    if (!inputEl || !errorEl) return;
    inputEl.classList.add("has-error");
    inputEl.setAttribute("aria-invalid", "true");
    errorEl.textContent = message;
    errorEl.classList.add("visible");
  }

  /**
   * Limpia mensaje de error inline de un campo.
   */
  function clearFieldError(inputEl, errorEl) {
    if (!inputEl || !errorEl) return;
    inputEl.classList.remove("has-error");
    inputEl.removeAttribute("aria-invalid");
    errorEl.textContent = "";
    errorEl.classList.remove("visible");
  }

  /**
   * Muestra notificación Toast flotante con temporizador automático.
   */
  let toastTimer = null;
  function showToast(message, icon = "ℹ️", duration = 3500) {
    if (!dom.toastNotification) return;
    clearTimeout(toastTimer);
    dom.toastIcon.textContent = icon;
    dom.toastText.textContent = message;
    dom.toastNotification.classList.remove("hidden");

    toastTimer = setTimeout(() => {
      dom.toastNotification.classList.add("hidden");
    }, duration);
  }

  // ==========================================================================
  // CONTROLADOR DE NAVEGACIÓN Y VISTAS (SPA)
  // ==========================================================================

  function switchView(viewName) {
    const views = {
      login: dom.viewLogin,
      summary: dom.viewSummary,
      transfer: dom.viewTransfer,
      currency: dom.viewCurrency
    };

    const tabs = {
      summary: dom.tabSummary,
      transfer: dom.tabTransfer,
      currency: dom.tabCurrency
    };

    // Ocultar todas las vistas
    Object.values(views).forEach(v => {
      if (v) {
        v.classList.remove("active");
        v.setAttribute("hidden", "true");
      }
    });

    // Desactivar todas las pestañas
    Object.values(tabs).forEach(t => {
      if (t) {
        t.classList.remove("active");
        t.setAttribute("aria-selected", "false");
      }
    });

    // Activar la vista solicitada
    const targetView = views[viewName];
    if (targetView) {
      targetView.removeAttribute("hidden");
      targetView.classList.add("active");
    }

    // Activar pestaña correspondiente si no es login
    if (viewName !== "login" && tabs[viewName]) {
      tabs[viewName].classList.add("active");
      tabs[viewName].setAttribute("aria-selected", "true");
    }

    // Desplazar al inicio del contenido principal
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  // ==========================================================================
  // RENDERIZADO DE RESUMEN Y MOVIMIENTOS
  // ==========================================================================

  function updateSummaryDisplay() {
    const cc = state.accounts.cc;
    const totalAvailable = cc.balance + cc.overdraft;

    dom.ccBalance.innerHTML = `${formatMoney(cc.balance, "")} <small>CLP</small>`;
    dom.ccOverdraft.textContent = formatMoney(cc.overdraft);
    dom.ccTotalAvailable.textContent = formatMoney(totalAvailable);

    // Actualizar hint en formulario de transferencias
    dom.transferAmountHint.textContent = `Comisión: $0 CLP. Saldo disponible en cuenta: ${formatMoney(cc.balance)}.`;

    renderMovementsTable();
  }

  function renderMovementsTable() {
    const filter = dom.filterMovementType.value;
    const filtered = state.movements.filter(m => {
      if (filter === "ALL") return true;
      return m.type === filter;
    });

    if (filtered.length === 0) {
      dom.movementsTbody.innerHTML = `
        <tr>
          <td colspan="5" style="text-align: center; padding: 2.5rem; color: var(--color-text-muted);">
            No se encontraron movimientos registrados para el filtro seleccionado.
          </td>
        </tr>
      `;
      return;
    }

    dom.movementsTbody.innerHTML = filtered.map(m => {
      const isAbono = m.type === "ABONO";
      const badgeClass = isAbono ? "badge-abono" : "badge-cargo";
      const amountClass = isAbono ? "amount-abono" : "amount-cargo";
      const sign = isAbono ? "+" : "-";

      return `
        <tr>
          <td>
            <time datetime="${m.date}">${m.date}</time>
          </td>
          <td>
            <strong>${m.description}</strong>
          </td>
          <td>
            <span class="badge-mov ${badgeClass}">${m.type}</span>
          </td>
          <td class="text-right ${amountClass}">
            ${sign} ${formatMoney(m.amount, "")}
          </td>
          <td class="text-right" style="font-family: monospace; font-weight: 600;">
            ${formatMoney(m.balanceAfter, "")}
          </td>
        </tr>
      `;
    }).join("");
  }

  // ==========================================================================
  // PANTALLA 1: FLUJO DE INICIO DE SESIÓN
  // ==========================================================================

  // Autoformato de RUT mientras se escribe
  dom.loginRut.addEventListener("blur", function () {
    const formatted = formatRut(this.value);
    if (formatted) this.value = formatted;
  });

  dom.loginRut.addEventListener("input", function () {
    clearFieldError(dom.loginRut, dom.loginRutError);
    dom.loginAlert.classList.add("hidden");
  });

  dom.loginPass.addEventListener("input", function () {
    clearFieldError(dom.loginPass, dom.loginPassError);
    dom.loginAlert.classList.add("hidden");
  });

  // Mostrar / Ocultar Contraseña
  dom.btnTogglePassword.addEventListener("click", function () {
    const isPassword = dom.loginPass.getAttribute("type") === "password";
    dom.loginPass.setAttribute("type", isPassword ? "text" : "password");
    dom.togglePasswordIcon.textContent = isPassword ? "🙈" : "👁️";
    dom.btnTogglePassword.setAttribute("title", isPassword ? "Ocultar clave" : "Mostrar clave");
  });

  // Envío del Login
  dom.formLogin.addEventListener("submit", function (e) {
    e.preventDefault();

    let isValid = true;
    const rutVal = dom.loginRut.value.trim();
    const passVal = dom.loginPass.value.trim();

    // Validación Campo RUT
    if (!rutVal) {
      setFieldError(dom.loginRut, dom.loginRutError, "Debe ingresar su RUT de titular.");
      isValid = false;
    } else if (!isValidChileanRut(rutVal)) {
      setFieldError(
        dom.loginRut,
        dom.loginRutError,
        "El RUT ingresado no es válido según el algoritmo Módulo 11 (Ej: 12.345.678-5)."
      );
      isValid = false;
    }

    // Validación Campo Clave
    if (!passVal) {
      setFieldError(dom.loginPass, dom.loginPassError, "Debe ingresar su clave secreta.");
      isValid = false;
    } else if (passVal.length < 6) {
      setFieldError(dom.loginPass, dom.loginPassError, "La clave debe contener al menos 6 caracteres.");
      isValid = false;
    }

    if (!isValid) return;

    // Estado de Carga
    dom.btnSubmitLogin.disabled = true;
    dom.loginSpinner.classList.remove("hidden");
    dom.loginBtnText.textContent = "Verificando Credenciales...";

    // Simulación de autenticación segura (600ms)
    setTimeout(() => {
      dom.btnSubmitLogin.disabled = false;
      dom.loginSpinner.classList.add("hidden");
      dom.loginBtnText.textContent = "Ingresar a mi Cuenta";

      // Aceptamos cualquier RUT válido con clave demo o la clave 123456
      if (passVal !== state.user.passwordDemo && passVal !== "123456") {
        dom.loginAlertText.textContent = "Clave secreta incorrecta. Utilice la clave de prueba '123456'.";
        dom.loginAlert.classList.remove("hidden");
        dom.loginPass.focus();
        return;
      }

      // Autenticación Exitosa
      state.isAuthenticated = true;
      state.user.rut = formatRut(rutVal);

      // Mostrar controles de sesión en el Header
      dom.sessionUserName.textContent = state.user.name;
      dom.sessionUserRut.textContent = `RUT: ${state.user.rut}`;
      dom.userSession.classList.remove("hidden");
      dom.mainNav.classList.remove("hidden");

      // Limpiar formulario de login
      dom.formLogin.reset();

      // Cambiar a vista de resumen
      updateSummaryDisplay();
      switchView("summary");
      showToast(`¡Bienvenido(a) a SouthPark Bank, ${state.user.name}!`, "👋");
    }, 600);
  });

  // Cerrar Sesión
  dom.btnLogout.addEventListener("click", function () {
    state.isAuthenticated = false;
    dom.userSession.classList.add("hidden");
    dom.mainNav.classList.add("hidden");
    switchView("login");
    showToast("Su sesión ha sido cerrada de forma segura.", "🔒");
  });

  // ==========================================================================
  // PANTALLA 3: FLUJO DE TRANSFERENCIA CON CONFIRMACIÓN
  // ==========================================================================

  // Autoformato RUT Destinatario
  dom.transferRut.addEventListener("blur", function () {
    const formatted = formatRut(this.value);
    if (formatted) this.value = formatted;
  });

  // Limpiar errores inline al escribir
  [
    [dom.transferRut, dom.transferRutError],
    [dom.transferName, dom.transferNameError],
    [dom.transferBank, dom.transferBankError],
    [dom.transferAccountNum, dom.transferAccountNumError],
    [dom.transferAmount, dom.transferAmountError]
  ].forEach(([input, error]) => {
    input.addEventListener("input", () => clearFieldError(input, error));
  });

  // Chips de montos rápidos
  document.querySelectorAll(".btn-chip").forEach(btn => {
    btn.addEventListener("click", function () {
      const chipAmount = parseInt(this.getAttribute("data-amount"), 10);
      const current = parseInt(dom.transferAmount.value, 10) || 0;
      dom.transferAmount.value = current + chipAmount;
      clearFieldError(dom.transferAmount, dom.transferAmountError);
    });
  });

  // Envío a Confirmación
  dom.formTransfer.addEventListener("submit", function (e) {
    e.preventDefault();

    let isValid = true;
    const destRut = dom.transferRut.value.trim();
    const destName = dom.transferName.value.trim();
    const destBank = dom.transferBank.value.trim();
    const destAccNum = dom.transferAccountNum.value.trim();
    const amountVal = parseFloat(dom.transferAmount.value);
    const message = dom.transferMessage.value.trim() || "Transferencia electrónica";

    // 1. Validar RUT
    if (!destRut) {
      setFieldError(dom.transferRut, dom.transferRutError, "Ingrese el RUT del destinatario.");
      isValid = false;
    } else if (!isValidChileanRut(destRut)) {
      setFieldError(
        dom.transferRut,
        dom.transferRutError,
        "El RUT ingresado no es válido según algoritmo Módulo 11 (Ej: 19.876.543-2)."
      );
      isValid = false;
    } else if (cleanRut(destRut) === cleanRut(state.user.rut)) {
      setFieldError(
        dom.transferRut,
        dom.transferRutError,
        "No puede transferir a su propio RUT como destinatario de terceros."
      );
      isValid = false;
    }

    // 2. Validar Nombre
    if (!destName) {
      setFieldError(dom.transferName, dom.transferNameError, "Ingrese el nombre del destinatario.");
      isValid = false;
    } else if (destName.length < 3) {
      setFieldError(dom.transferName, dom.transferNameError, "El nombre debe tener al menos 3 caracteres.");
      isValid = false;
    }

    // 3. Validar Banco
    if (!destBank) {
      setFieldError(dom.transferBank, dom.transferBankError, "Seleccione la institución bancaria de destino.");
      isValid = false;
    }

    // 4. Validar Número de Cuenta
    if (!destAccNum) {
      setFieldError(dom.transferAccountNum, dom.transferAccountNumError, "Ingrese el número de cuenta de destino.");
      isValid = false;
    } else if (destAccNum.length < 4) {
      setFieldError(dom.transferAccountNum, dom.transferAccountNumError, "El número de cuenta es demasiado corto.");
      isValid = false;
    }

    // 5. Validar Monto y Saldo Disponible
    const cc = state.accounts.cc;
    if (isNaN(amountVal) || amountVal <= 0) {
      setFieldError(dom.transferAmount, dom.transferAmountError, "Ingrese un monto válido mayor a $0.");
      isValid = false;
    } else if (amountVal < 1000) {
      setFieldError(dom.transferAmount, dom.transferAmountError, "El monto mínimo de transferencia es de $1.000 CLP.");
      isValid = false;
    } else if (amountVal > cc.balance) {
      setFieldError(
        dom.transferAmount,
        dom.transferAmountError,
        `Saldo insuficiente. Su saldo disponible es de ${formatMoney(cc.balance)}.`
      );
      isValid = false;
    }

    if (!isValid) {
      // Enfocar el primer campo con error
      const firstErrorInput = dom.formTransfer.querySelector(".has-error");
      if (firstErrorInput) firstErrorInput.focus();
      return;
    }

    // Datos válidos -> Preparar Modal de Confirmación
    state.pendingTransfer = {
      destRut: formatRut(destRut),
      destName,
      destBank,
      destAccountType: dom.transferAccountType.value,
      destAccountNum: destAccNum,
      sourceAccount: dom.transferSource.options[dom.transferSource.selectedIndex].text,
      amount: amountVal,
      message
    };

    // Población de datos en el modal
    dom.modalDestName.textContent = state.pendingTransfer.destName;
    dom.modalDestRut.textContent = state.pendingTransfer.destRut;
    dom.modalDestBank.textContent = state.pendingTransfer.destBank;
    dom.modalDestAccount.textContent = `${state.pendingTransfer.destAccountType} N° ${state.pendingTransfer.destAccountNum}`;
    dom.modalSourceAccount.textContent = state.pendingTransfer.sourceAccount;
    dom.modalMessage.textContent = state.pendingTransfer.message;
    dom.modalAmount.textContent = formatMoney(state.pendingTransfer.amount);

    // Abrir Modal
    dom.modalConfirm.classList.remove("hidden");
    dom.btnModalConfirm.focus();
  });

  // Cancelar Confirmación
  dom.btnModalCancel.addEventListener("click", function () {
    dom.modalConfirm.classList.add("hidden");
    state.pendingTransfer = null;
    dom.transferAmount.focus();
  });

  // Confirmar y Ejecutar Transferencia
  dom.btnModalConfirm.addEventListener("click", function () {
    if (!state.pendingTransfer) return;

    dom.btnModalConfirm.disabled = true;
    dom.btnModalCancel.disabled = true;
    dom.modalSpinner.classList.remove("hidden");
    dom.modalBtnText.textContent = "Procesando...";

    setTimeout(() => {
      // Aplicar débito al saldo de Cuenta Corriente
      const amount = state.pendingTransfer.amount;
      state.accounts.cc.balance -= amount;
      const newBalance = state.accounts.cc.balance;

      // Registrar movimiento de CARGO
      const now = new Date();
      const dateStr = now.toLocaleDateString("es-CL") + " " + now.toLocaleTimeString("es-CL", { hour: "2-digit", minute: "2-digit" });
      const txId = "#SPB-" + Math.floor(100000 + Math.random() * 900000);

      state.movements.unshift({
        id: state.movements.length + 101,
        date: dateStr,
        description: `Transferencia a ${state.pendingTransfer.destName}`,
        type: "CARGO",
        amount: amount,
        balanceAfter: newBalance
      });

      // Cerrar modal de confirmación
      dom.btnModalConfirm.disabled = false;
      dom.btnModalCancel.disabled = false;
      dom.modalSpinner.classList.add("hidden");
      dom.modalBtnText.textContent = "Autorizar y Transferir";
      dom.modalConfirm.classList.add("hidden");

      // Poblar Comprobante
      dom.receiptAmount.textContent = formatMoney(amount);
      dom.receiptTxId.textContent = txId;
      dom.receiptDatetime.textContent = dateStr;
      dom.receiptDestName.textContent = state.pendingTransfer.destName;
      dom.receiptDestRut.textContent = state.pendingTransfer.destRut;
      dom.receiptBank.textContent = `${state.pendingTransfer.destBank} (${state.pendingTransfer.destAccountType})`;
      dom.receiptNewBalance.textContent = formatMoney(newBalance);

      // Mostrar Modal Comprobante
      dom.modalReceipt.classList.remove("hidden");
      dom.btnReceiptClose.focus();

      // Limpiar Formulario de Transferencia
      dom.formTransfer.reset();
      updateSummaryDisplay();
      state.pendingTransfer = null;
    }, 800);
  });

  // Cerrar Comprobante e ir al Resumen de Movimientos
  dom.btnReceiptClose.addEventListener("click", function () {
    dom.modalReceipt.classList.add("hidden");
    switchView("summary");
    showToast("Transferencia registrada exitosamente en su cartola.", "✅");
  });

  // Accesibilidad en Modales: Cerrar con tecla Escape
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") {
      if (!dom.modalConfirm.classList.contains("hidden")) {
        dom.modalConfirm.classList.add("hidden");
        state.pendingTransfer = null;
      }
      if (!dom.modalReceipt.classList.contains("hidden")) {
        dom.modalReceipt.classList.add("hidden");
        switchView("summary");
      }
    }
  });

  // ==========================================================================
  // PANTALLA 4: CONVERSIÓN DE DIVISAS Y CONSUMO DE TASAS
  // ==========================================================================

  function calculateConversion() {
    const rawVal = parseFloat(dom.converterAmount.value);
    const rate = state.rates.dolar;

    if (isNaN(rawVal) || rawVal <= 0) {
      dom.converterResultValue.textContent = "-";
      return;
    }

    if (state.converterDirection === "CLP_TO_USD") {
      const usdResult = rawVal / rate;
      dom.converterResultValue.textContent = usdResult.toLocaleString("en-US", {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      }) + " USD";
    } else {
      const clpResult = Math.round(rawVal * rate);
      dom.converterResultValue.textContent = formatMoney(clpResult);
    }
  }

  // Swap de dirección de conversión
  dom.btnSwapCurrency.addEventListener("click", function () {
    if (state.converterDirection === "CLP_TO_USD") {
      state.converterDirection = "USD_TO_CLP";
      dom.converterAmountLabel.textContent = "Monto en Dólares (USD)";
      dom.converterPrefix.textContent = "US$";
      dom.converterResultLabel.textContent = "Monto Equivalente en Pesos Chilenos (CLP)";
      dom.converterAmount.value = "100";
    } else {
      state.converterDirection = "CLP_TO_USD";
      dom.converterAmountLabel.textContent = "Monto en Pesos Chilenos ($ CLP)";
      dom.converterPrefix.textContent = "$";
      dom.converterResultLabel.textContent = "Monto Equivalente en Dólares (USD)";
      dom.converterAmount.value = "100000";
    }
    calculateConversion();
  });

  dom.converterAmount.addEventListener("input", calculateConversion);

  // Consulta de indicadores (con resiliencia y timeout)
  async function fetchIndicators() {
    dom.btnRefreshRates.disabled = true;
    dom.ratesSpinner.classList.remove("hidden");
    dom.ratesBtnText.textContent = "Consultando...";

    try {
      // Petición con AbortController para timeout de 3 segundos
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 3000);

      const resp = await fetch("https://mindicador.cl/api", { signal: controller.signal });
      clearTimeout(timeoutId);

      if (!resp.ok) throw new Error("HTTP " + resp.status);

      const data = await resp.json();
      if (data.dolar && data.dolar.valor) {
        state.rates.dolar = parseFloat(data.dolar.valor);
      }
      if (data.uf && data.uf.valor) {
        state.rates.uf = parseFloat(data.uf.valor);
      }
      state.rates.lastUpdated = new Date().toLocaleDateString("es-CL");
      showToast("Indicadores actualizados desde mindicador.cl", "📈");
    } catch (err) {
      // Fallback resiliente
      console.warn("No se pudo conectar a la API externa de mindicador.cl. Usando valores oficiales de respaldo.", err);
      showToast("Modo sin internet: Mostrando última tasa oficial registrada.", "⚠️");
    } finally {
      // Actualizar DOM con valores
      dom.valDolar.textContent = `$ ${state.rates.dolar.toLocaleString("es-CL", { minimumFractionDigits: 2 })}`;
      dom.valUf.textContent = `$ ${state.rates.uf.toLocaleString("es-CL", { minimumFractionDigits: 2 })}`;
      dom.dateDolar.textContent = `Fecha de referencia: ${state.rates.lastUpdated}`;
      dom.dateUf.textContent = `Fecha de referencia: ${state.rates.lastUpdated}`;
      dom.converterAppliedRate.textContent = `1 USD = $ ${state.rates.dolar.toLocaleString("es-CL", { minimumFractionDigits: 2 })} CLP`;

      calculateConversion();

      dom.btnRefreshRates.disabled = false;
      dom.ratesSpinner.classList.add("hidden");
      dom.ratesBtnText.textContent = "🔄 Actualizar Indicadores";
    }
  }

  dom.btnRefreshRates.addEventListener("click", fetchIndicators);

  // ==========================================================================
  // EVENT LISTENERS DE NAVEGACIÓN ENTRE PESTAÑAS
  // ==========================================================================

  dom.tabSummary.addEventListener("click", () => switchView("summary"));
  dom.tabTransfer.addEventListener("click", () => switchView("transfer"));
  dom.tabCurrency.addEventListener("click", () => switchView("currency"));

  dom.btnQuickTransfer.addEventListener("click", () => switchView("transfer"));
  dom.filterMovementType.addEventListener("change", renderMovementsTable);

  // ==========================================================================
  // INICIALIZACIÓN
  // ==========================================================================

  function init() {
    updateSummaryDisplay();
    calculateConversion();
    switchView("login"); // Iniciar en pantalla de inicio de sesión
  }

  // Arrancar cuando el DOM esté listo
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

})();
