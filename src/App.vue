<template>
  <div class="dashboard-container">
    <header class="header">
      <h1>Dashboard</h1>
      <p>Money Manager Analytics</p>
    </header>

    <main class="main-content">
      
      <!-- UPLOAD ZONE INIZIALE -->
      <div v-if="!fileLoaded" class="upload-section">
        <label class="upload-dropzone">
          <div class="upload-content">
            <span class="icon">📁</span>
            <span class="upload-text">Carica il tuo file <b>.mmbak</b></span>
          </div>
          <input type="file" accept=".mmbak, .sqlite, .db" @change="handleFileUpload" style="display: none;" />
        </label>
        <p class="status-msg" :class="{ 'error': isError }">{{ statusMessage }}</p>
      </div>

      <!-- BARRA CONTROLLI (Selezione Periodo + Aggiornamento) -->
      <div v-if="fileLoaded" class="controls-bar">
        <div class="period-selector">
          <select class="period-select" v-model="selectedPeriod" @change="refreshData">
            <option value="current_month">Questo Mese</option>
            <option value="last_month">Mese Scorso</option>
            <option value="ytd">Anno in Corso</option>
            <option value="all">Tutto</option>
          </select>
        </div>
        <label class="update-btn">
          🔄 Aggiorna DB
          <input type="file" accept=".mmbak, .sqlite, .db" @change="handleFileUpload" style="display: none;" />
        </label>
      </div>

      <!-- KPI CARDS (2x2 Grid) -->
      <div v-if="fileLoaded" class="kpi-grid">
        <div class="kpi-card income-card">
          <div class="kpi-header"><h3>Entrate</h3><span class="kpi-icon income-icon">↑</span></div>
          <p class="kpi-value">+€ {{ currentStats.income.toFixed(0) }}</p>
        </div>
        
        <div class="kpi-card expense-card">
          <div class="kpi-header"><h3>Uscite</h3><span class="kpi-icon expense-icon">↓</span></div>
          <p class="kpi-value">-€ {{ currentStats.expense.toFixed(0) }}</p>
        </div>
        
        <div class="kpi-card net-card" :class="{ 'negative-card': currentStats.net < 0 }">
          <div class="kpi-header"><h3>Risparmio</h3><span class="kpi-icon net-icon" :class="{ 'negative-icon': currentStats.net < 0 }">💰</span></div>
          <p class="kpi-value">{{ currentStats.net >= 0 ? '+' : '' }}€ {{ currentStats.net.toFixed(0) }}</p>
        </div>

        <div class="kpi-card rate-card" :class="{ 'negative-rate': currentStats.rate < 0 }">
          <div class="kpi-header"><h3>% Risparmio</h3><span class="kpi-icon rate-icon">📈</span></div>
          <p class="kpi-value">{{ currentStats.rate.toFixed(1) }}%</p>
        </div>
      </div>

      <!-- SEZIONE BUDGET DINAMICI (Regola Somma 100%) -->
      <div v-if="fileLoaded" class="budget-section">
        
        <!-- Impostazioni Budget -->
        <div class="budget-settings">
          <div class="budget-input-group">
            <label>Necessità %</label>
            <input type="number" v-model.number="budgetSettings.necessity" min="0" max="100" @change="updateNecessity" class="b-input" />
          </div>
          <div class="budget-input-group">
            <label>Extra %</label>
            <input type="number" v-model.number="budgetSettings.extra" min="0" max="100" @change="updateExtra" class="b-input" />
          </div>
          <div class="budget-input-group target-group">
            <label>Target Risparmio</label>
            <div class="target-val">{{ targetSavingsPct }}%</div>
          </div>
        </div>

        <!-- Barra di Progresso: Necessità -->
        <div class="budget-progress-container">
          <div class="budget-header">
            <span class="budget-title">Necessità (Max €{{ budgetLimits.necessity.toFixed(0) }})</span>
            <span class="budget-pct" :class="getBudgetColorClass(budgetUsedPcts.necessity)">
              {{ budgetUsedPcts.necessity.toFixed(1) }}% Utilizzato
            </span>
          </div>
          <div class="progress-bg">
            <div class="progress-fill" :class="getBudgetBgClass(budgetUsedPcts.necessity)" :style="{ width: Math.min(budgetUsedPcts.necessity, 100) + '%' }"></div>
          </div>
        </div>

        <!-- Barra di Progresso: Extra -->
        <div class="budget-progress-container mt-3">
          <div class="budget-header">
            <span class="budget-title">Extra (Max €{{ budgetLimits.extra.toFixed(0) }})</span>
            <span class="budget-pct" :class="getBudgetColorClass(budgetUsedPcts.extra)">
              {{ budgetUsedPcts.extra.toFixed(1) }}% Utilizzato
            </span>
          </div>
          <div class="progress-bg">
            <div class="progress-fill" :class="getBudgetBgClass(budgetUsedPcts.extra)" :style="{ width: Math.min(budgetUsedPcts.extra, 100) + '%' }"></div>
          </div>
        </div>
      </div>

      <!-- ZONA TAB NAVIGABILI -->
      <div v-if="fileLoaded" class="analysis-section">
        <Tabs value="0">
          <TabList>
            <Tab value="0">📊 CashFlow</Tab>
            <Tab value="1">📈 Trend</Tab>
            <Tab value="2">🏆 Storico</Tab>
          </TabList>
          
          <TabPanels>
            <TabPanel value="0">
              <div class="chart-card">
                <div class="chart-wrapper">
                  <Chart v-if="waterfallData" type="bar" :data="waterfallData" :options="waterfallOptions" :plugins="waterfallPlugins" />
                </div>
              </div>
            </TabPanel>
            
            <TabPanel value="1">
              <div class="placeholder-card">
                <span class="placeholder-icon">🚧</span>
                <h3>Trend 12 Mesi</h3>
                <p>In arrivo: Grafico a linee delle medie di spesa.</p>
              </div>
            </TabPanel>
            <TabPanel value="2">
              <div class="placeholder-card">
                <span class="placeholder-icon">🚧</span>
                <h3>Cumulativo</h3>
                <p>In arrivo: Andamento storico del risparmio totale.</p>
              </div>
            </TabPanel>
          </TabPanels>
        </Tabs>
      </div>

    </main>
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

