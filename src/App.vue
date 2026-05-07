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

          <!-- CASHFLOW — tab Cascata + Top Categorie -->
          <div class="panel cashflow-panel glass-panel">
            <Tabs :value="activeCfTab" @update:value="activeCfTab = $event">
              <TabList class="cf-tablist">
                <Tab value="cascata" class="cf-tab">
                  <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" width="13" height="13"><rect x="2" y="4" width="3" height="8" rx="1"/><rect x="7" y="2" width="3" height="10" rx="1"/><rect x="12" y="6" width="3" height="6" rx="1"/></svg>
                  Cascata
                </Tab>
                <Tab value="topcat" class="cf-tab">
                  <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" width="13" height="13"><path d="M3 4h10M3 8h7M3 12h5"/></svg>
                  Top Categorie
                </Tab>
              </TabList>
              <TabPanels>
                <TabPanel value="cascata">
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
                </TabPanel>
                <TabPanel value="topcat">
                  <div class="chart-wrap topcat-wrap">
                    <Chart
                      v-if="topCatData"
                      type="bar"
                      :data="topCatData"
                      :options="topCatOptions"
                      style="height:100%;width:100%"
                    />
                    <div v-else class="chart-empty">
                      <svg viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="1.5" width="36" height="36" opacity="0.3"><path d="M6 10h28M6 20h20M6 30h14"/></svg>
                      <p>Nessun dato disponibile</p>
                    </div>
                  </div>
                </TabPanel>
              </TabPanels>
            </Tabs>
          </div>

        </section>

        <!-- ── ANALYSIS TABS ── -->
        <section class="panel tabs-panel">
          <Tabs :value="activeBottomTab" @update:value="activeBottomTab = $event">
            <TabList class="tab-list-custom">
              <Tab value="trend" class="tab-custom">
                <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><path d="M2 12 L5 8 L9 10 L14 4"/></svg>
                Trend 12 Mesi
              </Tab>
              <Tab value="storico" class="tab-custom">
                <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><rect x="3" y="3" width="10" height="10" rx="2"/><path d="M8 6v4"/></svg>
                Storico Cumulativo
              </Tab>
              <Tab value="dettaglio" class="tab-custom">
                <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><rect x="2" y="9" width="3" height="5" rx="1"/><rect x="7" y="5" width="3" height="9" rx="1"/><rect x="12" y="2" width="3" height="12" rx="1"/></svg>
                Dettaglio Mese
              </Tab>
            </TabList>
            <TabPanels>

              <!-- TAB 1: TREND 12 MESI -->
              <TabPanel value="trend">
                <div v-if="trend12BarData" class="chart-tab-body">
                  <!-- KPI summary -->
                  <div class="trend-summary-row">
                    <div class="trend-stat">
                      <span class="trend-stat-label">Media Entrate</span>
                      <span class="trend-stat-val income-text">€ {{ fmt0(trendSummary.avgIncome) }}</span>
                    </div>
                    <div class="trend-stat">
                      <span class="trend-stat-label">Media Uscite</span>
                      <span class="trend-stat-val expense-text">€ {{ fmt0(trendSummary.avgExpense) }}</span>
                    </div>
                    <div class="trend-stat">
                      <span class="trend-stat-label">Mese Migliore</span>
                      <span class="trend-stat-val net-text">{{ trendSummary.bestMonth }}</span>
                    </div>
                    <div class="trend-stat">
                      <span class="trend-stat-label">Mese Peggiore</span>
                      <span class="trend-stat-val expense-text">{{ trendSummary.worstMonth }}</span>
                    </div>
                  </div>

                  <!-- Grafico 1: Barre affiancate Entrate vs Uscite -->
                  <div class="trend-chart-block">
                    <div class="trend-chart-label">
                      <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" width="13" height="13"><rect x="2" y="8" width="4" height="6" rx="1"/><rect x="10" y="4" width="4" height="10" rx="1"/></svg>
                      Entrate vs Uscite
                    </div>
                    <div class="chart-wrap-tall">
                      <Chart type="bar" :data="trend12BarData" :options="trend12BarOptions" style="height:100%;width:100%" />
                    </div>
                  </div>

                  <!-- Grafico 2: Risparmio cumulativo 12 mesi -->
                  <div class="trend-chart-block">
                    <div class="trend-chart-label">
                      <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" width="13" height="13"><path d="M2 13 C4 10 6 11 8 8 S12 3 14 3"/><path d="M2 13 L14 3 L14 13 Z" fill="currentColor" opacity="0.15"/></svg>
                      Percorso del Risparmio
                    </div>
                    <div class="chart-wrap-tall">
                      <Chart type="line" :data="trend12CumData" :options="trend12CumOptions" style="height:100%;width:100%" />
                    </div>
                  </div>
                </div>
                <div v-else class="chart-empty">
                  <svg viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="1.5" width="36" height="36" opacity="0.3"><path d="M4 30 L12 20 L20 22 L28 12 L36 15"/></svg>
                  <p>Nessun dato disponibile</p>
                </div>
              </TabPanel>

              <!-- TAB 2: STORICO CUMULATIVO -->
              <TabPanel value="storico">
                <div v-if="storicoData" class="chart-tab-body">
                  <div class="trend-summary-row">
                    <div class="trend-stat">
                      <span class="trend-stat-label">Risparmio Totale</span>
                      <span class="trend-stat-val net-text">€ {{ fmt0(storicoSummary.totalNet) }}</span>
                    </div>
                    <div class="trend-stat">
                      <span class="trend-stat-label">Massimo Storico</span>
                      <span class="trend-stat-val income-text">€ {{ fmt0(storicoSummary.maxCumulative) }}</span>
                    </div>
                    <div class="trend-stat">
                      <span class="trend-stat-label">Mesi Analizzati</span>
                      <span class="trend-stat-val">{{ storicoSummary.months }}</span>
                    </div>
                    <div class="trend-stat">
                      <span class="trend-stat-label">Media Mensile</span>
                      <span class="trend-stat-val net-text">€ {{ fmt0(storicoSummary.avgMonthly) }}</span>
                    </div>
                  </div>
                  <div class="chart-wrap-tall">
                    <Chart type="line" :data="storicoData" :options="storicoOptions" style="height:100%;width:100%" />
                  </div>
                </div>
                <div v-else class="chart-empty">
                  <svg viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="1.5" width="36" height="36" opacity="0.3"><circle cx="20" cy="20" r="14"/><path d="M20 10v10l6 5"/></svg>
                  <p>Nessun dato disponibile</p>
                </div>
              </TabPanel>

              <!-- TAB 3: DETTAGLIO MESE -->
              <TabPanel value="dettaglio">
                <div class="chart-tab-body">
                  <div class="dettaglio-toolbar">
                    <label class="dettaglio-label">Seleziona mese:</label>
                    <select class="dettaglio-select" v-model="dettaglioMonth" @change="loadDettaglio">
                      <option v-for="m in dettaglioMonthOptions" :key="m.value" :value="m.value">{{ m.label }}</option>
                    </select>
                  </div>
                  <div v-if="dettaglioData" class="dettaglio-grid">
                    <div class="dettaglio-kpi-row">
                      <div class="dettaglio-kpi income-bg">
                        <span class="dettaglio-kpi-label">Entrate</span>
                        <span class="dettaglio-kpi-val">+€ {{ fmt0(dettaglioStats.income) }}</span>
                      </div>
                      <div class="dettaglio-kpi expense-bg">
                        <span class="dettaglio-kpi-label">Uscite</span>
                        <span class="dettaglio-kpi-val">-€ {{ fmt0(dettaglioStats.expense) }}</span>
                      </div>
                      <div class="dettaglio-kpi" :class="dettaglioStats.net >= 0 ? 'net-bg' : 'neg-bg'">
                        <span class="dettaglio-kpi-label">Netto</span>
                        <span class="dettaglio-kpi-val">{{ dettaglioStats.net >= 0 ? '+' : '' }}€ {{ fmt0(dettaglioStats.net) }}</span>
                      </div>
                    </div>
                    <div class="chart-wrap-tall">
                      <Chart type="bar" :data="dettaglioData" :options="dettaglioOptions" style="height:100%;width:100%" />
                    </div>
                  </div>
                  <div v-else class="chart-empty">
                    <svg viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="1.5" width="36" height="36" opacity="0.3"><rect x="4" y="20" width="8" height="16" rx="1"/><rect x="16" y="12" width="8" height="24" rx="1"/><rect x="28" y="4" width="8" height="32" rx="1"/></svg>
                    <p>Seleziona un mese per vedere il dettaglio</p>
                  </div>
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
import { ref, computed, watch } from 'vue';
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

