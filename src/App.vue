<template>
  <div class="mm-app" :data-theme="theme">

    <!-- ═══ HEADER ═══ -->
    <header class="mm-header">
      <div class="header-inner">
        <div class="header-brand">
          <svg class="brand-logo" viewBox="0 0 32 32" fill="none" aria-label="Money Manager Logo">
            <rect x="3" y="8" width="26" height="18" rx="3" stroke="currentColor" stroke-width="2"/>
            <path d="M3 13h26" stroke="currentColor" stroke-width="2"/>
            <circle cx="10" cy="20" r="2" fill="currentColor"/>
            <rect x="15" y="19" width="8" height="2" rx="1" fill="currentColor"/>
          </svg>
          <div>
            <span class="brand-name">Money Manager</span>
            <span class="brand-sub">Dashboard</span>
          </div>
        </div>
        <div class="header-actions">
          <div v-if="fileLoaded" class="period-pill">
            <select class="period-select" v-model="selectedPeriod" @change="refreshData" aria-label="Seleziona periodo">
              <option value="current_month">Questo Mese</option>
              <option value="last_month">Mese Scorso</option>
              <option value="ytd">Anno in Corso</option>
              <option value="all">Tutto</option>
            </select>
          </div>
          <label v-if="fileLoaded" class="btn-update" title="Cambia file database">
            <svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16"><path d="M4 10a6 6 0 1 0 6-6"/><path d="M4 6v4h4"/></svg>
            <span class="btn-update-text">Aggiorna</span>
            <input type="file" accept=".mmbak,.sqlite,.db" @change="handleFileUpload" style="display:none" />
          </label>
          <button class="theme-toggle" @click="toggleTheme" :aria-label="'Passa a tema ' + (theme === 'dark' ? 'chiaro' : 'scuro')">
            <svg v-if="theme === 'dark'" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18"><circle cx="10" cy="10" r="4"/><path d="M10 2v2M10 16v2M2 10h2M16 10h2M4.9 4.9l1.4 1.4M13.7 13.7l1.4 1.4M4.9 15.1l1.4-1.4M13.7 6.3l1.4-1.4"/></svg>
            <svg v-else viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18"><path d="M17.5 11.5A7.5 7.5 0 1 1 8.5 2.5a5.5 5.5 0 1 0 9 9z"/></svg>
          </button>
        </div>
      </div>
    </header>

    <!-- ═══ MAIN ═══ -->
    <main class="mm-main">

      <!-- ── UPLOAD SCREEN ── -->
      <div v-if="!fileLoaded" class="upload-screen">
        <div class="upload-card">
          <div class="upload-icon-wrap">
            <svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.5" width="48" height="48">
              <rect x="6" y="10" width="36" height="30" rx="4" stroke-opacity="0.4"/>
              <path d="M16 10V8a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v2"/>
              <path d="M24 22v8M20 26l4-4 4 4"/>
              <path d="M16 34h16"/>
            </svg>
          </div>
          <h2 class="upload-title">Carica il tuo file</h2>
          <p class="upload-desc">Seleziona il file <code>.mmbak</code> esportato da Money Manager.</p>
          <label class="upload-btn">
            <svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16"><path d="M10 2v10M6 6l4-4 4 4"/><path d="M3 14v2a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-2"/></svg>
            Seleziona file
            <input type="file" accept=".mmbak,.sqlite,.db" @change="handleFileUpload" style="display:none" />
          </label>
          <p class="status-msg" :class="{ 'status-error': isError }">{{ statusMessage }}</p>
          <div class="upload-formats">
            <span class="format-chip">.mmbak</span>
            <span class="format-chip">.sqlite</span>
            <span class="format-chip">.db</span>
          </div>
        </div>
      </div>

      <!-- ── DASHBOARD CONTENT ── -->
      <div v-if="fileLoaded" class="dashboard-content">

        <!-- ── KPI ROW (stile pastello originale) ── -->
        <section class="kpi-row" aria-label="Riepilogo finanziario">

          <div class="kpi-card income-card">
            <div class="kpi-header">
              <h3>Entrate</h3>
              <span class="kpi-icon income-icon">
                <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2.5" width="14" height="14"><path d="M8 13V3M3 8l5-5 5 5"/></svg>
              </span>
            </div>
            <p class="kpi-value" :class="{ 'kpi-animating': animating }">+€ {{ fmt0(currentStats.income) }}</p>
            <p class="kpi-sub">Totale periodo</p>
          </div>

          <div class="kpi-card expense-card">
            <div class="kpi-header">
              <h3>Uscite</h3>
              <span class="kpi-icon expense-icon">
                <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2.5" width="14" height="14"><path d="M8 3v10M3 8l5 5 5-5"/></svg>
              </span>
            </div>
            <p class="kpi-value">-€ {{ fmt0(currentStats.expense) }}</p>
            <p class="kpi-sub">Totale periodo</p>
          </div>

          <div class="kpi-card" :class="currentStats.net >= 0 ? 'net-card' : 'negative-card'">
            <div class="kpi-header">
              <h3>Risparmio</h3>
              <span class="kpi-icon" :class="currentStats.net >= 0 ? 'net-icon' : 'negative-icon'">
                <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><circle cx="8" cy="8" r="5"/><path d="M8 5.5v2.5l1.5 1.5"/></svg>
              </span>
            </div>
            <p class="kpi-value">{{ currentStats.net >= 0 ? '+' : '' }}€ {{ fmt0(currentStats.net) }}</p>
            <p class="kpi-sub">{{ currentStats.net >= 0 ? 'In positivo' : 'In negativo' }}</p>
          </div>

          <div class="kpi-card" :class="currentStats.rate >= targetSavingsPct ? 'rate-card' : (currentStats.rate < 0 ? 'negative-rate' : 'warn-rate')">
            <div class="kpi-header">
              <h3>% Risparmio</h3>
              <span class="kpi-icon" :class="currentStats.rate >= targetSavingsPct ? 'rate-icon' : (currentStats.rate < 0 ? 'negative-icon' : 'warn-icon')">
                <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><path d="M2 12 L5 8 L9 10 L14 4"/></svg>
              </span>
            </div>
            <p class="kpi-value">{{ currentStats.rate.toFixed(1) }}%</p>
            <p class="kpi-sub">Target: {{ targetSavingsPct }}%</p>
          </div>

        </section>

        <!-- ── MID GRID: Budget | Waterfall ── -->
        <section class="mid-grid">

          <!-- BUDGET -->
          <div class="panel budget-panel glass-panel">
            <div class="panel-header">
              <h2 class="panel-title">Budget Mensile</h2>
              <span class="panel-badge">Regola 50/30/20</span>
            </div>
            <div class="budget-body">
              <div class="budget-sliders">
                <div class="budget-settings-row">
                  <div class="budget-input-group">
                    <label>Necessità %</label>
                    <input type="number" v-model.number="budgetSettings.necessity" min="0" max="100" @change="updateNecessity" class="b-input" />
                  </div>
                  <div class="budget-input-group">
                    <label>Extra %</label>
                    <input type="number" v-model.number="budgetSettings.extra" min="0" max="100" @change="updateExtra" class="b-input" />
                  </div>
                  <div class="budget-input-group target-group">
                    <label>Target Risp.</label>
                    <div class="target-val">{{ targetSavingsPct }}%</div>
                  </div>
                </div>

                <div class="budget-row">
                  <div class="budget-meta">
                    <span class="budget-name">Necessità</span>
                    <span class="budget-range">€ {{ fmt0(currentStats.sumNecessity) }} / {{ fmt0(budgetLimits.necessity) }}</span>
                  </div>
                  <div class="budget-pct-badge" :class="getBudgetColorClass(budgetUsedPcts.necessity)">
                    {{ budgetUsedPcts.necessity.toFixed(0) }}% usato
                  </div>
                  <div class="progress-track">
                    <div class="progress-bar" :class="getBudgetBgClass(budgetUsedPcts.necessity)" :style="{ width: Math.min(budgetUsedPcts.necessity, 100) + '%' }"></div>
                  </div>
                </div>

                <div class="budget-row">
                  <div class="budget-meta">
                    <span class="budget-name">Extra / Svago</span>
                    <span class="budget-range">€ {{ fmt0(currentStats.sumExtra) }} / {{ fmt0(budgetLimits.extra) }}</span>
                  </div>
                  <div class="budget-pct-badge" :class="getBudgetColorClass(budgetUsedPcts.extra)">
                    {{ budgetUsedPcts.extra.toFixed(0) }}% usato
                  </div>
                  <div class="progress-track">
                    <div class="progress-bar" :class="getBudgetBgClass(budgetUsedPcts.extra)" :style="{ width: Math.min(budgetUsedPcts.extra, 100) + '%' }"></div>
                  </div>
                </div>

                <div class="budget-savings-row">
                  <div class="savings-left">
                    <span class="savings-label">🎯 Target Risparmio</span>
                    <span class="savings-amount">€ {{ fmt0(currentStats.income * targetSavingsPct / 100) }}</span>
                  </div>
                  <div class="savings-right">
                    <span class="target-big">{{ targetSavingsPct }}%</span>
                    <span class="target-note">delle entrate</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- CASHFLOW WATERFALL (effetto vetro) -->
          <div class="panel cashflow-panel glass-panel">
            <div class="panel-header">
              <h2 class="panel-title">Flusso di Cassa</h2>
              <span class="panel-badge">CashFlow</span>
            </div>
            <div class="chart-wrap">
              <Chart
                v-if="waterfallData"
                type="bar"
                :data="waterfallData"
                :options="waterfallOptions"
                :plugins="waterfallPlugins"
                style="height:100%;width:100%"
              />
              <div v-else class="chart-empty">
                <svg viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="1.5" width="36" height="36" opacity="0.3"><rect x="4" y="20" width="8" height="16" rx="1"/><rect x="16" y="12" width="8" height="24" rx="1"/><rect x="28" y="4" width="8" height="32" rx="1"/></svg>
                <p>Nessun dato</p>
              </div>
            </div>
          </div>

        </section>

        <!-- ── ANALYSIS TABS (Trend + Storico) ── -->
        <section class="panel tabs-panel">
          <Tabs :value="activeBottomTab" @update:value="activeBottomTab = $event">
            <TabList class="tab-list-custom">
              <Tab value="trend" class="tab-custom">
                <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><path d="M2 12 L5 8 L9 10 L14 4"/></svg>
                Trend 12 Mesi
              </Tab>
              <Tab value="storico" class="tab-custom">
                <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><circle cx="8" cy="8" r="6"/><path d="M8 4v4l3 2"/></svg>
                Storico
              </Tab>
            </TabList>
            <TabPanels>
              <TabPanel value="trend">
                <div class="placeholder-state">
                  <svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.5" width="48" height="48" class="placeholder-icon"><path d="M4 36 L12 24 L20 28 L28 18 L36 22 L44 12"/><circle cx="12" cy="24" r="2" fill="currentColor"/><circle cx="20" cy="28" r="2" fill="currentColor"/><circle cx="28" cy="18" r="2" fill="currentColor"/><circle cx="36" cy="22" r="2" fill="currentColor"/></svg>
                  <h3>Trend 12 Mesi</h3>
                  <p>Prossimamente: grafico lineare con l'andamento mensile di entrate e uscite.</p>
                  <span class="coming-soon-badge">In sviluppo</span>
                </div>
              </TabPanel>
              <TabPanel value="storico">
                <div class="placeholder-state">
                  <svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.5" width="48" height="48" class="placeholder-icon"><circle cx="24" cy="24" r="18"/><path d="M24 12v12l8 6"/></svg>
                  <h3>Storico Cumulativo</h3>
                  <p>Prossimamente: andamento totale del risparmio nel tempo.</p>
                  <span class="coming-soon-badge">In sviluppo</span>
                </div>
              </TabPanel>
            </TabPanels>
          </Tabs>
        </section>

      </div><!-- /dashboard-content -->
    </main>

    <!-- ── FOOTER ── -->
    <footer v-if="fileLoaded" class="mm-footer">
      <span class="footer-file">{{ loadedFileName }}</span>
      <span class="footer-dot">·</span>
      <span class="footer-status" :class="{ 'footer-error': isError }">{{ statusMessage }}</span>
    </footer>

  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import initSqlJs from 'sql.js';
