// ANTIGRAVITY 2.0 SHELL CONTROLLER & EVENT BRIDGE

// Defensive anti-crash fallbacks for i18n
if (typeof window.t !== 'function') {
  window.t = function(key, params) {
    let text = String(key || '');
    if (params && typeof params === 'object') {
      for (const [k, v] of Object.entries(params)) {
        text = text.replace(new RegExp('\\{' + k + '\\}', 'g'), v);
      }
    }
    return text;
  };
}
if (typeof window.setLanguage !== 'function') {
  window.setLanguage = function() {};
}


let currentAuditData = null;

let appSettings = {};

document.addEventListener("DOMContentLoaded", async () => {

  initEventListeners();

  await loadSettings();

  await checkActiveAuditOnLoad();

});

async function checkActiveAuditOnLoad() {

  try {

    const res = await fetch("/api/audit-status");

    const st = await res.json();

    if (st.success && st.state === "running") {

      const target = st.target_dir || "";

      const targetInput = document.getElementById("targetFolderInput");

      if (targetInput && target) targetInput.value = target;

      showInstallerProgressView(target);

      for (const item of st.logs || []) {

        addInstallerLog(item.text, item.type || "info");

      }

      if (Array.isArray(st.plan) && st.plan.length > 0) {

        renderDynamicSegments(st.plan, true);

        applyScanProgress(st.plan, st.current);

      }

      const pct = Math.min(99, Math.max(1, Math.round(st.pct)));

      const secs = Math.floor(st.elapsed || 0);

      setOverallProgress(pct, `${st.message} (${secs}s)`, `${pct}%`);

      pollAuditProgress(st.job_id || "", st.next || 0);

    }

  } catch (e) {

    // do not block the page load if the connection fails

  }

}

function initEventListeners() {

  // Theme Toggle

  const themeToggleBtn = document.getElementById("themeToggleBtn");

  if (themeToggleBtn) themeToggleBtn.addEventListener("click", toggleTheme);

  document.querySelectorAll(".theme-card").forEach(card => {

    card.addEventListener("click", () => {

      const val = card.dataset.themeValue;

      if (val) applyThemeValue(val);

    });

  });

  // Settings Modal

  document.getElementById("settingsBtn").addEventListener("click", openSettingsModal);

  document.getElementById("closeSettingsBtn").addEventListener("click", closeSettingsModal);

  document.getElementById("cancelSettingsBtn").addEventListener("click", closeSettingsModal);

  document.getElementById("saveSettingsBtn").addEventListener("click", saveSettingsFromModal);

  // Update Modal

  document.getElementById("updateBtn").addEventListener("click", checkUpdate);

  document.getElementById("closeUpdateBtn").addEventListener("click", () => closeModal("updateModal"));

  document.getElementById("okUpdateBtn").addEventListener("click", () => closeModal("updateModal"));

  // Folder Select & Audit

  document.getElementById("browseFolderBtn").addEventListener("click", selectFolderNative);

  document.getElementById("runAuditBtn").addEventListener("click", runBenchmark);

  const topAIBtn = document.getElementById("topAIDeepReviewBtn");

  if (topAIBtn) {

    topAIBtn.addEventListener("click", handleTopAIDeepReview);

  }

  // Copy Prompt

  document.getElementById("copyPromptBtn").addEventListener("click", copyAiPrompt);

  // View Report from Installer view

  const viewReportBtn = document.getElementById("viewReportNowBtn");

  if (viewReportBtn) {

    viewReportBtn.addEventListener("click", hideInstallerProgressView);

  }

  // Footer Actions

  const openRep = document.getElementById("openReportBtn");

  if (openRep) openRep.addEventListener("click", openReportFile);

  const openFld = document.getElementById("openFolderBtn");

  if (openFld) openFld.addEventListener("click", openTargetFolder);

  const copyRepPath = document.getElementById("copyReportPathBtn");

  if (copyRepPath) copyRepPath.addEventListener("click", copyReportPath);

  // AI Deep Review

  document.getElementById("triggerLLMBtn").addEventListener("click", triggerLLMReview);

  // Tabs

  document.querySelectorAll(".tab-btn").forEach(btn => {

    btn.addEventListener("click", () => {

      document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));

      document.querySelectorAll(".tab-panel").forEach(p => p.classList.remove("active"));

      btn.classList.add("active");

      const targetPanel = document.getElementById(btn.dataset.tab);

      if (targetPanel) targetPanel.classList.add("active");

      // Sync the sidebar state when switching tabs

      if (btn.dataset.tab === "tab-overview") {

        document.querySelectorAll(".pillar-item").forEach(i => i.classList.remove("active"));

        const overviewItem = document.querySelector('.pillar-item[data-pillar="overview"]');

        if (overviewItem) overviewItem.classList.add("active");

        const pillarTabBtn = document.getElementById("tabBtnPillar");

        if (pillarTabBtn) pillarTabBtn.style.display = "none";

      }

    });

  });

  // Pillar click

  document.querySelectorAll(".pillar-item").forEach(item => {

    item.addEventListener("click", () => {

      document.querySelectorAll(".pillar-item").forEach(i => i.classList.remove("active"));

      item.classList.add("active");

      handlePillarSelection(item.dataset.pillar);

    });

  });

}

// -------------------------------------------------------------

// SETTINGS & THEMES

// -------------------------------------------------------------

async function loadSettings() {

  try {

    const res = await fetch("/api/settings");

    appSettings = await res.json();

    // Apply the theme

    const theme = appSettings.theme || "dark";

    applyThemeValue(theme);

    // Interface language (English by default)

    const lang = appSettings.language === "vi" ? "vi" : "en";

    setLanguage(lang);

    document.getElementById("settingsLanguageSelect").value = lang;

    loadAboutVersion();

    // Update the most recent folder

    if (appSettings.last_target_directory) {

      document.getElementById("targetFolderInput").value = appSettings.last_target_directory;

    }

    // Update the LLM config

    document.getElementById("settingsLLMProvider").value = appSettings.llm_provider || "gemini";

    document.getElementById("settingsIncludeCode").checked = !!appSettings.include_code;

    updateApiKeyInputForProvider(appSettings.llm_provider || "gemini");

    document.getElementById("settingsModelInput").value = appSettings.selected_model || "gemini-2.0-flash";

    // Update the light/dark state of the AI Deep Review button on the Toolbar

    updateAIButtonState();

  } catch (e) {

    console.error("Failed to load settings:", e);

  }

}

const THEME_META_COLORS = {

  "dark": "#0e0d13",

  "light": "#ffffff",

  "midnight": "#000000",

  "dracula": "#141220",

  "tokyo-night": "#13131a",

  "nord": "#1b1e26",

  "emerald": "#06120e",

  "sepia": "#f4ecd8"

};

function applyThemeValue(theme) {

  const chosen = theme || "dark";

  document.documentElement.setAttribute("data-theme", chosen);

  const meta = document.querySelector('meta[name="theme-color"]');

  if (meta) {

    meta.setAttribute("content", THEME_META_COLORS[chosen] || "#0e0d13");

  }

  const sel = document.getElementById("settingsThemeSelect");

  if (sel && sel.value !== chosen) {

    sel.value = chosen;

  }

  document.querySelectorAll(".theme-card").forEach(card => {

    card.classList.toggle("active", card.dataset.themeValue === chosen);

  });

}

function toggleTheme() {

  const current = document.documentElement.getAttribute("data-theme") || "dark";

  const isLight = current === "light" || current === "sepia";

  const next = isLight ? "dark" : "light";

  applyThemeValue(next);

  appSettings.theme = next;

  fetch("/api/settings", {

    method: "POST",

    headers: { "Content-Type": "application/json" },

    body: JSON.stringify({ theme: next })

  });

}

let settingsSnapshot = null;

// Switch language everywhere, including already-rendered audit results.

function applyLanguage(lang) {

  if (currentLang() === lang) return;

  setLanguage(lang);

  updateAIButtonState();

  updateApiKeyInputForProvider(document.getElementById("settingsLLMProvider").value);

  if (currentAuditData) renderAuditResults(currentAuditData);

}

function showSettingsSection(name) {

  document.querySelectorAll("#settingsNav .settings-nav-item").forEach(b =>

    b.classList.toggle("active", b.dataset.section === name));

  document.querySelectorAll(".settings-section").forEach(sec =>

    sec.classList.toggle("active", sec.id === `settings-${name}`));

}

async function loadAboutVersion() {

  const el = document.getElementById("aboutVersion");

  if (!el) return;

  try {

    const res = await fetch("/api/status");

    const data = await res.json();

    el.textContent = data.version ? `v${data.version}` : t("Unknown");

  } catch (e) {

    el.textContent = t("Unknown");

  }

}

function openSettingsModal() {

  settingsSnapshot = { theme: document.documentElement.getAttribute("data-theme") || "dark", language: currentLang() };

  applyThemeValue(settingsSnapshot.theme);

  document.getElementById("settingsLanguageSelect").value = settingsSnapshot.language;

  document.getElementById("settingsModal").classList.add("open");

  const provider = document.getElementById("settingsLLMProvider").value;

  updateApiKeyInputForProvider(provider);

  refreshConnectivity();

}

// Pass true after a successful save; any other call (Cancel, X) reverts the live previews.

function closeSettingsModal(keep) {

  if (keep !== true && settingsSnapshot) {

    applyThemeValue(settingsSnapshot.theme);

    applyLanguage(settingsSnapshot.language);

  }

  settingsSnapshot = null;

  document.getElementById("settingsModal").classList.remove("open");

}

document.querySelectorAll("#settingsNav .settings-nav-item").forEach(b =>

  b.addEventListener("click", () => showSettingsSection(b.dataset.section)));

document.getElementById("settingsThemeSelect").addEventListener("change", (e) => applyThemeValue(e.target.value));

document.getElementById("settingsLanguageSelect").addEventListener("change", (e) => applyLanguage(e.target.value));

document.getElementById("aboutCheckUpdateBtn").addEventListener("click", () => checkUpdate());

function closeModal(modalId) {

  document.getElementById(modalId).classList.remove("open");

}

