// ANTIGRAVITY 2.0 SHELL CONTROLLER & EVENT BRIDGE

let currentAuditData = null;
let appSettings = {};

document.addEventListener("DOMContentLoaded", async () => {
  initEventListeners();
  await loadSettings();
});

function initEventListeners() {
  // Theme Toggle
  document.getElementById("themeToggleBtn").addEventListener("click", toggleTheme);

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

      // Đồng bộ trạng thái sidebar khi chuyển tab
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

    // Áp dụng theme
    const theme = appSettings.theme || "dark";
    document.documentElement.setAttribute("data-theme", theme);
    const themeColorMeta = document.querySelector('meta[name="theme-color"]');
    if (themeColorMeta) {
      themeColorMeta.setAttribute("content", theme === "dark" ? "#0e0d13" : "#ffffff");
    }
    document.getElementById("settingsThemeSelect").value = theme;

    // Cập nhật thư mục gần nhất
    if (appSettings.last_target_directory) {
      document.getElementById("targetFolderInput").value = appSettings.last_target_directory;
    }

    // Cập nhật LLM config
    document.getElementById("settingsLLMProvider").value = appSettings.llm_provider || "gemini";
    updateApiKeyInputForProvider(appSettings.llm_provider || "gemini");
    document.getElementById("settingsModelInput").value = appSettings.selected_model || "gemini-2.0-flash";

    // Cập nhật trạng thái sáng/tối của nút AI Deep Review trên Toolbar
    updateAIButtonState();
  } catch (e) {
    console.error("Lỗi nạp cấu hình:", e);
  }
}

function toggleTheme() {
  const current = document.documentElement.getAttribute("data-theme") || "dark";
  const next = current === "dark" ? "light" : "dark";
  document.documentElement.setAttribute("data-theme", next);
  const themeColorMeta = document.querySelector('meta[name="theme-color"]');
  if (themeColorMeta) {
    themeColorMeta.setAttribute("content", next === "dark" ? "#0e0d13" : "#ffffff");
  }
  appSettings.theme = next;
  fetch("/api/settings", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ theme: next })
  });
}

function openSettingsModal() {
  document.getElementById("settingsModal").classList.add("open");
  const provider = document.getElementById("settingsLLMProvider").value;
  updateApiKeyInputForProvider(provider);
}

function closeSettingsModal() {
  document.getElementById("settingsModal").classList.remove("open");
}

function closeModal(modalId) {
  document.getElementById(modalId).classList.remove("open");
}

function updateApiKeyInputForProvider(provider) {
  const keyField = `${provider}_api_key`;
  document.getElementById("settingsApiKeyInput").value = appSettings[keyField] || "";
}

document.getElementById("settingsLLMProvider").addEventListener("change", (e) => {
  updateApiKeyInputForProvider(e.target.value);
  if (e.target.value === "gemini") {
    document.getElementById("settingsModelInput").value = "gemini-2.0-flash";
  } else if (e.target.value === "openai") {
    document.getElementById("settingsModelInput").value = "gpt-4o";
  } else if (e.target.value === "claude") {
    document.getElementById("settingsModelInput").value = "claude-3-5-sonnet-20241022";
  }
});

async function saveSettingsFromModal() {
  const theme = document.getElementById("settingsThemeSelect").value;
  const provider = document.getElementById("settingsLLMProvider").value;
  const apiKey = document.getElementById("settingsApiKeyInput").value.trim();
  const model = document.getElementById("settingsModelInput").value.trim();

  const updates = {
    theme: theme,
    llm_provider: provider,
    selected_model: model
  };
  updates[`${provider}_api_key`] = apiKey;

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
      updateAIButtonState();
      closeSettingsModal();
      setStatus("Cấu hình đã được lưu thành công.");
    } else {
      alert("Lỗi lưu cấu hình: " + result.message);
    }
  } catch (e) {
    alert("Lỗi kết nối lưu cấu hình: " + e.message);
  }
}

// -------------------------------------------------------------
// AI REVIEW BUTTON CONTROLLER & REACTIVE BINDING
// -------------------------------------------------------------
function hasConfiguredApiKey() {
  if (!appSettings) return false;
  const currentProvider = appSettings.llm_provider || "gemini";
  const currentKey = appSettings[`${currentProvider}_api_key`];
  if (currentKey && currentKey.trim().length > 0) return true;

  // Fallback: kiểm tra bất kỳ provider nào có key
  const anyKey = appSettings.gemini_api_key || appSettings.openai_api_key || appSettings.claude_api_key;
  return !!(anyKey && anyKey.trim().length > 0);
}

