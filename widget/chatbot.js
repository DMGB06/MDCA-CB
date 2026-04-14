(function () {
  "use strict";

  // ============================================================
  // CONFIGURACIÓN - Cambia esto según tu servidor
  // ============================================================
  const CONFIG = {
    wsUrl: "ws://localhost:8000/chat/ws",
    botName: "Asistente Virtual",
    botStatus: "En línea",
    welcomeMessage:
      "Hola, soy tu asistente virtual. Puedo ayudarte con trámites, consultas y servicios.",
    placeholder: "Escribe tu consulta...",
    maxMessageLength: 500,
    reconnectDelay: 3000,
    maxReconnectAttempts: 5,
    // 👇 CAMBIA ESTA URL por la ruta real de tu logo
    logoUrl: "URL_DE_TU_LOGO_AQUI",
  };
  // ============================================================
  // COLORES - Personalizados
  // ============================================================
  const COLORS = {
    primary: "#3d7dae",
    primaryDark: "#2c5d82",
    primaryLight: "#5a9bc9",
    botBubble: "#3d7dae", // Bot: azul institucional
    userBubble: "#16a34a", // Usuario: verde (diferenciado)
    userBubbleDark: "#15803d", // Usuario hover/dark
    background: "#f5f7fa",
    text: "#1e3a52",
    white: "#ffffff",
  };

  // ============================================================
  // ESTILOS
  // ============================================================
  const styles = `
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    .muni-widget * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }

    /* ══════════════════════════════════════════════════════════
       BOTÓN FLOTANTE (Bubble) - más pequeño
       ══════════════════════════════════════════════════════════ */
    .muni-bubble {
      position: fixed;
      bottom: 24px;
      right: 24px;
      width: 50px;
      height: 50px;
      border-radius: 50%;
      background: ${COLORS.primaryDark};
      box-shadow: 0 4px 20px rgba(61, 125, 174, 0.4);
      cursor: pointer;
      border: none;
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 99998;
      transition: transform 0.25s cubic-bezier(.34,1.56,.64,1), box-shadow 0.25s;
    }

    .muni-bubble:hover {
      transform: scale(1.08);
      box-shadow: 0 6px 28px rgba(61, 125, 174, 0.5);
    }

    .muni-bubble-icon {
      width: 24px;
      height: 24px;
      fill: ${COLORS.white};
    }

    /* ══════════════════════════════════════════════════════════
       VENTANA DEL CHAT
       ══════════════════════════════════════════════════════════ */
    .muni-window {
      position: fixed;
      bottom: 86px;
      right: 24px;
      width: 400px;
      height: 520px;
      background: ${COLORS.white};
      border-radius: 16px;
      box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15), 0 2px 10px rgba(0,0,0,0.08);
      display: flex;
      flex-direction: column;
      overflow: hidden;
      z-index: 99999;
      opacity: 0;
      transform: translateY(20px) scale(0.96);
      pointer-events: none;
      transition: opacity 0.3s ease, transform 0.3s ease;
    }

    .muni-window.open {
      opacity: 1;
      transform: translateY(0) scale(1);
      pointer-events: all;
    }

    /* ══════════════════════════════════════════════════════════
       HEADER
       ══════════════════════════════════════════════════════════ */
    .muni-header {
      background: ${COLORS.primary};
      padding: 16px 18px;
      display: flex;
      align-items: center;
      gap: 14px;
      flex-shrink: 0;
    }

    .muni-header-logo {
      width: 48px;
      height: 48px;
      border-radius: 50%;
      background: ${COLORS.white};
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
      overflow: hidden;
    }

    .muni-header-logo img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      border-radius: 50%;
    }

    .muni-header-logo svg {
      width: 28px;
      height: 28px;
      fill: ${COLORS.primary};
    }

    .muni-header-info { flex: 1; }

    .muni-header-name {
      color: ${COLORS.white};
      font-weight: 700;
      font-size: 17px;
      letter-spacing: -0.2px;
    }

    .muni-header-status {
      display: flex;
      align-items: center;
      gap: 6px;
      margin-top: 4px;
    }

    .muni-status-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: #4ade80;
      animation: muni-pulse 2s infinite;
    }

    @keyframes muni-pulse {
      0%, 100% { opacity: 1; }
      50%      { opacity: 0.5; }
    }

    .muni-status-text {
      color: rgba(255,255,255,0.9);
      font-size: 13px;
      font-weight: 500;
    }

    .muni-header-actions {
      display: flex;
      gap: 8px;
    }

    .muni-header-btn {
      width: 32px;
      height: 32px;
      border-radius: 6px;
      background: transparent;
      border: none;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      color: ${COLORS.white};
      font-size: 20px;
      font-weight: 300;
      transition: background 0.2s;
      flex-shrink: 0;
    }

    .muni-header-btn:hover { 
      background: rgba(255,255,255,0.15); 
    }

    /* ══════════════════════════════════════════════════════════
       BARRA DE ERROR
       ══════════════════════════════════════════════════════════ */
    .muni-error-bar {
      background: #fee2e2;
      color: #b91c1c;
      font-size: 12px;
      font-weight: 500;
      text-align: center;
      padding: 8px;
      display: none;
      flex-shrink: 0;
    }

    .muni-error-bar.show { display: block; }

    /* ══════════════════════════════════════════════════════════
       ÁREA DE MENSAJES
       ══════════════════════════════════════════════════════════ */
    .muni-messages {
      flex: 1;
      overflow-y: auto;
      padding: 20px 16px;
      display: flex;
      flex-direction: column;
      gap: 12px;
      background: ${COLORS.background};
      scroll-behavior: smooth;
    }

    .muni-messages::-webkit-scrollbar { width: 5px; }
    .muni-messages::-webkit-scrollbar-track { background: transparent; }
    .muni-messages::-webkit-scrollbar-thumb {
      background: rgba(61, 125, 174, 0.25);
      border-radius: 5px;
    }

    .muni-msg {
      display: flex;
      max-width: 85%;
      animation: muni-fadeIn 0.25s ease;
    }

    @keyframes muni-fadeIn {
      from { opacity: 0; transform: translateY(10px); }
      to   { opacity: 1; transform: translateY(0); }
    }

    .muni-msg.bot  { align-self: flex-start; }
    .muni-msg.user { align-self: flex-end; }

    .muni-msg-bubble {
      padding: 12px 16px;
      border-radius: 16px;
      font-size: 14px;
      line-height: 1.5;
      word-break: break-word;
    }

    /* Bot: azul */
    .muni-msg.bot .muni-msg-bubble {
      background: ${COLORS.botBubble};
      color: ${COLORS.white};
      border-bottom-left-radius: 4px;
    }

    /* Usuario: verde - claramente diferente */
    .muni-msg.user .muni-msg-bubble {
      background: ${COLORS.userBubble};
      color: ${COLORS.white};
      border-bottom-right-radius: 4px;
    }

    /* ══════════════════════════════════════════════════════════
       INDICADOR DE ESCRITURA
       ══════════════════════════════════════════════════════════ */
    .muni-typing {
      display: flex;
      align-items: center;
      gap: 5px;
      padding: 12px 16px;
      background: ${COLORS.botBubble};
      border-radius: 16px;
      border-bottom-left-radius: 4px;
      width: fit-content;
    }

    .muni-typing span {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: rgba(255,255,255,0.7);
      animation: muni-bounce 1.2s infinite ease-in-out;
    }

    .muni-typing span:nth-child(1) { animation-delay: -0.32s; }
    .muni-typing span:nth-child(2) { animation-delay: -0.16s; }
    .muni-typing span:nth-child(3) { animation-delay: 0s; }

    @keyframes muni-bounce {
      0%, 80%, 100% { transform: scale(0.6); opacity: 0.4; }
      40%           { transform: scale(1);   opacity: 1; }
    }

    /* ══════════════════════════════════════════════════════════
       ÁREA DE INPUT
       ══════════════════════════════════════════════════════════ */
    .muni-input-area {
      padding: 16px;
      background: ${COLORS.white};
      border-top: 1px solid #e8edf2;
      display: flex;
      align-items: flex-end;
      gap: 12px;
      flex-shrink: 0;
    }

    .muni-input-wrapper {
      flex: 1;
      position: relative;
      display: flex;
      align-items: center;
      background: #f5f7fa;
      border: 1.5px solid #e0e6ed;
      border-radius: 24px;
      transition: border-color 0.2s, background 0.2s;
    }

    .muni-input-wrapper:focus-within {
      border-color: ${COLORS.primary};
      background: ${COLORS.white};
    }

    .muni-input {
      flex: 1;
      border: none;
      padding: 12px 16px;
      font-size: 14px;
      color: ${COLORS.text};
      outline: none;
      resize: none;
      max-height: 100px;
      line-height: 1.4;
      background: transparent;
      font-family: 'Inter', sans-serif;
    }

    .muni-input::placeholder { 
      color: #9ca3af; 
    }

    .muni-input-icons {
      display: flex;
      align-items: center;
      gap: 4px;
      padding-right: 12px;
    }

    .muni-input-icon {
      width: 32px;
      height: 32px;
      border: none;
      background: transparent;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 50%;
      transition: background 0.2s;
    }

    .muni-input-icon:hover {
      background: rgba(61, 125, 174, 0.1);
    }

    .muni-input-icon svg {
      width: 20px;
      height: 20px;
      fill: #9ca3af;
    }

    .muni-send-btn {
      width: 48px;
      height: 48px;
      border-radius: 50%;
      background: ${COLORS.primary};
      border: none;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
      transition: transform 0.2s, background 0.2s, box-shadow 0.2s;
      box-shadow: 0 4px 12px rgba(61, 125, 174, 0.3);
    }

    .muni-send-btn:hover {
      transform: scale(1.05);
      background: ${COLORS.primaryDark};
      box-shadow: 0 6px 16px rgba(61, 125, 174, 0.4);
    }

    .muni-send-btn:active { 
      transform: scale(0.95); 
    }

    .muni-send-btn:disabled {
      background: #ccd5dc;
      box-shadow: none;
      cursor: not-allowed;
      transform: none;
    }

    .muni-send-btn svg {
      width: 22px;
      height: 22px;
      fill: ${COLORS.white};
      margin-left: 2px;
    }

    /* ══════════════════════════════════════════════════════════
       RESPONSIVE
       ══════════════════════════════════════════════════════════ */
    @media (max-width: 450px) {
      .muni-window {
        width: calc(100vw - 16px);
        height: calc(100vh - 100px);
        max-height: 600px;
        bottom: 80px;
        right: 8px;
        border-radius: 16px;
      }
      .muni-bubble {
        bottom: 16px;
        right: 16px;
        width: 44px;
        height: 44px;
      }
      .muni-bubble-icon {
        width: 22px;
        height: 22px;
      }
    }
  `;

  // ============================================================
  // INICIALIZACIÓN
  // ============================================================
  function initWidget() {
    const styleEl = document.createElement("style");
    styleEl.textContent = styles;
    document.head.appendChild(styleEl);

    // Construir el contenido del logo según si hay URL configurada
    const logoContent =
      CONFIG.logoUrl && CONFIG.logoUrl !== "URL_DE_TU_LOGO_AQUI"
        ? `<img src="${CONFIG.logoUrl}" alt="Logo" />`
        : `<svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/></svg>`;

    const wrapper = document.createElement("div");
    wrapper.className = "muni-widget";
    wrapper.innerHTML = `
      <div class="muni-window" id="muniWindow">
        <div class="muni-header">
          <div class="muni-header-logo">
            ${logoContent}
          </div>
          <div class="muni-header-info">
            <div class="muni-header-name">${CONFIG.botName}</div>
            <div class="muni-header-status">
              <div class="muni-status-dot"></div>
              <span class="muni-status-text">${CONFIG.botStatus}</span>
            </div>
          </div>
          <div class="muni-header-actions">
            <button class="muni-header-btn" id="muniMinimize" title="Minimizar">─</button>
            <button class="muni-header-btn" id="muniClose" title="Cerrar">✕</button>
          </div>
        </div>

        <div class="muni-error-bar" id="muniErrorBar">
          Sin conexión. Reintentando...
        </div>

        <div class="muni-messages" id="muniMessages"></div>

        <div class="muni-input-area">
          <div class="muni-input-wrapper">
            <textarea
              class="muni-input"
              id="muniInput"
              placeholder="${CONFIG.placeholder}"
              rows="1"
              maxlength="${CONFIG.maxMessageLength}"
            ></textarea>
  
          </div>
          <button class="muni-send-btn" id="muniSend" title="Enviar" disabled>
            <svg viewBox="0 0 24 24"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/></svg>
          </button>
        </div>
      </div>

      <button class="muni-bubble" id="muniBubble" title="Abrir asistente">
        <svg class="muni-bubble-icon" viewBox="0 0 24 24">
          <path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H6l-2 2V4h16v12z"/>
        </svg>
      </button>
    `;
    document.body.appendChild(wrapper);
    initFunctionality();
  }

  // ============================================================
  // FUNCIONALIDAD
  // ============================================================
  function initFunctionality() {
    const bubble = document.getElementById("muniBubble");
    const window_ = document.getElementById("muniWindow");
    const messages = document.getElementById("muniMessages");
    const input = document.getElementById("muniInput");
    const sendBtn = document.getElementById("muniSend");
    const closeBtn = document.getElementById("muniClose");
    const minimizeBtn = document.getElementById("muniMinimize");
    const errorBar = document.getElementById("muniErrorBar");

    let ws = null;
    let isOpen = false;
    let typingEl = null;
    let reconnectAttempts = 0;
    let reconnectTimer = null;
    let welcomeShown = false;

    // ── Abrir / cerrar ──────────────────────────────────────
    function openChat() {
      isOpen = true;
      window_.classList.add("open");
      bubble.innerHTML = `<svg class="muni-bubble-icon" viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>`;
      if (!ws || ws.readyState !== WebSocket.OPEN) connectWS();
      setTimeout(() => input.focus(), 300);
    }

    function closeChat() {
      isOpen = false;
      window_.classList.remove("open");
      bubble.innerHTML = `<svg class="muni-bubble-icon" viewBox="0 0 24 24"><path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H6l-2 2V4h16v12z"/></svg>`;
    }

    function toggleChat() {
      if (isOpen) closeChat();
      else openChat();
    }

    bubble.addEventListener("click", toggleChat);
    closeBtn.addEventListener("click", closeChat);
    minimizeBtn.addEventListener("click", closeChat);

    // ── WebSocket ────────────────────────────────────────────
    function connectWS() {
      if (reconnectTimer) clearTimeout(reconnectTimer);
      try {
        ws = new WebSocket(CONFIG.wsUrl);

        ws.onopen = () => {
          reconnectAttempts = 0;
          setError(false);
          sendBtn.disabled = false;
          if (!welcomeShown) {
            addMessage(CONFIG.welcomeMessage, "bot");
            welcomeShown = true;
          }
        };

        ws.onmessage = (event) => {
          hideTyping();
          try {
            const data = JSON.parse(event.data);
            if (data.response) addMessage(data.response, "bot");
            else if (data.error)
              addMessage("Ocurrió un error. Intenta nuevamente.", "bot");
          } catch {
            addMessage(event.data, "bot");
          }
        };

        ws.onerror = () => {
          hideTyping();
          setError(true);
          sendBtn.disabled = true;
        };

        ws.onclose = () => {
          ws = null;
          sendBtn.disabled = true;
          if (reconnectAttempts < CONFIG.maxReconnectAttempts) {
            reconnectAttempts++;
            setError(true);
            reconnectTimer = setTimeout(connectWS, CONFIG.reconnectDelay);
          } else {
            errorBar.textContent = "No se pudo conectar. Recarga la página.";
            setError(true);
          }
        };
      } catch {
        setError(true);
      }
    }

    // ── Mensajes ─────────────────────────────────────────────
    function addMessage(text, sender) {
      const msg = document.createElement("div");
      msg.className = `muni-msg ${sender}`;
      msg.innerHTML = `<div class="muni-msg-bubble">${escapeHtml(text)}</div>`;
      messages.appendChild(msg);
      scrollBottom();
    }

    function showTyping() {
      if (typingEl) return;
      typingEl = document.createElement("div");
      typingEl.className = "muni-msg bot";
      typingEl.innerHTML = `<div class="muni-typing"><span></span><span></span><span></span></div>`;
      messages.appendChild(typingEl);
      scrollBottom();
    }

    function hideTyping() {
      if (typingEl) {
        typingEl.remove();
        typingEl = null;
      }
    }

    function scrollBottom() {
      setTimeout(() => {
        messages.scrollTop = messages.scrollHeight;
      }, 50);
    }

    // ── Enviar ───────────────────────────────────────────────
    function sendMessage() {
      const text = input.value.trim();
      if (!text) return;
      if (!ws || ws.readyState !== WebSocket.OPEN) {
        addMessage(
          "Sin conexión. Espera un momento e intenta de nuevo.",
          "bot",
        );
        return;
      }
      addMessage(text, "user");
      input.value = "";
      input.style.height = "auto";
      showTyping();
      try {
        ws.send(text);
      } catch {
        hideTyping();
        addMessage("Error al enviar. Intenta de nuevo.", "bot");
      }
    }

    sendBtn.addEventListener("click", sendMessage);

    input.addEventListener("keydown", (e) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
      }
    });

    input.addEventListener("input", () => {
      input.style.height = "auto";
      input.style.height = Math.min(input.scrollHeight, 90) + "px";
    });

    // ── Utilidades ───────────────────────────────────────────
    function setError(show) {
      errorBar.classList.toggle("show", show);
    }

    function escapeHtml(text) {
      const div = document.createElement("div");
      div.textContent = text;
      return div.innerHTML.replace(/\n/g, "<br>");
    }
  }

  // ── Arrancar cuando el DOM esté listo ────────────────────
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initWidget);
  } else {
    initWidget();
  }
})();