// ── CASHFLOW TAB ──
const activeCfTab = ref('cascata');

// ── TOP CATEGORIE ──
const topCatData    = ref(null);
const topCatOptions = ref({});

const loadTopCat = () => {
  if (!dbInstance) return;
  try {
    const now = new Date();
    const y = now.getFullYear(), m = now.getMonth();
    let startMs = 0, endMs = Date.now();
    if (selectedPeriod.value === 'current_month') startMs = new Date(y, m, 1).getTime();
    else if (selectedPeriod.value === 'last_month') { startMs = new Date(y, m - 1, 1).getTime(); endMs = new Date(y, m, 0, 23, 59, 59, 999).getTime(); }
    else if (selectedPeriod.value === 'ytd') startMs = new Date(y, 0, 1).getTime();

    const safeExec = (q) => { try { const r = dbInstance.exec(q); return (r.length && r[0].values) ? r[0].values : []; } catch(e) { return []; } };

    // Prova con JOIN CATEGORY
    let rows = safeExec(`
      SELECT c.ZNAME as cat, SUM(i.ZMONEY) as tot
      FROM INOUTCOME i
      LEFT JOIN CATEGORY c ON i.categoryUid = c.uid
      WHERE i.DO_TYPE = 1
        AND CAST(i.ZDATE AS REAL) >= ${startMs} AND CAST(i.ZDATE AS REAL) <= ${endMs}
        AND c.ZNAME IS NOT NULL AND c.ZNAME != ''
      GROUP BY c.ZNAME ORDER BY tot DESC LIMIT 10
    `);

    // Fallback WDATE
    if (!rows.length) rows = safeExec(`
      SELECT c.ZNAME as cat, SUM(i.ZMONEY) as tot
      FROM INOUTCOME i
      LEFT JOIN CATEGORY c ON i.categoryUid = c.uid
      WHERE i.DO_TYPE = 1
        AND CAST(i.WDATE AS REAL) >= ${startMs} AND CAST(i.WDATE AS REAL) <= ${endMs}
        AND c.ZNAME IS NOT NULL AND c.ZNAME != ''
      GROUP BY c.ZNAME ORDER BY tot DESC LIMIT 10
    `);

    // Fallback NIC_NAME
    if (!rows.length) rows = safeExec(`
      SELECT COALESCE(a.NIC_NAME, 'Altro') as cat, SUM(i.ZMONEY) as tot
      FROM INOUTCOME i
      LEFT JOIN ASSETS a ON i.assetUid = a.uid
      WHERE i.DO_TYPE = 1
        AND CAST(i.ZDATE AS REAL) >= ${startMs} AND CAST(i.ZDATE AS REAL) <= ${endMs}
      GROUP BY a.uid ORDER BY tot DESC LIMIT 10
    `);

    if (!rows.length) { topCatData.value = null; return; }

    const isDark = theme.value === 'dark';
    const labels = rows.map(([cat]) => cat || 'Altro');
    const values = rows.map(([, v]) => Number(v) || 0);
    const maxVal = Math.max(...values);

    // Palette di rossi graduali dal più scuro (top spesa) al più chiaro
    const bgColors = values.map((v) => {
      const ratio = maxVal > 0 ? v / maxVal : 0;
      const alpha = isDark ? 0.30 + ratio * 0.45 : 0.25 + ratio * 0.45;
      return `rgba(239,68,68,${alpha.toFixed(2)})`;
    });
    const borderColors = values.map((v) => {
      const ratio = maxVal > 0 ? v / maxVal : 0;
      return ratio > 0.6 ? (isDark ? '#dc2626' : '#b91c1c') : (isDark ? '#f87171' : '#ef4444');
    });

    topCatData.value = {
      labels,
      datasets: [{
        label: 'Spesa',
        data: values,
        backgroundColor: bgColors,
        borderColor: borderColors,
        borderWidth: 1.5,
        borderRadius: 5,
        borderSkipped: false
      }]
    };

    topCatOptions.value = {
      responsive: true,
      maintainAspectRatio: false,
      indexAxis: 'y',
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: isDark ? 'rgba(28,27,25,0.95)' : 'rgba(15,23,42,0.95)',
          titleColor: isDark ? '#94a3b8' : '#cbd5e1',
          bodyColor: '#f1f5f9',
          padding: 12, cornerRadius: 8,
          borderColor: isDark ? 'rgba(255,255,255,0.08)' : 'rgba(0,0,0,0.08)',
          borderWidth: 1,
          callbacks: {
            label: (ctx) => ` € ${Math.round(ctx.raw).toLocaleString('it-IT')}`,
            afterLabel: (ctx) => {
              const total = values.reduce((a, b) => a + b, 0);
              const pct = total > 0 ? ((ctx.raw / total) * 100).toFixed(1) : 0;
              return ` ${pct}% del totale`;
            }
          }
        }
      },
      scales: {
        x: {
          beginAtZero: true,
          grid: { color: isDark ? 'rgba(255,255,255,0.04)' : 'rgba(0,0,0,0.04)' },
          border: { display: false },
          ticks: {
            font: { size: 10, family: 'Inter, sans-serif' },
            color: isDark ? '#64748b' : '#94a3b8',
            callback: (v) => `€ ${v >= 1000 ? (v/1000).toFixed(0)+'k' : v}`
          }
        },
        y: {
          grid: { display: false },
          border: { display: false },
          ticks: {
            font: { size: 12, weight: '600', family: 'Inter, sans-serif' },
            color: isDark ? '#94a3b8' : '#475569'
          }
        }
      }
    };
  } catch(e) { console.error('loadTopCat:', e); topCatData.value = null; }
};

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
    // Carica anche i grafici storici
    loadTrend12();
    loadStorico();
    loadTopCat();
    buildDettaglioOptions();
    if (dettaglioMonth.value) loadDettaglio();
  } catch (err) {
    console.error(err);
    statusMessage.value = 'Errore: ' + err.message;
    isError.value = true;
  }
};