// STATO GLOBALE
let dbInstance = null;
const selectedPeriod = ref('current_month');
const statusMessage = ref("In attesa del file...");
const isError = ref(false);
const fileLoaded = ref(false);

const currentStats = ref({ income: 0, expense: 0, net: 0, rate: 0, sumNecessity: 0, sumExtra: 0 });

// IMPOSTAZIONI BUDGET E LOGICA "SMART BALANCE" A 100%
const budgetSettings = ref({ necessity: 50, extra: 30 });
const targetSavingsPct = computed(() => Math.max(0, 100 - budgetSettings.value.necessity - budgetSettings.value.extra));

const updateNecessity = () => {
  let n = budgetSettings.value.necessity || 0;
  if (n < 0) n = 0;
  if (n > 100) n = 100;
  budgetSettings.value.necessity = n;
  
  // Se sforiamo il 100%, riduciamo gli Extra
  if (budgetSettings.value.necessity + budgetSettings.value.extra > 100) {
    budgetSettings.value.extra = 100 - budgetSettings.value.necessity;
  }
  refreshData();
};

const updateExtra = () => {
  let e = budgetSettings.value.extra || 0;
  if (e < 0) e = 0;
  if (e > 100) e = 100;
  budgetSettings.value.extra = e;
  
  // Se sforiamo il 100%, riduciamo le Necessità
  if (budgetSettings.value.necessity + budgetSettings.value.extra > 100) {
    budgetSettings.value.necessity = 100 - budgetSettings.value.extra;
  }
  refreshData();
};

// LIMITI E PERCENTUALI DI BUDGET CALCOLATI IN BASE ALLE ENTRATE
const budgetLimits = computed(() => {
  const inc = currentStats.value.income;
  return {
    necessity: inc * (budgetSettings.value.necessity / 100),
    extra: inc * (budgetSettings.value.extra / 100)
  };
});
const budgetUsedPcts = computed(() => {
  return {
    necessity: budgetLimits.value.necessity > 0 ? (currentStats.value.sumNecessity / budgetLimits.value.necessity) * 100 : 0,
    extra: budgetLimits.value.extra > 0 ? (currentStats.value.sumExtra / budgetLimits.value.extra) * 100 : 0
  };
});