function updateAIButtonState() {
  const aiBtn = document.getElementById("topAIDeepReviewBtn");
  if (!aiBtn) return;

  const hasKey = hasConfiguredApiKey();
  if (hasKey) {
    aiBtn.disabled = false;
    aiBtn.title = "Kích hoạt phân tích kiến trúc chuyên sâu bằng Senior Architect AI";
  } else {
    aiBtn.disabled = true;
    aiBtn.title = "Cần cấu hình API Key trong Cài đặt (góc trên bên phải) để kích hoạt AI Review";
  }
}

async function handleTopAIDeepReview() {
  if (!hasConfiguredApiKey()) {
    openSettingsModal();
    alert("Vui lòng nhập API Key trong Cài đặt để kích hoạt tính năng AI Deep Review.");
    return;
  }

  const folder = document.getElementById("targetFolderInput").value.trim();
  if (!folder) {
    alert("Vui lòng chọn thư mục dự án trước khi thực hiện Review.");
    return;
  }

  // Nếu chưa có dữ liệu đo kiểm tiêu chuẩn, tự động chạy Standard Review trước
  if (!currentAuditData) {
    setStatus("Đang chạy Standard Review trước để thu thập dữ liệu thẩm định cho AI...");
    await runBenchmark();
    if (!currentAuditData) return;
  }

  // Chuyển sang panel AI Deep Review chuyên biệt
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

  // Kích hoạt phân tích chuyên sâu bằng AI
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
  const hasTime = /^\[\d{2}:\d{2}:\d{2}\]/.test(message);
  line.textContent = hasTime ? message : `${getTimestamp()} ${message}`;
  feed.appendChild(line);
  feed.scrollTop = feed.scrollHeight;
}