import Chart from 'primevue/chart';
import Tabs from 'primevue/tabs';
import TabList from 'primevue/tablist';
import Tab from 'primevue/tab';
import TabPanels from 'primevue/tabpanels';
import TabPanel from 'primevue/tabpanel';
import annotationPlugin from 'chartjs-plugin-annotation';
import { Chart as ChartJS } from 'chart.js';

ChartJS.register(annotationPlugin);

// ── TEMA ──
const theme = ref(window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
const toggleTheme = () => { theme.value = theme.value === 'dark' ? 'light' : 'dark'; };

// ── STATO ──
let dbInstance = null;
const selectedPeriod = ref('current_month');
const statusMessage = ref('In attesa del file...');
const isError = ref(false);
const fileLoaded = ref(false);
const loadedFileName = ref('');
const animating = ref(false);
const activeBottomTab = ref('trend');

const currentStats = ref({ income: 0, expense: 0, net: 0, rate: 0, sumNecessity: 0, sumExtra: 0 });

// ── TOP 10 DATI ──
// ── BUDGET ──
const budgetSettings = ref({ necessity: 50, extra: 30 });
const targetSavingsPct = computed(() => Math.max(0, 100 - budgetSettings.value.necessity - budgetSettings.value.extra));

const updateNecessity = () => {
  let n = Math.min(100, Math.max(0, budgetSettings.value.necessity || 0));
  budgetSettings.value.necessity = n;
  if (n + budgetSettings.value.extra > 100) budgetSettings.value.extra = 100 - n;
  refreshData();
};
const updateExtra = () => {
  let e = Math.min(100, Math.max(0, budgetSettings.value.extra || 0));
  budgetSettings.value.extra = e;
  if (budgetSettings.value.necessity + e > 100) budgetSettings.value.necessity = 100 - e;
  refreshData();
};

const budgetLimits = computed(() => ({
  necessity: currentStats.value.income * (budgetSettings.value.necessity / 100),
  extra: currentStats.value.income * (budgetSettings.value.extra / 100),
}));
const budgetUsedPcts = computed(() => ({
  necessity: budgetLimits.value.necessity > 0 ? (currentStats.value.sumNecessity / budgetLimits.value.necessity) * 100 : 0,
  extra: budgetLimits.value.extra > 0 ? (currentStats.value.sumExtra / budgetLimits.value.extra) * 100 : 0,
}));

const getBudgetColorClass = (pct) => pct >= 100 ? 'clr-danger' : pct >= 80 ? 'clr-warn' : 'clr-ok';
const getBudgetBgClass = (pct) => pct >= 100 ? 'bar-danger' : pct >= 80 ? 'bar-warn' : 'bar-ok';

// ── FORMATO ──
const fmt0 = (n) => Math.abs(Math.round(n || 0)).toLocaleString('it-IT');

// ── WATERFALL ──
const waterfallData = ref(null);
const waterfallOptions = ref({});

const buildWaterfallOptions = () => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: {
      backgroundColor: theme.value === 'dark' ? 'rgba(28,27,25,0.95)' : 'rgba(15,23,42,0.95)',
      titleColor: '#94a3b8',
      bodyColor: '#f1f5f9',
      padding: 12,
      cornerRadius: 8,
      borderColor: theme.value === 'dark' ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)',
      borderWidth: 1,
      callbacks: {
        label: (ctx) => ` € ${Math.round(Math.abs(ctx.raw[1] - ctx.raw[0])).toLocaleString('it-IT')}`
      }
    },
    annotation: {
      annotations: {
        targetLine: {
          type: 'line',
          yMin: currentStats.value.income * (targetSavingsPct.value / 100),
          yMax: currentStats.value.income * (targetSavingsPct.value / 100),
          borderColor: '#f59e0b',
          borderWidth: 2,
          borderDash: [5, 5],
          label: {
            display: true,
            content: `Target ${targetSavingsPct.value}%`,
            position: 'end',
            backgroundColor: theme.value === 'dark' ? 'rgba(217,119,6,0.15)' : 'rgba(254,243,199,0.9)',
            color: theme.value === 'dark' ? '#fbbf24' : '#d97706',
            font: { weight: '700', size: 10, family: 'Inter, sans-serif' },
            borderRadius: 4,
            padding: { x: 6, y: 3 }
          }
        }
      }
    }
  },
  scales: {
    x: {
      grid: { display: false },
      border: { display: false },
      ticks: {
        font: { size: 12, weight: '600', family: 'Inter, sans-serif' },
        color: theme.value === 'dark' ? '#94a3b8' : '#64748b'
      }
    },
    y: {
      beginAtZero: true,
      grace: '15%',
      border: { display: false },
      grid: { color: theme.value === 'dark' ? 'rgba(255,255,255,0.04)' : 'rgba(0,0,0,0.04)' },
      ticks: {
        font: { size: 11, family: 'Inter, sans-serif' },
        color: theme.value === 'dark' ? '#64748b' : '#94a3b8',
        callback: (v) => `€ ${v >= 1000 ? (v / 1000).toFixed(1) + 'k' : v}`
      }
    }
  }
});