// ══════════════════════════════════════════════
// TREND 12 MESI
// ══════════════════════════════════════════════
const trend12BarData  = ref(null);
const trend12BarOptions = ref({});
const trend12CumData  = ref(null);
const trend12CumOptions = ref({});
const trendSummary = ref({ avgIncome: 0, avgExpense: 0, bestMonth: '-', worstMonth: '-' });

const MESI = ['Gen','Feb','Mar','Apr','Mag','Giu','Lug','Ago','Set','Ott','Nov','Dic'];

const baseScales = (isDark, extra = {}) => ({
  x: {
    grid: { display: false },
    border: { display: false },
    ticks: { font: { size: 10, weight: '600', family: 'Inter, sans-serif' }, color: isDark ? '#64748b' : '#94a3b8', maxRotation: 0 }
  },
  y: {
    beginAtZero: true,
    grace: '10%',
    border: { display: false },
    grid: { color: isDark ? 'rgba(255,255,255,0.04)' : 'rgba(0,0,0,0.04)' },
    ticks: {
      font: { size: 10, family: 'Inter, sans-serif' },
      color: isDark ? '#64748b' : '#94a3b8',
      callback: (v) => `€ ${v >= 1000 ? (v/1000).toFixed(0)+'k' : v}`
    }
  },
  ...extra
});

