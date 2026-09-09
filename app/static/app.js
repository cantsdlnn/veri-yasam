const roleHeaders = { "X-Demo-Role": "admin" };
const state = { due: [], assets: [] };
const today = new Date().toISOString().slice(0, 10);
document.querySelector('[name="collected_on"]').value = today;

async function request(url, options = {}) {
  const response = await fetch(url, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...roleHeaders,
      ...(options.headers || {}),
    },
  });
  if (!response.ok) {
    const body = await response.json().catch(() => ({ detail: "Beklenmeyen hata" }));
    throw new Error(body.detail || "İşlem tamamlanamadı.");
  }
  return response.json();
}

function statusLabel(status) {
  return {
    active: "Aktif",
    review_due: "İnceleme gerekli",
    anonymized: "Anonimleştirildi",
    deleted: "Silindi",
  }[status] || status;
}

function renderAssets() {
  const table = document.querySelector("#asset-table");
  table.replaceChildren();
  for (const asset of state.assets) {
    const row = document.createElement("tr");
    row.innerHTML =
      "<td><strong></strong><br><small></small></td>" +
      "<td></td><td></td><td><span class='status'></span></td>";
    row.querySelector("strong").textContent = asset.record_name;
    row.querySelector("small").textContent = asset.data_category;
    row.children[1].textContent = asset.purpose;
    row.children[2].textContent = asset.expires_on;
    const status = row.querySelector(".status");
    status.textContent = statusLabel(asset.status);
    status.classList.add(asset.status);
    table.appendChild(row);
  }
  document.querySelector("#asset-count").textContent = state.assets.length + " kayıt";
}

function renderDue() {
  const list = document.querySelector("#due-list");
  list.replaceChildren();
  if (!state.due.length) {
    const empty = document.createElement("p");
    empty.textContent = "Bugün için insan kararı bekleyen kayıt yok.";
    list.appendChild(empty);
    return;
  }
  for (const item of state.due) {
    const card = document.createElement("article");
    card.className = "due-card";
    const title = document.createElement("h3");
    title.textContent = item.record_name;
    const reason = document.createElement("p");
    reason.textContent = item.reason;
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = "Karar ver";
    button.addEventListener("click", () => openDecision(item));
    card.append(title, reason, button);
    list.appendChild(card);
  }
}

async function load() {
  try {
    const [assets, due, chain] = await Promise.all([
      request("/api/assets"),
      request("/api/retention/due"),
      request("/api/audit/verify"),
    ]);
    state.assets = assets;
    state.due = due;
    renderAssets();
    renderDue();
    const indicator = document.querySelector("#chain-indicator");
    indicator.classList.toggle("valid", chain.valid);
    document.querySelector("#chain-status").textContent = chain.valid
      ? "Denetim zinciri doğrulandı"
      : "Denetim zinciri bozuk";
    document.querySelector("#chain-count").textContent = chain.event_count + " olay";
  } catch (error) {
    document.querySelector("#due-list").textContent = error.message;
  }
}

function openDecision(item) {
  const dialog = document.querySelector("#decision-dialog");
  const form = document.querySelector("#decision-form");
  form.elements.asset_id.value = item.asset_id;
  document.querySelector("#decision-record").textContent = item.record_name + " — " + item.reason;
  dialog.showModal();
}

document.querySelector("#asset-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  const data = Object.fromEntries(new FormData(form));
  data.retention_days = Number(data.retention_days);
  const message = document.querySelector("#form-message");
  try {
    await request("/api/assets", { method: "POST", body: JSON.stringify(data) });
    message.textContent = "Kayıt ve denetim olayı oluşturuldu.";
    await load();
  } catch (error) {
    message.textContent = error.message;
  }
});

document.querySelector("#decision-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  const data = Object.fromEntries(new FormData(form));
  const assetId = data.asset_id;
  delete data.asset_id;
  try {
    await request("/api/assets/" + assetId + "/decision", {
      method: "POST",
      body: JSON.stringify(data),
    });
    document.querySelector("#decision-dialog").close();
    form.elements.reason.value = "";
    await load();
  } catch (error) {
    document.querySelector("#decision-record").textContent = error.message;
  }
});

document.querySelector("#cancel-decision").addEventListener("click", () => {
  document.querySelector("#decision-dialog").close();
});
document.querySelector("#refresh-button").addEventListener("click", load);
load();