// Effetto vetro: colori con glassmorphism (fill semitrasparente + bordo scuro)
const glassColors = (isDark) => ({
  income:  { bg: isDark ? 'rgba(16,185,129,0.60)' : 'rgba(16,185,129,0.55)', border: isDark ? '#059669' : '#065f46' },
  expense: { bg: isDark ? 'rgba(239,68,68,0.60)'  : 'rgba(239,68,68,0.55)',  border: isDark ? '#dc2626' : '#991b1b' },
  net:     { bg: isDark ? 'rgba(59,130,246,0.60)'  : 'rgba(59,130,246,0.55)', border: isDark ? '#2563eb' : '#1e3a8a' },
});

const waterfallConnector = {
  id: 'waterfallConnector',
  afterDatasetsDraw(chart) {
    const ctx = chart.ctx;
    const meta = chart.getDatasetMeta(0);
    ctx.save();
    ctx.strokeStyle = 'rgba(148,163,184,0.4)';
    ctx.lineWidth = 1.5;
    ctx.setLineDash([4, 4]);
    for (let i = 0; i < meta.data.length - 1; i++) {
      const b1 = meta.data[i], b2 = meta.data[i + 1];
      ctx.beginPath();
      ctx.moveTo(b1.x + b1.width / 2, b2.y);
      ctx.lineTo(b2.x - b2.width / 2, b2.y);
      ctx.stroke();
    }
    ctx.restore();
  }
};
const waterfallPlugins = ref([waterfallConnector]);