const baseTooltip = (isDark) => ({
  backgroundColor: isDark ? 'rgba(28,27,25,0.95)' : 'rgba(15,23,42,0.95)',
  titleColor: isDark ? '#94a3b8' : '#cbd5e1',
  bodyColor: '#f1f5f9',
  padding: 12, cornerRadius: 8,
  borderColor: isDark ? 'rgba(255,255,255,0.08)' : 'rgba(0,0,0,0.08)',
  borderWidth: 1,
  callbacks: { label: (ctx) => ` ${ctx.dataset.label}: € ${Math.round(ctx.raw).toLocaleString('it-IT')}` }
});

const buildLineOptions = (isDark, extraOpts = {}) => ({
  responsive: true,
  maintainAspectRatio: false,
  interaction: { mode: 'index', intersect: false },
  plugins: {
    legend: {
      display: true, position: 'top', align: 'end',
      labels: { boxWidth: 10, boxHeight: 10, borderRadius: 4, font: { size: 11, family: 'Inter, sans-serif', weight: '600' }, color: isDark ? '#94a3b8' : '#64748b', padding: 16, usePointStyle: true, pointStyle: 'circle' }
    },
    tooltip: baseTooltip(isDark)
  },
  scales: baseScales(isDark, extraOpts)
});

const loadTrend12 = () => {
  if (!dbInstance) return;
  try {
    const now = new Date();
    const months = [];
    for (let i = 11; i >= 0; i--) {
      const d = new Date(now.getFullYear(), now.getMonth() - i, 1);
      months.push({ y: d.getFullYear(), m: d.getMonth(), label: MESI[d.getMonth()] + ' ' + String(d.getFullYear()).slice(2) });
    }

    const incomes = [], expenses = [], nets = [];
    months.forEach(({ y, m }) => {
      const start = new Date(y, m, 1).getTime();
      const end   = new Date(y, m + 1, 0, 23, 59, 59, 999).getTime();
      const run   = (q) => { const r = dbInstance.exec(q); return (r.length > 0 && r[0].values[0][0]) ? Number(r[0].values[0][0]) : 0; };
      const inc   = run(`SELECT SUM(ZMONEY) FROM INOUTCOME WHERE DO_TYPE=0 AND CAST(ZDATE AS REAL) >= ${start} AND CAST(ZDATE AS REAL) <= ${end}`);
      const exp   = run(`SELECT SUM(ZMONEY) FROM INOUTCOME WHERE DO_TYPE=1 AND CAST(ZDATE AS REAL) >= ${start} AND CAST(ZDATE AS REAL) <= ${end}`);
      incomes.push(inc);
      expenses.push(exp);
      nets.push(inc - exp);
    });

    const isDark = theme.value === 'dark';
    const labels = months.map(mo => mo.label);

    // ── Grafico 1: barre affiancate Entrate/Uscite + linea netto grigia ──
    trend12BarData.value = {
      labels,
      datasets: [
        {
          type: 'bar',
          label: 'Entrate',
          data: incomes,
          backgroundColor: isDark ? 'rgba(16,185,129,0.70)' : 'rgba(16,185,129,0.65)',
          borderColor: '#059669',
          borderWidth: 1.5,
          borderRadius: 4,
          borderSkipped: false,
          yAxisID: 'y'
        },
        {
          type: 'bar',
          label: 'Uscite',
          data: expenses,
          backgroundColor: isDark ? 'rgba(239,68,68,0.70)' : 'rgba(239,68,68,0.65)',
          borderColor: '#dc2626',
          borderWidth: 1.5,
          borderRadius: 4,
          borderSkipped: false,
          yAxisID: 'y'
        },
        {
          type: 'line',
          label: 'Netto',
          data: nets,
          borderColor: isDark ? 'rgba(148,163,184,0.55)' : 'rgba(100,116,139,0.45)',
          backgroundColor: 'transparent',
          borderWidth: 1.5,
          borderDash: [4, 3],
          pointRadius: 3,
          pointBackgroundColor: (ctx) => nets[ctx.dataIndex] >= 0
            ? (isDark ? 'rgba(16,185,129,0.7)' : 'rgba(5,150,105,0.7)')
            : (isDark ? 'rgba(239,68,68,0.7)'  : 'rgba(220,38,38,0.7)'),
          pointBorderWidth: 0,
          tension: 0.35,
          yAxisID: 'y',
          order: 0
        }
      ]
    };
    trend12BarOptions.value = {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: 'index', intersect: false },
      plugins: {
        legend: {
          display: true, position: 'top', align: 'end',
          labels: {
            boxWidth: 10, boxHeight: 10, borderRadius: 3,
            font: { size: 11, family: 'Inter, sans-serif', weight: '600' },
            color: isDark ? '#94a3b8' : '#64748b',
            padding: 12, usePointStyle: true,
            filter: (item) => item.text !== 'Netto',
            generateLabels: (chart) => {
              const def = chart.data.datasets.map((ds, i) => ({
                text: ds.label,
                fillStyle: Array.isArray(ds.backgroundColor) ? ds.backgroundColor[0] : ds.backgroundColor,
                strokeStyle: ds.borderColor,
                lineWidth: ds.borderWidth,
                hidden: !chart.isDatasetVisible(i),
                datasetIndex: i,
                pointStyle: ds.type === 'line' ? 'line' : 'rectRounded'
              }));
              // Override label netto: linea tratteggiata grigia
              const nettoItem = def.find(d => d.text === 'Netto');
              if (nettoItem) {
                nettoItem.fillStyle = 'transparent';
                nettoItem.strokeStyle = isDark ? 'rgba(148,163,184,0.6)' : 'rgba(100,116,139,0.5)';
                nettoItem.lineDash = [4, 3];
                nettoItem.text = 'Netto';
              }
              return def;
            }
          }
        },
        tooltip: {
          ...baseTooltip(isDark),
          callbacks: {
            label: (ctx) => {
              const v = ctx.raw;
              if (ctx.dataset.label === 'Netto') return ` Netto: ${v >= 0 ? '+' : ''}€ ${Math.round(v).toLocaleString('it-IT')}`;
              return ` ${ctx.dataset.label}: € ${Math.round(v).toLocaleString('it-IT')}`;
            }
          }
        }
      },
      scales: baseScales(isDark)
    };

    // ── Grafico 2: area cumulativa risparmio ──
    let cum = 0;
    const cumulative = nets.map(n => { cum += n; return cum; });
    // Colora il fill in base al segno finale
    const isPositive = cumulative[cumulative.length - 1] >= 0;
    const fillColor  = isPositive
      ? (isDark ? 'rgba(59,130,246,0.18)' : 'rgba(59,130,246,0.12)')
      : (isDark ? 'rgba(239,68,68,0.18)'  : 'rgba(239,68,68,0.12)');
    const lineColor  = isPositive ? '#3b82f6' : '#ef4444';

    trend12CumData.value = {
      labels,
      datasets: [{
        label: 'Risparmio Cumulativo',
        data: cumulative,
        borderColor: lineColor,
        backgroundColor: fillColor,
        borderWidth: 2.5,
        pointRadius: (ctx) => ctx.raw === Math.max(...cumulative) || ctx.raw === Math.min(...cumulative) ? 6 : 3,
        pointBackgroundColor: (ctx) => ctx.raw < 0 ? '#ef4444' : lineColor,
        pointBorderColor: '#fff',
        pointBorderWidth: 1.5,
        tension: 0.4,
        fill: 'origin'
      }]
    };
    trend12CumOptions.value = {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: 'index', intersect: false },
      plugins: {
        legend: { display: false },
        tooltip: {
          ...baseTooltip(isDark),
          callbacks: {
            label: (ctx) => {
              const v = ctx.raw;
              return ` Cumulativo: ${v >= 0 ? '+' : ''}€ ${Math.round(v).toLocaleString('it-IT')}`;
            }
          }
        }
      },
      scales: baseScales(isDark)
    };

    // ── Summary ──
    const validInc = incomes.filter(v => v > 0);
    const validExp = expenses.filter(v => v > 0);
    const avgIncome  = validInc.length ? validInc.reduce((a,b) => a+b, 0) / validInc.length : 0;
    const avgExpense = validExp.length ? validExp.reduce((a,b) => a+b, 0) / validExp.length : 0;
    const bestIdx    = nets.indexOf(Math.max(...nets));
    const worstIdx   = nets.indexOf(Math.min(...nets));
    trendSummary.value = { avgIncome, avgExpense, bestMonth: labels[bestIdx] || '-', worstMonth: labels[worstIdx] || '-' };

  } catch(e) { console.error('loadTrend12:', e); }
};