function renderDynamicSegments(activePillars) {
  const container = document.getElementById("installerSegmentsContainer");
  const labelEl = document.getElementById("segmentedBarLabel");
  if (!container) return;

  const count = Array.isArray(activePillars) ? activePillars.length : 0;
  if (labelEl) {
    labelEl.textContent = `Các chặng đo kiểm tiêu chuẩn (${count} Hạng mục)`;
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
          <span class="segment-name" title="${escapeHtml(p.name)}">${escapeHtml(p.name)}</span>
        </div>
        <div class="segment-track"><div class="segment-fill"></div></div>
        <div class="segment-points">${p.max}đ</div>
      `;
      container.appendChild(stepEl);
    });
  }
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
  if (msgEl) msgEl.textContent = statusMsg;
  if (badgeEl) badgeEl.textContent = stepBadge;
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
  if (targetDirEl) targetDirEl.textContent = `Dự án: ${targetDir}`;
  if (finishBox) finishBox.style.display = "none";
  if (logFeed) logFeed.innerHTML = "";

  // Đặt lại spinner về trạng thái xoay
  if (spinnerEl) spinnerEl.className = "installer-spinner";
  if (mainTitleEl) mainTitleEl.textContent = "Đang thẩm định kiến trúc mã nguồn...";

  // Đồng bộ sidebar: chọn mục "history" (Lịch sử quét)
  document.querySelectorAll(".pillar-item").forEach(i => {
    i.classList.toggle("active", i.getAttribute("data-pillar") === "history");
  });

  const dotHistory = document.getElementById("dot_history");
  const scoreHistory = document.getElementById("score_history");
  if (dotHistory) {
    dotHistory.className = "status-dot dot-warning";
  }
  if (scoreHistory) {
    scoreHistory.textContent = "Đang quét...";
    scoreHistory.style.color = "#f59e0b";
  }

  // Reset container các chặng kiểm tra
  const segContainer = document.getElementById("installerSegmentsContainer");
  if (segContainer) segContainer.innerHTML = "";

  setOverallProgress(0, "Đang khởi tạo các module kiểm tra...", "Khởi động");
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

  // Đồng bộ trạng thái sidebar sang TỔNG QUAN
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
    setStatus(`Đã chọn thư mục: ${folderPath}`);
  }
};

async function selectFolderNative() {
  if (window.chrome && window.chrome.webview) {
    window.chrome.webview.postMessage("select-folder");
    return;
  }

  setStatus("Đang mở hộp thoại chọn thư mục Windows...");
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
      setStatus("Đã hủy chọn thư mục.");
    }
  } catch (e) {
    setStatus("Lỗi khi mở hộp thoại chọn thư mục: " + e.message);
  }
}

async function runBenchmark() {
  const folder = document.getElementById("targetFolderInput").value.trim();
  if (!folder) {
    alert("Vui lòng chọn thư mục dự án cần Review.");
    return;
  }

  const runBtn = document.getElementById("runAuditBtn");
  runBtn.disabled = true;
  runBtn.innerHTML = `<span>Đang thẩm định...</span>`;
  setStatus("Đang đo kiểm kiến trúc mã nguồn...");

  // 1. Mở màn hình tiến trình thẩm định kiểu cài đặt app
  showInstallerProgressView(folder);
  addInstallerLog("Khởi động bộ máy đo kiểm Universal Project Auditor...", "info");
  addInstallerLog(`Khảo sát tệp tin cấu hình tại: ${folder}`, "muted");

  try {
    const res = await fetch("/api/run-audit", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ target_dir: folder })
    });
    const data = await res.json();

    if (!data.success) {
      addInstallerLog(`Lỗi đo kiểm: ${data.error}`, "error");
      setOverallProgress(100, `Thất bại: ${data.error}`, "LỖI");
      alert("Lỗi Review: " + data.error);
      setStatus("Đo kiểm thất bại.");
      runBtn.disabled = false;
      runBtn.innerHTML = `<svg width="11" height="11" viewBox="0 0 24 24" fill="currentColor"><polygon points="6 3 20 12 6 21 6 3"/></svg><span>Standard Review</span>`;
      return;
    }

    currentAuditData = data;

    // 2. Render các chặng đo kiểm tiêu chuẩn động theo đúng active_pillars thực tế của dự án
    renderDynamicSegments(data.active_pillars || []);

    // 3. Playback authentic real scan logs từ backend Python
    const logs = Array.isArray(data.scan_logs) && data.scan_logs.length > 0 
      ? data.scan_logs 
      : [{ text: "Đã hoàn thành quét dự án.", type: "info" }];

    let logIdx = 0;
    const playbackInterval = 40; // 40ms mỗi dòng log (~1.2s toàn bộ)
    const totalLogs = logs.length;

    if (installerTimer) clearInterval(installerTimer);
    installerTimer = setInterval(() => {
      if (logIdx < totalLogs) {
        const item = logs[logIdx];
        addInstallerLog(item.text, item.type || "info");

        // Cập nhật trạng thái chặng tương ứng nếu có
        if (item.stage && item.stage !== "general" && item.stage !== "init" && item.stage !== "finish" && item.stage !== "indexing" && item.stage !== "profiling") {
          setSegmentStatus(item.stage, "active");
        }

        const pct = Math.min(95, Math.round(((logIdx + 1) / totalLogs) * 95));
        const cleanMsg = item.text.replace(/^\[\d{2}:\d{2}:\d{2}\]\s*/, '');
        setOverallProgress(pct, `Đang xử lý: ${cleanMsg.slice(0, 55)}...`, `${pct}%`);
        logIdx++;
      } else {
        clearInterval(installerTimer);
        installerTimer = null;

        // Hoàn tất tất cả các chặng
        if (data.active_pillars) {
          data.active_pillars.forEach(p => setSegmentStatus(p.key, "completed"));
        }
        setOverallProgress(100, `✓ Hoàn tất đo kiểm toàn diện! Tổng điểm: ${data.total_score}/100`, "XONG 100%");

        // Dừng xoay spinner và hiển thị trạng thái hoàn tất
        const spinnerEl = document.getElementById("installerSpinner");
        const mainTitleEl = document.getElementById("installerMainTitle");
        if (spinnerEl) spinnerEl.className = "installer-spinner spinner-done";
        if (mainTitleEl) mainTitleEl.textContent = `Đã hoàn tất đo kiểm kiến trúc (${data.total_score}/100)`;

        // Cập nhật trạng thái "Lịch sử quét" trên Sidebar
        const dotHistory = document.getElementById("dot_history");
        const scoreHistory = document.getElementById("score_history");
        if (dotHistory) dotHistory.className = "status-dot dot-success";
        if (scoreHistory) {
          scoreHistory.textContent = "Hoàn tất";
          scoreHistory.style.color = "#10b981";
        }

        // Hiển thị thanh thông báo hoàn tất với nút chuyển
        const finishBox = document.getElementById("installerFinishBox");
        if (finishBox) finishBox.style.display = "flex";
        const summaryEl = document.getElementById("finishScoreSummary");
        if (summaryEl) summaryEl.textContent = `Hoàn tất đo kiểm toàn diện! Tổng điểm: ${data.total_score}/100 [Hạng ${data.grade}]`;

        // Render toàn bộ 12 hạng mục (với N/A disable) lên sidebar
        renderAuditResults(data);
        setStatus(`Hoàn tất Review! Điểm: ${data.total_score}/100.`);

        // Khôi phục nút bấm
        runBtn.disabled = false;
        runBtn.innerHTML = `<svg width="11" height="11" viewBox="0 0 24 24" fill="currentColor"><polygon points="6 3 20 12 6 21 6 3"/></svg><span>Standard Review</span>`;
      }
    }, playbackInterval);

  } catch (e) {
    if (installerTimer) clearInterval(installerTimer);
    installerTimer = null;
    addInstallerLog(`Lỗi kết nối Backend: ${e.message}`, "error");
    setOverallProgress(100, `Lỗi kết nối: ${e.message}`, "LỖI");
    alert("Lỗi kết nối Backend: " + e.message);
    setStatus("Lỗi kết nối.");
    runBtn.disabled = false;
    runBtn.innerHTML = `<svg width="11" height="11" viewBox="0 0 24 24" fill="currentColor"><polygon points="6 3 20 12 6 21 6 3"/></svg><span>Standard Review</span>`;
  }
}
function updateStatusDot(dotId, score, max) {
  const dot = document.getElementById(dotId);
  if (!dot) return;
  dot.className = "status-dot";
  if (!max || max <= 0) {
    dot.classList.add("dot-neutral");
    return;
  }
  const ratio = score / max;
  if (ratio >= 0.8) {
    dot.classList.add("dot-success");
  } else if (ratio >= 0.5) {
    dot.classList.add("dot-warning");
  } else {
    dot.classList.add("dot-danger");
  }
}

// -------------------------------------------------------------
// VIOLATION GROUPING CONTROLLER (GOM NHÓM & TẦN SUẤT LỖI)
// -------------------------------------------------------------
function groupViolations(violations) {
  if (!violations || !Array.isArray(violations)) return [];
  const map = new Map();

  violations.forEach(v => {
    const key = v.type || "OTHER_VIOLATION";
    if (!map.has(key)) {
      map.set(key, {
        type: v.type || "UNKNOWN",
        desc: v.desc || "Vi phạm quy chuẩn mã nguồn",
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
  if (!violations || violations.length === 0) {
    containerEl.innerHTML = `<div style="color: #10b981; font-size: 13px; padding: 16px 0;">🎉 Không phát hiện vi phạm mã nguồn hoặc lỗi Anti-Crash.</div>`;
    return;
  }

  const groups = groupViolations(violations);
  const totalCount = violations.length;
  const groupCount = groups.length;

  let html = `
    <div class="violation-summary-bar">
      <span class="violation-summary-text">Phát hiện <strong style="color: #ef4444;">${totalCount} vị trí vi phạm</strong> (thuộc <span class="violation-type-count">${groupCount} loại lỗi kiến trúc chuẩn</span>):</span>
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
            <span class="v-frequency-badge">${g.count} vị trí vi phạm</span>
          </div>
          ${g.locations.length > 1 ? `<button class="btn-toggle-locations" data-target="loc_${gIdx}_${containerEl.id}">Chi tiết ${g.count} vị trí ▾</button>` : ""}
        </div>
        <div class="v-desc">${escapeHtml(g.desc)}</div>
        ${g.snippet ? `<div class="v-snippet-box"><code>${escapeHtml(g.snippet)}</code></div>` : ""}
        <div class="v-locations-section">
          <div class="v-locations-pills">
            ${pillLocations.map(loc => `<span class="v-location-pill">${escapeHtml(loc.file)}:${loc.line}</span>`).join("")}
            ${hasMore ? `<span class="v-location-pill" style="color: var(--text-dim);">+ ${g.locations.length - 5} vị trí khác</span>` : ""}
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

  // Gắn sự kiện mở rộng/thu gọn danh sách chi tiết các vị trí
  containerEl.querySelectorAll(".btn-toggle-locations").forEach(btn => {
    btn.addEventListener("click", () => {
      const targetId = btn.getAttribute("data-target");
      const list = containerEl.querySelector(`#${targetId}`);
      if (list) {
        const isOpen = list.classList.toggle("open");
        const match = btn.textContent.match(/\d+/);
        const count = match ? match[0] : "";
        btn.textContent = isOpen ? `Thu gọn danh sách ▴` : `Chi tiết ${count} vị trí ▾`;
      }
    });
  });
}

function renderAuditResults(data) {
  // 1. Total Score & Màu điểm
  const totalScoreEl = document.getElementById("totalScore");
  if (totalScoreEl) {
    totalScoreEl.textContent = data.total_score;
    totalScoreEl.className = "score-number";
    if (data.total_score >= 80) totalScoreEl.classList.add("score-success");
    else if (data.total_score >= 50) totalScoreEl.classList.add("score-warning");
    else totalScoreEl.classList.add("score-danger");
  }

  // 2. Metadata (Có title đầy đủ khi hover, không bị tràn đè)
  const archTypeEl = document.getElementById("metaArchetype");
  const archStyleEl = document.getElementById("metaArchStyle");
  if (archTypeEl) {
    const rawType = data.profiler?.archetype || "Chưa xác định";
    archTypeEl.textContent = rawType;
    archTypeEl.setAttribute("title", rawType);
  }
  if (archStyleEl) {
    const rawStyle = data.profiler?.arch_style || "Chưa xác định";
    archStyleEl.textContent = rawStyle;
    archStyleEl.setAttribute("title", rawStyle);
  }

  // 3. Render Dynamic Sidebar Pillars (Luôn hiển thị đủ 12 hạng mục tiêu chuẩn)
  const pillarList = document.getElementById("pillarList");
  const sidebarTitle = document.getElementById("sidebarPillarsTitle") || document.querySelector(".sidebar-title");

  const pillarsToRender = (data.all_pillars && Array.isArray(data.all_pillars) && data.all_pillars.length > 0)
    ? data.all_pillars
    : (data.active_pillars || []);

  if (pillarList && pillarsToRender.length > 0) {
    if (sidebarTitle) {
      sidebarTitle.textContent = `Hạng mục kiểm tra (${pillarsToRender.length})`;
    }
    pillarList.innerHTML = "";
    pillarsToRender.forEach(p => {
      const li = document.createElement("li");
      li.setAttribute("data-pillar", p.key);

      if (p.is_na) {
        // Hạng mục N/A: không áp dụng cho dự án, hiển thị xám và disable không click được
        li.className = "pillar-item pillar-disabled";
        li.setAttribute("title", "Hạng mục này không áp dụng cho cấu trúc dự án hiện tại");
        li.innerHTML = `
          <div class="pillar-left">
            <span class="status-dot dot-neutral" id="dot_${p.key}"></span>
            <span class="pillar-name" style="color: var(--text-dim);">${escapeHtml(p.name)}</span>
          </div>
          <span class="pillar-score pillar-score-na" id="score_${p.key}">N/A</span>
        `;
      } else {
        // Hạng mục ĐANG HOẠT ĐỘNG: hiển thị điểm, màu trạng thái và click được
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
            <span class="pillar-name">${escapeHtml(p.name)}</span>
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

  // 4. Tech Stack Tags
  const techCloud = document.getElementById("techStackTags");
  if (techCloud) {
    techCloud.innerHTML = "";
    const allTechs = [
      ...(data.profiler?.languages || []),
      ...(data.profiler?.frameworks || []),
      ...(data.profiler?.databases || []),
      ...(data.profiler?.tools || [])
    ];
    if (allTechs.length === 0) {
      techCloud.innerHTML = `<span class="tech-tag">Không nhận diện được framework cụ thể</span>`;
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
    if (data.strengths && data.strengths.length > 0) {
      data.strengths.forEach(s => {
        const li = document.createElement("li");
        li.className = "bullet-item";
        li.innerHTML = `<span class="bullet-dot dot-success"></span><span>${escapeHtml(s)}</span>`;
        strList.appendChild(li);
      });
    } else {
      strList.innerHTML = `<li class="muted-item">Chưa có điểm nổi bật nào đạt mức chuẩn mực.</li>`;
    }
  }

  // 6. Gaps & Bloat
  const gapsList = document.getElementById("gapsList");
  if (gapsList) {
    gapsList.innerHTML = "";
    if (data.gaps && data.gaps.length > 0) {
      data.gaps.forEach(g => {
        const li = document.createElement("li");
        li.className = "bullet-item";
        li.innerHTML = `<span class="bullet-dot dot-warning"></span><span>${escapeHtml(g)}</span>`;
        gapsList.appendChild(li);
      });
    } else {
      gapsList.innerHTML = `<li class="bullet-item"><span class="bullet-dot dot-success"></span><span>Dự án không bị thiếu các thành phần cốt lõi.</span></li>`;
    }
  }
  const gapCountBadge = document.getElementById("gapCountBadge");
  if (gapCountBadge) {
    gapCountBadge.textContent = (data.gaps?.length || 0) + (data.bloat?.length || 0);
  }

  const bloatList = document.getElementById("bloatList");
  if (bloatList) {
    bloatList.innerHTML = "";
    if (data.bloat && data.bloat.length > 0) {
      data.bloat.forEach(b => {
        const li = document.createElement("li");
        li.className = "bullet-item";
        li.innerHTML = `<span class="bullet-dot dot-danger"></span><span>${escapeHtml(b)}</span>`;
        bloatList.appendChild(li);
      });
    } else {
      bloatList.innerHTML = `<li class="bullet-item"><span class="bullet-dot dot-success"></span><span>Mã nguồn sạch sẽ, không có tệp thừa.</span></li>`;
    }
  }

  // 7. Grouped Violations (Tab Vi phạm mã nguồn toàn dự án)
  const violationBadge = document.getElementById("violationCountBadge");
  if (violationBadge) violationBadge.textContent = (data.violations || []).length;
  renderGroupedViolations(data.violations || [], document.getElementById("violationGroupedContainer"));

  // 8. Cập nhật Panel Báo cáo & Prompt AI
  updateReportPromptPanel();
}

function updateReportPromptPanel() {
  const pathDisplay = document.getElementById("reportFilePathDisplay");
  const statusBadge = document.getElementById("reportFileStatusBadge");
  const promptBox = document.getElementById("aiPromptBox");

  if (pathDisplay) {
    pathDisplay.textContent = currentAuditData?.report_file || "Chưa có báo cáo. Nhấn 'Standard Review' để khởi tạo.";
  }
  if (statusBadge) {
    if (currentAuditData?.report_file) {
      statusBadge.textContent = "Đã xuất bản";
      statusBadge.className = "status-pill pill-ready";
    } else {
      statusBadge.textContent = "Chưa có";
      statusBadge.className = "status-pill";
      statusBadge.style.color = "var(--text-dim)";
    }
  }
  if (promptBox) {
    promptBox.textContent = currentAuditData?.ai_prompt || "Nhấn 'Standard Review' để sinh prompt chuẩn cho Agent.";
  }
}

function copyReportPath() {
  const pathText = currentAuditData?.report_file;
  if (!pathText) {
    alert("Chưa có tệp báo cáo để sao chép đường dẫn.");
    return;
  }
  navigator.clipboard.writeText(pathText).then(() => {
    const btn = document.getElementById("copyReportPathBtn");
    if (btn) {
      btn.innerHTML = `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg><span>Đã sao chép!</span>`;
      setTimeout(() => {
        btn.innerHTML = `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg><span>Sao chép đường dẫn</span>`;
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
    // 1. Chế độ LỊCH SỬ QUÉT: Hiển thị lại toàn bộ tiến trình quét, 6 chặng chia vạch và log feed
    if (progressView) progressView.style.display = "flex";
    if (resultView) resultView.style.display = "none";
    return;
  }

  // Với mọi hạng mục khác: Ẩn tiến trình quét và hiển thị canvas kết quả đo kiểm
  if (progressView) progressView.style.display = "none";
  if (resultView) resultView.style.display = "flex";

  if (pillarKey === "overview") {
    // 2. Chế độ TỔNG QUAN: Hiển thị lại banner điểm tổng và các tabs tổng quan
    if (overviewBanner) overviewBanner.style.display = "flex";
    if (overviewTabs) overviewTabs.style.display = "flex";
    if (tabPillar) tabPillar.classList.remove("active");

    // Mặc định kích hoạt tab Tổng quan
    switchOverviewTab("tab-overview");
    return;
  }

  if (pillarKey === "report_prompt") {
    // 3. Chế độ BÁO CÁO & PROMPT AI CHUYÊN BIỆT
    if (overviewBanner) overviewBanner.style.display = "none";
    if (overviewTabs) overviewTabs.style.display = "none";
    if (tabPillar) tabPillar.classList.remove("active");

    document.querySelectorAll(".tab-panel").forEach(p => p.classList.remove("active"));
    const reportPanel = document.getElementById("tab-report-prompt");
    if (reportPanel) reportPanel.classList.add("active");

    updateReportPromptPanel();
    return;
  }

  // 4. Chế độ XEM CHI TIẾT HẠNG MỤC:
  // Ẩn thanh tabs và metrics banner của tổng quan để tránh gây nhiễu
  if (overviewBanner) overviewBanner.style.display = "none";
  if (overviewTabs) overviewTabs.style.display = "none";

  // Ẩn toàn bộ các tab panel của tổng quan
  document.querySelectorAll(".tab-panel").forEach(p => p.classList.remove("active"));
  if (tabPillar) tabPillar.classList.add("active");

  const titleMap = {
    readme: "Readme & Onboarding",
    backend: "Backend & Core Flow",
    frontend: "Frontend & UI/UX",
    database: "Database & Query Safety",
    anticrash: "Runtime Anti-Crash",
    agent_ecosystem: "Hệ Sinh Thái AI Agent (Rules, Skills & Workflows)",
    contracts: "Hồ Sơ Kiến Trúc & Hợp Đồng API"
  };

  const catMap = {
    readme: currentAuditData?.categories?.["01_readme"],
    backend: currentAuditData?.categories?.["02_backend"],
    frontend: currentAuditData?.categories?.["03_frontend"],
    database: currentAuditData?.categories?.["04_database"],
    anticrash: currentAuditData?.categories?.["05_anticrash"],
    agent_ecosystem: currentAuditData?.categories?.["07_agent_ecosystem"],
    contracts: currentAuditData?.categories?.["06_contracts"]
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

  if (titleEl) titleEl.textContent = activePillar ? activePillar.name : (titleMap[pillarKey] || pillarKey);
  if (subTitleEl) subTitleEl.textContent = "Thẩm định chi tiết theo bộ tiêu chuẩn Starter Kit";

  if (!cat) {
    if (scoreValEl) {
      scoreValEl.textContent = "-- / --";
      scoreValEl.className = "pillar-score-val";
      scoreValEl.style.color = "";
    }
    if (foundList) foundList.innerHTML = `<li class="muted-item">Chưa có dữ liệu đo kiểm.</li>`;
    if (missingList) missingList.innerHTML = `<li class="muted-item">Chưa có dữ liệu đo kiểm.</li>`;
    if (missingTitleEl) missingTitleEl.className = "section-title";
    if (violationsSection) violationsSection.style.display = "none";
    return;
  }

  // Xử lý trường hợp hạng mục N/A (không áp dụng cho dự án)
  if (cat.is_na || cat.max === 0) {
    if (scoreValEl) {
      scoreValEl.textContent = "N/A (Không áp dụng)";
      scoreValEl.className = "pillar-score-val";
      scoreValEl.style.color = "var(--text-dim)";
    }
    if (foundList) {
      foundList.innerHTML = `<li class="bullet-item"><span class="bullet-dot dot-neutral"></span><span>Hạng mục này không áp dụng cho cấu trúc dự án hiện tại (${escapeHtml(currentAuditData?.profiler?.archetype || "N/A")}).</span></li>`;
    }
    if (missingList) {
      missingList.innerHTML = `<li class="bullet-item"><span class="bullet-dot dot-neutral"></span><span>Không có yêu cầu bắt buộc hay tiêu chí chưa đạt.</span></li>`;
    }
    if (missingTitleEl) {
      missingTitleEl.className = "section-title";
    }
    if (violationsSection) violationsSection.style.display = "none";
    return;
  }

  // Điểm số có màu sắc động (Không có chữ "đ")
  const ratio = cat.max > 0 ? (cat.score / cat.max) : 0;
  if (scoreValEl) {
    scoreValEl.textContent = `${cat.score} / ${cat.max}`;
    scoreValEl.className = "pillar-score-val";
    scoreValEl.style.color = "";
    if (ratio >= 0.8) scoreValEl.classList.add("score-success");
    else if (ratio >= 0.5) scoreValEl.classList.add("score-warning");
    else scoreValEl.classList.add("score-danger");
  }

  // Danh sách Tiêu chí đã đạt (Chỉ dùng bullet tròn màu xanh lá)
  if (foundList) {
    foundList.innerHTML = "";
    if (cat.found && cat.found.length > 0) {
      cat.found.forEach(item => {
        const li = document.createElement("li");
        li.className = "bullet-item";
        li.innerHTML = `<span class="bullet-dot dot-success"></span><span>${escapeHtml(item)}</span>`;
        foundList.appendChild(li);
      });
    } else {
      foundList.innerHTML = `<li class="muted-item">Chưa có tiêu chí nào được ghi nhận hoàn tất.</li>`;
    }
  }

  // Danh sách Tiêu chí chưa đạt:
  // Đổi màu tiêu đề và bullet động: Đỏ khi < 50% (nguy cơ cao), Cam khi 50% - 79% (cảnh báo)
  if (missingTitleEl) {
    if (ratio < 0.5) {
      missingTitleEl.className = "section-title section-title-danger";
    } else {
      missingTitleEl.className = "section-title section-title-warning";
    }
  }

  if (missingList) {
    missingList.innerHTML = "";
    if (cat.missing && cat.missing.length > 0) {
      const dotClass = ratio < 0.5 ? "bullet-dot dot-danger" : "bullet-dot dot-warning";
      cat.missing.forEach(item => {
        const li = document.createElement("li");
        li.className = "bullet-item";
        li.innerHTML = `<span class="${dotClass}"></span><span>${escapeHtml(item)}</span>`;
        missingList.appendChild(li);
      });
    } else {
      missingList.innerHTML = `<li class="bullet-item"><span class="bullet-dot dot-success"></span><span>Đã đáp ứng đầy đủ tất cả tiêu chí của hạng mục này.</span></li>`;
    }
  }

  // Riêng hạng mục Anti-Crash: hiển thị chi tiết vi phạm mã nguồn gom nhóm theo loại & tần suất
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
      txtSpan.textContent = "Đã sao chép!";
      setTimeout(() => { txtSpan.textContent = "Sao chép Prompt"; }, 2000);
    } else if (btn) {
      btn.textContent = "Đã sao chép!";
      setTimeout(() => { btn.textContent = "Sao chép Prompt"; }, 2000);
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
    alert("Vui lòng chạy Benchmark trước khi yêu cầu AI phân tích.");
    return;
  }

  const btn = document.getElementById("triggerLLMBtn");
  btn.disabled = true;
  btn.textContent = "⏳ Đang kết nối AI...";
  const box = document.getElementById("llmAnalysisBox");
  box.textContent = "Đang gửi dữ liệu đo kiểm và yêu cầu Senior Architect AI phân tích...";

  try {
    const res = await fetch("/api/llm-review", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        provider: appSettings.llm_provider || "gemini",
        model: appSettings.selected_model || "gemini-2.0-flash",
        audit_data: currentAuditData
      })
    });
    const result = await res.json();
    if (result.success) {
      box.textContent = result.analysis;
    } else {
      box.textContent = "⚠️ Lỗi: " + result.error;
    }
  } catch (e) {
    box.textContent = "⚠️ Lỗi kết nối AI: " + e.message;
  } finally {
    btn.disabled = false;
    btn.textContent = "✨ Phân Tích Bằng AI";
  }
}

async function checkUpdate() {
  const modal = document.getElementById("updateModal");
  const body = document.getElementById("updateModalBody");
  modal.classList.add("open");
  body.textContent = "Đang kiểm tra phiên bản mới từ GitHub...";

  try {
    const res = await fetch("/api/check-update");
    const data = await res.json();
    if (data.has_update) {
      body.innerHTML = `
        <div style="font-size: 13.5px; color: #10b981; font-weight: 600; margin-bottom: 8px;">
          🚀 Đã có phiên bản mới: v${escapeHtml(data.latest_version)}
        </div>
        <p style="color: var(--text-muted); font-size: 12px; margin-bottom: 12px;">
          Phiên bản hiện tại của bạn: v${escapeHtml(data.current_version)}
        </p>
        <div style="font-size: 12.5px; color: var(--text-secondary); background: var(--bg-card); padding: 12px; border-radius: 6px; white-space: pre-wrap;">${escapeHtml(data.release_notes)}</div>
        <div style="margin-top: 14px;">
          <a href="${escapeHtml(data.html_url)}" target="_blank" class="btn btn-primary" style="text-decoration: none;">Xem Bản Phát Hành Trên GitHub</a>
        </div>
      `;
    } else {
      body.innerHTML = `
        <div style="font-size: 13.5px; color: #38bdf8; font-weight: 600; margin-bottom: 6px;">
          ✅ Bạn đang sử dụng phiên bản mới nhất!
        </div>
        <p style="color: var(--text-muted); font-size: 12px;">
          Phiên bản hiện tại: v${escapeHtml(data.current_version)}
        </p>
      `;
    }
  } catch (e) {
    body.innerHTML = `<span style="color: #ef4444;">Không thể kiểm tra cập nhật: ${escapeHtml(e.message)}</span>`;
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

window.addEventListener("beforeunload", () => {
  try {
    navigator.sendBeacon("/api/shutdown");
  } catch (e) {}
});