function updateApiKeyInputForProvider(provider) {

  // The server never returns the API key to the UI; it only shows the saved status.

  const input = document.getElementById("settingsApiKeyInput");

  input.value = "";

  input.placeholder = appSettings[`has_${provider}_api_key`]

    ? t("•••••••• (saved — leave blank to keep)")

    : t("Enter API Key");

}

document.getElementById("settingsLLMProvider").addEventListener("change", (e) => {

  updateApiKeyInputForProvider(e.target.value);

  if (e.target.value === "gemini") {

    document.getElementById("settingsModelInput").value = "gemini-2.0-flash";

  } else if (e.target.value === "openai") {

    document.getElementById("settingsModelInput").value = "gpt-4o";

  } else if (e.target.value === "claude") {

    document.getElementById("settingsModelInput").value = "claude-sonnet-5-5";

  }

});

async function saveSettingsFromModal() {

  const theme = document.getElementById("settingsThemeSelect").value;

  const language = document.getElementById("settingsLanguageSelect").value;

  const provider = document.getElementById("settingsLLMProvider").value;

  const apiKey = document.getElementById("settingsApiKeyInput").value.trim();

  const model = document.getElementById("settingsModelInput").value.trim();

  const updates = {

    theme: theme,

    language: language,

    llm_provider: provider,

    selected_model: model,

    include_code: document.getElementById("settingsIncludeCode").checked

  };

  if (apiKey) updates[`${provider}_api_key`] = apiKey;

  try {

    const res = await fetch("/api/settings", {

      method: "POST",

      headers: { "Content-Type": "application/json" },

      body: JSON.stringify(updates)

    });

    const result = await res.json();

    if (result.success) {

      document.documentElement.setAttribute("data-theme", theme);

      appSettings = { ...appSettings, ...updates };

      if (apiKey) {

        appSettings[`has_${provider}_api_key`] = true;

        appSettings[`${provider}_api_key`] = "";

      }

      applyLanguage(language);

      updateAIButtonState();

      closeSettingsModal(true);

      setStatus(t("Settings saved."));

    } else {

      alert(t("Could not save settings: ") + result.message);

    }

  } catch (e) {

    alert(t("Connection error while saving settings: ") + e.message);

  }

}

// -------------------------------------------------------------

// AI REVIEW BUTTON CONTROLLER & REACTIVE BINDING

// -------------------------------------------------------------

function hasConfiguredApiKey() {

  if (!appSettings) return false;

  const currentProvider = appSettings.llm_provider || "gemini";

  if (appSettings[`has_${currentProvider}_api_key`]) return true;

  // Fallback: check whether any provider has a key

  return !!(appSettings.has_gemini_api_key || appSettings.has_openai_api_key || appSettings.has_claude_api_key);

}

function updateAIButtonState() {

  const aiBtn = document.getElementById("topAIDeepReviewBtn");

  if (!aiBtn) return;

  const hasKey = hasConfiguredApiKey();

  if (hasKey) {

    aiBtn.disabled = false;

    aiBtn.title = t("Run a deep architecture review with Senior Architect AI");

  } else {

    aiBtn.disabled = true;

    aiBtn.title = t("Configure an API Key in Settings (top right) to enable AI Review");

  }

}

async function handleTopAIDeepReview() {

  if (!hasConfiguredApiKey()) {

    openSettingsModal();

    alert(t("Enter an API Key in Settings > API Keys to enable AI Deep Review."));

    return;

  }

  const folder = document.getElementById("targetFolderInput").value.trim();

  if (!folder) {

    alert(t("Select a project folder before running a review."));

    return;

  }

  // If there is no standard audit data yet, automatically run Analytics first

  if (!currentAuditData) {

    setStatus(t("Running Analytics first to collect audit data for the AI..."));

    await runBenchmark();

    if (!currentAuditData) return;

  }

  // Switch to the dedicated AI Deep Review panel

  const progressView = document.getElementById("installerProgressView");

  const resultView = document.getElementById("auditResultView");

  const overviewBanner = document.getElementById("overviewMetricsBanner");

  const overviewTabs = document.getElementById("overviewTabsNav");

  if (progressView) progressView.style.display = "none";

  if (resultView) resultView.style.display = "flex";

  if (overviewBanner) overviewBanner.style.display = "none";

  if (overviewTabs) overviewTabs.style.display = "none";

  document.querySelectorAll(".pillar-item").forEach(i => i.classList.remove("active"));

  document.querySelectorAll(".tab-panel").forEach(p => p.classList.remove("active"));

  const aiDeepPanel = document.getElementById("tab-ai-deep");

  if (aiDeepPanel) aiDeepPanel.classList.add("active");

  // Trigger the deep AI analysis

  await triggerLLMReview();

}

// -------------------------------------------------------------

// INSTALLATION-STYLE PROGRESS & LOG CONTROLLER

// -------------------------------------------------------------

let installerTimer = null;

let autoSwitchTimer = null;

function getTimestamp() {

  const now = new Date();

  return `[${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}:${String(now.getSeconds()).padStart(2, '0')}]`;

}

function addInstallerLog(message, type = 'info') {

  const feed = document.getElementById("installerLogFeed");

  if (!feed) return;

  const line = document.createElement("div");

  line.className = `log-line log-${type}`;

  const match = String(message || "").match(/^(\[\d{2}:\d{2}:\d{2}\])\s*(.*)$/);
  let timeStr = "";
  let bodyStr = String(message || "");
  if (match) {
    timeStr = match[1];
    bodyStr = match[2];
  } else {
    timeStr = getTimestamp();
  }
  const translated = window.t ? window.t(bodyStr) : bodyStr;
  line.textContent = `${timeStr} ${translated}`;

  feed.appendChild(line);

  feed.scrollTop = feed.scrollHeight;

}

function renderDynamicSegments(activePillars, planned = false) {

  const container = document.getElementById("installerSegmentsContainer");

  const labelEl = document.getElementById("segmentedBarLabel");

  if (!container) return;

  const count = Array.isArray(activePillars) ? activePillars.length : 0;

  if (labelEl) {

    labelEl.textContent = t("Audit stages ({count} pillars)", { count });

  }

  container.innerHTML = "";

  if (Array.isArray(activePillars)) {

    activePillars.forEach((p, idx) => {

      const stepEl = document.createElement("div");

      stepEl.className = "segment-step pending";

      stepEl.id = `seg_${p.key}`;

      stepEl.innerHTML = `

        <div class="segment-top">

          <span class="segment-num">${idx + 1}</span>

          <span class="segment-name" title="${escapeHtml(pillarName(p))}">${escapeHtml(pillarName(p))}</span>

        </div>

        <div class="segment-track"><div class="segment-fill"></div></div>

        <div class="segment-points">${planned ? t("not measured") : t("{n} pts", { n: p.max })}</div>

      `;

      container.appendChild(stepEl);

    });

  }

}

// Sidebar state per stage: not measured (N/A) -> measuring (waiting / measuring / measured) -> real score.

const SIDEBAR_NON_PILLAR = new Set(["overview", "report_prompt", "history"]);

// The engine reports pillar names in its own language; show a localized label by pillar key instead.

const PILLAR_NAMES = {

  readme: "Readme & Onboarding", backend: "Backend & Core Flow", frontend: "Frontend & UI/UX",

  database: "Database & Query Safety", security: "Security & Supply Chain",

  cloud: "Cloud Infrastructure & DevOps", microservices: "Distributed Systems & Gateway",

  data_caching: "Data Engineering & Cache", observability: "Monitoring & Operations",

  anticrash: "Runtime Anti-Crash", agent_ecosystem: "AI Agent Ecosystem",

  contracts: "Architecture Records & API Contracts"

};

function pillarName(p) {

  return PILLAR_NAMES[p.key] ? t(PILLAR_NAMES[p.key]) : p.name;

}

function setPillarLabel(key, text, dotClass, color) {

  const scoreEl = document.getElementById(`score_${key}`);

  const dotEl = document.getElementById(`dot_${key}`);

  if (scoreEl) {

    scoreEl.className = "pillar-score";

    scoreEl.textContent = text;

    scoreEl.style.color = color || "";

  }

  if (dotEl) dotEl.className = `status-dot ${dotClass}`;

}

function resetSidebarScores() {

  document.querySelectorAll("#pillarList .pillar-item").forEach(li => {

    const key = li.getAttribute("data-pillar");

    if (!key || SIDEBAR_NON_PILLAR.has(key)) return;

    li.classList.remove("pillar-disabled");

    setPillarLabel(key, "N/A", "dot-neutral", "");

  });

  const totalEl = document.getElementById("totalScore");

  if (totalEl) {

    totalEl.textContent = "--";

    totalEl.className = "score-number";

  }

}

function applyScanProgress(plan, current) {

  const keys = plan.map(p => p.key);

  const curIdx = keys.indexOf(current);

  // a current outside the plan (gap analysis, safety scan) means every category has been measured

  const doneUpTo = current == null ? 0 : (curIdx === -1 ? keys.length : curIdx);

  document.querySelectorAll("#pillarList .pillar-item").forEach(li => {

    const key = li.getAttribute("data-pillar");

    if (!key || SIDEBAR_NON_PILLAR.has(key)) return;

    const i = keys.indexOf(key);

    if (i === -1) {

      setPillarLabel(key, "N/A", "dot-neutral", "");

    } else if (i < doneUpTo) {

      setPillarLabel(key, t("Measured"), "dot-success", "");

      setSegmentStatus(key, "completed");

    } else if (i === doneUpTo && current != null && curIdx !== -1) {

      setPillarLabel(key, t("Measuring…"), "dot-warning", "#f59e0b");

      setSegmentStatus(key, "active");

    } else {

      setPillarLabel(key, t("Queued"), "dot-neutral", "");

      setSegmentStatus(key, "pending");

    }

  });

}

function setSegmentStatus(segKey, status) {

  const el = document.getElementById(`seg_${segKey}`);

  if (!el) return;

  el.classList.remove("pending", "active", "completed");

  el.classList.add(status);

}