// ══════════════════════════════════════════════
// STORICO CUMULATIVO
// ══════════════════════════════════════════════
const storicoData   = ref(null);
const storicoOptions = ref({});
const storicoSummary = ref({ totalNet: 0, maxCumulative: 0, months: 0, avgMonthly: 0 });

const loadStorico = () => {
  if (!dbInstance) return;
  try {
    // Prendi tutti i mesi distinti dal db
    const res = dbInstance.exec(`
      SELECT
        CAST(strftime('%Y', datetime(CAST(ZDATE AS REAL)/1000, 'unixepoch')) AS INTEGER) as yr,
        CAST(strftime('%m', datetime(CAST(ZDATE AS REAL)/1000, 'unixepoch')) AS INTEGER) as mo,
        SUM(CASE WHEN DO_TYPE=0 THEN ZMONEY ELSE 0 END) as inc,
        SUM(CASE WHEN DO_TYPE=1 THEN ZMONEY ELSE 0 END) as exp
      FROM INOUTCOME
      GROUP BY yr, mo
      ORDER BY yr, mo
    `);

    if (!res.length || !res[0].values.length) { storicoData.value = null; return; }

    const rows = res[0].values;
    const labels = [], cumulative = [], monthly = [];
    let cum = 0;
    rows.forEach(([yr, mo, inc, exp]) => {
      const net = (inc || 0) - (exp || 0);
      cum += net;
      labels.push(MESI[mo - 1] + ' ' + String(yr).slice(2));
      monthly.push(net);
      cumulative.push(cum);
    });

    const isDark = theme.value === 'dark';

    storicoData.value = {
      labels,
      datasets: [
        {
          label: 'Netto Mensile',
          data: monthly,
          borderColor: isDark ? '#64748b' : '#cbd5e1',
          backgroundColor: isDark ? 'rgba(100,116,139,0.2)' : 'rgba(203,213,225,0.3)',
          borderWidth: 1.5,
          pointRadius: 2, pointHoverRadius: 4,
          tension: 0.2, fill: false,
          yAxisID: 'yMonthly'
        },
        {
          label: 'Cumulativo',
          data: cumulative,
          borderColor: '#8b5cf6',
          backgroundColor: isDark ? 'rgba(139,92,246,0.15)' : 'rgba(139,92,246,0.10)',
          borderWidth: 3,
          pointRadius: 3, pointHoverRadius: 6,
          pointBackgroundColor: '#8b5cf6',
          tension: 0.4, fill: true,
          yAxisID: 'yCumulative'
        }
      ]
    };

    storicoOptions.value = buildLineOptions(isDark, {
      yMonthly: {
        type: 'linear', position: 'right',
        grid: { display: false },
        border: { display: false },
        ticks: {
          font: { size: 10, family: 'Inter, sans-serif' },
          color: isDark ? '#475569' : '#cbd5e1',
          callback: (v) => `€ ${v >= 1000 ? (v/1000).toFixed(0)+'k' : v}`
        }
      },
      yCumulative: {
        type: 'linear', position: 'left',
        grace: '10%',
        border: { display: false },
        grid: { color: isDark ? 'rgba(255,255,255,0.04)' : 'rgba(0,0,0,0.04)' },
        ticks: {
          font: { size: 11, family: 'Inter, sans-serif' },
          color: isDark ? '#64748b' : '#94a3b8',
          callback: (v) => `€ ${v >= 1000 ? (v/1000).toFixed(1)+'k' : v}`
        }
      }
    });

    // Summary
    const totalNet = cumulative[cumulative.length - 1] || 0;
    const maxCumulative = Math.max(...cumulative);
    const validMonthly = monthly.filter(v => v !== 0);
    storicoSummary.value = {
      totalNet, maxCumulative,
      months: rows.length,
      avgMonthly: validMonthly.length ? validMonthly.reduce((a,b) => a+b,0) / validMonthly.length : 0
    };
  } catch(e) { console.error('loadStorico:', e); }
};

