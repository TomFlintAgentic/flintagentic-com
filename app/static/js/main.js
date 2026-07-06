(function () {
  const form = document.getElementById("chatForm");
  const input = document.getElementById("chatInput");
  const sendBtn = document.getElementById("chatSend");
  const messagesEl = document.getElementById("chatMessages");

  const history = [];

  function appendMessage(role, content) {
    const bubble = document.createElement("div");
    bubble.className = "chat-message " + role;
    bubble.textContent = content;
    messagesEl.appendChild(bubble);
    messagesEl.scrollTop = messagesEl.scrollHeight;
    return bubble;
  }

  form.addEventListener("submit", async function (e) {
    e.preventDefault();
    const message = input.value.trim();
    if (!message) return;

    appendMessage("user", message);
    input.value = "";
    sendBtn.disabled = true;

    const pending = appendMessage("assistant pending", "Thinking...");

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: message, history: history }),
      });

      if (!res.ok) throw new Error("request failed");

      const data = await res.json();
      pending.textContent = data.reply;
      pending.classList.remove("pending");

      history.push({ role: "user", content: message });
      history.push({ role: "assistant", content: data.reply });
    } catch (err) {
      pending.textContent = "Sorry, something went wrong. Please try again or email tom@flintagentic.co.uk.";
      pending.classList.remove("pending");
    } finally {
      sendBtn.disabled = false;
      input.focus();
    }
  });
})();