// COLORI PROGRESS BAR
const getBudgetColorClass = (pct) => {
  if (pct >= 100) return 'text-red';
  if (pct >= 80) return 'text-orange';
  return 'text-green';
};
const getBudgetBgClass = (pct) => {
  if (pct >= 100) return 'bg-red';
  if (pct >= 80) return 'bg-orange';
  return 'bg-green';
};

// GRAFICO A CASCATA
const waterfallData = ref(null);
const waterfallOptions = ref({});
const waterfallConnector = {
  id: 'waterfallConnector',
  afterDatasetsDraw(chart) {
    const ctx = chart.ctx;
    const meta = chart.getDatasetMeta(0);
    ctx.save();
    ctx.strokeStyle = '#9ca3af'; 
    ctx.lineWidth = 2;
    ctx.setLineDash([4, 4]);

    for (let i = 0; i < meta.data.length - 1; i++) {
      const bar1 = meta.data[i];
      const bar2 = meta.data[i + 1];
      const bar1RightEdge = bar1.x + (bar1.width / 2);
      const bar2LeftEdge = bar2.x - (bar2.width / 2);
      let yPoint = bar2.y; 
      
      ctx.beginPath();
      ctx.moveTo(bar1RightEdge, yPoint);
      ctx.lineTo(bar2LeftEdge, yPoint);
      ctx.stroke();
    }
    ctx.restore();
  }
};
const waterfallPlugins = ref([waterfallConnector]);

// GESTIONE CARICAMENTO FILE
const handleFileUpload = async (event) => {
  const file = event.target.files[0];
  if (!file) return;

  try {
    statusMessage.value = "Caricamento database...";
    isError.value = false;
    
    const arrayBuffer = await file.arrayBuffer();
    const SQL = await initSqlJs({ locateFile: file => `/sql-wasm.wasm` });
    dbInstance = new SQL.Database(new Uint8Array(arrayBuffer));
    
    fileLoaded.value = true;
    refreshData(); 

  } catch (error) {
    isError.value = true;
    statusMessage.value = error.message;
  }
};