// ══════════════════════════════════════════════
// DETTAGLIO MESE
// ══════════════════════════════════════════════
const dettaglioMonth = ref('');
const dettaglioMonthOptions = ref([]);
const dettaglioData = ref(null);
const dettaglioOptions = ref({});
const dettaglioStats = ref({ income: 0, expense: 0, net: 0 });

const buildDettaglioOptions = () => {
  const isDark = theme.value === 'dark';
  dettaglioOptions.value = {
    responsive: true,
    maintainAspectRatio: false,
    indexAxis: 'y',
    plugins: {
      legend: { display: false },
      tooltip: {
        backgroundColor: isDark ? 'rgba(28,27,25,0.95)' : 'rgba(15,23,42,0.95)',
        titleColor: isDark ? '#94a3b8' : '#cbd5e1',
        bodyColor: '#f1f5f9',
        padding: 12, cornerRadius: 8,
        callbacks: { label: (ctx) => ` € ${Math.round(ctx.raw).toLocaleString('it-IT')}` }
      }
    },
    scales: {
      x: {
        beginAtZero: true,
        grid: { color: isDark ? 'rgba(255,255,255,0.04)' : 'rgba(0,0,0,0.04)' },
        border: { display: false },
        ticks: {
          font: { size: 10, family: 'Inter, sans-serif' },
          color: isDark ? '#64748b' : '#94a3b8',
          callback: (v) => `€ ${v >= 1000 ? (v/1000).toFixed(0)+'k' : v}`
        }
      },
      y: {
        grid: { display: false },
        border: { display: false },
        ticks: {
          font: { size: 11, weight: '600', family: 'Inter, sans-serif' },
          color: isDark ? '#94a3b8' : '#475569'
        }
      }
    }
  };

  // Popola selettore mesi
  const now = new Date();
  const opts = [];
  for (let i = 0; i < 24; i++) {
    const d = new Date(now.getFullYear(), now.getMonth() - i, 1);
    const val = `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}`;
    const lbl = MESI[d.getMonth()] + ' ' + d.getFullYear();
    opts.push({ value: val, label: lbl });
  }
  dettaglioMonthOptions.value = opts;
  if (!dettaglioMonth.value && opts.length) dettaglioMonth.value = opts[0].value;
};