function setOverallProgress(percent, statusMsg, stepBadge) {

  const pctEl = document.getElementById("installerPercent");

  const fillEl = document.getElementById("installerOverallFill");

  const msgEl = document.getElementById("installerStatusMessage");

  const badgeEl = document.getElementById("installerStepBadge");

  if (pctEl) pctEl.textContent = `${percent}%`;

  if (fillEl) fillEl.style.width = `${percent}%`;

  if (msgEl) msgEl.textContent = window.t ? window.t(statusMsg) : statusMsg;

  if (badgeEl) badgeEl.textContent = window.t ? window.t(stepBadge) : stepBadge;

}

function showInstallerProgressView(targetDir) {

  if (autoSwitchTimer) {

    clearTimeout(autoSwitchTimer);

    autoSwitchTimer = null;

  }

  if (installerTimer) clearInterval(installerTimer);

  const progressView = document.getElementById("installerProgressView");

  const resultView = document.getElementById("auditResultView");

  const targetDirEl = document.getElementById("installerTargetDir");

  const finishBox = document.getElementById("installerFinishBox");

  const logFeed = document.getElementById("installerLogFeed");

  const spinnerEl = document.getElementById("installerSpinner");

  const mainTitleEl = document.getElementById("installerMainTitle");

  if (progressView) progressView.style.display = "flex";

  if (resultView) resultView.style.display = "none";

  if (targetDirEl) targetDirEl.textContent = t("Project: {dir}", { dir: targetDir });

  if (finishBox) finishBox.style.display = "none";

  if (logFeed) logFeed.innerHTML = "";

  // Reset the spinner to its spinning state

  if (spinnerEl) spinnerEl.className = "installer-spinner";

  if (mainTitleEl) mainTitleEl.textContent = t("Auditing source architecture...");

  // Sync the sidebar: select the "history" item (Scan history)

  document.querySelectorAll(".pillar-item").forEach(i => {

    i.classList.toggle("active", i.getAttribute("data-pillar") === "history");

  });

  const dotHistory = document.getElementById("dot_history");

  const scoreHistory = document.getElementById("score_history");

  if (dotHistory) {

    dotHistory.className = "status-dot dot-warning";

  }

  if (scoreHistory) {

    scoreHistory.textContent = t("Scanning...");

    scoreHistory.style.color = "#f59e0b";

  }

  // Reset the container of audit stages: which categories will be measured is unknown until the project is identified

  const segContainer = document.getElementById("installerSegmentsContainer");

  if (segContainer) {

    segContainer.innerHTML = `<div class="segment-placeholder">${t("Detecting project architecture to decide which pillars to measure...")}</div>`;

  }

  const segLabel = document.getElementById("segmentedBarLabel");

  if (segLabel) segLabel.textContent = t("Audit stages");

  // Clear the previous scan's score: the system does not know any score until measurement ends

  currentAuditData = null;

  resetSidebarScores();

  setOverallProgress(0, t("Initializing audit modules..."), t("Starting"));

}

function hideInstallerProgressView() {

  if (autoSwitchTimer) {

    clearTimeout(autoSwitchTimer);

    autoSwitchTimer = null;

  }

  const progressView = document.getElementById("installerProgressView");

  const resultView = document.getElementById("auditResultView");

  if (progressView) progressView.style.display = "none";

  if (resultView) resultView.style.display = "flex";

  // Sync the sidebar state to OVERVIEW

  document.querySelectorAll(".pillar-item").forEach(i => {

    i.classList.toggle("active", i.getAttribute("data-pillar") === "overview");

  });

  handlePillarSelection("overview");

}

// -------------------------------------------------------------

// FOLDER PICKER & AUDIT EXECUTION

// -------------------------------------------------------------

window.onFolderSelected = function (folderPath) {

  if (folderPath) {

    document.getElementById("targetFolderInput").value = folderPath;

    setStatus(t("Folder selected: {path}", { path: folderPath }));

  }

};

async function selectFolderNative() {

  if (window.chrome && window.chrome.webview) {

    window.chrome.webview.postMessage("select-folder");

    return;

  }

  setStatus(t("Opening the Windows folder picker..."));

  try {

    const res = await fetch("/api/select-folder", {

      method: "POST",

      headers: { "Content-Type": "application/json" },

      body: JSON.stringify({ initial: document.getElementById("targetFolderInput").value })

    });

    const data = await res.json();

    if (data.folder) {

      onFolderSelected(data.folder);

    } else {

      setStatus(t("Folder selection cancelled."));

    }

  } catch (e) {

    setStatus(t("Could not open the folder picker: ") + e.message);

  }

}

async function runBenchmark() {

  const folder = document.getElementById("targetFolderInput").value.trim();

  if (!folder) {

    alert(t("Select the project folder to audit."));

    return;

  }

  const runBtn = document.getElementById("runAuditBtn");

  runBtn.disabled = true;

  runBtn.innerHTML = `<span>${t("Auditing...")}</span>`;

  setStatus(t("Measuring source architecture..."));

  // 1. Open the audit progress screen in an app-installer style

  showInstallerProgressView(folder);

  addInstallerLog(t("Starting the Universal Project Auditor engine..."), "info");

  addInstallerLog(t("Scanning configuration files at: {dir}", { dir: folder }), "muted");

  try {

    // Run in the background on the backend and ask for real progress: the log appears as soon as the engine writes it, with a seconds clock.

    const startRes = await fetch("/api/run-audit", {

      method: "POST",

      headers: { "Content-Type": "application/json" },

      body: JSON.stringify({ target_dir: folder, async: true })

    });

    const started = await startRes.json();

    if (!started.success) {

      addInstallerLog(t("Audit error: {msg}", { msg: started.error }), "error");

      setOverallProgress(100, t("Failed: {msg}", { msg: started.error }), t("ERROR"));

      alert(t("Analytics error: ") + started.error);

      setStatus(t("Audit failed."));

      runBtn.disabled = false;

      runBtn.innerHTML = `<svg width="11" height="11" viewBox="0 0 24 24" fill="currentColor"><polygon points="6 3 20 12 6 21 6 3"/></svg><span>Run Analytics</span>`;

      return;

    }

    await pollAuditProgress(started.job_id, 0);

  } catch (e) {

    if (installerTimer) clearInterval(installerTimer);

    installerTimer = null;

    addInstallerLog(t("Backend connection error: {msg}", { msg: e.message }), "error");

    setOverallProgress(100, t("Connection error: {msg}", { msg: e.message }), t("ERROR"));

    alert(t("Backend connection error: {msg}", { msg: e.message }));

    setStatus(t("Connection error."));

    runBtn.disabled = false;

    runBtn.innerHTML = `<svg width="11" height="11" viewBox="0 0 24 24" fill="currentColor"><polygon points="6 3 20 12 6 21 6 3"/></svg><span>Run Analytics</span>`;

  }

}

async function pollAuditProgress(jobId, initialSince = 0) {

  const runBtn = document.getElementById("runAuditBtn");

  if (runBtn) {

    runBtn.disabled = true;

    runBtn.innerHTML = `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> <span>${t("Checking...")}</span>`;

  }

  let since = initialSince;

  let data = null;

  let failures = 0;

  let planSig = "";

  try {

    while (!data) {

      await new Promise(r => setTimeout(r, 400));

      let st;

      try {

        st = await (await fetch(`/api/audit-status?job=${encodeURIComponent(jobId)}&since=${since}`)).json();

        failures = 0;

      } catch (e) {

        if (++failures >= 10) throw e;

        continue;

      }

      if (!st.success) throw new Error(st.error || t("Scan session lost."));

      for (const item of st.logs || []) {

        addInstallerLog(item.text, item.type || "info");

      }

      since = st.next;

      if (Array.isArray(st.plan) && st.plan.length > 0) {

        const sig = st.plan.map(p => p.key).join(",");

        if (sig !== planSig) {

          planSig = sig;

          renderDynamicSegments(st.plan, true);

        }

        applyScanProgress(st.plan, st.current);

      }

      if (st.state === "done") {

        data = st.result;

      } else {

        const pct = Math.min(99, Math.max(1, Math.round(st.pct)));

        const secs = Math.floor(st.elapsed || 0);

        setOverallProgress(pct, `${st.message} (${secs}s)`, `${pct}%`);

      }

    }

    if (!data.success) {

      addInstallerLog(t("Audit error: {msg}", { msg: data.error }), "error");

      setOverallProgress(100, t("Failed: {msg}", { msg: data.error }), t("ERROR"));

      alert(t("Analytics error: ") + data.error);

      setStatus(t("Audit failed."));

      if (runBtn) {

        runBtn.disabled = false;

        runBtn.innerHTML = `<svg width="11" height="11" viewBox="0 0 24 24" fill="currentColor"><polygon points="6 3 20 12 6 21 6 3"/></svg><span>Run Analytics</span>`;

      }

      return;

    }

    currentAuditData = data;

    renderDynamicSegments(data.active_pillars || []);

    if (Array.isArray(data.active_pillars)) {

      data.active_pillars.forEach(p => setSegmentStatus(p.key, "completed"));

    }

    setOverallProgress(100, t("✓ Audit complete! Total score: {score}/100", { score: data.total_score }), t("DONE 100%"));

    const spinnerEl = document.getElementById("installerSpinner");

    const mainTitleEl = document.getElementById("installerMainTitle");

    if (spinnerEl) spinnerEl.className = "installer-spinner spinner-done";

    if (mainTitleEl) mainTitleEl.textContent = t("Architecture audit finished ({score}/100)", { score: data.total_score });

    const dotHistory = document.getElementById("dot_history");

    const scoreHistory = document.getElementById("score_history");

    if (dotHistory) dotHistory.className = "status-dot dot-success";

    if (scoreHistory) {

      scoreHistory.textContent = t("Done");

      scoreHistory.style.color = "#10b981";

    }

    const finishBox = document.getElementById("installerFinishBox");

    if (finishBox) finishBox.style.display = "flex";

    const summaryEl = document.getElementById("finishScoreSummary");

    if (summaryEl) summaryEl.textContent = t("Audit complete! Total score: {score}/100 [Grade {grade}]", { score: data.total_score, grade: data.grade });

    renderAuditResults(data);

    setStatus(t("Analytics complete! Score: {score}/100.", { score: data.total_score }));

    if (runBtn) {

      runBtn.disabled = false;

      runBtn.innerHTML = `<svg width="11" height="11" viewBox="0 0 24 24" fill="currentColor"><polygon points="6 3 20 12 6 21 6 3"/></svg><span>Run Analytics</span>`;

    }

  } catch (e) {

    if (installerTimer) clearInterval(installerTimer);

    installerTimer = null;

    addInstallerLog(t("Backend connection error: {msg}", { msg: e.message }), "error");

    setOverallProgress(100, t("Connection error: {msg}", { msg: e.message }), t("ERROR"));

    alert(t("Backend connection error: {msg}", { msg: e.message }));

    setStatus(t("Connection error."));

    if (runBtn) {

      runBtn.disabled = false;

      runBtn.innerHTML = `<svg width="11" height="11" viewBox="0 0 24 24" fill="currentColor"><polygon points="6 3 20 12 6 21 6 3"/></svg><span>Run Analytics</span>`;

    }

  }

}