// ── CARICAMENTO FILE ──
const handleFileUpload = async (event) => {
  const file = event.target.files[0];
  if (!file) return;
  try {
    statusMessage.value = 'Apertura database...';
    isError.value = false;
    loadedFileName.value = file.name;
    const buf = await file.arrayBuffer();
    const SQL = await initSqlJs({ locateFile: f => `/sql-wasm.wasm` });
    dbInstance = new SQL.Database(new Uint8Array(buf));
    fileLoaded.value = true;
    refreshData();
  } catch (err) {
    isError.value = true;
    statusMessage.value = 'Errore: ' + err.message;
  }
};

// ── REFRESH DATI ──
const refreshData = () => {
  if (!dbInstance) return;
  try {
    animating.value = true;
    setTimeout(() => { animating.value = false; }, 500);

    const now = new Date();
    const y = now.getFullYear(), m = now.getMonth();
    let startMs = 0, endMs = Date.now();

    if (selectedPeriod.value === 'current_month') startMs = new Date(y, m, 1).getTime();
    else if (selectedPeriod.value === 'last_month') { startMs = new Date(y, m - 1, 1).getTime(); endMs = new Date(y, m, 0, 23, 59, 59, 999).getTime(); }
    else if (selectedPeriod.value === 'ytd') startMs = new Date(y, 0, 1).getTime();

    const run = (q) => { const r = dbInstance.exec(q); return (r.length > 0 && r[0].values[0][0]) ? r[0].values[0][0] : 0; };

    const income = run(`SELECT SUM(ZMONEY) FROM INOUTCOME WHERE DO_TYPE=0 AND CAST(ZDATE AS REAL) >= ${startMs} AND CAST(ZDATE AS REAL) <= ${endMs}`);
    const expense = run(`SELECT SUM(ZMONEY) FROM INOUTCOME WHERE DO_TYPE=1 AND CAST(ZDATE AS REAL) >= ${startMs} AND CAST(ZDATE AS REAL) <= ${endMs}`);
    const net = income - expense;
    const rate = income > 0 ? (net / income) * 100 : 0;

    let sumNecessity = 0, sumExtra = 0;
    const r2 = dbInstance.exec(`
      SELECT ASSETS.NIC_NAME, SUM(INOUTCOME.ZMONEY)
      FROM INOUTCOME LEFT JOIN ASSETS ON INOUTCOME.assetUid = ASSETS.uid
      WHERE INOUTCOME.DO_TYPE=1 AND CAST(INOUTCOME.ZDATE AS REAL) >= ${startMs} AND CAST(INOUTCOME.ZDATE AS REAL) <= ${endMs}
      GROUP BY ASSETS.uid
    `);
    if (r2.length > 0) r2[0].values.forEach(([name, val]) => {
      String(name || '').toLowerCase().includes('necess') ? sumNecessity += val : sumExtra += val;
    });

    currentStats.value = { income, expense, net, rate, sumNecessity, sumExtra };

    // ── WATERFALL ──
    const s1 = income, s2 = s1 - sumNecessity, s3 = s2 - sumExtra;
    const isDark = theme.value === 'dark';
    const gc = glassColors(isDark);

    waterfallData.value = {
      labels: ['Entrate', 'Necessità', 'Extra', 'Netto'],
      datasets: [{
        label: 'Flusso',
        data: [[0, s1], [s2, s1], [s3, s2], [0, s3]],
        backgroundColor: [gc.income.bg, gc.expense.bg, gc.expense.bg, gc.net.bg],
        borderColor:     [gc.income.border, gc.expense.border, gc.expense.border, gc.net.border],
        borderWidth: 2,
        borderRadius: 6,
        borderSkipped: false
      }]
    };
    waterfallOptions.value = buildWaterfallOptions();

    statusMessage.value = 'Aggiornato · ' + new Date().toLocaleTimeString('it-IT', { hour: '2-digit', minute: '2-digit' });
    isError.value = false;
  } catch (err) {
    console.error(err);
    statusMessage.value = 'Errore: ' + err.message;
    isError.value = true;
  }
};
</script>