const loadDettaglio = () => {
  if (!dbInstance || !dettaglioMonth.value) return;
  try {
    const [y, m] = dettaglioMonth.value.split('-').map(Number);
    const start = new Date(y, m - 1, 1).getTime();
    const end   = new Date(y, m, 0, 23, 59, 59, 999).getTime();
    const isDark = theme.value === 'dark';

    // Helper sicuro
    const safeExec = (q) => { try { const r = dbInstance.exec(q); return (r.length && r[0].values) ? r[0].values : []; } catch(e) { return []; } };

    // Prova 1: JOIN con CATEGORY
    let expRows = safeExec(`
      SELECT c.ZNAME as cat, SUM(i.ZMONEY) as tot
      FROM INOUTCOME i
      LEFT JOIN CATEGORY c ON i.categoryUid = c.uid
      WHERE i.DO_TYPE = 1
        AND CAST(i.ZDATE AS REAL) >= ${start} AND CAST(i.ZDATE AS REAL) <= ${end}
        AND c.ZNAME IS NOT NULL AND c.ZNAME != ''
      GROUP BY c.ZNAME ORDER BY tot DESC LIMIT 10
    `);

    // Prova 2: fallback su WDATE se ZDATE non ha dati
    if (!expRows.length) {
      expRows = safeExec(`
        SELECT c.ZNAME as cat, SUM(i.ZMONEY) as tot
        FROM INOUTCOME i
        LEFT JOIN CATEGORY c ON i.categoryUid = c.uid
        WHERE i.DO_TYPE = 1
          AND CAST(i.WDATE AS REAL) >= ${start} AND CAST(i.WDATE AS REAL) <= ${end}
          AND c.ZNAME IS NOT NULL AND c.ZNAME != ''
        GROUP BY c.ZNAME ORDER BY tot DESC LIMIT 10
      `);
    }

    // Prova 3: fallback su NIC_NAME di ASSETS senza JOIN CATEGORY
    if (!expRows.length) {
      expRows = safeExec(`
        SELECT COALESCE(a.NIC_NAME, 'Altro') as cat, SUM(i.ZMONEY) as tot
        FROM INOUTCOME i
        LEFT JOIN ASSETS a ON i.assetUid = a.uid
        WHERE i.DO_TYPE = 1
          AND CAST(i.ZDATE AS REAL) >= ${start} AND CAST(i.ZDATE AS REAL) <= ${end}
        GROUP BY a.uid ORDER BY tot DESC LIMIT 10
      `);
    }

    // Prova 4: fallback ultra-safe senza join
    if (!expRows.length) {
      expRows = safeExec(`
        SELECT 'Uscita' as cat, SUM(ZMONEY) as tot
        FROM INOUTCOME
        WHERE DO_TYPE = 1
          AND CAST(ZDATE AS REAL) >= ${start} AND CAST(ZDATE AS REAL) <= ${end}
      `);
    }

    // Totali
    const totalInc = safeExec(`SELECT SUM(ZMONEY) FROM INOUTCOME WHERE DO_TYPE=0 AND CAST(ZDATE AS REAL) >= ${start} AND CAST(ZDATE AS REAL) <= ${end}`).reduce((s,r) => s+(r[0]||0), 0);
    const totalExp = expRows.reduce((s,[,v]) => s + (Number(v)||0), 0);
    dettaglioStats.value = { income: totalInc, expense: totalExp, net: totalInc - totalExp };

    if (!expRows.length) { dettaglioData.value = null; return; }

    const labels = expRows.map(([cat]) => cat || 'Altro');
    const values = expRows.map(([,v]) => Number(v) || 0);
    const maxVal = Math.max(...values);

    // Colori graduali per le barre (dal più scuro al più chiaro)
    const bgColors = values.map((v, i) => {
      const alpha = isDark ? 0.35 + (0.35 * (1 - i / values.length)) : 0.30 + (0.30 * (1 - i / values.length));
      return `rgba(239,68,68,${alpha.toFixed(2)})`;
    });

    dettaglioData.value = {
      labels,
      datasets: [{
        label: 'Uscite',
        data: values,
        backgroundColor: bgColors,
        borderColor: isDark ? '#dc2626' : '#991b1b',
        borderWidth: 1.5,
        borderRadius: 5,
        borderSkipped: false
      }]
    };

    buildDettaglioOptions();
  } catch(e) { console.error('loadDettaglio:', e); dettaglioData.value = null; }
};