// -------------------------------------------------------------

// VIOLATION GROUPING CONTROLLER (GROUPING & FREQUENCY OF VIOLATIONS)

// -------------------------------------------------------------

function groupViolations(violations) {

  if (!violations || !Array.isArray(violations)) return [];

  const map = new Map();

  violations.forEach(v => {

    const key = v.type || "OTHER_VIOLATION";

    if (!map.has(key)) {

      map.set(key, {

        type: v.type || "UNKNOWN",

        desc: v.desc || t("Source code standard violation"),

        snippet: v.snippet || "",

        count: 0,

        locations: []

      });

    }

    const group = map.get(key);

    group.count += 1;

    group.locations.push({

      file: v.file,

      line: v.line,

      snippet: v.snippet

    });

    if (!group.snippet && v.snippet) {

      group.snippet = v.snippet;

    }

  });

  return Array.from(map.values()).sort((a, b) => b.count - a.count);

}

function renderGroupedViolations(violations, containerEl) {

  if (!containerEl) return;

  if (!violations || !Array.isArray(violations) || violations.length === 0) {

    containerEl.innerHTML = `<div style="color: #10b981; font-size: 13px; padding: 16px 0;">🎉 ${t("No source violations or Anti-Crash issues found.")}</div>`;

    return;

  }

  const groups = groupViolations(violations);

  const totalCount = violations.length;

  const groupCount = groups.length;

  let html = `

    <div class="violation-summary-bar">

      <span class="violation-summary-text">${t("Found")} <strong style="color: #ef4444;">${t("{n} violating locations", { n: totalCount })}</strong> (${t("across")} <span class="violation-type-count">${t("{n} standard architecture issue types", { n: groupCount })}</span>):</span>

    </div>

    <div class="violation-group-list">

  `;

  groups.forEach((g, gIdx) => {

    const pillLocations = g.locations.slice(0, 5);

    const hasMore = g.locations.length > 5;

    html += `

      <div class="violation-group-card">

        <div class="v-card-header">

          <div class="v-header-left">

            <span class="v-type-badge">${escapeHtml(g.type)}</span>

            <span class="v-frequency-badge">${t("{n} violating locations", { n: g.count })}</span>

          </div>

          ${g.locations.length > 1 ? `<button class="btn-toggle-locations" data-target="loc_${gIdx}_${containerEl.id}">${t("Details: {n} locations ▾", { n: g.count })}</button>` : ""}

        </div>

        <div class="v-desc">${escapeHtml(g.desc)}</div>

        ${g.snippet ? `<div class="v-snippet-box"><code>${escapeHtml(g.snippet)}</code></div>` : ""}

        <div class="v-locations-section">

          <div class="v-locations-pills">

            ${pillLocations.map(loc => `<span class="v-location-pill">${escapeHtml(loc.file)}:${loc.line}</span>`).join("")}

            ${hasMore ? `<span class="v-location-pill" style="color: var(--text-dim);">${t("+ {n} more locations", { n: g.locations.length - 5 })}</span>` : ""}

          </div>

          ${g.locations.length > 1 ? `

            <div class="v-full-locations-list" id="loc_${gIdx}_${containerEl.id}">

              ${g.locations.map(loc => `

                <div class="v-location-item">

                  <span style="color: var(--text-primary); font-weight: 500;">${escapeHtml(loc.file)}:${loc.line}</span>

                  ${loc.snippet ? `<span style="color: #f87171; max-width: 50%; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">${escapeHtml(loc.snippet)}</span>` : ""}

                </div>

              `).join("")}

            </div>

          ` : ""}

        </div>

      </div>

    `;

  });

  html += `</div>`;

  containerEl.innerHTML = html;

  containerEl.querySelectorAll(".btn-toggle-locations").forEach(btn => {

    btn.addEventListener("click", () => {

      const targetId = btn.getAttribute("data-target");

      const list = containerEl.querySelector(`#${targetId}`);

      if (list) {

        const isOpen = list.classList.toggle("open");

        const match = btn.textContent.match(/\d+/);

        const count = match ? match[0] : "";

        btn.textContent = isOpen ? t("Collapse list ▴") : t("Details: {n} locations ▾", { n: count });

      }

    });

  });

}

// -------------------------------------------------------------

// RENDER SECTION 2 (ACTIONABLE FINDINGS), SECTION 4 (BASELINE), SECTIONS 0 & 7 (SAFETY & SCOPE)

// -------------------------------------------------------------

const SEV_EN = { "High": "High", "Medium": "Medium", "Low": "Low" };

function sevLabel(sev) { return currentLang() === "vi" ? sev : (SEV_EN[sev] || sev); }

function getSeverityClass(sev) {

  if (sev === "High") return "sev-high";

  if (sev === "Medium") return "sev-medium";

  return "sev-low";

}

function renderFindingsTable(findings) {

  const container = document.getElementById("findingsTableContainer");

  const badge = document.getElementById("findingCountBadge");

  const list = Array.isArray(findings) ? findings : [];

  if (badge) {
    badge.textContent = list.length;
    badge.classList.toggle("has-items", list.length > 0);
  }

  if (!container) return;

  if (list.length === 0) {

    container.innerHTML = `<div style="color: #10b981; font-size: 13px; padding: 12px 0;">🎉 ${t("No findings to fix! The project meets every standard.")}</div>`;

    return;

  }

  const rowsHtml = list.map(f => {

    const docsList = Array.isArray(f?.docs) ? f.docs : [];

    const docsHtml = docsList.length > 0

      ? docsList.map(d => `<a href="${escapeHtml(d.url)}" target="_blank" rel="noopener noreferrer" class="doc-link" title="${escapeHtml(d.title)}">[${escapeHtml(d.id)}] ${escapeHtml(d.path)} ↗</a>`).join("<br>")

      : "—";

    const locHtml = f?.location ? `<code class="code-pill">${escapeHtml(f.location)}</code>` : "—";

    return `

      <tr>

        <td><span class="code-pill">${escapeHtml(f?.code ?? "GEN-001")}</span></td>

        <td><span class="sev-badge ${getSeverityClass(f?.severity)}">${escapeHtml(sevLabel(f?.severity ?? "Medium"))}</span></td>

        <td>${locHtml}</td>

        <td>${escapeHtml(t(f?.title ?? ""))}</td>

        <td>${docsHtml}</td>

      </tr>

    `;

  }).join("");

  container.innerHTML = `

    <div class="audit-table-wrapper">

      <table class="audit-table">

        <thead>

          <tr>

            <th>${t("Code")}</th>

            <th>${t("Severity")}</th>

            <th>${t("Location")}</th>

            <th>${t("Finding")}</th>

            <th>${t("Remediation doc (Kit)")}</th>

          </tr>

        </thead>

        <tbody>${rowsHtml}</tbody>

      </table>

    </div>

  `;

}

function renderBaselineTable(baseline) {

  const container = document.getElementById("baselineTableContainer");

  const badge = document.getElementById("baselineCountBadge");

  const list = Array.isArray(baseline) ? baseline : [];

  const passedCount = list.filter(b => b?.ok).length;

  if (badge) {
    badge.textContent = `${passedCount}/${list.length || 9}`;
    badge.classList.toggle("all-passed", passedCount === (list.length || 9));
  }

  if (!container) return;

  if (list.length === 0) {

    container.innerHTML = `<div class="muted-item">${t("No Core Baseline data yet.")}</div>`;

    return;

  }

  const rowsHtml = list.map(item => {

    const statusHtml = item?.ok

      ? `<span class="sev-badge sev-ok">✓ ${t("Pass")}</span>`

      : `<span class="sev-badge sev-high">✗ ${t("Fail")}</span> <span style="margin-left: 6px; color: #f87171;">${escapeHtml(t(item?.detail ?? ""))}</span>`;

    return `

      <tr>

        <td><span class="code-pill">${escapeHtml(item?.id ?? "")}</span></td>

        <td style="font-weight: 500; color: var(--text-primary);">${escapeHtml(t(item?.name ?? ""))}</td>

        <td>${statusHtml}</td>

      </tr>

    `;

  }).join("");

  container.innerHTML = `

    <div class="audit-table-wrapper">

      <table class="audit-table">

        <thead>

          <tr>

            <th style="width: 80px;">${t("Code")}</th>

            <th>${t("Core Baseline component")}</th>

            <th>${t("Check status")}</th>

          </tr>

        </thead>

        <tbody>${rowsHtml}</tbody>

      </table>

    </div>

  `;

}