// GESTIONE AGGIORNAMENTO DATI
const refreshData = () => {
  if (!dbInstance) return;

  try {
    const dateObj = new Date();
    const y = dateObj.getFullYear();
    const m = dateObj.getMonth();

    let startMs = 0;
    let endMs = Date.now();

    if (selectedPeriod.value === 'current_month') {
      startMs = new Date(y, m, 1).getTime();
    } else if (selectedPeriod.value === 'last_month') {
      startMs = new Date(y, m - 1, 1).getTime();
      endMs = new Date(y, m, 0, 23, 59, 59, 999).getTime();
    } else if (selectedPeriod.value === 'ytd') {
      startMs = new Date(y, 0, 1).getTime();
    } else if (selectedPeriod.value === 'all') {
      startMs = 0;
    }

    const incomeQ = `SELECT SUM(ZMONEY) FROM INOUTCOME WHERE DO_TYPE = 0 AND CAST(ZDATE AS REAL) >= ${startMs} AND CAST(ZDATE AS REAL) <= ${endMs}`;
    const expenseQ = `SELECT SUM(ZMONEY) FROM INOUTCOME WHERE DO_TYPE = 1 AND CAST(ZDATE AS REAL) >= ${startMs} AND CAST(ZDATE AS REAL) <= ${endMs}`;
    
    const iRes = dbInstance.exec(incomeQ);
    const eRes = dbInstance.exec(expenseQ);
    const totalIncome = (iRes.length > 0 && iRes[0].values[0][0]) ? iRes[0].values[0][0] : 0;
    const totalExpense = (eRes.length > 0 && eRes[0].values[0][0]) ? eRes[0].values[0][0] : 0;
    const netSavings = totalIncome - totalExpense;
    
    let rate = 0;
    if (totalIncome > 0) rate = (netSavings / totalIncome) * 100;

    let sumNecessity = 0; let sumExtra = 0;
    const monthExpQ = `
      SELECT ASSETS.NIC_NAME as budget, SUM(INOUTCOME.ZMONEY) as total
      FROM INOUTCOME LEFT JOIN ASSETS ON INOUTCOME.assetUid = ASSETS.uid
      WHERE INOUTCOME.DO_TYPE = 1 AND CAST(INOUTCOME.ZDATE AS REAL) >= ${startMs} AND CAST(INOUTCOME.ZDATE AS REAL) <= ${endMs}
      GROUP BY ASSETS.uid;
    `;
    const mRes = dbInstance.exec(monthExpQ);
    if (mRes.length > 0) {
      mRes[0].values.forEach(row => {
        String(row[0]||'').toLowerCase().includes('necess') ? sumNecessity += row[1] : sumExtra += row[1];
      });
    }

    currentStats.value = { 
      income: totalIncome, expense: totalExpense, net: netSavings, rate: rate,
      sumNecessity, sumExtra 
    };

    const step1 = totalIncome;
    const step2 = step1 - sumNecessity;
    const step3 = step2 - sumExtra;
    const targetSavingsEuro = totalIncome * (targetSavingsPct.value / 100);

    waterfallData.value = {
      labels: ['Entrate', 'Necessità', 'Extra', 'Netto'],
      datasets: [{
        label: 'Flusso',
        data: [[0, step1], [step2, step1], [step3, step2], [0, step3]],
        backgroundColor: ['rgba(16, 185, 129, 0.7)', 'rgba(239, 68, 68, 0.7)', 'rgba(239, 68, 68, 0.7)', 'rgba(59, 130, 246, 0.7)'],
        borderColor: ['#059669', '#be123c', '#be123c', '#1d4ed8'],
        borderWidth: 2, borderRadius: 4, borderSkipped: false
      }]
    };

    waterfallOptions.value = {
      responsive: true, maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: '#1e293b', padding: 10,
          titleFont: { size: 12, family: 'Inter' }, bodyFont: { size: 14, weight: 'bold', family: 'Inter' },
          callbacks: { label: (ctx) => `€ ${Math.abs(ctx.raw[1] - ctx.raw[0]).toFixed(0)}` }
        },
        annotation: {
          annotations: {
            line1: {
              type: 'line', yMin: targetSavingsEuro, yMax: targetSavingsEuro,
              borderColor: '#f59e0b', borderWidth: 2, borderDash: [5, 5],
              label: {
                display: true, content: `Target ${targetSavingsPct.value}%`, position: 'end',
                backgroundColor: '#fef3c7', color: '#d97706', font: { weight: 'bold', family: 'Inter', size: 10 }, borderRadius: 6
              }
            }
          }
        }
      },
      scales: { 
        x: { grid: { display: false }, ticks: { font: { size: 11 } } },
        y: { beginAtZero: true, grace: '10%', border: { display: false }, ticks: { font: { size: 11 } } } 
      }
    };

    statusMessage.value = "Dati aggiornati correttamente.";

  } catch (error) {
    console.error(error);
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.dashboard-container {
  min-height: 100vh; background-color: #f8fafc; color: #0f172a;
  font-family: 'Inter', sans-serif;
  padding: 1.5rem 1rem;
}

.header { text-align: center; margin-bottom: 1.5rem; }
.header h1 { font-size: 1.8rem; font-weight: 800; letter-spacing: -0.03em; margin-bottom: 0.2rem; color: #0f172a; }
.header p { color: #64748b; font-size: 0.95rem; font-weight: 500; margin: 0; }

.main-content { max-width: 800px; margin: 0 auto; }

/* === UPLOAD ZONE === */
.upload-section { margin-bottom: 1.5rem; text-align: center; }
.upload-dropzone { display: block; background-color: #ffffff; border: 2px dashed #cbd5e1; border-radius: 16px; padding: 2rem; cursor: pointer; }
.upload-content { display: flex; flex-direction: column; align-items: center; gap: 0.5rem; }
.icon { font-size: 2rem; }
.upload-text { font-size: 1rem; color: #475569; }

/* === CONTROLS BAR === */
.controls-bar {
  display: flex; justify-content: space-between; align-items: center;
  background: white; padding: 0.6rem 0.8rem; border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.02); margin-bottom: 1.5rem;
}
.period-select {
  border: none; background: #f1f5f9; padding: 8px 12px; border-radius: 8px;
  font-family: 'Inter'; font-weight: 600; color: #0f172a; font-size: 0.9rem; outline: none; cursor: pointer;
}
.update-btn {
  background: #0f172a; color: white; padding: 8px 14px; border-radius: 8px;
  font-size: 0.85rem; font-weight: 700; cursor: pointer; transition: 0.2s;
}

/* === KPI CARDS === */
.kpi-grid {
  display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.8rem; margin-bottom: 1.5rem;
}
.kpi-card { padding: 1rem; border-radius: 16px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
.kpi-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.6rem; }
.kpi-header h3 { margin: 0; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.02em; }
.kpi-value { margin: 0; font-size: 1.5rem; font-weight: 800; letter-spacing: -0.03em; }
.kpi-icon { display: flex; justify-content: center; align-items: center; width: 28px; height: 28px; border-radius: 50%; font-size: 1rem; font-weight: bold; }

.income-card { background-color: #d1fae5; } .income-card h3, .income-card .kpi-value { color: #065f46; } .income-icon { background-color: #059669; color: #ffffff; }
.expense-card { background-color: #fee2e2; } .expense-card h3, .expense-card .kpi-value { color: #991b1b; } .expense-icon { background-color: #e11d48; color: #ffffff; }
.net-card { background-color: #dbeafe; } .net-card h3, .net-card .kpi-value { color: #1e3a8a; } .net-icon { background-color: #2563eb; color: #ffffff; }
.negative-card { background-color: #ffedd5; } .negative-card h3, .negative-card .kpi-value { color: #9a3412; } .negative-card .net-icon { background-color: #ea580c; color: #ffffff; }
.rate-card { background-color: #ede9fe; } .rate-card h3, .rate-card .kpi-value { color: #3730a3; } .rate-icon { background-color: #4f46e5; color: #ffffff; }
.negative-rate { background-color: #fce7f3; } .negative-rate h3, .negative-rate .kpi-value { color: #be123c; }

/* === SEZIONE BUDGET === */
.budget-section {
  background: white; padding: 1.2rem; border-radius: 16px; margin-bottom: 1.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.02);
}
.budget-settings {
  display: flex; justify-content: space-between; gap: 0.5rem; margin-bottom: 1.5rem;
  background: #f8fafc; padding: 0.8rem; border-radius: 12px; border: 1px solid #e2e8f0;
}
.budget-input-group { display: flex; flex-direction: column; align-items: flex-start; gap: 0.3rem; }
.budget-input-group label { font-size: 0.75rem; font-weight: 700; color: #64748b; text-transform: uppercase; }
.b-input {
  width: 60px; padding: 6px; border-radius: 6px; border: 1px solid #cbd5e1; font-weight: bold; color: #0f172a; text-align: center; outline: none;
}
.target-group { align-items: flex-end; }
.target-val { font-size: 1.2rem; font-weight: 800; color: #d97706; }

.budget-progress-container { margin-bottom: 1rem; }
.mt-3 { margin-top: 1rem; }
.budget-header { display: flex; justify-content: space-between; margin-bottom: 0.5rem; font-size: 0.85rem; font-weight: 600; }
.budget-title { color: #475569; }
.progress-bg { background: #f1f5f9; height: 8px; border-radius: 4px; overflow: hidden; }
.progress-fill { height: 100%; border-radius: 4px; transition: width 0.4s ease; }

.text-green { color: #059669; } .bg-green { background-color: #10b981; }
.text-orange { color: #d97706; } .bg-orange { background-color: #f59e0b; }
.text-red { color: #e11d48; } .bg-red { background-color: #ef4444; }

/* === ZONA TABS & CHARTS === */
.analysis-section { background: white; border-radius: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.02); overflow: hidden; }
:deep(.p-tablist-tab-list) { background: #f8fafc; border-bottom: 1px solid #e2e8f0; }
:deep(.p-tab) { padding: 1rem 0.5rem; font-family: 'Inter'; font-weight: 600; color: #64748b; border: none; font-size: 0.9rem; flex: 1; text-align: center; justify-content: center; }
:deep(.p-tab-active) { color: #0f172a; border-bottom: 2px solid #0f172a; }
:deep(.p-tabpanels) { padding: 1.5rem 1rem; background: white; }

.chart-card { width: 100%; }

.chart-wrapper { height: 17rem; position: relative; } 
:deep(.p-chart) { height: 100%; width: 100%; }
.responsive-chart { height: 100% !important; }

.placeholder-card { text-align: center; padding: 3rem 1rem; color: #64748b; }
.placeholder-icon { font-size: 3rem; display: block; margin-bottom: 1rem; }
.placeholder-card h3 { color: #0f172a; margin-bottom: 0.5rem; }
</style>