// Carica dettaglio quando si apre il tab
watch(activeBottomTab, (tab) => {
  if (tab === 'dettaglio' && dbInstance) {
    if (!dettaglioMonthOptions.value.length) buildDettaglioOptions();
    if (!dettaglioData.value) loadDettaglio();
  }
});
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
/* Tab interni al cashflow panel */
.cf-tablist {
  display: flex; gap: 0; padding: var(--s2) var(--s4) 0;
  border-bottom: 1px solid var(--border);
  background: transparent !important;
}
.cf-tab {
  display: flex; align-items: center; gap: 6px;
  font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em;
  padding: var(--s2) var(--s4); border-radius: var(--r-md) var(--r-md) 0 0;
  color: var(--text-muted); cursor: pointer; border: none; background: none;
  border-bottom: 2px solid transparent; margin-bottom: -1px;
  transition: color 160ms, border-color 160ms;
}
.cf-tab:hover { color: var(--text); }
:deep(.p-tab-active).cf-tab { color: var(--primary); border-bottom-color: var(--primary); }
.topcat-wrap { height: auto !important; min-height: 260px; max-height: 340px; }
/* ---*/

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

/* ════════════════════════════════
   GRAFICI ANALISI — tab body
════════════════════════════════ */
.chart-tab-body { display: flex; flex-direction: column; gap: var(--s4); padding: var(--s4); }
.chart-wrap-tall { height: 280px; position: relative; }
@media (min-width: 640px) { .chart-wrap-tall { height: 320px; } }

/* Trend summary bar */
.trend-summary-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--s2);
}
@media (min-width: 480px) { .trend-summary-row { grid-template-columns: repeat(4, 1fr); } }

.trend-stat {
  display: flex; flex-direction: column; gap: 2px;
  background: var(--surface-2); border-radius: var(--r-md);
  padding: var(--s3) var(--s3); border: 1px solid var(--border);
}
.trend-stat-label { font-size: 10px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: var(--text-muted); }
.trend-stat-val { font-size: 14px; font-weight: 800; letter-spacing: -0.02em; color: var(--text); font-variant-numeric: tabular-nums; }
.income-text { color: #059669; }
.expense-text { color: #dc2626; }
.net-text { color: #2563eb; }
.mm-app[data-theme="dark"] .income-text { color: #34d399; }
.mm-app[data-theme="dark"] .expense-text { color: #f87171; }
.mm-app[data-theme="dark"] .net-text { color: #60a5fa; }

/* Dettaglio mese */
.dettaglio-toolbar {
  display: flex; align-items: center; gap: var(--s3);
  flex-wrap: wrap;
}
.dettaglio-label { font-size: 13px; font-weight: 600; color: var(--text-muted); }
.dettaglio-select {
  background: var(--surface-2); border: 1px solid var(--border);
  border-radius: var(--r-md); padding: 6px 12px;
  font-size: 13px; font-weight: 600; color: var(--text);
  cursor: pointer; outline: none; font-family: var(--font);
}
.dettaglio-grid { display: flex; flex-direction: column; gap: var(--s4); }
.dettaglio-kpi-row {
  display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--s2);
}
.dettaglio-kpi {
  padding: var(--s3); border-radius: var(--r-md);
  display: flex; flex-direction: column; gap: 2px;
}
.dettaglio-kpi-label { font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em; opacity: 0.75; }
.dettaglio-kpi-val { font-size: 15px; font-weight: 800; letter-spacing: -0.02em; font-variant-numeric: tabular-nums; }
.income-bg { background: #d1fae5; color: #065f46; }
.expense-bg { background: #fee2e2; color: #991b1b; }
.net-bg { background: #dbeafe; color: #1e3a8a; }
.neg-bg { background: #ffedd5; color: #9a3412; }
.mm-app[data-theme="dark"] .income-bg  { background: rgba(16,185,129,0.15); color: #34d399; }
.mm-app[data-theme="dark"] .expense-bg { background: rgba(239,68,68,0.15); color: #f87171; }
.mm-app[data-theme="dark"] .net-bg     { background: rgba(59,130,246,0.15); color: #60a5fa; }
.mm-app[data-theme="dark"] .neg-bg     { background: rgba(234,88,12,0.15);  color: #fb923c; }

/* ── Trend: due grafici impilati ── */
.trend-chart-block { display: flex; flex-direction: column; gap: var(--s2); }
.trend-chart-label {
  display: flex; align-items: center; gap: var(--s2);
  font-size: 12px; font-weight: 700; text-transform: uppercase;
  letter-spacing: 0.05em; color: var(--text-muted);
}
</style>