function renderSafetyAndScope(safety, scope) {

  const safetyContainer = document.getElementById("safetyContainer");

  const scopeContainer = document.getElementById("scopeContainer");

  const safetyBadge = document.getElementById("safetyCountBadge");

  const safetyTitle = document.getElementById("safetySectionTitle");

  const safetyFindings = Array.isArray(safety?.findings) ? safety.findings : [];

  const totalFlags = safety?.total_findings ?? safetyFindings.length;

  if (safetyBadge) {
    if (totalFlags > 0) {
      safetyBadge.textContent = `⚠️ ${totalFlags}`;
      safetyBadge.classList.add("has-warning");
      safetyBadge.classList.remove("is-safe");
    } else {
      safetyBadge.textContent = t("Safe");
      safetyBadge.classList.remove("has-warning");
      safetyBadge.classList.add("is-safe");
    }
  }

  if (safetyContainer) {

    const scannedCount = safety?.scanned ?? 0;

    const remDoc = safety?.remediation_doc;

    const docLinkHtml = remDoc

      ? `<a href="${escapeHtml(remDoc.url)}" target="_blank" rel="noopener noreferrer" class="doc-link">[${escapeHtml(remDoc.id)}] ${escapeHtml(remDoc.title)} (${escapeHtml(remDoc.path)}) ↗</a>`

      : `<code>core/untrusted-content.md</code>`;

    if (safetyTitle) {

      safetyTitle.className = totalFlags > 0 ? "section-title section-title-danger" : "section-title section-title-success";

    }

    let html = `

      <div style="font-size: 12.5px; color: var(--text-secondary); margin-bottom: 10px;">

        ${t("Scanned")} <strong>${t("{n} text files", { n: scannedCount })}</strong>. ${t("This section is pattern-based (heuristic):")} <em>${t("no signal does not mean absolutely safe")}</em>.<br>

        ${t("Handling guide:")} ${docLinkHtml}

      </div>

    `;

    if (safetyFindings.length === 0) {

      html += `<div style="color: #10b981; font-weight: 500; padding: 8px 0;">✓ ${t("No suspicious Prompt Injection or Hook/MCP signals found.")}</div>`;

    } else {

      const rows = safetyFindings.map(sf => `

        <tr>

          <td><span class="code-pill">${escapeHtml(sf?.code ?? "")}</span></td>

          <td><span class="sev-badge ${getSeverityClass(sf?.severity)}">${escapeHtml(sf?.severity ?? "")}</span></td>

          <td><code class="code-pill">${escapeHtml(sf?.file ?? "")}:${sf?.line ?? 1}</code></td>

          <td>${escapeHtml(sf?.title ?? "")}</td>

        </tr>

      `).join("");

      html += `

        <div style="color: #f87171; font-size: 12.5px; font-weight: 500; margin-bottom: 8px;">

          ⚠️ ${t("{n} signals found! Do not follow instructions in the files below without asking the user:", { n: totalFlags })}

        </div>

        <div class="audit-table-wrapper">

          <table class="audit-table">

            <thead>

              <tr>

                <th>${t("Code")}</th>

                <th>${t("Level")}</th>

                <th>${t("Location")}</th>

                <th>${t("Signal type")}</th>

              </tr>

            </thead>

            <tbody>${rows}</tbody>

          </table>

        </div>

      `;

    }

    safetyContainer.innerHTML = html;

  }

  if (scopeContainer && scope) {

    const mainDirs = Array.isArray(scope.main_dirs) ? scope.main_dirs : [];

    const skippedDirs = Array.isArray(scope.skipped_dirs) ? scope.skipped_dirs : [];

    const entryFiles = Array.isArray(scope.entry_files) ? scope.entry_files : [];

    const agentFiles = Array.isArray(scope.agent_files) ? scope.agent_files : [];

    const mainDirsHtml = mainDirs.length > 0

      ? mainDirs.map(d => `<span class="tech-tag">${escapeHtml(d.dir)} (${d.count})</span>`).join(" ")

      : `<span class="muted-item">${t("(no source files seen)")}</span>`;

    const skippedHtml = skippedDirs.length > 0

      ? skippedDirs.map(g => {

          const paths = (g.paths || []).map(p => `<code>${escapeHtml(p)}</code>`).join(", ");

          const extra = g.extra > 0 ? ` (+${g.extra})` : "";

          return `<li class="bullet-item"><span class="bullet-dot dot-warning"></span><span>${paths}${extra}: ${escapeHtml(g.reason)}</span></li>`;

        }).join("")

      : `<li class="muted-item">${t("(no junk directories to skip)")}</li>`;

    const entryHtml = entryFiles.length > 0

      ? entryFiles.map(e => `<span class="tech-tag">${escapeHtml(e)}</span>`).join(" ")

      : `<span class="muted-item">${t("(none seen)")}</span>`;

    const agentHtml = agentFiles.length > 0

      ? agentFiles.map(a => `<span class="tech-tag">${escapeHtml(a)}</span>`).join(" ")

        + (scope.agent_files_extra > 0 ? ` <span class="tech-tag">+${scope.agent_files_extra}</span>` : "")

      : `<span class="muted-item">${t("(none yet)")}</span>`;

    scopeContainer.innerHTML = `

      <div style="font-size: 12.5px; color: var(--text-secondary);">

        ${t("Indexed")} <strong>${t("{n} files", { n: scope.scanned_total ?? 0 })}</strong> (${t("including")} <strong>${t("{n} source files", { n: scope.scanned_code ?? 0 })}</strong> ${t("and")} <strong>${t("{n} text files", { n: scope.scanned_safety ?? 0 })}</strong> ${t("scanned for safety")}).

      </div>

      <div class="scope-block">

        <div class="scope-block-title">${t("Main source directories:")}</div>

        <div class="tag-cloud">${mainDirsHtml}</div>

      </div>

      <div class="scope-block">

        <div class="scope-block-title">${t("Config / entry files to read first:")}</div>

        <div class="tag-cloud">${entryHtml}</div>

      </div>

      <div class="scope-block">

        <div class="scope-block-title">${t("Detected AI Agent instruction / config files:")}</div>

        <div class="tag-cloud">${agentHtml}</div>

      </div>

      <div class="scope-block">

        <div class="scope-block-title">${t("Automatically pruned directories (Agents should NOT re-read them, to save tokens):")}</div>

        <ul class="clean-bullet-list">${skippedHtml}</ul>

      </div>

    `;

  }

}

function renderAuditResults(data) {

  // 1. Total Score & score color (Red Alarm when a high-severity issue exists)

  const totalScoreEl = document.getElementById("totalScore");
  const alertContainer = document.getElementById("qualityGateAlertContainer");
  const hasCritical = Boolean(data.critical_count > 0 || data.quality_gate === "FAILED");

  if (totalScoreEl) {
    totalScoreEl.textContent = data.total_score;
    totalScoreEl.className = "score-number";
    if (hasCritical) {
      totalScoreEl.classList.add("score-danger");
    } else if (data.total_score >= 80) {
      totalScoreEl.classList.add("score-success");
    } else if (data.total_score >= 50) {
      totalScoreEl.classList.add("score-warning");
    } else {
      totalScoreEl.classList.add("score-danger");
    }
  }

  if (alertContainer) {
    if (hasCritical) {
      alertContainer.innerHTML = `
        <div class="quality-gate-alarm-badge" title="${t("Quality Gate Failed: Critical security or architecture issues detected")}">
          <span class="alarm-pulsing-dot"></span>
          <span>🚨 ${t("RED ALARM: {n} High-Severity Risk", { n: data.critical_count || 1 })}</span>
        </div>
      `;
    } else {
      alertContainer.innerHTML = `
        <div class="quality-gate-passed-badge" title="${t("Quality Gate Passed")}">
          <span>✓ ${t("Quality Gate Passed")}</span>
        </div>
      `;
    }
  }

  // 2. Metadata (with Profile & Guardrail info from .builder/kit.json)

  const archTypeEl = document.getElementById("metaArchetype");

  const archStyleEl = document.getElementById("metaArchStyle");

  if (archTypeEl) {

    const rawType = data.profiler?.archetype || t("Undetermined");

    archTypeEl.textContent = t(rawType);

    archTypeEl.setAttribute("title", t(rawType));

  }

  if (archStyleEl) {

    const rawStyle = data.profiler?.arch_style || t("Undetermined");

    const declaredProfile = data.kit_config?.declared_architecture;

    const guardrailLvl = data.kit_config?.guardrail_level;

    const kitRef = data.kit_config?.kit_ref;

    const profileSuffix = declaredProfile

      ? ` · Profile: ${declaredProfile}${guardrailLvl ? ` (${guardrailLvl})` : ""}${kitRef ? ` [${kitRef}]` : ""}`

      : "";

    const fullStyle = `${rawStyle}${profileSuffix}`;

    const translatedStyle = `${t(rawStyle)}${profileSuffix}`;

    archStyleEl.textContent = translatedStyle;

    archStyleEl.setAttribute("title", translatedStyle);

  }

  // 3. Render the dynamic sidebar pillars (always show all 12 standard categories)

  const pillarList = document.getElementById("pillarList");

  const sidebarTitle = document.getElementById("sidebarPillarsTitle") || document.querySelector(".sidebar-title");

  const pillarsToRender = (data.all_pillars && Array.isArray(data.all_pillars) && data.all_pillars.length > 0)

    ? data.all_pillars

    : (data.active_pillars || []);

  if (pillarList && pillarsToRender.length > 0) {

    if (sidebarTitle) {

      sidebarTitle.textContent = t("Audit pillars ({n})", { n: pillarsToRender.length });

    }

    pillarList.innerHTML = "";

    pillarsToRender.forEach(p => {

      const li = document.createElement("li");

      li.setAttribute("data-pillar", p.key);

      if (p.is_na) {

        li.className = "pillar-item pillar-disabled";

        li.setAttribute("title", t("This pillar does not apply to the current project structure"));

        li.innerHTML = `

          <div class="pillar-left">

            <span class="status-dot dot-neutral" id="dot_${p.key}"></span>

            <span class="pillar-name" style="color: var(--text-dim);">${escapeHtml(pillarName(p))}</span>

          </div>

          <span class="pillar-score pillar-score-na" id="score_${p.key}">N/A</span>

        `;

      } else {

        li.className = "pillar-item";

        let dotClass = "dot-neutral";

        let scoreClass = "";

        if (p.max > 0) {

          const ratio = p.score / p.max;

          if (ratio >= 0.8) {

            dotClass = "dot-success";

            scoreClass = "score-success";

          } else if (ratio >= 0.5) {

            dotClass = "dot-warning";

            scoreClass = "score-warning";

          } else {

            dotClass = "dot-danger";

            scoreClass = "score-danger";

          }

        }

        li.innerHTML = `

          <div class="pillar-left">

            <span class="status-dot ${dotClass}" id="dot_${p.key}"></span>

            <span class="pillar-name">${escapeHtml(pillarName(p))}</span>

          </div>

          <span class="pillar-score ${scoreClass}" id="score_${p.key}">${p.score} / ${p.max}</span>

        `;

        li.addEventListener("click", () => {

          document.querySelectorAll(".pillar-item").forEach(item => item.classList.remove("active"));

          li.classList.add("active");

          handlePillarSelection(p.key);

        });

      }

      pillarList.appendChild(li);

    });

  }

  // 4. Tech Stack Tags & Kit Ledger Tags

  const techCloud = document.getElementById("techStackTags");

  if (techCloud) {

    techCloud.innerHTML = "";

    const allTechs = [

      ...(data.profiler?.languages || []),

      ...(data.profiler?.frameworks || []),

      ...(data.profiler?.databases || []),

      ...(data.profiler?.tools || [])

    ];

    if (data.kit_config?.declared_architecture) {

      allTechs.push(`PROFILE: ${data.kit_config.declared_architecture.toUpperCase()}`);

    }

    if (data.kit_config?.guardrail_level) {

      allTechs.push(`GUARDRAIL: ${data.kit_config.guardrail_level}`);

    }

    if (allTechs.length === 0) {

      techCloud.innerHTML = `<span class="tech-tag">${t("No specific framework detected")}</span>`;

    } else {

      allTechs.forEach(t => {

        const tag = document.createElement("span");

        tag.className = "tech-tag";

        tag.textContent = t;

        techCloud.appendChild(tag);

      });

    }

  }

  // 5. Strengths

  const strList = document.getElementById("strengthList");

  if (strList) {

    strList.innerHTML = "";

    if (Array.isArray(data.strengths) && data.strengths.length > 0) {

      data.strengths.forEach(s => {

        const li = document.createElement("li");

        li.className = "bullet-item";

        li.innerHTML = `<span class="bullet-dot dot-success"></span><span>${escapeHtml(t(s))}</span>`;

        strList.appendChild(li);

      });

    } else {

      strList.innerHTML = `<li class="muted-item">${t("No standout strengths reached the standard yet.")}</li>`;

    }

  }

  // 6. Gaps & Bloat

  const gapsList = document.getElementById("gapsList");

  if (gapsList) {

    gapsList.innerHTML = "";

    if (Array.isArray(data.gaps) && data.gaps.length > 0) {

      data.gaps.forEach(g => {

        const li = document.createElement("li");

        li.className = "bullet-item";

        li.innerHTML = `<span class="bullet-dot dot-warning"></span><span>${escapeHtml(t(g))}</span>`;

        gapsList.appendChild(li);

      });

    } else {

      gapsList.innerHTML = `<li class="bullet-item"><span class="bullet-dot dot-success"></span><span>${t("The project is not missing any core components.")}</span></li>`;

    }

  }

  const gapCountBadge = document.getElementById("gapCountBadge");
  if (gapCountBadge) {
    const totalGaps = (data.gaps?.length || 0) + (data.bloat?.length || 0);
    gapCountBadge.textContent = totalGaps;
    gapCountBadge.classList.toggle("has-items", totalGaps > 0);
  }

  const bloatList = document.getElementById("bloatList");

  if (bloatList) {

    bloatList.innerHTML = "";

    if (Array.isArray(data.bloat) && data.bloat.length > 0) {

      data.bloat.forEach(b => {

        const li = document.createElement("li");

        li.className = "bullet-item";

        li.innerHTML = `<span class="bullet-dot dot-danger"></span><span>${escapeHtml(t(b))}</span>`;

        bloatList.appendChild(li);

      });

    } else {

      bloatList.innerHTML = `<li class="bullet-item"><span class="bullet-dot dot-success"></span><span>${t("Clean codebase, no surplus files.")}</span></li>`;

    }

  }

  // 7. Grouped Violations (project-wide source violations tab)

  const violationBadge = document.getElementById("violationCountBadge");
  if (violationBadge) {
    const totalViolations = (data.violations || []).length;
    violationBadge.textContent = totalViolations;
    violationBadge.classList.toggle("has-violations", totalViolations > 0);
  }

  renderGroupedViolations(data.violations || [], document.getElementById("violationGroupedContainer"));

  // 8. Render Section 2 (Findings), Section 4 (Core Baseline B1-B9), Sections 0 & 7 (Safety & Scope)

  renderFindingsTable(data.findings ?? []);

  renderBaselineTable(data.baseline ?? []);

  renderSafetyAndScope(data.safety ?? {}, data.scope ?? {});

  renderAnalysis(data.analysis, data.insights);

  // 9. Update the Report & AI Prompt panel

  updateReportPromptPanel();

}