<style scoped>
/* ════════════════════════════════
   DESIGN TOKENS
════════════════════════════════ */
.mm-app {
  --bg:         #f8fafc;
  --surface:    #ffffff;
  --surface-2:  #f1f5f9;
  --border:     rgba(15,23,42,0.08);
  --divider:    rgba(15,23,42,0.05);
  --text:       #0f172a;
  --text-muted: #64748b;
  --text-faint: #94a3b8;
  --primary:    #0f172a;
  --primary-hl: #e2e8f0;
  --font: 'Inter', system-ui, sans-serif;
  --r-sm: 6px; --r-md: 10px; --r-lg: 16px; --r-xl: 20px;
  --sh-sm: 0 1px 3px rgba(15,23,42,0.06), 0 1px 2px rgba(15,23,42,0.04);
  --sh-md: 0 4px 16px rgba(15,23,42,0.08), 0 2px 4px rgba(15,23,42,0.04);
  --s1:4px;--s2:8px;--s3:12px;--s4:16px;--s5:20px;--s6:24px;--s8:32px;--s10:40px;--s12:48px;

  background: var(--bg);
  color: var(--text);
  font-family: var(--font);
  font-size: 15px;
  line-height: 1.5;
  min-height: 100dvh;
  transition: background 0.2s, color 0.2s;
}
.mm-app[data-theme="dark"] {
  --bg:         #0f172a;
  --surface:    #1e293b;
  --surface-2:  #0f172a;
  --border:     rgba(248,250,252,0.08);
  --divider:    rgba(248,250,252,0.04);
  --text:       #f1f5f9;
  --text-muted: #94a3b8;
  --text-faint: #475569;
  --primary:    #f1f5f9;
  --primary-hl: #1e293b;
  --sh-sm: 0 1px 3px rgba(0,0,0,0.3);
  --sh-md: 0 4px 16px rgba(0,0,0,0.4);
}
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