function updateReportPromptPanel() {

  const pathDisplay = document.getElementById("reportFilePathDisplay");

  const statusBadge = document.getElementById("reportFileStatusBadge");

  const promptBox = document.getElementById("aiPromptBox");

  if (pathDisplay) {

    pathDisplay.textContent = currentAuditData?.report_file || t("No report yet. Click 'Run Analytics' to create one.");

  }

  if (statusBadge) {

    if (currentAuditData?.report_file) {

      statusBadge.textContent = t("Published");

      statusBadge.className = "status-pill pill-ready";

    } else {

      statusBadge.textContent = t("None yet");

      statusBadge.className = "status-pill";

      statusBadge.style.color = "var(--text-dim)";

    }

  }

  if (promptBox) {

    promptBox.textContent = currentAuditData?.ai_prompt || t("Click 'Run Analytics' to generate the standard Agent prompt.");

  }

}

function copyReportPath() {

  const pathText = currentAuditData?.report_file;

  if (!pathText) {

    alert(t("There is no report file path to copy yet."));

    return;

  }

  navigator.clipboard.writeText(pathText).then(() => {

    const btn = document.getElementById("copyReportPathBtn");

    if (btn) {

      btn.innerHTML = `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg><span>${t("Copied!")}</span>`;

      setTimeout(() => {

        btn.innerHTML = `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg><span>${t("Copy path")}</span>`;

      }, 2000);

    }

  });

}

function handlePillarSelection(pillarKey) {

  const progressView = document.getElementById("installerProgressView");

  const resultView = document.getElementById("auditResultView");

  const overviewBanner = document.getElementById("overviewMetricsBanner");

  const overviewTabs = document.getElementById("overviewTabsNav");

  const tabPillar = document.getElementById("tab-pillar");

  if (pillarKey === "history") {

    if (progressView) progressView.style.display = "flex";

    if (resultView) resultView.style.display = "none";

    return;

  }

  if (progressView) progressView.style.display = "none";

  if (resultView) resultView.style.display = "flex";

  if (pillarKey === "overview") {

    if (overviewBanner) overviewBanner.style.display = "flex";

    if (overviewTabs) overviewTabs.style.display = "flex";

    if (tabPillar) tabPillar.classList.remove("active");

    switchOverviewTab("tab-overview");

    return;

  }

  if (pillarKey === "report_prompt") {

    if (overviewBanner) overviewBanner.style.display = "none";

    if (overviewTabs) overviewTabs.style.display = "none";

    if (tabPillar) tabPillar.classList.remove("active");

    document.querySelectorAll(".tab-panel").forEach(p => p.classList.remove("active"));

    const reportPanel = document.getElementById("tab-report-prompt");

    if (reportPanel) reportPanel.classList.add("active");

    updateReportPromptPanel();

    return;

  }

  if (overviewBanner) overviewBanner.style.display = "none";

  if (overviewTabs) overviewTabs.style.display = "none";

  document.querySelectorAll(".tab-panel").forEach(p => p.classList.remove("active"));

  if (tabPillar) tabPillar.classList.add("active");

  const titleMap = {

    readme: "Readme & Onboarding",

    backend: "Backend & Core Flow",

    frontend: "Frontend & UI/UX",

    database: "Database & Query Safety",

    security: t("Security & Supply Chain"),

    cloud: t("Cloud Infrastructure & DevOps"),

    microservices: t("Distributed Systems & Gateway"),

    data_caching: t("Data Engineering & Cache"),

    observability: t("Monitoring & Operations"),

    anticrash: "Runtime Anti-Crash",

    agent_ecosystem: t("AI Agent Ecosystem (Rules, Skills & Workflows)"),

    contracts: t("Architecture Records & API Contracts")

  };

  const catMap = {

    readme: currentAuditData?.categories?.["01_readme"],

    backend: currentAuditData?.categories?.["02_backend"],

    frontend: currentAuditData?.categories?.["03_frontend"],

    database: currentAuditData?.categories?.["04_database"],

    anticrash: currentAuditData?.categories?.["05_anticrash"],

    contracts: currentAuditData?.categories?.["06_contracts"],

    agent_ecosystem: currentAuditData?.categories?.["07_agent_ecosystem"],

    security: currentAuditData?.categories?.["08_security"],

    cloud: currentAuditData?.categories?.["09_cloud"],

    microservices: currentAuditData?.categories?.["10_microservices"],

    data_caching: currentAuditData?.categories?.["11_data_caching"],

    observability: currentAuditData?.categories?.["12_observability"]

  };

  const activePillar = currentAuditData?.all_pillars?.find(p => p.key === pillarKey) || currentAuditData?.active_pillars?.find(p => p.key === pillarKey);

  const cat = activePillar || catMap[pillarKey];

  const titleEl = document.getElementById("pillarDetailTitle");

  const subTitleEl = document.getElementById("pillarDetailSubtitle");

  const scoreValEl = document.getElementById("pillarDetailScore");

  const foundList = document.getElementById("pillarFoundList");

  const missingList = document.getElementById("pillarMissingList");

  const missingTitleEl = document.getElementById("pillarMissingTitle");

  const violationsSection = document.getElementById("pillarViolationsSection");

  if (titleEl) titleEl.textContent = t(titleMap[pillarKey] || (activePillar ? pillarName(activePillar) : pillarKey));

  if (subTitleEl) subTitleEl.textContent = t("Detailed audit against the Project-Builder-4-Agents standards");

  if (!cat) {

    if (scoreValEl) {

      scoreValEl.textContent = "-- / --";

      scoreValEl.className = "pillar-score-val";

      scoreValEl.style.color = "";

    }

    if (foundList) foundList.innerHTML = `<li class="muted-item">${t("No audit data yet.")}</li>`;

    if (missingList) missingList.innerHTML = `<li class="muted-item">${t("No audit data yet.")}</li>`;

    if (missingTitleEl) missingTitleEl.className = "section-title";

    if (violationsSection) violationsSection.style.display = "none";

    return;

  }

  if (cat.is_na || cat.max === 0) {

    if (scoreValEl) {

      scoreValEl.textContent = t("N/A (Not applicable)");

      scoreValEl.className = "pillar-score-val";

      scoreValEl.style.color = "var(--text-dim)";

    }

    if (foundList) {

      foundList.innerHTML = `<li class="bullet-item"><span class="bullet-dot dot-neutral"></span><span>${t("This pillar does not apply to the current project structure")} (${escapeHtml(currentAuditData?.profiler?.archetype || "N/A")}).</span></li>`;

    }

    if (missingList) {

      missingList.innerHTML = `<li class="bullet-item"><span class="bullet-dot dot-neutral"></span><span>${t("No mandatory requirements or failed criteria.")}</span></li>`;

    }

    if (missingTitleEl) {

      missingTitleEl.className = "section-title";

    }

    if (violationsSection) violationsSection.style.display = "none";

    return;

  }

  const isPillarCritical = Boolean(cat.has_critical || cat.critical_count > 0);
  const ratio = cat.max > 0 ? (cat.score / cat.max) : 0;

  if (scoreValEl) {
    scoreValEl.className = "pillar-score-val";
    scoreValEl.style.color = "";
    if (isPillarCritical) {
      scoreValEl.classList.add("score-danger");
      scoreValEl.innerHTML = `${cat.score} / ${cat.max} <span class="pillar-detail-critical-badge">🚨 ${t("CRITICAL RISK")}</span>`;
    } else {
      scoreValEl.textContent = `${cat.score} / ${cat.max}`;
      if (ratio >= 0.8) scoreValEl.classList.add("score-success");
      else if (ratio >= 0.5) scoreValEl.classList.add("score-warning");
      else scoreValEl.classList.add("score-danger");
    }
  }

  if (foundList) {

    foundList.innerHTML = "";

    if (Array.isArray(cat.found) && cat.found.length > 0) {

      cat.found.forEach(item => {

        const title = typeof item === "string" ? item : (item.title || "");

        const evidence = typeof item === "object" ? (item.evidence || item.location || "") : "";

        const snippet = typeof item === "object" ? (item.snippet || "") : "";

        const details = typeof item === "object" ? (item.details || "") : "";

        const badge = typeof item === "object" ? (item.badge || "") : "";

        const li = document.createElement("li");

        li.className = "analysis-criterion-item met";

        li.innerHTML = `

          <div class="criterion-card-content">

            <div class="criterion-top-row">

              <div class="criterion-title-wrap">

                <span class="criterion-status-icon success-icon">

                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>

                </span>

                <span class="criterion-main-title">${escapeHtml(t(title))}</span>

              </div>

              ${badge ? `<span class="criterion-chip chip-success">${escapeHtml(t(badge))}</span>` : ""}

            </div>

            ${details ? `<div class="criterion-desc">${escapeHtml(t(details))}</div>` : ""}

            ${(evidence || snippet) ? `

              <div class="criterion-evidence-box">

                ${evidence ? `

                  <div class="evidence-file-tag">

                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>

                    <span>${escapeHtml(t(evidence))}</span>

                  </div>` : ""}

                ${snippet ? `<pre class="evidence-snippet"><code>${escapeHtml(snippet)}</code></pre>` : ""}

              </div>

            ` : ""}

          </div>

        `;

        foundList.appendChild(li);

      });

    } else {

      foundList.innerHTML = `<li class="muted-item">${t("No criteria recorded as met yet.")}</li>`;

    }

  }

  if (missingTitleEl) {
    if (isPillarCritical || ratio < 0.5) {
      missingTitleEl.className = "section-title section-title-danger";
    } else {
      missingTitleEl.className = "section-title section-title-warning";
    }
  }

  if (missingList) {

    missingList.innerHTML = "";

    if (Array.isArray(cat.missing) && cat.missing.length > 0) {

      cat.missing.forEach(item => {

        const title = typeof item === "string" ? item : (item.title || "");

        const evidence = typeof item === "object" ? (item.evidence || item.location || "") : "";

        const snippet = typeof item === "object" ? (item.snippet || "") : "";

        const details = typeof item === "object" ? (item.details || "") : "";

        const badge = typeof item === "object" ? (item.badge || "") : "";

        const remediation = typeof item === "object" ? (item.remediation || "") : "";

        const isCritical = (typeof item === "object" && (item.is_critical || item.severity === "High"));
        const li = document.createElement("li");
        li.className = isCritical ? "analysis-criterion-item unmet critical-risk" : "analysis-criterion-item unmet";
        const dotClass = (isCritical || isPillarCritical || ratio < 0.5) ? 'danger-icon' : 'warning-icon';
        li.innerHTML = `
          <div class="criterion-card-content">
            <div class="criterion-top-row">
              <div class="criterion-title-wrap">
                <span class="criterion-status-icon ${dotClass}">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
                </span>
                <span class="criterion-main-title">${escapeHtml(t(title))}</span>
              </div>
              ${isCritical ? `<span class="criterion-chip chip-critical">🚨 ${t("CRITICAL")}</span>` : (badge ? `<span class="criterion-chip chip-warning">${escapeHtml(t(badge))}</span>` : "")}
            </div>

            ${details ? `<div class="criterion-desc">${escapeHtml(t(details))}</div>` : ""}

            ${(evidence || snippet) ? `

              <div class="criterion-evidence-box">

                ${evidence ? `

                  <div class="evidence-file-tag missing-target">

                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>

                    <span>${escapeHtml(t(evidence))}</span>

                  </div>` : ""}

                ${snippet ? `<pre class="evidence-snippet"><code>${escapeHtml(snippet)}</code></pre>` : ""}

              </div>

            ` : ""}

            ${remediation ? `

              <div class="criterion-action-box">

                <span class="action-icon">💡</span>

                <span class="action-text"><strong>${t("Remediation")}:</strong> ${escapeHtml(remediation)}</span>

              </div>` : ""}

          </div>

        `;

        missingList.appendChild(li);

      });

    } else {

      missingList.innerHTML = `<li class="bullet-item"><span class="bullet-dot dot-success"></span><span>${t("All criteria of this pillar are met.")}</span></li>`;

    }

  }

  if (violationsSection) {

    if (pillarKey === "anticrash") {

      violationsSection.style.display = "block";

      renderGroupedViolations(currentAuditData?.violations || [], document.getElementById("pillarViolationsContainer"));

    } else {

      violationsSection.style.display = "none";

    }

  }

}

function switchOverviewTab(tabId) {

  document.querySelectorAll(".tab-btn").forEach(b => {

    b.classList.toggle("active", b.dataset.tab === tabId);

  });

  document.querySelectorAll(".tab-panel").forEach(p => {

    p.classList.toggle("active", p.id === tabId);

  });

}

function copyAiPrompt() {

  const promptBox = document.getElementById("aiPromptBox");

  const promptText = promptBox ? promptBox.textContent : "";

  if (!promptText) return;

  navigator.clipboard.writeText(promptText).then(() => {

    const txtSpan = document.getElementById("copyPromptBtnText");

    const btn = document.getElementById("copyPromptBtn");

    if (txtSpan) {

      txtSpan.textContent = t("Copied!");

      setTimeout(() => { txtSpan.textContent = t("Copy Prompt"); }, 2000);

    } else if (btn) {

      btn.textContent = t("Copied!");

      setTimeout(() => { btn.textContent = t("Copy Prompt"); }, 2000);

    }

  });

}

async function openReportFile() {

  if (!currentAuditData?.report_file) return;

  await fetch("/api/open-report", {

    method: "POST",

    headers: { "Content-Type": "application/json" },

    body: JSON.stringify({ path: currentAuditData.report_file })

  });

}

async function openTargetFolder() {

  if (!currentAuditData?.target_dir) return;

  await fetch("/api/open-folder", {

    method: "POST",

    headers: { "Content-Type": "application/json" },

    body: JSON.stringify({ path: currentAuditData.target_dir })

  });

}

async function triggerLLMReview() {

  if (!currentAuditData) {

    alert(t("Run Analytics before asking the AI to analyze."));

    return;

  }

  const btn = document.getElementById("triggerLLMBtn");

  btn.disabled = true;

  btn.textContent = t("⏳ Connecting to AI...");

  const box = document.getElementById("llmAnalysisBox");

  box.textContent = t("Sending audit data to Senior Architect AI for analysis...");

  try {

    const res = await fetch("/api/llm-review", {

      method: "POST",

      headers: { "Content-Type": "application/json" },

      body: JSON.stringify({

        provider: appSettings.llm_provider || "gemini",

        model: appSettings.selected_model || "gemini-2.0-flash",

        include_code: !!appSettings.include_code,

        language: currentLang(),

        audit_data: currentAuditData

      })

    });

    const result = await res.json();

    if (result.success) {

      box.textContent = result.analysis + (result.saved_to ? "\n\n— " + t("Saved:") + " " + result.saved_to : "");

    } else {

      box.textContent = "⚠️ " + t("Error:") + " " + result.error;

    }

  } catch (e) {

    box.textContent = "⚠️ " + t("AI connection error:") + " " + e.message;

  } finally {

    btn.disabled = false;

    btn.textContent = t("✨ Analyze With AI");

  }

}

// Reachability is probed by the engine (it does the downloading), not by navigator.onLine.
let netHosts = null;

async function probeInternet() {
  try {
    const res = await fetch("/api/connectivity");
    const data = await res.json();
    netHosts = (data && data.hosts) || {};
  } catch (e) {
    netHosts = {};
  }
  return netHosts;
}

async function refreshConnectivity() {
  const el = document.getElementById("netStatus");
  if (el) {
    el.style.color = "var(--text-dim)";
    el.textContent = t("Checking connection...");
  }
  const hosts = await probeInternet();
  const updOk = !!hosts["api.github.com"];
  const kbOk = !!hosts["raw.githubusercontent.com"];
  const upd = document.getElementById("aboutCheckUpdateBtn");
  const kb = document.getElementById("updateKnowledgeBtn");
  if (upd) upd.classList.toggle("is-offline", !updOk);
  if (kb) kb.classList.toggle("is-offline", !kbOk);
  if (el) {
    const online = updOk && kbOk;
    el.style.color = online ? "var(--success, #2ecc71)" : "var(--danger, #e74c3c)";
    el.textContent = online ? t("Internet connected") : t("No internet connection. Updates are unavailable.");
  }
}