/* ════════════════════════════════
   HEADER
════════════════════════════════ */
.mm-header {
  position: sticky; top: 0; z-index: 100;
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  box-shadow: var(--sh-sm);
}
.header-inner {
  max-width: 960px; margin: 0 auto;
  display: flex; align-items: center; justify-content: space-between;
  padding: var(--s3) var(--s4); gap: var(--s3);
}
.header-brand { display: flex; align-items: center; gap: var(--s3); }
.brand-logo { width: 30px; height: 30px; color: #3b82f6; flex-shrink: 0; }
.brand-name { font-size: 15px; font-weight: 700; color: var(--text); letter-spacing: -0.02em; display: block; line-height: 1.1; }
.brand-sub { font-size: 11px; font-weight: 500; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; display: block; }
.header-actions { display: flex; align-items: center; gap: var(--s2); }
.period-pill { background: var(--surface-2); border-radius: var(--r-md); border: 1px solid var(--border); }
.period-select {
  background: transparent; border: none; padding: 6px 10px;
  font-size: 13px; font-weight: 600; color: var(--text); cursor: pointer;
  border-radius: var(--r-md); outline: none; font-family: var(--font);
}
.btn-update {
  display: flex; align-items: center; gap: var(--s1);
  background: var(--primary); color: var(--bg);
  padding: 6px 12px; border-radius: var(--r-md);
  font-size: 13px; font-weight: 600; cursor: pointer; border: none; transition: opacity 0.15s;
}
.btn-update:hover { opacity: 0.8; }
.btn-update-text { display: none; }
@media (min-width: 480px) { .btn-update-text { display: inline; } }
.theme-toggle {
  width: 36px; height: 36px; display: flex; align-items: center; justify-content: center;
  background: var(--surface-2); border: 1px solid var(--border);
  border-radius: var(--r-md); color: var(--text-muted); cursor: pointer;
  transition: background 0.15s, color 0.15s;
}
.theme-toggle:hover { background: var(--primary-hl); color: var(--text); }

/* ════════════════════════════════
   MAIN + UPLOAD
════════════════════════════════ */
.mm-main { max-width: 960px; margin: 0 auto; padding: var(--s5) var(--s4) var(--s12); }
.upload-screen {
  display: flex; justify-content: center; align-items: center;
  min-height: calc(100dvh - 130px); padding: var(--s8) 0;
}
.upload-card {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: var(--r-xl); padding: var(--s10) var(--s8);
  max-width: 420px; width: 100%; text-align: center; box-shadow: var(--sh-md);
}
.upload-icon-wrap {
  width: 80px; height: 80px; border-radius: var(--r-lg);
  background: #dbeafe; color: #1d4ed8;
  display: flex; align-items: center; justify-content: center; margin: 0 auto var(--s6);
}
.upload-title { font-size: 20px; font-weight: 700; color: var(--text); margin-bottom: var(--s2); letter-spacing: -0.02em; }
.upload-desc { font-size: 14px; color: var(--text-muted); max-width: 32ch; margin: 0 auto var(--s6); line-height: 1.6; }
.upload-desc code { background: var(--surface-2); padding: 1px 6px; border-radius: 4px; font-size: 12px; font-family: monospace; color: #3b82f6; }
.upload-btn {
  display: inline-flex; align-items: center; gap: var(--s2);
  background: #0f172a; color: white;
  padding: 10px 20px; border-radius: var(--r-md);
  font-size: 14px; font-weight: 600; cursor: pointer; transition: opacity 0.15s; margin-bottom: var(--s4);
}
.upload-btn:hover { opacity: 0.85; }
.status-msg { font-size: 13px; color: var(--text-muted); margin-bottom: var(--s4); min-height: 20px; }
.status-error { color: #e11d48 !important; }
.upload-formats { display: flex; justify-content: center; gap: var(--s2); }
.format-chip {
  font-size: 11px; padding: 3px 8px; border-radius: var(--r-sm);
  background: var(--surface-2); color: var(--text-muted);
  border: 1px solid var(--border); font-family: monospace;
}

/* ════════════════════════════════
   KPI CARDS — stile pastello originale
════════════════════════════════ */
.kpi-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.8rem;
  margin-bottom: 1.5rem;
}
@media (min-width: 640px) { .kpi-row { grid-template-columns: repeat(4, 1fr); } }

.kpi-card {
  padding: 1rem; border-radius: 16px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
.kpi-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.6rem; }
.kpi-header h3 { margin: 0; font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em; }
.kpi-value { margin: 0; font-size: 1.45rem; font-weight: 800; letter-spacing: -0.03em; font-variant-numeric: tabular-nums lining-nums; transition: opacity 0.3s; }
.kpi-animating { opacity: 0.3; }
.kpi-sub { margin: 0.3rem 0 0; font-size: 0.72rem; font-weight: 500; opacity: 0.7; }
.kpi-icon {
  display: flex; justify-content: center; align-items: center;
  width: 28px; height: 28px; border-radius: 50%;
}

/* Colori pastello */
.income-card  { background-color: #d1fae5; }
.income-card  h3, .income-card .kpi-value { color: #065f46; }
.income-card  .kpi-sub { color: #065f46; }
.income-icon  { background-color: #059669; color: #fff; }

.expense-card { background-color: #fee2e2; }
.expense-card h3, .expense-card .kpi-value { color: #991b1b; }
.expense-card .kpi-sub { color: #991b1b; }
.expense-icon { background-color: #e11d48; color: #fff; }

.net-card     { background-color: #dbeafe; }
.net-card     h3, .net-card .kpi-value { color: #1e3a8a; }
.net-card     .kpi-sub { color: #1e3a8a; }
.net-icon     { background-color: #2563eb; color: #fff; }

.negative-card { background-color: #ffedd5; }
.negative-card h3, .negative-card .kpi-value { color: #9a3412; }
.negative-card .kpi-sub { color: #9a3412; }
.negative-icon { background-color: #ea580c; color: #fff; }

.rate-card    { background-color: #ede9fe; }
.rate-card    h3, .rate-card .kpi-value { color: #3730a3; }
.rate-card    .kpi-sub { color: #3730a3; }
.rate-icon    { background-color: #4f46e5; color: #fff; }

.warn-rate    { background-color: #fef9c3; }
.warn-rate    h3, .warn-rate .kpi-value { color: #854d0e; }
.warn-rate    .kpi-sub { color: #854d0e; }
.warn-icon    { background-color: #d97706; color: #fff; }

.negative-rate { background-color: #fce7f3; }
.negative-rate h3, .negative-rate .kpi-value { color: #be123c; }
.negative-rate .kpi-sub { color: #be123c; }

/* dark override kpi */
.mm-app[data-theme="dark"] .income-card  { background-color: rgba(16,185,129,0.15); }
.mm-app[data-theme="dark"] .income-card  h3,
.mm-app[data-theme="dark"] .income-card  .kpi-value,
.mm-app[data-theme="dark"] .income-card  .kpi-sub { color: #34d399; }
.mm-app[data-theme="dark"] .expense-card { background-color: rgba(239,68,68,0.15); }
.mm-app[data-theme="dark"] .expense-card h3,
.mm-app[data-theme="dark"] .expense-card .kpi-value,
.mm-app[data-theme="dark"] .expense-card .kpi-sub { color: #f87171; }
.mm-app[data-theme="dark"] .net-card     { background-color: rgba(59,130,246,0.15); }
.mm-app[data-theme="dark"] .net-card     h3,
.mm-app[data-theme="dark"] .net-card     .kpi-value,
.mm-app[data-theme="dark"] .net-card     .kpi-sub { color: #93c5fd; }
.mm-app[data-theme="dark"] .negative-card { background-color: rgba(234,88,12,0.15); }
.mm-app[data-theme="dark"] .negative-card h3,
.mm-app[data-theme="dark"] .negative-card .kpi-value,
.mm-app[data-theme="dark"] .negative-card .kpi-sub { color: #fb923c; }
.mm-app[data-theme="dark"] .rate-card    { background-color: rgba(79,70,229,0.15); }
.mm-app[data-theme="dark"] .rate-card    h3,
.mm-app[data-theme="dark"] .rate-card    .kpi-value,
.mm-app[data-theme="dark"] .rate-card    .kpi-sub { color: #a5b4fc; }
.mm-app[data-theme="dark"] .warn-rate    { background-color: rgba(217,119,6,0.15); }
.mm-app[data-theme="dark"] .warn-rate    h3,
.mm-app[data-theme="dark"] .warn-rate    .kpi-value,
.mm-app[data-theme="dark"] .warn-rate    .kpi-sub { color: #fcd34d; }
.mm-app[data-theme="dark"] .negative-rate { background-color: rgba(190,18,60,0.15); }
.mm-app[data-theme="dark"] .negative-rate h3,
.mm-app[data-theme="dark"] .negative-rate .kpi-value,
.mm-app[data-theme="dark"] .negative-rate .kpi-sub { color: #fb7185; }

/* ════════════════════════════════
   MID GRID
════════════════════════════════ */
.mid-grid {
  display: grid; grid-template-columns: 1fr;
  gap: 1rem; margin-bottom: 1rem;
}
@media (min-width: 680px) { .mid-grid { grid-template-columns: 1fr 1fr; } }

.panel {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: var(--r-lg); overflow: hidden; box-shadow: var(--sh-sm);
}
.panel-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: var(--s3) var(--s4); border-bottom: 1px solid var(--divider);
}
.panel-title { font-size: 14px; font-weight: 700; color: var(--text); letter-spacing: -0.01em; }
.panel-badge {
  font-size: 11px; font-weight: 600; color: #3b82f6;
  background: #dbeafe; padding: 3px 8px; border-radius: var(--r-sm);
  text-transform: uppercase; letter-spacing: 0.04em;
}
.mm-app[data-theme="dark"] .panel-badge { background: rgba(59,130,246,0.15); color: #93c5fd; }

/* ── Budget body ── */
.budget-body { padding: var(--s4); }

/* ── BUDGET CONTENT ── */
.budget-sliders { display: flex; flex-direction: column; gap: var(--s4); }
.budget-settings-row {
  display: flex; justify-content: space-between; gap: var(--s2);
  background: var(--surface-2); padding: var(--s3); border-radius: var(--r-md);
  border: 1px solid var(--border);
}
.budget-input-group { display: flex; flex-direction: column; gap: 4px; align-items: flex-start; }
.budget-input-group label { font-size: 0.7rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.04em; }
.b-input {
  width: 56px; padding: 5px 6px; border-radius: var(--r-sm);
  border: 1px solid var(--border); background: var(--surface);
  font-size: 13px; font-weight: 700; text-align: center; color: var(--text);
  outline: none; font-family: var(--font);
}
.b-input:focus { border-color: #3b82f6; }
.target-group { align-items: flex-end; }
.target-val { font-size: 1.3rem; font-weight: 800; color: #d97706; font-variant-numeric: tabular-nums; }

.budget-row { display: flex; flex-direction: column; gap: var(--s1); }
.budget-meta { display: flex; justify-content: space-between; align-items: baseline; }
.budget-name { font-size: 13px; font-weight: 600; color: var(--text); }
.budget-range { font-size: 12px; color: var(--text-muted); font-variant-numeric: tabular-nums; }
.budget-pct-badge { font-size: 11px; font-weight: 700; }
.clr-ok     { color: #059669; }
.clr-warn   { color: #d97706; }
.clr-danger { color: #e11d48; }
.progress-track {
  height: 11px;
  background: rgba(255,255,255,0.35);
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
  border-radius: 6px;
  overflow: hidden;
  border: 1px solid rgba(255,255,255,0.55);
  box-shadow: inset 0 1px 3px rgba(0,0,0,0.1);
}
.mm-app[data-theme="dark"] .progress-track {
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.1);
  box-shadow: inset 0 1px 3px rgba(0,0,0,0.3);
}
.progress-bar {
  height: 100%; border-radius: 6px;
  transition: width 0.4s cubic-bezier(0.16,1,0.3,1);
  box-shadow: 0 1px 4px rgba(0,0,0,0.15);
}
.bar-ok     { background: linear-gradient(90deg, #059669, #10b981); }
.bar-warn   { background: linear-gradient(90deg, #d97706, #f59e0b); }
.bar-danger { background: linear-gradient(90deg, #dc2626, #ef4444); }

.budget-savings-row {
  display: flex; justify-content: space-between; align-items: center;
  background: var(--surface-2); border-radius: var(--r-md);
  padding: var(--s3); border: 1px solid var(--border);
}
.savings-left { display: flex; flex-direction: column; gap: 2px; }
.savings-label { font-size: 12px; font-weight: 600; color: var(--text-muted); }
.savings-amount { font-size: 13px; font-weight: 700; color: var(--text); font-variant-numeric: tabular-nums; }
.savings-right { display: flex; flex-direction: column; align-items: flex-end; }
.target-big { font-size: 26px; font-weight: 800; color: #d97706; letter-spacing: -0.03em; font-variant-numeric: tabular-nums; }
.target-note { font-size: 11px; color: var(--text-muted); }



/* ── CASHFLOW GLASS PANEL ── */
.glass-panel {
  background: rgba(255,255,255,0.55);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255,255,255,0.7);
  box-shadow: 0 4px 24px rgba(15,23,42,0.08), inset 0 1px 0 rgba(255,255,255,0.8);
}
.mm-app[data-theme="dark"] .glass-panel {
  background: rgba(30,41,59,0.6);
  border: 1px solid rgba(255,255,255,0.07);
  box-shadow: 0 4px 24px rgba(0,0,0,0.35), inset 0 1px 0 rgba(255,255,255,0.05);
}
.cashflow-panel .chart-wrap { height: 260px; padding: var(--s3) var(--s4) var(--s4); position: relative; }
.chart-empty {
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  height: 100%; gap: var(--s3); color: var(--text-muted);
}
.chart-empty p { font-size: 13px; }

/* ════════════════════════════════
   BOTTOM TABS (Trend + Storico)
════════════════════════════════ */
.tabs-panel { overflow: hidden; }
:deep(.p-tablist-tab-list) { background: var(--surface-2) !important; border-bottom: 1px solid var(--border); padding: 0 var(--s4); display: flex; }
:deep(.p-tab) {
  display: flex; align-items: center; gap: var(--s1);
  padding: var(--s3) var(--s4); font-size: 13px; font-weight: 600;
  color: var(--text-muted); border: none; background: transparent; cursor: pointer;
  border-bottom: 2px solid transparent; transition: color 0.15s, border-color 0.15s;
  font-family: var(--font);
}
:deep(.p-tab-active) { color: var(--text) !important; border-bottom-color: #3b82f6 !important; }
:deep(.p-tabpanels) { padding: 0; background: var(--surface) !important; }
:deep(.p-tabpanel) { padding: var(--s5); }

.placeholder-state {
  display: flex; flex-direction: column; align-items: center;
  text-align: center; padding: var(--s12) var(--s8); gap: var(--s3);
}
.placeholder-icon { color: var(--text-faint); margin-bottom: var(--s2); }
.placeholder-state h3 { font-size: 16px; font-weight: 700; color: var(--text); }
.placeholder-state p { font-size: 13px; color: var(--text-muted); max-width: 36ch; line-height: 1.6; }
.coming-soon-badge {
  font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em;
  background: #dbeafe; color: #1d4ed8;
  padding: 4px 10px; border-radius: var(--r-sm); margin-top: var(--s1);
}
.mm-app[data-theme="dark"] .coming-soon-badge { background: rgba(59,130,246,0.15); color: #93c5fd; }

/* ════════════════════════════════
   FOOTER
════════════════════════════════ */
.mm-footer {
  max-width: 960px; margin: 0 auto;
  padding: var(--s3) var(--s4) var(--s6);
  display: flex; align-items: center; gap: var(--s2);
  font-size: 12px; color: var(--text-faint);
  border-top: 1px solid var(--divider);
}
.footer-file { font-weight: 600; color: var(--text-muted); font-family: monospace; }
.footer-dot { opacity: 0.4; }
.footer-error { color: #e11d48; }
</style>