window.addEventListener("online", refreshConnectivity);
window.addEventListener("offline", refreshConnectivity);

async function checkUpdate() {

  const modal = document.getElementById("updateModal");

  const body = document.getElementById("updateModalBody");

  modal.classList.add("open");

  body.textContent = t("Checking GitHub for a new version...");

  try {

    const hosts = await probeInternet();

    if (!hosts["api.github.com"]) {

      body.innerHTML = `<span style="color: #ef4444;">${t("No internet connection. Connect and try again.")}</span>`;

      return;

    }

    const res = await fetch("/api/check-update");

    const data = await res.json();

    if (data.error) {

      body.innerHTML = `<span style="color: #ef4444;">${t("Could not check for updates:")} ${escapeHtml(data.error)}</span>`;

      return;

    }

    if (data.has_update) {

      body.innerHTML = `

        <div style="font-size: 13.5px; color: #10b981; font-weight: 600; margin-bottom: 8px;">

          🚀 ${t("New version available:")} v${escapeHtml(data.latest_version)}

        </div>

        <p style="color: var(--text-muted); font-size: 12px; margin-bottom: 12px;">

          ${t("Your current version:")} v${escapeHtml(data.current_version)}

        </p>

        <div style="font-size: 12.5px; color: var(--text-secondary); background: var(--bg-card); padding: 12px; border-radius: 6px; white-space: pre-wrap;">${escapeHtml(data.release_notes)}</div>

        <div style="margin-top: 14px;">

          <a href="${escapeHtml(data.html_url)}" target="_blank" class="btn btn-primary" style="text-decoration: none;">${t("View Release on GitHub")}</a>

        </div>

      `;

    } else {

      body.innerHTML = `

        <div style="font-size: 13.5px; color: #38bdf8; font-weight: 600; margin-bottom: 6px;">

          ✅ ${t("You are on the latest version!")}

        </div>

        <p style="color: var(--text-muted); font-size: 12px;">

          ${t("Current version:")} v${escapeHtml(data.current_version)}

        </p>

      `;

    }

  } catch (e) {

    body.innerHTML = `<span style="color: #ef4444;">${t("Could not check for updates:")} ${escapeHtml(e.message)}</span>`;

  }

}

function setStatus(msg) {

  const el = document.getElementById("footerStatusText");

  if (el) el.textContent = msg;

}

function escapeHtml(text) {

  if (!text) return "";

  return String(text)

    .replace(/&/g, "&amp;")

    .replace(/</g, "&lt;")

    .replace(/>/g, "&gt;")

    .replace(/"/g, "&quot;")

    .replace(/'/g, "&#039;");

}

// -------------------------------------------------------------

// DYNAMIC OVERLAY SCROLLBAR CONTROLLER

// -------------------------------------------------------------

window.addEventListener('scroll', (e) => {

  const target = e.target;

  if (target && target.classList) {

    target.classList.add('is-scrolling');

    if (target._scrollTimeout) clearTimeout(target._scrollTimeout);

    target._scrollTimeout = setTimeout(() => {

      target.classList.remove('is-scrolling');

    }, 1200);

  }

}, true);

// -------------------------------------------------------------

// KEEPALIVE HEARTBEAT & SHUTDOWN DETECTOR

// -------------------------------------------------------------

setInterval(() => {

  fetch("/api/heartbeat", { method: "POST" }).catch(() => {});

}, 2000);

// NOTE (Handoff 004 Item C): removed beforeunload -> sendBeacon("/api/shutdown") so a reload (F5) does not stop the server.

// -------------------------------------------------------------

// PROJECT ANALYSIS (Project Model + conclusions compared with the Knowledge Pack)

// -------------------------------------------------------------

function renderAnalysis(a, ins) {

  const box = document.getElementById("analysisContainer");

  if (!box) return;

  if (!a || !ins) {

    box.innerHTML = `<div style="text-align:center;color:var(--text-dim);padding:32px;">${t("No analysis data for this scan.")}</div>`;

    return;

  }

  const e = escapeHtml;

  const list = (items, fn) => items.length ? `<ul class="bullet-list">${items.map(fn).join("")}</ul>` : `<div class="muted-item">${t("None.")}</div>`;

  const card = (title, body) => `<div class="dashboard-card"><div class="dashboard-card-header"><strong>${e(title)}</strong></div>${body}</div>`;

  const md = (t) => e(t).replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");

  const statusLabel = { ok: "✅ " + t("pass"), violated: "❌ " + t("violated"), unverified: "❔ " + t("needs confirmation") };

  const langRows = a.languages.slice(0, 6).map(l => `<tr><td>${e(l.name)}</td><td>${l.loc}</td><td>${l.files}</td><td>${l.share}%</td></tr>`).join("");

  const comps = a.components.filter(c => c.role === "code").slice(0, 10)

    .map(c => `<tr><td><code>${e(c.name)}</code></td><td>${c.loc}</td><td>${e(c.language)}</td><td>${c.fan_out}</td><td>${c.fan_in}</td></tr>`).join("");

  const prof = ins.profile || {};

  box.innerHTML = [

    card(t("Summary"), list(ins.summary, s => `<li class="bullet-item"><span>${md(t(s))}</span></li>`)),

    card(t("Languages"), `<table class="data-table"><thead><tr><th>${t("Language")}</th><th>${t("Lines of code")}</th><th>${t("Files")}</th><th>${t("Share")}</th></tr></thead><tbody>${langRows}</tbody></table>`),

    card(t("Components & dependencies"), `<table class="data-table"><thead><tr><th>${t("Component")}</th><th>${t("Lines of code")}</th><th>${t("Language")}</th><th>${t("Depends on")}</th><th>${t("Used by")}</th></tr></thead><tbody>${comps}</tbody></table>`),

    prof.slug ? card(t("Comparison with the kit architecture profile"),

      `<div><strong>${e(prof.title || prof.slug)}</strong> (${e(prof.doc_id || "")})</div>` +

      (prof.when ? `<div><em>${t("Fits when:")}</em> ${e(prof.when)}</div><div><em>${t("Does not fit when:")}</em> ${e(prof.not_when)}</div>` : "") +

      list(prof.reasons || [], r => `<li class="bullet-item"><span>${e(r)}</span></li>`)) : "",

    card(t("Strengths"), list(ins.strengths, s => `<li class="bullet-item"><span class="bullet-dot dot-success"></span><span>${e(t(s.text))} <small>(${e(s.evidence.slice(0, 2).join("; "))})</small></span></li>`)),

    card(t("Bottlenecks"), list(ins.bottlenecks, b => `<li class="bullet-item"><span class="bullet-dot dot-danger"></span><span><strong>[${e(sevLabel(b.severity))}] ${e(t(b.title))}</strong> — ${e(t(b.why))}<br><small>${e(b.evidence.slice(0, 4).join(" · "))}</small></span></li>`)),

    card(t("Prioritized recommendations"), list(ins.recommendations, r => `<li class="bullet-item"><span>[${e(sevLabel(r.priority))}] ${e(t(r.action))} <small>${e(r.doc_ids.join(", "))}</small></span></li>`)),

    ins.checklist.length ? card(t("Profile constraint check"),

      `<table class="data-table"><thead><tr><th>${t("Source")}</th><th>${t("Constraint")}</th><th>${t("Result")}</th><th>${t("Evidence")}</th></tr></thead><tbody>${ins.checklist.map(c => `<tr><td>${e(c.source)}</td><td>${e(t(c.text))}</td><td>${statusLabel[c.status]}</td><td>${e(t(c.evidence))}</td></tr>`).join("")}</tbody></table>`) : "",

    `<div class="muted-item" style="padding:8px 4px;">${t("Kit knowledge:")} ${t("build")} ${e(ins.pack.generated)} (${e(ins.pack.source)}, ${t("{n} docs", { n: ins.pack.docs })}). ${e(ins.limits.join(" "))}</div>`

  ].join('<div style="height:16px"></div>');

}

async function testLLMConnection() {

  const out = document.getElementById("testLLMResult");

  const provider = document.getElementById("settingsLLMProvider").value;

  out.style.color = "var(--text-dim)";

  out.textContent = t("Checking...");

  try {

    const res = await fetch("/api/llm-test", {

      method: "POST", headers: { "Content-Type": "application/json" },

      body: JSON.stringify({

        provider, model: document.getElementById("settingsModelInput").value.trim(),

        api_key: document.getElementById("settingsApiKeyInput").value.trim()

      })

    });

    const r = await res.json();

    out.style.color = r.success ? "var(--success, #2ecc71)" : "var(--danger, #e74c3c)";

    out.textContent = r.success ? r.message : r.error;

  } catch (err) {

    out.style.color = "var(--danger, #e74c3c)";

    out.textContent = t("Could not reach the local server: ") + err.message;

  }

}

async function updateKnowledgePack() {

  const out = document.getElementById("updateKnowledgeResult");

  out.style.color = "var(--text-dim)";

  out.textContent = t("Checking connection...");

  const hosts = await probeInternet();

  if (!hosts["raw.githubusercontent.com"]) {

    out.style.color = "var(--danger, #e74c3c)";

    out.textContent = t("No internet connection. Connect and try again.");

    return;

  }

  out.textContent = t("Downloading...");

  try {

    const res = await fetch("/api/update-knowledge", { method: "POST", headers: { "Content-Type": "application/json" }, body: "{}" });

    const r = await res.json();

    out.style.color = r.ok ? "var(--success, #2ecc71)" : "var(--danger, #e74c3c)";

    out.textContent = r.message;

  } catch (err) {

    out.textContent = t("Error:") + " " + err.message;

  }

}

document.getElementById("testLLMBtn")?.addEventListener("click", testLLMConnection);

document.getElementById("updateKnowledgeBtn")?.addEventListener("click", updateKnowledgePack);