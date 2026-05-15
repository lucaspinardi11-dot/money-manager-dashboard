<template>
  <div class="mm-app" :data-theme="theme">

    <!-- ═══ HEADER ═══ -->
    <header class="mm-header">
      <div class="header-inner">
        <div class="header-top">
          <div class="header-brand">
            <svg class="brand-logo" viewBox="0 0 32 32" fill="none" aria-label="Money Manager Logo">
              <rect x="3" y="8" width="26" height="18" rx="3" stroke="currentColor" stroke-width="2"/>
              <path d="M3 13h26" stroke="currentColor" stroke-width="2"/>
              <circle cx="10" cy="20" r="2" fill="currentColor"/>
              <rect x="15" y="19" width="8" height="2" rx="1" fill="currentColor"/>
            </svg>
            <div class="brand-copy">
              <span class="brand-name">Money Manager</span>
              <span class="brand-sub">Dashboard</span>
            </div>
          </div>

          <div class="header-actions">
            <label v-if="fileLoaded" class="btn-update" title="Cambia file database">
              <svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16"><path d="M4 10a6 6 0 1 0 6-6"/><path d="M4 6v4h4"/></svg>
              <span class="btn-update-text">Aggiorna</span>
              <input type="file" accept=".mmbak,.sqlite,.db" @change="handleFileUpload" style="display:none" />
            </label>

            <button class="theme-toggle" @click="toggleTheme" :aria-label="'Passa a tema ' + (theme === 'dark' ? 'chiaro' : 'scuro')">
              <svg v-if="theme === 'dark'" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18"><circle cx="10" cy="10" r="4"/><path d="M10 2v2M10 16v2M2 10h2M16 10h2M4.9 4.9l1.4 1.4M13.7 13.7l1.4 1.4M4.9 15.1l1.4-1.4M13.7 6.3l1.4-1.4"/></svg>
              <svg v-else viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18"><path d="M17.5 11.5A7.5 7.5 0 1 1 8.5 2.5a5.5 5.5 0 1 0 9 9z"/></svg>
            </button>

            <div v-if="googleUser" class="user-chip">
              <img
                v-if="googleUser.picture"
                :src="googleUser.picture"
                :alt="googleUser.name"
                class="user-avatar"
                referrerpolicy="no-referrer"
                @error="avatarError = true"
              />
              <span
                v-if="!googleUser.picture || avatarError"
                class="user-avatar user-avatar-fallback"
                :title="googleUser.name"
              >{{ (googleUser.given_name || googleUser.name || '?')[0].toUpperCase() }}</span>
              <span class="user-name">{{ googleUser.given_name || googleUser.name }}</span>
              <button class="btn-logout" @click="handleLogout" title="Esci">
                <svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><path d="M13 3h4v14h-4M8 7l-4 3 4 3M4 10h9"/></svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- ═══ MAIN ═══ -->
    <main class="mm-main">

      <!-- ── LOGIN / UPLOAD SCREEN ── -->
      <div v-if="!fileLoaded" class="upload-screen">
        <div class="login-card">

          <!-- Logo + titolo -->
          <div class="login-header">
            <svg style="width:48px;height:48px;color:var(--color-primary,#01696f)" viewBox="0 0 32 32" fill="none">
              <rect x="3" y="8" width="26" height="18" rx="3" stroke="currentColor" stroke-width="2"/>
              <path d="M3 13h26" stroke="currentColor" stroke-width="2"/>
              <circle cx="10" cy="20" r="2" fill="currentColor"/>
              <rect x="15" y="19" width="8" height="2" rx="1" fill="currentColor"/>
            </svg>
            <h2 class="login-title">Money Manager</h2>
            <p class="login-subtitle">Dashboard personale</p>
          </div>

          <!-- Messaggio di stato -->
          <p v-if="statusMessage" class="login-status" :class="{ 'status-error': isError }">
            <svg v-if="driveLoading" viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" style="flex-shrink:0;animation:spin 0.8s linear infinite">
              <circle cx="12" cy="12" r="10" stroke-opacity="0.3"/>
              <path d="M12 2a10 10 0 0 1 10 10" stroke-linecap="round"/>
            </svg>
            {{ statusMessage }}
          </p>

          <!-- ── SEZIONE GOOGLE DRIVE ── -->
          <div class="login-section">
            <div class="login-section-label">
              <svg viewBox="0 0 87.3 78" width="16" height="14" xmlns="http://www.w3.org/2000/svg">
                <path d="m6.6 66.85 3.85 6.65c.8 1.4 1.95 2.5 3.3 3.3l13.75-23.8h-27.5c0 1.55.4 3.1 1.2 4.5z" fill="#0066da"/>
                <path d="m43.65 25-13.75-23.8c-1.35.8-2.5 1.9-3.3 3.3l-25.4 44a9.06 9.06 0 0 0-1.2 4.5h27.5z" fill="#00ac47"/>
                <path d="m73.55 76.8c1.35-.8 2.5-1.9 3.3-3.3l1.6-2.75 7.65-13.25c.8-1.4 1.2-2.95 1.2-4.5h-27.502l5.852 11.5z" fill="#ea4335"/>
                <path d="m43.65 25 13.75-23.8c-1.35-.8-2.9-1.2-4.5-1.2h-18.5c-1.6 0-3.15.45-4.5 1.2z" fill="#00832d"/>
                <path d="m59.8 53h-32.3l-13.75 23.8c1.35.8 2.9 1.2 4.5 1.2h50.8c1.6 0 3.15-.45 4.5-1.2z" fill="#2684fc"/>
                <path d="m73.4 26.5-12.7-22c-.8-1.4-1.95-2.5-3.3-3.3l-13.75 23.8 16.15 28h27.45c0-1.55-.4-3.1-1.2-4.5z" fill="#ffba00"/>
              </svg>
              Accedi con Google Drive
            </div>
            <p class="login-section-desc">Accedi per caricare automaticamente il backup <code>.mmbak</code> più recente.</p>

            <!-- Web: pulsante GSI Google -->
            <div v-if="!isNative" id="google-signin-btn" class="gsi-btn-wrap"></div>

            <!-- Native: pulsante nativo -->
            <button v-else @click="loginNative" class="login-btn login-btn-google" :disabled="driveLoading">
              <svg viewBox="0 0 24 24" width="18" height="18" xmlns="http://www.w3.org/2000/svg">
                <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
                <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
                <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l3.66-2.84z" fill="#FBBC05"/>
                <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
              </svg>
              {{ driveLoading ? 'Connessione...' : 'Accedi con Google' }}
            </button>

            <!-- Web: pulsante Drive (visibile dopo login GSI) -->
            <button
              v-if="!isNative && googleUser"
              @click="loadFromDrive({ interactive: false })"
              :disabled="driveLoading"
              class="login-btn login-btn-drive"
              style="margin-top:0.5rem"
            >
              <svg v-if="!driveLoading" viewBox="0 0 87.3 78" width="16" height="14" xmlns="http://www.w3.org/2000/svg">
                <path d="m6.6 66.85 3.85 6.65c.8 1.4 1.95 2.5 3.3 3.3l13.75-23.8h-27.5c0 1.55.4 3.1 1.2 4.5z" fill="#0066da"/>
                <path d="m43.65 25-13.75-23.8c-1.35.8-2.5 1.9-3.3 3.3l-25.4 44a9.06 9.06 0 0 0-1.2 4.5h27.5z" fill="#00ac47"/>
                <path d="m59.8 53h-32.3l-13.75 23.8c1.35.8 2.9 1.2 4.5 1.2h50.8c1.6 0 3.15-.45 4.5-1.2z" fill="#2684fc"/>
                <path d="m73.4 26.5-12.7-22c-.8-1.4-1.95-2.5-3.3-3.3l-13.75 23.8 16.15 28h27.45c0-1.55-.4-3.1-1.2-4.5z" fill="#ffba00"/>
              </svg>
              <svg v-else viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" style="animation:spin 0.8s linear infinite">
                <circle cx="12" cy="12" r="10" stroke-opacity="0.3"/>
                <path d="M12 2a10 10 0 0 1 10 10" stroke-linecap="round"/>
              </svg>
              {{ driveLoading ? 'Caricamento...' : 'Carica da Google Drive' }}
            </button>
          </div>

          <!-- ── DIVISORE ── -->
          <div class="login-divider"><span>oppure</span></div>

          <!-- ── SEZIONE UPLOAD MANUALE ── -->
          <div class="login-section">
            <div class="login-section-label">
              <svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2" width="15" height="15">
                <path d="M10 2v10M6 6l4-4 4 4"/>
                <path d="M3 14v2a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-2"/>
              </svg>
              Carica file manualmente
            </div>
            <p class="login-section-desc">Seleziona il file <code>.mmbak</code> esportato dall'app Money Manager.</p>
            <label class="login-btn login-btn-file">
              <svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2" width="15" height="15">
                <rect x="3" y="4" width="14" height="14" rx="2"/>
                <path d="M7 4V3a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v1"/>
                <path d="M10 9v4M8 11l2-2 2 2"/>
              </svg>
              Sfoglia file
              <input type="file" accept=".mmbak,.sqlite,.db" @change="handleFileUpload" style="display:none" />
            </label>
            <div class="upload-formats" style="margin-top:0.75rem">
              <span class="format-chip">.mmbak</span>
              <span class="format-chip">.sqlite</span>
              <span class="format-chip">.db</span>
            </div>
          </div>

          <p style="font-size:11px;color:var(--text-faint);text-align:center;margin-top:1rem;line-height:1.5">
            🔒 I tuoi dati rimangono solo sul tuo dispositivo.<br>Nessun dato viene inviato a server esterni.
          </p>

        </div>
      </div>

      <!-- ── DASHBOARD CONTENT ── -->
      <div v-if="fileLoaded" class="dashboard-content">

        <section class="period-panel hybrid-period-panel" aria-label="Filtro periodo">
          <div class="period-panel-head hybrid-period-head">
            <div class="period-pill period-pill-panel hybrid-period-pill">
              <select class="period-select" v-model="selectedPeriod" @change="refreshData" aria-label="Seleziona periodo">
                <option value="current_month">Questo Mese</option>
                <option value="last_month">Mese Scorso</option>
                <option value="ytd">Da Inizio Anno</option>
                <option value="all">Tutto</option>
                <option value="custom">Personalizzato…</option>
              </select>
            </div>
          </div>

          <Transition name="custom-fade">
            <div v-if="showCustom" class="custom-range-shell period-panel-range-shell hybrid-range-shell">
              <div class="custom-range compact-range period-panel-range hybrid-period-range">
                <label class="date-card date-card-start">
                  <span class="date-card-label">Dal</span>
                  <input type="date" v-model="customStart" @change="refreshData" class="date-input date-input-wide" aria-label="Data inizio" />
                </label>
                <label class="date-card date-card-end">
                  <span class="date-card-label">Al</span>
                  <input type="date" v-model="customEnd" @change="refreshData" class="date-input date-input-wide" aria-label="Data fine" />
                </label>
              </div>
            </div>
          </Transition>
        </section>

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
                  <!-- Target -->
                  <div class="savings-kpi-block">
                    <span class="skb-label">🎯 Target</span>
                    <span class="skb-value skb-target">€ {{ fmt0(currentStats.income * targetSavingsPct / 100) }}</span>
                    <span class="skb-sub">{{ targetSavingsPct }}% del reddito</span>
                  </div>
                  <!-- Divisore -->
                  <div class="savings-divider"></div>
                  <!-- Risparmiato effettivo -->
                  <div class="savings-kpi-block">
                    <span class="skb-label">💰 Risparmiato</span>
                    <span class="skb-value" :class="currentStats.net >= currentStats.income * targetSavingsPct / 100 ? 'skb-ok' : 'skb-warn'">
                      € {{ fmt0(currentStats.net) }}
                    </span>
                    <span class="skb-sub" :class="currentStats.net >= currentStats.income * targetSavingsPct / 100 ? 'skb-ok' : 'skb-warn'">
                      {{ currentStats.income > 0 ? ((currentStats.net / currentStats.income) * 100).toFixed(1) : '0' }}% del reddito
                    </span>
                  </div>
                  <!-- Divisore -->
                  <div class="savings-divider"></div>
                  <!-- Consiglio -->
                  <div v-if="currentStats.income > 0" class="savings-tip-inline" :class="currentStats.net >= currentStats.income * targetSavingsPct / 100 ? 'sti-ok' : 'sti-warn'">
                    <template v-if="currentStats.net >= currentStats.income * targetSavingsPct / 100">
                      <span class="sti-delta">+€ {{ fmt0(currentStats.net - currentStats.income * targetSavingsPct / 100) }}</span>
                      <span class="sti-msg">puoi ancora spendere questa cifra restando sopra l'obiettivo</span>
                    </template>
                    <template v-else>
                      <span class="sti-delta">-€ {{ fmt0(currentStats.income * targetSavingsPct / 100 - currentStats.net) }}</span>
                      <span class="sti-msg">da recuperare il mese prossimo per rientrare nel target</span>
                    </template>
                  </div>
                </div>
              </div>
            </div>
          </div>




          <!-- CASHFLOW — tab Cascata + Top Categorie -->
          <div class="panel cashflow-panel glass-panel">
            <Tabs :value="activeCfTab" @update:value="activeCfTab = $event">
              <TabList class="cf-tablist">
                <Tab value="cashflow" class="cf-tab">
                  <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" width="13" height="13"><rect x="2" y="4" width="3" height="8" rx="1"/><rect x="7" y="2" width="3" height="10" rx="1"/><rect x="12" y="6" width="3" height="6" rx="1"/></svg>
                  CashFlow
                </Tab>
                <Tab value="topcat" class="cf-tab">
                  <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" width="13" height="13"><path d="M3 4h10M3 8h7M3 12h5"/></svg>
                  Top Categorie
                </Tab>
                <Tab value="confronto" class="cf-tab">
                  <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" width="13" height="13"><rect x="2" y="5" width="3" height="7" rx="1"/><rect x="7" y="3" width="3" height="9" rx="1"/><rect x="12" y="6" width="3" height="6" rx="1"/><path d="M1 13h14" stroke-width="1.5"/></svg>
                  Confronto
                </Tab>
              </TabList>
              <TabPanels>
                <TabPanel value="cashflow">
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
                <TabPanel value="confronto">
                  <div class="confronto-wrap">
                    <div class="confronto-header">
                      <div class="confronto-toggle">
                        <button class="ctg-btn" :class="{ active: confrontoMode === 'prev' }" @click="confrontoMode = 'prev'; loadConfronto()">
                          <svg viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="2" width="11" height="11"><path d="M8 2L3 7l5 5"/></svg>
                          Periodo prec.
                        </button>
                        <button class="ctg-btn" :class="{ active: confrontoMode === 'year' }" @click="confrontoMode = 'year'; loadConfronto()">
                          <svg viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="2" width="11" height="11"><path d="M8 2L3 7l5 5M12 2L7 7l5 5"/></svg>
                          Anno prec.
                        </button>
                      </div>
                      <div class="confronto-range-label" v-if="confrontoPrevLabel">
                        <span class="crl-prev">{{ confrontoPrevLabel }}</span>
                        <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" width="11" height="11" opacity="0.4"><path d="M3 8h10M9 4l4 4-4 4"/></svg>
                        <span class="crl-cur">{{ confrontoCurLabel }}</span>
                      </div>
                    </div>
                    <div class="chart-wrap" v-if="confrontoData">
                      <Chart type="bar" :data="confrontoData" :options="confrontoOptions" style="height:100%;width:100%"/>
                    </div>
                    <div v-else class="chart-empty">
                      <svg viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="1.5" width="36" height="36" opacity="0.3"><rect x="4" y="20" width="8" height="16" rx="1"/><rect x="16" y="12" width="8" height="24" rx="1"/><rect x="28" y="4" width="8" height="32" rx="1"/></svg>
                      <p>Nessun dato disponibile</p>
                    </div>
                    <div class="confronto-kpis" v-if="confrontoDelta">
                      <div class="ckpi" :class="confrontoDelta.incDelta >= 0 ? 'ckpi-pos' : 'ckpi-neg'">
                        <span class="ckpi-label">Entrate</span>
                        <span class="ckpi-delta">{{ confrontoDelta.incDelta >= 0 ? '+' : '' }}{{ confrontoDelta.incDelta.toFixed(1) }}%</span>
                      </div>
                      <div class="ckpi" :class="confrontoDelta.expDelta <= 0 ? 'ckpi-pos' : 'ckpi-neg'">
                        <span class="ckpi-label">Uscite</span>
                        <span class="ckpi-delta">{{ confrontoDelta.expDelta >= 0 ? '+' : '' }}{{ confrontoDelta.expDelta.toFixed(1) }}%</span>
                      </div>
                      <div class="ckpi" :class="confrontoDelta.netDelta >= 0 ? 'ckpi-pos' : 'ckpi-neg'">
                        <span class="ckpi-label">Netto</span>
                        <span class="ckpi-delta">{{ confrontoDelta.netDelta >= 0 ? '+' : '' }}{{ confrontoDelta.netDelta.toFixed(1) }}%</span>
                      </div>
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
                <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><rect x="2" y="2" width="3" height="3" rx="0.5"/><rect x="7" y="2" width="3" height="3" rx="0.5"/><rect x="12" y="2" width="3" height="3" rx="0.5"/><rect x="2" y="7" width="3" height="3" rx="0.5"/><rect x="7" y="7" width="3" height="3" rx="0.5"/><rect x="12" y="7" width="3" height="3" rx="0.5"/><rect x="2" y="12" width="3" height="3" rx="0.5"/><rect x="7" y="12" width="3" height="3" rx="0.5"/><rect x="12" y="12" width="3" height="3" rx="0.5"/></svg>
                Heatmap
              </Tab>
              <Tab value="anomalie" class="tab-custom">
                <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><path d="M8 2v7M8 12v2"/><circle cx="8" cy="13" r="0.5" fill="currentColor"/><path d="M2 14L8 2l6 12H2z"/></svg>
                Anomalie
              </Tab>
              <Tab value="previsioni" class="tab-custom">
                <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><path d="M2 12 L5 8 L9 10 L14 4"/><path d="M14 4h-3M14 4v3" stroke-linecap="round"/></svg>
                Previsioni
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
                      Entrate vs Uscite · Netto Cumulato
                    </div>
                    <div class="chart-wrap-tall">
                      <Chart type="bar" :data="trend12BarData" :options="trend12BarOptions" style="height:100%;width:100%" />
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
                      <span class="trend-stat-val" :class="storicoSummary.isAbove ? 'net-text' : 'expense-text'">€ {{ fmt0(storicoSummary.totalNet) }}</span>
                    </div>
                    <div class="trend-stat">
                      <span class="trend-stat-label">Massimo Storico</span>
                      <span class="trend-stat-val income-text">€ {{ fmt0(storicoSummary.maxCumulative) }}</span>
                    </div>
                    <div class="trend-stat">
                      <span class="trend-stat-label">vs Obiettivo</span>
                      <span class="trend-stat-val" :class="storicoSummary.isAbove ? 'net-text' : 'expense-text'">
                        {{ storicoSummary.isAbove ? '+' : '' }}€ {{ fmt0(storicoSummary.deltaVsTarget) }}
                      </span>
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
                <div class="heatmap-wrap">
                  <!-- Toggle Spese / Entrate -->
                  <div class="heatmap-header">
                    <div class="heatmap-header-left">
                      <div class="heatmap-toggle">
                        <button class="ctg-btn" :class="{ active: heatmapMode === 'exp' }" @click="heatmapMode = 'exp'; loadHeatmap()">Uscite</button>
                        <button class="ctg-btn" :class="{ active: heatmapMode === 'inc' }" @click="heatmapMode = 'inc'; loadHeatmap()">Entrate</button>
                      </div>
                      <div class="hm-from-year" v-if="heatmapYearList.length > 1">
                        <span class="hm-from-label">Dal</span>
                        <select class="hm-year-select" v-model.number="heatmapFromYear" @change="loadHeatmap()">
                          <option v-for="y in heatmapYearList" :key="y" :value="y">{{ y }}</option>
                        </select>
                      </div>
                    </div>
                    <span class="heatmap-legend">
                      <span class="hml-low">basso</span>
                      <span class="hml-bar" :class="heatmapMode === 'inc' ? 'hml-bar-inc' : ''"></span>
                      <span class="hml-high">alto</span>
                    </span>
                  </div>
                  <!-- Tabella heatmap -->
                  <div class="heatmap-kpi-row" v-if="heatmapData.length">
                    <div class="hm-kpi">
                      <span class="hm-kpi-label">Mese Min</span>
                      <span :class="['hm-kpi-val', heatmapMode === 'exp' ? 'hm-kpi-low' : 'hm-kpi-high']">€ {{ fmt0(heatmapKpi.min) }}</span>
                      <span class="hm-kpi-sub">{{ heatmapKpi.minLabel }}</span>
                    </div>
                    <div class="hm-kpi">
                      <span class="hm-kpi-label">Mese Max</span>
                      <span :class="['hm-kpi-val', heatmapMode === 'exp' ? 'hm-kpi-high' : 'hm-kpi-low']">€ {{ fmt0(heatmapKpi.max) }}</span>
                      <span class="hm-kpi-sub">{{ heatmapKpi.maxLabel }}</span>
                    </div>
                    <div class="hm-kpi">
                      <span class="hm-kpi-label">Media Mensile</span>
                      <span class="hm-kpi-val">€ {{ fmt0(heatmapKpi.avg) }}</span>
                      <span class="hm-kpi-sub">per mese</span>
                    </div>
                    <div class="hm-kpi">
                      <span class="hm-kpi-label">Media Annuale</span>
                      <span class="hm-kpi-val">€ {{ fmt0(heatmapKpi.avgYear) }}</span>
                      <span class="hm-kpi-sub">per anno</span>
                    </div>
                  </div>
                  <div class="heatmap-scroll" v-if="heatmapData.length">
                    <table class="heatmap-table">
                      <thead>
                        <tr>
                          <th class="hm-year-col"></th>
                          <th v-for="m in heatmapMonths" :key="m" class="hm-month-col">{{ m }}</th>
                          <th class="hm-tot-col">TOT</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="row in heatmapData" :key="row.year">
                          <td class="hm-year-label">{{ row.year }}</td>
                          <td v-for="(val, mi) in row.months" :key="mi"
                              :class="['hm-cell', row.year === heatmapNowYear && mi > heatmapNowMonth ? 'hm-future' : '']"
                              :style="row.year === heatmapNowYear && mi > heatmapNowMonth ? {} : { background: heatColor(val, heatmapMax), color: val > heatmapMax * 0.55 ? '#fff' : 'inherit' }"
                              :title="row.year === heatmapNowYear && mi > heatmapNowMonth ? '' : `${heatmapMonths[mi]} ${row.year}: € ${fmt0(val)}`">
                            <span class="hm-val" v-if="val > 0 && !(row.year === heatmapNowYear && mi > heatmapNowMonth)">{{ fmtK(val) }}</span>
                          </td>
                          <td class="hm-total" :style="{ background: heatColor(row.total, heatmapYearMax), color: row.total > heatmapYearMax * 0.55 ? '#fff' : 'inherit' }">
                            {{ fmtK(row.total) }}
                          </td>
                        </tr>
                      </tbody>
                      <tfoot>
                        <tr>
                          <td class="hm-year-label">Media</td>
                          <td v-for="(avg, mi) in heatmapMonthAvg" :key="mi" class="hm-cell hm-avg">
                            {{ avg > 0 ? fmtK(avg) : '—' }}
                          </td>
                          <td class="hm-total hm-avg">{{ fmtK(heatmapGrandAvg) }}</td>
                        </tr>
                      </tfoot>
                    </table>
                  </div>
                  <div v-else class="chart-empty">
                    <svg viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="1.5" width="36" height="36" opacity="0.3"><rect x="4" y="4" width="8" height="8" rx="1"/><rect x="16" y="4" width="8" height="8" rx="1"/><rect x="28" y="4" width="8" height="8" rx="1"/><rect x="4" y="16" width="8" height="8" rx="1"/><rect x="16" y="16" width="8" height="8" rx="1"/><rect x="28" y="16" width="8" height="8" rx="1"/></svg>
                    <p>Nessun dato disponibile</p>
                  </div>
                </div>
              </TabPanel>
              <TabPanel value="anomalie">
                <div class="anomalie-wrap">
                  <!-- Header: selettore mese di riferimento -->
                  <div class="anomalie-header">
                    <div class="anomalie-title-group">
                      <span class="anomalie-label">Mese analizzato</span>
                      <select class="hm-year-select anomalie-month-sel" v-model="anomalieMonth" @change="loadAnomalie()">
                        <option v-for="m in anomalieMonthOptions" :key="m.value" :value="m.value">{{ m.label }}</option>
                      </select>
                    </div>
                    <span class="anomalie-sub">vs media degli ultimi 12 mesi</span>
                  </div>

                  <div v-if="anomalieData" class="anomalie-body">
                    <!-- Split: Cattivi | Buoni -->
                    <div class="anomalie-split">
                      <!-- CATTIVI: speso più del solito -->
                      <div class="anomalie-col anomalie-bad">
                        <div class="anomalie-col-header">
                          <svg viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="2" width="12" height="12"><path d="M7 2v6M4 5l3-3 3 3"/></svg>
                          Sopra la media
                        </div>
                        <div v-if="anomalieData.bad.length" class="anomalie-list">
                          <div v-for="item in anomalieData.bad" :key="item.cat" class="anomalie-item anomalie-item-bad">
                            <div class="ai-top">
                              <span class="ai-cat">{{ item.cat }}</span>
                              <span class="ai-delta bad-delta">+€ {{ fmt0(item.delta) }}</span>
                            </div>
                            <div class="ai-bar-wrap">
                              <div class="ai-bar-avg" :style="{ width: item.avgPct + '%' }"></div>
                              <div class="ai-bar-cur bad-bar" :style="{ width: item.curPct + '%' }"></div>
                            </div>
                            <div class="ai-vals">
                              <span class="ai-val-avg">Media: € {{ fmt0(item.avg) }}</span>
                              <span class="ai-val-cur">Questo mese: € {{ fmt0(item.cur) }}</span>
                            </div>
                          </div>
                        </div>
                        <div v-else class="anomalie-empty">
                          <span>✅ Nessuna categoria sopra la media</span>
                        </div>
                      </div>

                      <!-- BUONI: speso meno del solito -->
                      <div class="anomalie-col anomalie-good">
                        <div class="anomalie-col-header">
                          <svg viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="2" width="12" height="12"><path d="M7 12V6M4 9l3 3 3-3"/></svg>
                          Sotto la media
                        </div>
                        <div v-if="anomalieData.good.length" class="anomalie-list">
                          <div v-for="item in anomalieData.good" :key="item.cat" class="anomalie-item anomalie-item-good">
                            <div class="ai-top">
                              <span class="ai-cat">{{ item.cat }}</span>
                              <span class="ai-delta good-delta">-€ {{ fmt0(item.delta) }}</span>
                            </div>
                            <div class="ai-bar-wrap">
                              <div class="ai-bar-avg" :style="{ width: item.avgPct + '%' }"></div>
                              <div class="ai-bar-cur good-bar" :style="{ width: item.curPct + '%' }"></div>
                            </div>
                            <div class="ai-vals">
                              <span class="ai-val-avg">Media: € {{ fmt0(item.avg) }}</span>
                              <span class="ai-val-cur">Questo mese: € {{ fmt0(item.cur) }}</span>
                            </div>
                          </div>
                        </div>
                        <div v-else class="anomalie-empty">
                          <span>📊 Nessuna categoria sotto la media</span>
                        </div>
                      </div>
                    </div>

                    <!-- Scatter sanguisuga: alta freq, basso importo -->
                    <div class="sanguisuga-wrap" v-if="sanguisugaData && sanguisugaData.length">
                      <div class="sanguisuga-title">
                        <svg viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="2" width="11" height="11"><circle cx="7" cy="7" r="5"/><path d="M7 4v3l2 2"/></svg>
                        Spese frequenti a basso importo unitario — "sanguisughe"
                      </div>
                      <div class="sanguisuga-list">
                        <div v-for="s in sanguisugaData" :key="s.cat" class="sg-item">
                          <span class="sg-cat">{{ s.cat }}</span>
                          <span class="sg-freq">{{ s.count }}×</span>
                          <div class="sg-bar-wrap">
                            <div class="sg-bar" :style="{ width: s.pct + '%' }"></div>
                          </div>
                          <span class="sg-tot">€ {{ fmt0(s.total) }}</span>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div v-else class="chart-empty">
                    <svg viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="1.5" width="36" height="36" opacity="0.3"><path d="M20 4v18M10 13l10-9 10 9"/><circle cx="20" cy="28" r="4"/></svg>
                    <p>Seleziona un mese per l'analisi</p>
                  </div>
                </div>
              </TabPanel>

              <TabPanel value="previsioni">
                <div class="prev-wrap">

                  <!-- ① PREVISIONE STAGIONALE -->
                  <div class="prev-section" v-if="previsioneData">
                    <div class="prev-section-title">
                      <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><path d="M2 12 L5 8 L9 10 L14 4"/><path d="M14 4h-3M14 4v3" stroke-linecap="round"/></svg>
                      Previsione {{ MESI[new Date().getMonth()] }} {{ new Date().getFullYear() }}
                      <span class="prev-method-badge">{{ previsioneData.method }}</span>
                    </div>

                    <!-- KPI principali -->
                    <div class="prev-kpi-row">
                      <div class="prev-kpi">
                        <span class="prev-kpi-label">Entrate attese</span>
                        <span class="prev-kpi-val income-text">€ {{ Math.round(previsioneData.predInc).toLocaleString('it-IT') }}</span>
                        <span class="prev-kpi-sub" v-if="previsioneData.deltaIncYoY !== null">
                          <span :class="previsioneData.deltaIncYoY >= 0 ? 'clr-ok' : 'clr-warn'">{{ previsioneData.deltaIncYoY >= 0 ? '+' : '' }}{{ previsioneData.deltaIncYoY.toFixed(1) }}%</span>
                          vs {{ MESI[new Date().getMonth()] }} {{ new Date().getFullYear()-1 }}
                        </span>
                      </div>
                      <div class="prev-kpi">
                        <span class="prev-kpi-label">Uscite attese</span>
                        <span class="prev-kpi-val expense-text">€ {{ Math.round(previsioneData.predExp).toLocaleString('it-IT') }}</span>
                        <span class="prev-kpi-sub" v-if="previsioneData.deltaExpYoY !== null">
                          <span :class="previsioneData.deltaExpYoY <= 0 ? 'clr-ok' : 'clr-warn'">{{ previsioneData.deltaExpYoY >= 0 ? '+' : '' }}{{ previsioneData.deltaExpYoY.toFixed(1) }}%</span>
                          vs {{ MESI[new Date().getMonth()] }} {{ new Date().getFullYear()-1 }}
                        </span>
                      </div>
                      <div class="prev-kpi" :class="previsioneData.onTrack ? 'prev-kpi-ok' : 'prev-kpi-warn'">
                        <span class="prev-kpi-label">Risparmio atteso</span>
                        <span class="prev-kpi-val" :class="previsioneData.predNet >= 0 ? 'income-text' : 'expense-text'">
                          {{ previsioneData.predNet >= 0 ? '+' : '' }}€ {{ Math.round(Math.abs(previsioneData.predNet)).toLocaleString('it-IT') }}
                        </span>
                        <span class="prev-kpi-sub">target € {{ Math.round(previsioneData.targetEuro).toLocaleString('it-IT') }}</span>
                      </div>
                      <div class="prev-kpi" :class="previsioneData.deltaVsTarget >= 0 ? 'prev-kpi-ok' : 'prev-kpi-warn'">
                        <span class="prev-kpi-label">Delta vs target</span>
                        <span class="prev-kpi-val" :class="previsioneData.deltaVsTarget >= 0 ? 'clr-ok' : 'clr-warn'">
                          {{ previsioneData.deltaVsTarget >= 0 ? '+' : '' }}€ {{ Math.round(Math.abs(previsioneData.deltaVsTarget)).toLocaleString('it-IT') }}
                        </span>
                        <span class="prev-kpi-sub">{{ previsioneData.onTrack ? '✓ In target' : '⚠ Sotto target' }}</span>
                      </div>
                    </div>

                    <!-- Indicatori del modello -->
                    <div class="prev-model-row">
                      <div class="prev-model-item">
                        <span class="prev-model-label">Indice stagionale entrate</span>
                        <span class="prev-model-val" :class="previsioneData.seasonIdxInc >= 1 ? 'clr-ok' : 'clr-warn'">
                          {{ previsioneData.seasonIdxInc >= 1 ? '+' : '' }}{{ ((previsioneData.seasonIdxInc - 1)*100).toFixed(1) }}%
                        </span>
                        <span class="prev-model-sub">vs media mensile anni prec.</span>
                      </div>
                      <div class="prev-model-item">
                        <span class="prev-model-label">Indice stagionale uscite</span>
                        <span class="prev-model-val" :class="previsioneData.seasonIdxExp <= 1 ? 'clr-ok' : 'clr-warn'">
                          {{ previsioneData.seasonIdxExp >= 1 ? '+' : '' }}{{ ((previsioneData.seasonIdxExp - 1)*100).toFixed(1) }}%
                        </span>
                        <span class="prev-model-sub">vs media mensile anni prec.</span>
                      </div>
                      <div class="prev-model-item">
                        <span class="prev-model-label">Trend YTD entrate</span>
                        <span class="prev-model-val" :class="previsioneData.trendInc >= 1 ? 'clr-ok' : 'clr-warn'">
                          {{ previsioneData.trendInc >= 1 ? '+' : '' }}{{ ((previsioneData.trendInc - 1)*100).toFixed(1) }}%
                        </span>
                        <span class="prev-model-sub">gen-{{ MESI[new Date().getMonth()-1] }} vs anno scorso</span>
                      </div>
                      <div class="prev-model-item">
                        <span class="prev-model-label">Trend YTD uscite</span>
                        <span class="prev-model-val" :class="previsioneData.trendExp <= 1 ? 'clr-ok' : 'clr-warn'">
                          {{ previsioneData.trendExp >= 1 ? '+' : '' }}{{ ((previsioneData.trendExp - 1)*100).toFixed(1) }}%
                        </span>
                        <span class="prev-model-sub">gen-{{ MESI[new Date().getMonth()-1] }} vs anno scorso</span>
                      </div>
                    </div>
                  </div>

                  <!-- ② RUNWAY RISPARMIO -->
                  <div class="prev-section" v-if="runwayData">
                    <div class="prev-section-title">
                      <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><path d="M2 13 C4 10 6 11 8 8 S12 3 14 3"/></svg>
                      Runway risparmio — storico 12 mesi + proiezione 6
                    </div>
                    <div class="prev-chart-wrap">
                      <Chart type="line" :data="runwayData" :options="runwayOptions" style="height:100%;width:100%"/>
                    </div>
                  </div>

                  <div v-if="!previsioneData" class="chart-empty">
                    <svg viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="1.5" width="36" height="36" opacity="0.3"><path d="M4 30 L12 20 L20 22 L28 12 L36 15"/><path d="M36 15h-4M36 15v4"/></svg>
                    <p>Carica un database per vedere le previsioni</p>
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
import { ref, computed, watch, onMounted } from 'vue';
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

// ── GOOGLE AUTH / DRIVE ──
import { SocialLogin } from '@capgo/capacitor-social-login';
import { Preferences } from '@capacitor/preferences';
import { Capacitor } from '@capacitor/core';

const WEB_CLIENT_ID = '1045116249963-98lmpknvv2rcmi347cn87ju720182kjn.apps.googleusercontent.com';
const ANDROID_CLIENT_ID = '1045116249963-93qenf947tljv3a4hs5je5djgs5i78pu.apps.googleusercontent.com';
const CLOUD_FUNCTION_URL = 'https://europe-west1-money-manager-dashboard-495714.cloudfunctions.net/exchangeToken';

const DRIVE_REFRESH_TOKEN_KEY = 'mm_drive_refresh_token';
const DRIVE_USER_KEY = 'mm_drive_user';
const DRIVE_DIRECT_SESSION_KEY = 'mm_drive_direct_session';
const DRIVE_LAST_FILE_KEY = 'mm_drive_file_name';

const isNative = ref(
  Capacitor.isNativePlatform() ||
  window.location.href.startsWith('capacitor://') ||
  (typeof window.Capacitor !== 'undefined' && window.Capacitor.getPlatform() !== 'web')
);

const googleUser = ref(null);
const driveLoading = ref(false);
const driveError = ref('');
const driveAccessToken = ref(null);
const driveTokenExpiry = ref(0);
const nativeGoogleReady = ref(false);
const loginInFlight = ref(false);
const avatarError = ref(false);

const mmLog = (...args) => console.log('[MM]', ...args);

// Pref helpers: Capacitor Preferences su native, localStorage (con fallback) su web
const prefSet = async (key, value) => {
  if (isNative.value) {
    await Preferences.set({ key, value });
  } else {
    try { localStorage.setItem(key, value); } catch { /* iframe sandbox: ignora */ }
  }
};

const prefGet = async (key) => {
  if (isNative.value) {
    const { value } = await Preferences.get({ key });
    return value ?? null;
  } else {
    try { return localStorage.getItem(key) ?? null; } catch { return null; }
  }
};

const prefRemove = async (key) => {
  if (isNative.value) {
    await Preferences.remove({ key }).catch(() => {});
  } else {
    try { localStorage.removeItem(key); } catch { /* ignora */ }
  }
};

const saveDriveUser = async (user) => {
  if (!user) return;
  await prefSet(DRIVE_USER_KEY, JSON.stringify(user));
};

const loadDriveUser = async () => {
  const raw = await prefGet(DRIVE_USER_KEY);
  if (!raw) return null;
  try {
    return JSON.parse(raw);
  } catch {
    return null;
  }
};

const saveRefreshToken = async (refreshToken) => {
  if (!refreshToken) return;
  await prefSet(DRIVE_REFRESH_TOKEN_KEY, refreshToken);
};

const loadRefreshToken = async () => {
  const value = await prefGet(DRIVE_REFRESH_TOKEN_KEY);
  return value || null;
};

const clearRefreshToken = async () => {
  await prefRemove(DRIVE_REFRESH_TOKEN_KEY);
};

const markDirectTokenSession = async () => {
  await prefSet(DRIVE_DIRECT_SESSION_KEY, '1');
};

const clearDirectTokenSession = async () => {
  await prefRemove(DRIVE_DIRECT_SESSION_KEY);
};

const hasDirectTokenSession = async () => {
  const value = await prefGet(DRIVE_DIRECT_SESSION_KEY);
  return value === '1';
};

const saveLastDriveFileName = async (name) => {
  if (!name) return;
  await prefSet(DRIVE_LAST_FILE_KEY, name);
};

const loadLastDriveFileName = async () => {
  return await prefGet(DRIVE_LAST_FILE_KEY);
};

const clearDrivePersistence = async () => {
  await clearRefreshToken();
  await clearDirectTokenSession();
  await prefRemove(DRIVE_USER_KEY);
  await prefRemove(DRIVE_LAST_FILE_KEY);
};

const ensureNativeGoogleInitialized = async () => {
  if (!isNative.value || nativeGoogleReady.value) return;
  await SocialLogin.initialize({
    google: {
      webClientId: WEB_CLIENT_ID,
      mode: 'offline'
    }
  });
  nativeGoogleReady.value = true;
  mmLog('SocialLogin.initialize OK');
};

const normalizeGoogleProfile = (profile = {}) => {
  return {
    email: profile.email || '',
    name: profile.name || profile.displayName || profile.email || 'Google User',
    given_name: profile.givenName || profile.given_name || '',
    family_name: profile.familyName || profile.family_name || '',
    picture: profile.imageUrl || profile.image || profile.picture || ''
  };
};

const getAuthorizationCode = async () => {
  try {
    const result = await SocialLogin.getAuthorizationCode({ provider: 'google' });
    const code = result?.code || result?.serverAuthCode || '';
    mmLog('getAuthorizationCode result:', !!code);
    return code || null;
  } catch (e) {
    console.warn('[MM] getAuthorizationCode error:', e);
    return null;
  }
};

const exchangeAuthCodeForTokens = async (serverAuthCode) => {
  const resp = await fetch(CLOUD_FUNCTION_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      action: 'exchange',
      code: serverAuthCode
    })
  });

  const text = await resp.text().catch(() => '');
  let data = {};
  try {
    data = text ? JSON.parse(text) : {};
  } catch {
    data = { raw: text };
  }

  if (!resp.ok) {
    throw new Error(data?.error || data?.message || `HTTP ${resp.status}`);
  }

  if (!data?.access_token) {
    throw new Error('Access token non ricevuto dalla Cloud Function.');
  }

  driveAccessToken.value = data.access_token;
  driveTokenExpiry.value = Date.now() + ((data.expires_in || 3600) * 1000);

  if (data?.refresh_token) {
    await saveRefreshToken(data.refresh_token);
    await clearDirectTokenSession();
    mmLog('Refresh token salvato');
  } else {
    mmLog('Nessun refresh token ricevuto');
  }

  return data;
};

const refreshAccessToken = async (refreshToken) => {
  const resp = await fetch(CLOUD_FUNCTION_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      action: 'refresh',
      refresh_token: refreshToken
    })
  });

  if (!resp.ok) {
    const err = await resp.json().catch(() => ({}));
    throw new Error(err?.error || 'Refresh token non valido o scaduto.');
  }

  const data = await resp.json();
  if (!data?.access_token) {
    throw new Error('Access token non ricevuto dal refresh.');
  }

  driveAccessToken.value = data.access_token;
  driveTokenExpiry.value = Date.now() + ((data.expires_in || 3600) * 1000);
  return driveAccessToken.value;
};

const getDriveAccessToken = async ({ interactive = true } = {}) => {
  mmLog('getDriveAccessToken START', { interactive });

  if (driveAccessToken.value && Date.now() < driveTokenExpiry.value - 60000) {
    mmLog('Uso access token in memoria');
    return driveAccessToken.value;
  }

  const savedRefreshToken = await loadRefreshToken();
  mmLog('savedRefreshToken exists:', !!savedRefreshToken);

  if (savedRefreshToken) {
    try {
      const token = await refreshAccessToken(savedRefreshToken);
      mmLog('Refresh token OK');
      return token;
    } catch (e) {
      console.warn('[MM] Refresh token fallito:', e);
      await clearRefreshToken();
      driveAccessToken.value = null;
      driveTokenExpiry.value = 0;
      if (!interactive) return null;
    }
  }

  if (!interactive) {
    mmLog('Modalità silenziosa: nessun token disponibile');
    return null;
  }

  // Su web il login interattivo è gestito da GSI (il pulsante Google nella login screen)
  // Non tentiamo SocialLogin su piattaforma web
  if (!isNative.value) {
    mmLog('Web: token non disponibile, richiesto nuovo login GSI');
    return null;
  }

  await ensureNativeGoogleInitialized();

  const loginRes = await SocialLogin.login({
  provider: 'google',
  options: {
    scopes: [
      'openid',
      'profile',
      'email',
      'https://www.googleapis.com/auth/drive.readonly'
    ],
    prompt: 'consent',
    access_type: 'offline',
    include_granted_scopes: true
  }
});

  mmLog('Social login completato');

  const payload = loginRes?.result || loginRes || {};
  const profile = normalizeGoogleProfile(payload?.profile || {});
  const rawAccessToken = payload?.accessToken?.token || payload?.accessToken || '';
  const serverAuthCode =
    payload?.serverAuthCode ||
    payload?.authorizationCode ||
    payload?.authCode ||
    null;

  mmLog('offline serverAuthCode exists:', !!serverAuthCode);

  if (profile.email || profile.name || profile.picture) {
    googleUser.value = profile;
    await saveDriveUser(profile);
  }

    if (serverAuthCode) {
    const exchanged = await exchangeAuthCodeForTokens(serverAuthCode);
    return exchanged.access_token;
  }

  if (!rawAccessToken) {
    throw new Error('Login Google riuscito ma token Drive non disponibile.');
  }

  driveAccessToken.value = rawAccessToken;
  driveTokenExpiry.value = Date.now() + 3600 * 1000;
  await markDirectTokenSession();
  mmLog('Fallback a token diretto');
  return rawAccessToken;
};

const loadFromDrive = async ({ interactive = true, accessToken = null } = {}) => {
  mmLog('loadFromDrive START', { interactive });

  driveLoading.value = true;
  driveError.value = '';

  try {
    const token = accessToken || await getDriveAccessToken({ interactive });

    if (!token) {
      if (!interactive) return;
      throw new Error('Accesso a Google Drive non disponibile.');
    }

    const searchUrl = `https://www.googleapis.com/drive/v3/files?q=name+contains+'.mmbak'+and+trashed%3Dfalse&orderBy=modifiedTime+desc&fields=files(id,name,modifiedTime,size)&pageSize=10`;

    const searchResp = await fetch(searchUrl, {
      headers: { Authorization: `Bearer ${token}` }
    });

    if (!searchResp.ok) {
      throw new Error(`Errore ricerca Drive: ${searchResp.status}`);
    }

    const searchData = await searchResp.json();
    const files = searchData?.files || [];

    if (!files.length) {
      throw new Error('Nessun file .mmbak trovato su Google Drive.');
    }

    const file = files[0];
    statusMessage.value = `Scaricamento "${file.name}"...`;
    isError.value = false;

    const downloadResp = await fetch(
      `https://www.googleapis.com/drive/v3/files/${file.id}?alt=media`,
      {
        headers: { Authorization: `Bearer ${token}` }
      }
    );

    if (!downloadResp.ok) {
      throw new Error(`Errore download file: ${downloadResp.status}`);
    }

    const arrayBuffer = await downloadResp.arrayBuffer();
    const SQL = await initSqlJs({ locateFile: () => '/sql-wasm.wasm' });

    dbInstance = new SQL.Database(new Uint8Array(arrayBuffer));
    fileLoaded.value = true;
    loadedFileName.value = file.name;
    await saveLastDriveFileName(file.name);

    refreshData();
    statusMessage.value = `✅ Caricato da Drive: ${file.name}`;
    isError.value = false;

    mmLog('loadFromDrive OK', file.name);
  } catch (e) {
    console.error('[MM] Errore Drive:', e);
    driveError.value = e?.message || 'Errore caricamento da Drive.';
    statusMessage.value = driveError.value;
    isError.value = true;
  } finally {
    driveLoading.value = false;
    mmLog('loadFromDrive END');
  }
};

const loginNative = async () => {
  if (loginInFlight.value) {
    mmLog('loginNative ignorato: già in corso');
    return;
  }

  loginInFlight.value = true;
  driveLoading.value = true;
  driveError.value = '';
  isError.value = false;

  try {
    statusMessage.value = 'Accesso a Google...';
    await ensureNativeGoogleInitialized();

    const token = await getDriveAccessToken({ interactive: true });

    if (!token) {
      throw new Error('Token Google Drive non disponibile.');
    }

    statusMessage.value = 'Google Drive collegato. Carico il backup più recente...';
    await loadFromDrive({ interactive: false, accessToken: token });
  } catch (e) {
    console.error('[MM] loginNative error:', e);
    driveError.value = e?.message || 'Errore login Google Drive.';
    statusMessage.value = driveError.value;
    isError.value = true;
  } finally {
    driveLoading.value = false;
    loginInFlight.value = false;
    mmLog('loginNative END');
  }
};

const handleLogout = async () => {
  try {
    if (isNative.value) {
      await SocialLogin.logout({ provider: 'google' }).catch(() => {});
    }
  } finally {
    googleUser.value = null;
    avatarError.value = false;
    driveAccessToken.value = null;
    driveTokenExpiry.value = 0;
    driveError.value = '';
    await clearDrivePersistence();

    fileLoaded.value = false;
    loadedFileName.value = '';
    statusMessage.value = 'In attesa del file...';
    isError.value = false;
    dbInstance = null;

    if (!isNative.value) {
      setTimeout(() => initGoogleSignIn(), 150);
    }
  }
};

// ── LOGIN WEB (GSI) ──
const initGoogleSignIn = () => {
  if (!window.google?.accounts) return;

  window.google.accounts.id.initialize({
    client_id: WEB_CLIENT_ID,
    callback: async (response) => {
      try {
        const payload = JSON.parse(atob(response.credential.split('.')[1]));
        const user = {
          name: payload.name,
          given_name: payload.given_name,
          picture: payload.picture,
          email: payload.email
        };
        googleUser.value = user;
        await saveDriveUser(user);
      } catch (e) {
        console.error('Errore token Google:', e);
      }
    },
    auto_select: false,
    cancel_on_tap_outside: true
  });

  const btnEl = document.getElementById('google-signin-btn');
  if (btnEl) {
    btnEl.innerHTML = '';
    window.google.accounts.id.renderButton(btnEl, {
      theme: 'outline',
      size: 'large',
      shape: 'rectangular',
      text: 'signin_with',
      locale: 'it',
      width: 280
    });
  }

  window.google.accounts.id.prompt();
};

onMounted(async () => {
  isNative.value =
    Capacitor.isNativePlatform() ||
    window.location.href.startsWith('capacitor://') ||
    (typeof window.Capacitor !== 'undefined' && window.Capacitor.getPlatform() !== 'web');

  if (isNative.value) {
    try {
      await ensureNativeGoogleInitialized();

      const savedUser = await loadDriveUser();
      const savedRefreshToken = await loadRefreshToken();
      const directSession = await hasDirectTokenSession();
      const lastFileName = await loadLastDriveFileName();

      mmLog(
        'onMounted savedUser:',
        !!savedUser,
        'savedRt:',
        !!savedRefreshToken,
        'directSession:',
        !!directSession
      );

      if (savedUser) {
        googleUser.value = savedUser;
        avatarError.value = false;
      }

      if (savedUser && savedRefreshToken) {
        statusMessage.value = lastFileName
          ? `Riapro ${lastFileName} da Google Drive...`
          : 'Controllo backup su Google Drive...';
        isError.value = false;
        setTimeout(() => {
          loadFromDrive({ interactive: false });
        }, 250);
        return;
      }

      if (savedUser && directSession) {
  statusMessage.value = 'Sessione Google ripristinata. Ricollega Drive per il caricamento automatico persistente.';
  isError.value = false;
  return;
}

statusMessage.value = 'Accedi con Google o carica un file manualmente.';
    } catch (e) {
      console.error('[MM] onMounted restore error:', e);
      statusMessage.value = 'Errore nel ripristino sessione Google.';
      isError.value = true;
    }
  } else {
    // ── WEB: prova a ripristinare la sessione da localStorage ──
    try {
      const savedUser    = await loadDriveUser();
      const savedRt      = await loadRefreshToken();
      const lastFileName = await loadLastDriveFileName();

      mmLog('onMounted WEB — savedUser:', !!savedUser, '| savedRt:', !!savedRt);

      if (savedUser) {
        googleUser.value = savedUser;
        avatarError.value = false;
      }

      if (savedUser && savedRt) {
        // Refresh token presente: carica automaticamente il file Drive al riavvio
        statusMessage.value = lastFileName
          ? `Riapro ${lastFileName} da Google Drive...`
          : 'Controllo backup su Google Drive...';
        isError.value = false;

        const script = document.createElement('script');
        script.src    = 'https://accounts.google.com/gsi/client';
        script.async  = true;
        script.defer  = true;
        script.onload = () => {
          initGoogleSignIn();
          setTimeout(() => loadFromDrive({ interactive: false }), 300);
        };
        document.head.appendChild(script);
        return;
      }

      // Utente noto ma senza refresh token
      statusMessage.value = savedUser
        ? 'Bentornato! Accedi con Google Drive o carica un file.'
        : 'Accedi con Google Drive o carica un file manualmente.';
      isError.value = false;

    } catch (e) {
      mmLog('onMounted WEB restore error:', e);
      statusMessage.value = 'Accedi con Google Drive o carica un file manualmente.';
    }

    const script = document.createElement('script');
    script.src    = 'https://accounts.google.com/gsi/client';
    script.async  = true;
    script.defer  = true;
    script.onload = () => initGoogleSignIn();
    document.head.appendChild(script);
  }
});

// ── TEMA ──
const theme = ref(window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
const toggleTheme = () => { theme.value = theme.value === 'dark' ? 'light' : 'dark'; };

// ── STATO ──
let dbInstance = null;
const selectedPeriod = ref('current_month');
const customStart = ref('');
const customEnd   = ref('');
const showCustom  = computed(() => selectedPeriod.value === 'custom');
const statusMessage = ref('In attesa del file...');
const isError = ref(false);
const fileLoaded = ref(false);
const loadedFileName = ref('');
const animating = ref(false);
const activeBottomTab = ref('trend');

const currentStats = ref({ income: 0, expense: 0, net: 0, rate: 0, sumNecessity: 0, sumExtra: 0 });

// ── BURN RATE ──
const burnTimePct = computed(() => {
  const now = new Date();
  const daysInMonth = new Date(now.getFullYear(), now.getMonth() + 1, 0).getDate();
  return (now.getDate() / daysInMonth) * 100;
});
const burnDaysLeft = computed(() => {
  const now = new Date();
  const daysInMonth = new Date(now.getFullYear(), now.getMonth() + 1, 0).getDate();
  return daysInMonth - now.getDate();
});
const burnSpendPct = computed(() => {
  const budget = currentStats.value.income; // usiamo entrate come budget totale
  if (!budget) return 0;
  return Math.min((currentStats.value.expense / budget) * 100, 100);
});
const burnBudgetLeft = computed(() => {
  return Math.max(currentStats.value.income - currentStats.value.expense, 0);
});
const burnDailyBudget = computed(() => {
  const days = burnDaysLeft.value;
  if (!days) return null;
  return burnBudgetLeft.value / days;
});
const burnColor = computed(() => {
  const diff = burnSpendPct.value - burnTimePct.value;
  if (diff <= 0)   return '#10b981'; // verde — sotto il ritmo
  if (diff <= 10)  return '#f59e0b'; // arancione — sul filo
  return '#ef4444';                  // rosso — troppo veloce
});
const burnVerdict = computed(() => {
  const diff = burnSpendPct.value - burnTimePct.value;
  if (diff <= 0)  return '✓ Ottimo ritmo';
  if (diff <= 10) return '⚡ Sul filo';
  return '⚠ Rallenta!';
});
const burnVerdictClass = computed(() => {
  const diff = burnSpendPct.value - burnTimePct.value;
  if (diff <= 0)  return 'verdict-ok';
  if (diff <= 10) return 'verdict-warn';
  return 'verdict-bad';
});
// SVG arc path per gauge semi-cerchio (da -180° a 0°, cioè da sx a dx)
const burnArcPath = computed(() => {
  const pct = Math.min(burnSpendPct.value / 100, 1);
  const angle = Math.PI * pct; // da 0 a π
  const r = 80, cx = 100, cy = 100;
  const startX = cx - r, startY = cy;
  const endX = cx + Math.cos(Math.PI - angle) * r;
  const endY = cy - Math.sin(angle) * r;
  const largeArc = pct > 0.5 ? 1 : 0;
  if (pct <= 0) return `M ${startX} ${startY} A ${r} ${r} 0 0 1 ${startX + 0.01} ${startY}`;
  return `M ${startX} ${startY} A ${r} ${r} 0 0 1 ${endX} ${endY}`;
});

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
const activeCfTab = ref('cashflow');

// ── TOP CATEGORIE ──
const topCatData    = ref(null);
const topCatOptions = ref({});

// ── ANOMALIE & SANGUISUGHE ──
const anomalieMonth       = ref('');
const anomalieMonthOptions = ref([]);
const anomalieData        = ref(null);

// ── PREVISIONI ──
const previsioneData      = ref(null);   // { proiezione, target, pctMonth, daysLeft, dailyPace, projectedExpense, projectedSaving }
const runwayData          = ref(null);   // Chart.js data per linea storica + proiezione
const runwayOptions       = ref(null);
const ricorrenzeData      = ref(null);   // { abbonamenti: [], periodiche: [] }
const sanguisugaData      = ref(null);


const loadPrevisioni = () => {
  if (!dbInstance) return;
  try {
    const now      = new Date();
    const y        = now.getFullYear();
    const m        = now.getMonth();           // 0-based
    const dayOfMonth = now.getDate();
    const isPostMid  = dayOfMonth >= 15;       // ibrido post-15

    const safeVal = (q) => {
      try { const r = dbInstance.exec(q); return (r.length && r[0].values[0][0]) ? Number(r[0].values[0][0]) : 0; }
      catch(e) { return 0; }
    };
    const ms = (yr, mo, d1, d2) => {
      const s = new Date(yr, mo, d1 || 1).getTime();
      const e = d2 ? new Date(yr, mo, d2, 23,59,59,999).getTime()
                   : new Date(yr, mo+1, 0, 23,59,59,999).getTime();
      return { s, e };
    };
    const monthInc = (yr, mo) => safeVal(`SELECT SUM(ZMONEY) FROM INOUTCOME WHERE DO_TYPE=0 AND CAST(ZDATE AS REAL) BETWEEN ${ms(yr,mo).s} AND ${ms(yr,mo).e} AND CAST(ZDATE AS REAL)>1000000000000`);
    const monthExp = (yr, mo) => safeVal(`SELECT SUM(ZMONEY) FROM INOUTCOME WHERE DO_TYPE=1 AND CAST(ZDATE AS REAL) BETWEEN ${ms(yr,mo).s} AND ${ms(yr,mo).e} AND CAST(ZDATE AS REAL)>1000000000000`);

    // ── A) METODO STAGIONALE (tuo modello) ────────────────────────────────────
    // 1. Indice stagionale del mese corrente su anni precedenti
    //    Per ogni anno con dati: rapporto tra mese M e media mensile dell'anno
    const seasonalInc = [], seasonalExp = [];
    for (let dy = 1; dy <= 3; dy++) {
      const py = y - dy;
      const annualInc = Array.from({length:12}, (_,i) => monthInc(py, i)).reduce((a,b) => a+b, 0);
      const annualExp = Array.from({length:12}, (_,i) => monthExp(py, i)).reduce((a,b) => a+b, 0);
      const avgMonthInc = annualInc / 12;
      const avgMonthExp = annualExp / 12;
      const mInc = monthInc(py, m);
      const mExp = monthExp(py, m);
      if (avgMonthInc > 0 && mInc > 0) seasonalInc.push(mInc / avgMonthInc);
      if (avgMonthExp > 0 && mExp > 0) seasonalExp.push(mExp / avgMonthExp);
    }
    const seasonIdxInc = seasonalInc.length ? seasonalInc.reduce((a,b)=>a+b,0)/seasonalInc.length : 1;
    const seasonIdxExp = seasonalExp.length ? seasonalExp.reduce((a,b)=>a+b,0)/seasonalExp.length : 1;

    // 2. Trend YTD: gen-(m-1) di quest'anno vs stesso periodo anno scorso
    let trendInc = 1, trendExp = 1;
    if (m > 0) {
      let ytdCurInc = 0, ytdCurExp = 0, ytdPrevInc = 0, ytdPrevExp = 0;
      for (let i = 0; i < m; i++) {
        ytdCurInc  += monthInc(y,   i);
        ytdCurExp  += monthExp(y,   i);
        ytdPrevInc += monthInc(y-1, i);
        ytdPrevExp += monthExp(y-1, i);
      }
      if (ytdPrevInc > 0) trendInc = ytdCurInc / ytdPrevInc;
      if (ytdPrevExp > 0) trendExp = ytdCurExp / ytdPrevExp;
    }

    // 3. Base: media mensile anno scorso
    const baseInc12 = Array.from({length:12}, (_,i) => monthInc(y-1, i)).reduce((a,b)=>a+b,0) / 12;
    const baseExp12 = Array.from({length:12}, (_,i) => monthExp(y-1, i)).reduce((a,b)=>a+b,0) / 12;

    // 4. Previsione stagionale pura
    let predIncSeasonal = baseInc12 * seasonIdxInc * trendInc;
    let predExpSeasonal = baseExp12 * seasonIdxExp * trendExp;

    // ── B) METODO FALLBACK: media ponderata mese M ultimi 3 anni ─────────────
    const sameMoVals = [1,2,3].map(dy => ({ inc: monthInc(y-dy, m), exp: monthExp(y-dy, m) })).filter(v => v.inc > 0);
    const weights    = [0.50, 0.33, 0.17].slice(0, sameMoVals.length);
    const wSum       = weights.reduce((a,b)=>a+b, 0);
    const predIncFallback = wSum > 0 ? sameMoVals.reduce((a,v,i) => a + v.inc * weights[i], 0) / wSum : predIncSeasonal;
    const predExpFallback = wSum > 0 ? sameMoVals.reduce((a,v,i) => a + v.exp * weights[i], 0) / wSum : predExpSeasonal;

    // ── C) IBRIDO POST-15: blenda previsione con dati reali ───────────────────
    let predInc, predExp, method;
    if (isPostMid) {
      const curInc = monthInc(y, m);
      const curExp = monthExp(y, m);
      const daysTotal = new Date(y, m+1, 0).getDate();
      // Peso: più giorni passati → più peso ai dati reali
      const wReal = (dayOfMonth - 14) / (daysTotal - 14);   // 0 al 15°, 1 all'ultimo
      const wPred = 1 - wReal;
      // Scala i dati reali a fine mese
      const scaledInc = curInc / (dayOfMonth / daysTotal);
      const scaledExp = curExp / (dayOfMonth / daysTotal);
      predInc = scaledInc * wReal + predIncSeasonal * wPred;
      predExp = scaledExp * wReal + predExpSeasonal * wPred;
      method  = `Ibrido (${dayOfMonth}gg reali + stagionale)`;
    } else {
      predInc = predIncSeasonal;
      predExp = predExpSeasonal;
      method  = 'Stagionale puro';
    }

    // Fallback: se stagionale dà 0 per dati insufficienti
    if (predInc < 1) { predInc = predIncFallback; predExp = predExpFallback; method += ' [fallback]'; }

    const predNet = predInc - predExp;
    const targetPct = (100 - budgetSettings.value.necessity - budgetSettings.value.extra) / 100;
    const targetEuro = predInc * targetPct;
    const deltaVsTarget = predNet - targetEuro;

    // Confronto vs stesso mese anno scorso
    const lastYearInc = monthInc(y-1, m);
    const lastYearExp = monthExp(y-1, m);
    const deltaIncYoY = lastYearInc > 0 ? ((predInc - lastYearInc) / lastYearInc * 100) : null;
    const deltaExpYoY = lastYearExp > 0 ? ((predExp - lastYearExp) / lastYearExp * 100) : null;

    previsioneData.value = {
      predInc, predExp, predNet, targetEuro, deltaVsTarget,
      seasonIdxInc, seasonIdxExp, trendInc, trendExp,
      lastYearInc, lastYearExp, deltaIncYoY, deltaExpYoY,
      method, isPostMid, dayOfMonth,
      onTrack: predNet >= targetEuro,
      // Fallback per confronto
      predIncFallback, predExpFallback
    };

    // ── RUNWAY: storico 12 mesi + proiezione 6 mesi ──────────────────────────
    let cum = 0;
    const historicalLabels = [], historicalCum = [];
    for (let i = 11; i >= 0; i--) {
      const d = new Date(y, m - i, 1);
      const inc = monthInc(d.getFullYear(), d.getMonth());
      const exp = monthExp(d.getFullYear(), d.getMonth());
      cum += (inc - exp);
      historicalLabels.push(MESI[d.getMonth()] + " '" + String(d.getFullYear()).slice(2));
      historicalCum.push(Math.round(cum));
    }

    // Proiezione: usa indici stagionali per i prossimi 6 mesi
    const projNull = [...new Array(historicalLabels.length - 1).fill(null), historicalCum[historicalCum.length - 1]];
    const projValues = [];
    const projLabels = [];
    let projCum = cum;
    for (let i = 1; i <= 6; i++) {
      const fd = new Date(y, m + i, 1);
      const fm = fd.getMonth(), fy = fd.getFullYear();
      // Indice stagionale per il mese futuro
      const futureSeasonalInc = [1,2,3].map(dy => {
        const a = Array.from({length:12},(_,k)=>monthInc(fy-dy,k)).reduce((a,b)=>a+b,0)/12;
        const mi = monthInc(fy-dy, fm);
        return a > 0 && mi > 0 ? mi/a : null;
      }).filter(v => v !== null);
      const futSeasonIdx = futureSeasonalInc.length ? futureSeasonalInc.reduce((a,b)=>a+b,0)/futureSeasonalInc.length : 1;
      const futureSeasonalExp = [1,2,3].map(dy => {
        const a = Array.from({length:12},(_,k)=>monthExp(fy-dy,k)).reduce((a,b)=>a+b,0)/12;
        const me = monthExp(fy-dy, fm);
        return a > 0 && me > 0 ? me/a : null;
      }).filter(v => v !== null);
      const futSeasonExpIdx = futureSeasonalExp.length ? futureSeasonalExp.reduce((a,b)=>a+b,0)/futureSeasonalExp.length : 1;

      const futInc = baseInc12 * futSeasonIdx * trendInc;
      const futExp = baseExp12 * futSeasonExpIdx * trendExp;
      projCum += (futInc - futExp);
      projValues.push(Math.round(projCum));
      projLabels.push(MESI[fm] + " '" + String(fy).slice(2));
    }

    const allLabels = [...historicalLabels, ...projLabels];
    const histPad   = [...historicalCum, ...new Array(6).fill(null)];
    const projPad   = [...projNull, ...projValues];

    const isDark = theme.value === 'dark';
    runwayData.value = {
      labels: allLabels,
      datasets: [
        { label: 'Storico', data: histPad, borderColor: isDark?'#6ee7b7':'#059669', backgroundColor: isDark?'rgba(110,231,183,0.10)':'rgba(5,150,105,0.08)', borderWidth:2.5, tension:0.35, fill:true, pointRadius:3, pointBackgroundColor:isDark?'#6ee7b7':'#059669', spanGaps:false },
        { label: 'Proiezione', data: projPad, borderColor: isDark?'#fbbf24':'#d97706', backgroundColor:'transparent', borderWidth:2, borderDash:[5,4], tension:0.35, pointRadius: ctx => ctx.dataIndex === 0 ? 0 : 4, pointBackgroundColor:isDark?'#fbbf24':'#d97706', spanGaps:false }
      ]
    };
    runwayOptions.value = {
      responsive:true, maintainAspectRatio:false, interaction:{mode:'index',intersect:false},
      plugins:{
        legend:{ display:true, position:'top', align:'end', labels:{boxWidth:10,boxHeight:10,borderRadius:4,font:{size:11,family:'Inter, sans-serif',weight:'600'},color:isDark?'#94a3b8':'#64748b',usePointStyle:true}},
        tooltip:{ backgroundColor:isDark?'rgba(28,27,25,0.95)':'rgba(15,23,42,0.95)', titleColor:isDark?'#94a3b8':'#cbd5e1', bodyColor:'#f1f5f9', padding:12, cornerRadius:8, callbacks:{label:ctx=>` € ${Math.round(ctx.raw).toLocaleString('it-IT')}`}}
      },
      scales:{
        x:{grid:{display:false},border:{display:false},ticks:{font:{size:10,weight:'600',family:'Inter, sans-serif'},color:isDark?'#64748b':'#94a3b8',maxRotation:0}},
        y:{grace:'10%',border:{display:false},grid:{color:isDark?'rgba(255,255,255,0.04)':'rgba(0,0,0,0.04)'},ticks:{font:{size:10,family:'Inter, sans-serif'},color:isDark?'#64748b':'#94a3b8',callback:v=>Math.abs(v)>=1000?`€ ${(v/1000).toFixed(1)}k`:`€ ${v}`}}
      }
    };

    // ── RICORRENZE: sezione C (abbonamenti fissi) + sezione A (periodiche) ──

    const since18 = new Date(y, m - 18, 1).getTime();
    const safeRows = (q) => { try { const r = dbInstance.exec(q); return r.length && r[0].values ? r[0].values : []; } catch(e) { return []; } };

    // Tutte le transazioni degli ultimi 18 mesi per categoria (sottocategorie)
    const allTxRows = safeRows(`
      SELECT s.name, CAST(i.ZDATE AS REAL) as ts, i.ZMONEY
      FROM INOUTCOME i
      LEFT JOIN ZCATEGORY s ON i.ctguid = s.uid
      WHERE i.DO_TYPE = 1
        AND CAST(i.ZDATE AS REAL) > ${since18}
        AND CAST(i.ZDATE AS REAL) > 1000000000000
        AND s.name IS NOT NULL AND s.name != ''
        AND s.puid IS NOT NULL
      ORDER BY s.name, ts
    `);

    // Raggruppa per categoria → mappa cat → [{ts, amount}]
    const catMap = {};
    allTxRows.forEach(([cat, ts, amount]) => {
      if (!catMap[cat]) catMap[cat] = [];
      catMap[cat].push({ ts: Number(ts), amount: Number(amount) });
    });

    // ── SEZIONE C: Abbonamenti fissi ──────────────────────────────────────────
    // Criteri: appare ogni mese (o quasi) con importo a bassa varianza (CV < 15%)
    const abbonamenti = [];
    Object.entries(catMap).forEach(([cat, txs]) => {
      // Raggruppa per mese
      const byMonth = {};
      txs.forEach(({ ts, amount }) => {
        const d = new Date(ts);
        const key = `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}`;
        if (!byMonth[key]) byMonth[key] = 0;
        byMonth[key] += amount;
      });
      const monthlyAmounts = Object.values(byMonth);
      if (monthlyAmounts.length < 3) return; // troppo pochi mesi

      // Frequenza: almeno 60% dei mesi negli ultimi 12
      const last12months = [];
      for (let i = 0; i < 12; i++) {
        const d = new Date(y, m - i, 1);
        const key = `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}`;
        last12months.push(key);
      }
      const presentIn12 = last12months.filter(k => byMonth[k]).length;
      if (presentIn12 < 7) return; // meno del 60% dei mesi

      // Varianza coefficiente (CV = std/mean) — bassa = importo costante
      const mean = monthlyAmounts.reduce((a,b)=>a+b,0) / monthlyAmounts.length;
      const std  = Math.sqrt(monthlyAmounts.map(v=>(v-mean)**2).reduce((a,b)=>a+b,0) / monthlyAmounts.length);
      const cv   = mean > 0 ? std / mean : 1;
      if (cv > 0.20) return; // troppo variabile per essere un abbonamento

      // Presente questo mese?
      const curKey = `${y}-${String(m+1).padStart(2,'0')}`;
      const paidThisMonth = !!byMonth[curKey];

      abbonamenti.push({ cat, mean: Math.round(mean), cv: Math.round(cv*100), presentIn12, paidThisMonth });
    });
    abbonamenti.sort((a,b) => b.mean - a.mean);

    // ── SEZIONE A: Spese periodiche in arrivo ─────────────────────────────────
    // Criteri: appare 2-6 volte in 18 mesi (non mensile), con intervallo stimato
    const periodiche = [];
    Object.entries(catMap).forEach(([cat, txs]) => {
      const byMonth = {};
      txs.forEach(({ ts, amount }) => {
        const d = new Date(ts);
        const key = `${d.getFullYear()}-${d.getMonth()}`;
        if (!byMonth[key]) byMonth[key] = { total: 0, d };
        byMonth[key].total += amount;
        byMonth[key].d = d;
      });
      const entries = Object.values(byMonth).sort((a,b) => a.d - b.d);
      if (entries.length < 2 || entries.length > 7) return; // skip mensili e rarissime

      // Non deve essere già un abbonamento
      if (abbonamenti.find(a => a.cat === cat)) return;

      const avgAmount = entries.reduce((a,e) => a + e.total, 0) / entries.length;

      // Intervallo medio tra occorrenze (in mesi)
      let intervals = [];
      for (let i = 1; i < entries.length; i++) {
        const diff = (entries[i].d.getFullYear() - entries[i-1].d.getFullYear()) * 12
                   + (entries[i].d.getMonth() - entries[i-1].d.getMonth());
        if (diff > 0) intervals.push(diff);
      }
      const avgInterval = intervals.length ? Math.round(intervals.reduce((a,b)=>a+b,0)/intervals.length) : 6;
      if (avgInterval <= 2 || avgInterval > 12) return; // esclude quasi-mensili (≤2 mesi)

      // Ultima occorrenza
      const lastEntry = entries[entries.length - 1];
      const lastDate  = lastEntry.d;
      const nextDate  = new Date(lastDate.getFullYear(), lastDate.getMonth() + avgInterval, 1);
      const monthsUntil = (nextDate.getFullYear() - y) * 12 + (nextDate.getMonth() - m);
      if (monthsUntil > 1 || monthsUntil < -1) return; // mostra solo: scaduto, questo mese, mese prossimo
      if (avgAmount < 25) return; // ignora spese troppo piccole

      const isPast    = monthsUntil < 0;
      const isCurrent = monthsUntil === 0;
      const nextLabel = isCurrent ? 'Questo mese'
                      : isPast    ? `Scaduto (${MESI[nextDate.getMonth()]})`
                      : 'Mese prossimo';

      periodiche.push({ cat, avgAmount, avgInterval, lastDate, nextLabel, isPast, isCurrent, monthsUntil, nOccorrenze: entries.length });
    });
    periodiche.sort((a,b) => a.monthsUntil - b.monthsUntil);

    ricorrenzeData.value = { abbonamenti, periodiche };

  } catch(e) { console.error('loadPrevisioni', e); previsioneData.value = null; }
};


const loadAnomalie = () => {
  if (!dbInstance) return;
  if (!anomalieMonth.value) { initAnomalieMonths(); }
  if (!anomalieMonth.value) return;
  try {
    const [y, m] = anomalieMonth.value.split('-').map(Number);
    const curStart = new Date(y, m - 1, 1).getTime();
    const curEnd   = new Date(y, m, 0, 23, 59, 59, 999).getTime();

    // Ultimi 6 mesi prima del mese selezionato
    const histEnd   = curStart - 1;
    const histStart = new Date(y, m - 13, 1).getTime();  // 12 mesi precedenti

    const safeExec = (q) => { try { const r = dbInstance.exec(q); return r.length && r[0].values ? r[0].values : []; } catch(e) { return []; } };

    // Rileva colonna data: prova ZDATE, fallback WDATE
    let curRows = safeExec(`
      SELECT s.name, SUM(i.ZMONEY) as tot
      FROM INOUTCOME i
      LEFT JOIN ZCATEGORY s ON i.ctguid = s.uid
      WHERE i.DO_TYPE = 1
        AND CAST(i.ZDATE AS REAL) BETWEEN ${curStart} AND ${curEnd}
        AND CAST(i.ZDATE AS REAL) > 1000000000000
        AND s.name IS NOT NULL AND s.name != ''
        AND s.puid IS NOT NULL
      GROUP BY s.uid ORDER BY tot DESC LIMIT 20
    `);
    let dc = 'ZDATE';
    if (!curRows.length) {
      dc = 'WDATE';
      curRows = safeExec(`
        SELECT s.name, SUM(i.ZMONEY) as tot
        FROM INOUTCOME i
        LEFT JOIN ZCATEGORY s ON i.ctguid = s.uid
        WHERE i.DO_TYPE = 1
          AND CAST(i.WDATE AS REAL) BETWEEN ${curStart} AND ${curEnd}
          AND CAST(i.WDATE AS REAL) > 1000000000000
          AND s.name IS NOT NULL AND s.name != ''
          AND s.puid IS NOT NULL
        GROUP BY s.uid ORDER BY tot DESC LIMIT 20
      `);
    }

    // Media storica per categoria (6 mesi precedenti)
    const histRows = safeExec(`
      SELECT s.name, SUM(i.ZMONEY) / 12.0 as avg_monthly
      FROM INOUTCOME i
      LEFT JOIN ZCATEGORY s ON i.ctguid = s.uid
      WHERE i.DO_TYPE = 1
        AND CAST(i.${dc} AS REAL) BETWEEN ${histStart} AND ${histEnd}
        AND CAST(i.${dc} AS REAL) > 1000000000000
        AND s.name IS NOT NULL AND s.name != ''
        AND s.puid IS NOT NULL
      GROUP BY s.uid
    `);

    const histMap = {};
    histRows.forEach(([name, avg]) => { histMap[name] = Number(avg) || 0; });

    // Calcola delta — includi tutte le categorie con almeno 1€
    const items = curRows
      .map(([cat, cur]) => {
        const avg   = histMap[cat] || 0;
        const delta = Number(cur) - avg;
        return { cat, cur: Number(cur), avg, delta };
      })
      .filter(x => x.cur > 1);

    const maxVal = Math.max(...items.map(x => Math.max(x.cur, x.avg)), 1);
    const enrich = items.map(x => ({
      ...x,
      curPct: Math.round((x.cur / maxVal) * 100),
      avgPct: Math.round((x.avg / maxVal) * 100),
      delta:  Math.abs(x.delta)
    }));

    // Soglia: delta > 15% della media storica (evita rumore su variazioni minime)
    const bad  = enrich.filter(x => x.cur > x.avg && x.avg > 0 && (x.cur - x.avg) / x.avg > 0.15)
                       .sort((a,b) => b.delta - a.delta).slice(0, 6);
    // Includi anche categorie nuove (avg=0) con spesa significativa (>30€)
    const badNew = enrich.filter(x => x.avg === 0 && x.cur > 30)
                         .sort((a,b) => b.cur - a.cur).slice(0, 2);
    const good = enrich.filter(x => x.cur < x.avg && x.avg > 0 && (x.avg - x.cur) / x.avg > 0.15)
                       .sort((a,b) => b.delta - a.delta).slice(0, 6);
    const allBad = [...bad, ...badNew].slice(0, 6);

    anomalieData.value = { bad: allBad, good };

    // Sanguisughe: alta frequenza, importo unitario basso (threshold: ≥3 transazioni, media ≤ 50€)
    const sgRows = safeExec(`
      SELECT s.name, COUNT(*) as cnt, SUM(i.ZMONEY) as tot, AVG(i.ZMONEY) as avg_tx
      FROM INOUTCOME i
      LEFT JOIN ZCATEGORY s ON i.ctguid = s.uid
      WHERE i.DO_TYPE = 1
        AND CAST(i.${dc} AS REAL) BETWEEN ${curStart} AND ${curEnd}
        AND CAST(i.${dc} AS REAL) > 1000000000000
        AND s.name IS NOT NULL AND s.name != ''
        AND s.puid IS NOT NULL
      GROUP BY s.uid
      HAVING cnt >= 3 AND avg_tx <= 15
      ORDER BY cnt DESC LIMIT 8
    `);

    if (sgRows.length) {
      const sgMax = Math.max(...sgRows.map(r => Number(r[2])), 1);
      sanguisugaData.value = sgRows.map(([cat, count, total]) => ({
        cat, count: Number(count), total: Number(total),
        pct: Math.round((Number(total) / sgMax) * 100)
      }));
    } else {
      sanguisugaData.value = null;
    }

  } catch(e) { console.error('loadAnomalie', e); anomalieData.value = null; }
};

// Popola le opzioni del selettore mese anomalie (ultimi 18 mesi)
const initAnomalieMonths = () => {
  const opts = [];
  const now = new Date();
  for (let i = 0; i < 18; i++) {
    const d = new Date(now.getFullYear(), now.getMonth() - i, 1);
    const val = `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}`;
    const label = d.toLocaleDateString('it-IT', { month: 'long', year: 'numeric' });
    opts.push({ value: val, label });
  }
  anomalieMonthOptions.value = opts;
  // Imposta default solo se il mese attuale non è già selezionato o non è valido
  const validValues = opts.map(o => o.value);
  if (!anomalieMonth.value || !validValues.includes(anomalieMonth.value)) {
    anomalieMonth.value = opts[0]?.value || '';
  }
};

// ── HEATMAP ANNO × MESE ──
const heatmapMode     = ref('exp');   // 'exp' | 'inc'
const heatmapData     = ref([]);
const heatmapMax      = ref(1);
const heatmapYearMax  = ref(1);
const heatmapMonthAvg = ref(Array(12).fill(0));
const heatmapGrandAvg = ref(0);
const heatmapMonths   = ['Gen','Feb','Mar','Apr','Mag','Giu','Lug','Ago','Set','Ott','Nov','Dic'];
const heatmapKpi      = ref({ min: 0, minLabel: '', max: 0, maxLabel: '', avg: 0, avgYear: 0 });
const heatmapFromYear = ref(null);   // null = tutti gli anni
const heatmapYearList = ref([]);     // anni disponibili nei dati
const heatmapNowYear  = new Date().getFullYear();
const heatmapNowMonth = new Date().getMonth(); // 0-based

const heatColor = (val, max) => {
  if (!val || !max) return 'transparent';
  const t = Math.min(val / max, 1);
  const isDark = theme.value === 'dark';
  if (heatmapMode.value === 'exp') {
    // Spese: bianco → arancio → rosso scuro
    if (isDark) {
      const r = Math.round(30  + t * 200);
      const g = Math.round(20  + (1-t) * 80);
      const b = Math.round(20  + (1-t) * 30);
      return `rgb(${r},${g},${b})`;
    } else {
      const r = Math.round(255);
      const g = Math.round(245 - t * 185);
      const b = Math.round(235 - t * 215);
      return `rgb(${r},${g},${b})`;
    }
  } else {
    // Entrate: bianco → verde acqua → verde scuro
    if (isDark) {
      const r = Math.round(10  + (1-t) * 30);
      const g = Math.round(60  + t * 130);
      const b = Math.round(50  + t * 60);
      return `rgb(${r},${g},${b})`;
    } else {
      const r = Math.round(240 - t * 210);
      const g = Math.round(255 - t * 60);
      const b = Math.round(240 - t * 140);
      return `rgb(${r},${g},${b})`;
    }
  }
};

const fmtK = (v) => {
  if (!v) return '';
  if (v >= 1000) return (v/1000).toFixed(1).replace('.0','') + 'k';
  return Math.round(v).toString();
};

const loadHeatmap = () => {
  if (!dbInstance) return;
  try {
    const doType = heatmapMode.value === 'exp' ? 1 : 0;
    const safeExec = (q) => { try { const r = dbInstance.exec(q); return (r.length && r[0].values) ? r[0].values : []; } catch(e) { return []; } };

    // Prendi tutti i dati aggregati per anno-mese, prova ZDATE poi WDATE
    let rows = safeExec(`
      SELECT
        CAST(strftime('%Y', datetime(CAST(ZDATE AS REAL)/1000, 'unixepoch')) AS INTEGER) as yr,
        CAST(strftime('%m', datetime(CAST(ZDATE AS REAL)/1000, 'unixepoch')) AS INTEGER) as mo,
        SUM(ZMONEY) as tot
      FROM INOUTCOME
      WHERE DO_TYPE = ${doType} AND ZDATE IS NOT NULL AND CAST(ZDATE AS REAL) > 0
      GROUP BY yr, mo
      ORDER BY yr, mo
    `);

    if (!rows.length) {
      rows = safeExec(`
        SELECT
          CAST(strftime('%Y', datetime(CAST(WDATE AS REAL)/1000, 'unixepoch')) AS INTEGER) as yr,
          CAST(strftime('%m', datetime(CAST(WDATE AS REAL)/1000, 'unixepoch')) AS INTEGER) as mo,
          SUM(ZMONEY) as tot
        FROM INOUTCOME
        WHERE DO_TYPE = ${doType} AND WDATE IS NOT NULL AND CAST(WDATE AS REAL) > 0
        GROUP BY yr, mo
        ORDER BY yr, mo
      `);
    }

    if (!rows.length) { heatmapData.value = []; return; }

    // Raggruppa per anno
    const byYear = {};
    rows.forEach(([yr, mo, tot]) => {
      if (!byYear[yr]) byYear[yr] = Array(12).fill(0);
      byYear[yr][mo - 1] = Number(tot) || 0;
    });

    // Prendi l'anno corrente + i 6 precedenti (max 7 righe), solo anni <= nowY
    const nowY = new Date().getFullYear();
    // Tutti gli anni disponibili <= anno corrente (per il selettore)
    const availableYears = Object.keys(byYear).map(Number)
      .filter(y => y <= nowY).sort((a,b) => a-b);
    heatmapYearList.value = availableYears;
    // Se heatmapFromYear non è ancora impostato, usa il primo anno disponibile
    if (heatmapFromYear.value === null && availableYears.length)
      heatmapFromYear.value = availableYears[0];

    // Filtra per anno minimo selezionato, poi prendi max 7 anni recenti
    const allYears = availableYears
      .filter(y => !heatmapFromYear.value || y >= heatmapFromYear.value)
      .slice(-7);

    const nowM = new Date().getMonth(); // 0-based
    const tableRows = allYears.map(yr => {
      const months = byYear[yr].map((v, mi) => {
        // Azzera mesi futuri: per l'anno corrente, oltre il mese attuale
        if (yr === nowY && mi > nowM) return 0;
        // Per anni futuri (non dovrebbe succedere) azzera tutto
        if (yr > nowY) return 0;
        return v;
      });
      const total = months.reduce((s,v) => s + v, 0);
      return { year: yr, months, total };
    });

    // Calcola max per colore
    const allVals = tableRows.flatMap(r => r.months).filter(v => v > 0);
    const yearTots = tableRows.map(r => r.total);
    heatmapMax.value     = allVals.length  ? Math.max(...allVals) : 1;
    heatmapYearMax.value = yearTots.length ? Math.max(...yearTots) : 1;

    // Media per colonna (mese)
    const monthAvg = Array(12).fill(0);
    allYears.forEach(yr => {
      byYear[yr].forEach((v, mi) => { monthAvg[mi] += v; });
    });
    heatmapMonthAvg.value = monthAvg.map(v => Math.round(v / allYears.length));
    heatmapGrandAvg.value = Math.round(heatmapMonthAvg.value.reduce((s,v) => s+v, 0));

    // Calcola KPI sui dati filtrati (tableRows, rispetta fromYear)
    const fmtMoYr = (yr, mo) => `${heatmapMonths[mo-1]} ${yr}`;
    const filteredVals = tableRows.flatMap(r =>
      r.months.map((v, mi) => ({ val: v, yr: r.year, mo: mi + 1 }))
    ).filter(({ val, yr, mo }) => {
      if (!val || val <= 0) return false;
      if (yr === nowY && (mo - 1) > nowM) return false; // escludi futuri
      return true;
    });
    const minVal  = filteredVals.length ? Math.min(...filteredVals.map(x => x.val)) : 0;
    const maxVal  = filteredVals.length ? Math.max(...filteredVals.map(x => x.val)) : 0;
    const minEntry = filteredVals.find(x => x.val === minVal);
    const maxEntry = filteredVals.find(x => x.val === maxVal);
    const grandTotal = filteredVals.reduce((s, x) => s + x.val, 0);
    const avgMonth   = filteredVals.length ? Math.round(grandTotal / filteredVals.length) : 0;
    const avgYear    = allYears.length ? Math.round(grandTotal / allYears.length) : 0;
    heatmapKpi.value = {
      min: minVal, minLabel: minEntry ? fmtMoYr(minEntry.yr, minEntry.mo) : '—',
      max: maxVal, maxLabel: maxEntry ? fmtMoYr(maxEntry.yr, maxEntry.mo) : '—',
      avg: avgMonth, avgYear
    };

    heatmapData.value = tableRows;
  } catch(e) { console.error('loadHeatmap', e); heatmapData.value = []; }
};

// ── CONFRONTO PERIODO ──
const confrontoMode  = ref('prev');    // 'prev' | 'year'
const confrontoPrevLabel = ref('');
const confrontoCurLabel  = ref('');
const confrontoData  = ref(null);
const confrontoOptions = ref({});
const confrontoDelta = ref(null);

const loadConfronto = () => {
  if (!dbInstance) return;
  try {
    const { startMs, endMs } = getPeriodRange();
    // Calcola il range del periodo precedente
    const spanMs = endMs - startMs;
    let prevStart, prevEnd;

    if (confrontoMode.value === 'year') {
      // Anno precedente: stesso range calendario, -1 anno
      const sDate = new Date(startMs), eDate = new Date(endMs);
      sDate.setFullYear(sDate.getFullYear() - 1);
      eDate.setFullYear(eDate.getFullYear() - 1);
      prevStart = sDate.getTime();
      prevEnd   = eDate.getTime();

    } else if (selectedPeriod.value === 'current_month') {
      // Mese calendario precedente completo
      const s = new Date(startMs);
      const prevMonthStart = new Date(s.getFullYear(), s.getMonth() - 1, 1);
      const prevMonthEnd   = new Date(s.getFullYear(), s.getMonth(), 0, 23, 59, 59, 999);
      prevStart = prevMonthStart.getTime();
      prevEnd   = prevMonthEnd.getTime();

    } else if (selectedPeriod.value === 'last_month') {
      // Due mesi fa (mese calendario completo)
      const s = new Date(startMs);
      const prevMonthStart = new Date(s.getFullYear(), s.getMonth() - 1, 1);
      const prevMonthEnd   = new Date(s.getFullYear(), s.getMonth(), 0, 23, 59, 59, 999);
      prevStart = prevMonthStart.getTime();
      prevEnd   = prevMonthEnd.getTime();

    } else if (selectedPeriod.value === 'ytd') {
      // YTD anno scorso: 1 gen anno prec → stesso giorno anno prec
      const s = new Date(startMs), e = new Date(endMs);
      s.setFullYear(s.getFullYear() - 1);
      e.setFullYear(e.getFullYear() - 1);
      prevStart = s.getTime();
      prevEnd   = e.getTime();

    } else {
      // custom / all: shift della stessa durata esatta
      prevStart = startMs - spanMs;
      prevEnd   = startMs - 1;
    }

    const run = (q) => { const r = dbInstance.exec(q); return r.length && r[0].values[0] ? Number(r[0].values[0][0]) : 0; };

    // Calcola label leggibili per i periodi
    const fmtDate = (ms) => {
      const d = new Date(ms);
      return d.toLocaleDateString('it-IT', { day: '2-digit', month: 'short', year: 'numeric' });
    };
    const fmtMonth = (ms) => new Date(ms).toLocaleDateString('it-IT', { month: 'long', year: 'numeric' });
    if (selectedPeriod.value === 'current_month' || selectedPeriod.value === 'last_month') {
      confrontoCurLabel.value  = fmtMonth(startMs);
      confrontoPrevLabel.value = fmtMonth(prevStart);
    } else if (selectedPeriod.value === 'ytd') {
      const y = new Date(startMs).getFullYear();
      confrontoCurLabel.value  = `Gen–oggi ${y}`;
      confrontoPrevLabel.value = `Gen–oggi ${y - 1}`;
    } else {
      confrontoCurLabel.value  = `${fmtDate(startMs)} – ${fmtDate(endMs)}`;
      confrontoPrevLabel.value = `${fmtDate(prevStart)} – ${fmtDate(prevEnd)}`;
    }

    const curInc = run(`SELECT SUM(ZMONEY) FROM INOUTCOME WHERE DO_TYPE=0 AND CAST(ZDATE AS REAL)>=${startMs} AND CAST(ZDATE AS REAL)<=${endMs}`);
    const curExp = run(`SELECT SUM(ZMONEY) FROM INOUTCOME WHERE DO_TYPE=1 AND CAST(ZDATE AS REAL)>=${startMs} AND CAST(ZDATE AS REAL)<=${endMs}`);
    const prevInc = run(`SELECT SUM(ZMONEY) FROM INOUTCOME WHERE DO_TYPE=0 AND CAST(ZDATE AS REAL)>=${prevStart} AND CAST(ZDATE AS REAL)<=${prevEnd}`);
    const prevExp = run(`SELECT SUM(ZMONEY) FROM INOUTCOME WHERE DO_TYPE=1 AND CAST(ZDATE AS REAL)>=${prevStart} AND CAST(ZDATE AS REAL)<=${prevEnd}`);

    const curNet  = curInc  - curExp;
    const prevNet = prevInc - prevExp;
    const isDark  = theme.value === 'dark';
    const periodLabel = confrontoMode.value === 'year' ? 'Anno prec.' : 'Periodo prec.';

    confrontoData.value = {
      labels: ['Entrate', 'Uscite', 'Netto'],
      datasets: [
        {
          label: confrontoPrevLabel.value || periodLabel,
          data: [prevInc, prevExp, prevNet],
          backgroundColor: isDark ? 'rgba(100,116,139,0.45)' : 'rgba(148,163,184,0.40)',
          borderColor:     isDark ? '#475569' : '#94a3b8',
          borderWidth: 1.5, borderRadius: 4, borderSkipped: false
        },
        {
          label: confrontoCurLabel.value || 'Periodo attuale',
          data: [curInc, curExp, curNet],
          backgroundColor: [
            isDark ? 'rgba(16,185,129,0.65)' : 'rgba(16,185,129,0.55)',
            isDark ? 'rgba(239,68,68,0.65)'  : 'rgba(239,68,68,0.55)',
            curNet >= 0
              ? (isDark ? 'rgba(59,130,246,0.65)'  : 'rgba(59,130,246,0.55)')
              : (isDark ? 'rgba(251,146,60,0.65)'  : 'rgba(251,146,60,0.55)')
          ],
          borderColor: [
            '#059669', '#dc2626', curNet >= 0 ? '#2563eb' : '#ea580c'
          ],
          borderWidth: 1.5, borderRadius: 4, borderSkipped: false,
          // Fix legenda: usa il colore della prima barra (entrate=verde) come colore del punto legenda
          pointBackgroundColor: isDark ? 'rgba(16,185,129,0.65)' : 'rgba(16,185,129,0.55)',
        }
      ]
    };

    const pct = (cur, prev) => prev !== 0 ? ((cur - prev) / Math.abs(prev)) * 100 : 0;
    confrontoDelta.value = {
      incDelta: pct(curInc, prevInc),
      expDelta: pct(curExp, prevExp),
      netDelta: pct(curNet, prevNet)
    };

    const tooltip = {
      backgroundColor: isDark ? 'rgba(28,27,25,0.95)' : 'rgba(15,23,42,0.95)',
      titleColor: isDark ? '#94a3b8' : '#cbd5e1', bodyColor: '#f1f5f9',
      padding: 10, cornerRadius: 8,
      borderColor: isDark ? 'rgba(255,255,255,0.08)' : 'rgba(0,0,0,0.08)', borderWidth: 1,
      callbacks: { label: ctx => `${ctx.dataset.label}: € ${Math.round(ctx.raw).toLocaleString('it-IT')}` }
    };

    confrontoOptions.value = {
      responsive: true, maintainAspectRatio: false,
      plugins: {
        legend: {
          display: true, position: 'top', align: 'end',
          labels: {
            boxWidth: 10, boxHeight: 10, borderRadius: 3,
            font: { size: 11, weight: '600' },
            color: isDark ? '#94a3b8' : '#64748b',
            usePointStyle: true,
            generateLabels: (chart) => {
              const labels = chart.data.datasets.map((ds, i) => ({
                text: ds.label,
                fillStyle: i === 0
                  ? (isDark ? 'rgba(100,116,139,0.45)' : 'rgba(148,163,184,0.40)')
                  : (isDark ? 'rgba(16,185,129,0.65)' : 'rgba(16,185,129,0.55)'),
                strokeStyle: i === 0
                  ? (isDark ? '#475569' : '#94a3b8')
                  : '#059669',
                lineWidth: 1.5,
                pointStyle: 'rectRounded',
                datasetIndex: i,
                hidden: !chart.isDatasetVisible(i),
              }));
              return labels;
            }
          }
        },
        tooltip
      },
      scales: {
        x: { grid: { display: false }, border: { display: false }, ticks: { font: { size: 12, weight: '600' }, color: isDark ? '#94a3b8' : '#475569' } },
        y: { beginAtZero: true, border: { display: false }, grid: { color: isDark ? 'rgba(255,255,255,0.04)' : 'rgba(0,0,0,0.04)' },
             ticks: { font: { size: 10 }, color: isDark ? '#64748b' : '#94a3b8', callback: v => v >= 1000 ? `€${(v/1000).toFixed(0)}k` : `€${v}` } }
      }
    };
  } catch(e) { console.error('loadConfronto', e); confrontoData.value = null; }
};

const loadTopCat = () => {
  if (!dbInstance) return;
  try {
    const { startMs, endMs } = getPeriodRange();
    const safeExec = (q) => { try { const r = dbInstance.exec(q); return (r.length && r[0].values) ? r[0].values : []; } catch(e) { return []; } };

    // Top Categorie: ctguid punta alla figlia (s), si risale al padre (c) via s.puid
    let rows = safeExec(`
      SELECT s.name as cat, SUM(i.ZMONEY) as tot
      FROM INOUTCOME i
      LEFT JOIN ZCATEGORY s ON i.ctguid = s.uid
      LEFT JOIN ZCATEGORY c ON c.uid = s.puid
      WHERE i.DO_TYPE = 1
        AND CAST(i.ZDATE AS REAL) >= ${startMs} AND CAST(i.ZDATE AS REAL) <= ${endMs}
        AND s.name IS NOT NULL AND s.name != ''
      GROUP BY s.uid
      ORDER BY tot DESC LIMIT 10
    `);
    // Fallback WDATE
    if (!rows.length) rows = safeExec(`
      SELECT s.name as cat, SUM(i.ZMONEY) as tot
      FROM INOUTCOME i
      LEFT JOIN ZCATEGORY s ON i.ctguid = s.uid
      LEFT JOIN ZCATEGORY c ON c.uid = s.puid
      WHERE i.DO_TYPE = 1
        AND CAST(i.WDATE AS REAL) >= ${startMs} AND CAST(i.WDATE AS REAL) <= ${endMs}
        AND s.name IS NOT NULL AND s.name != ''
      GROUP BY s.uid
      ORDER BY tot DESC LIMIT 10
    `);
    // Fallback: tutte le ZCATEGORY via ctguid senza gerarchia
    if (!rows.length) rows = safeExec(`
      SELECT s.name as cat, SUM(i.ZMONEY) as tot
      FROM INOUTCOME i
      LEFT JOIN ZCATEGORY s ON i.ctguid = s.uid
      WHERE i.DO_TYPE = 1
        AND CAST(i.ZDATE AS REAL) >= ${startMs} AND CAST(i.ZDATE AS REAL) <= ${endMs}
        AND s.name IS NOT NULL AND s.name != ''
      GROUP BY s.uid
      ORDER BY tot DESC LIMIT 10
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

    statusMessage.value = `✅ File caricato: ${file.name}`;
    isError.value = false;
  } catch (err) {
    isError.value = true;
    statusMessage.value = 'Errore: ' + err.message;
  }
};

// ── REFRESH DATI ──
const getPeriodRange = () => {
  const now = new Date();
  const y = now.getFullYear(), m = now.getMonth();
  let startMs = 0, endMs = Date.now();
  if (selectedPeriod.value === 'current_month') {
    startMs = new Date(y, m, 1).getTime();
  } else if (selectedPeriod.value === 'last_month') {
    startMs = new Date(y, m - 1, 1).getTime();
    endMs   = new Date(y, m, 0, 23, 59, 59, 999).getTime();
  } else if (selectedPeriod.value === 'ytd') {
    startMs = new Date(y, 0, 1).getTime();
  } else if (selectedPeriod.value === 'custom') {
    if (customStart.value) startMs = new Date(customStart.value + 'T00:00:00').getTime();
    if (customEnd.value)   endMs   = new Date(customEnd.value   + 'T23:59:59').getTime();
  }
  return { startMs, endMs };
};

const refreshData = () => {
  if (!dbInstance) return;
  try {
    animating.value = true;
    setTimeout(() => { animating.value = false; }, 500);

    const { startMs, endMs } = getPeriodRange();

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
    loadConfronto();
    loadHeatmap();
    initAnomalieMonths();
    loadAnomalie();
    loadPrevisioni();
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

    // Netto cumulato
    let _cum = 0;
    const cumulative = nets.map(v => { _cum += v; return _cum; });

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
          label: 'Netto Cumulato',
          data: cumulative,
          borderColor: isDark ? 'rgba(148,163,184,0.75)' : 'rgba(100,116,139,0.70)',
          backgroundColor: 'transparent',
          borderWidth: 2,
          borderDash: [5, 3],
          pointRadius: 3,
          pointHoverRadius: 5,
          pointBackgroundColor: cumulative.map(v =>
            v >= 0
              ? (isDark ? 'rgba(16,185,129,0.85)' : 'rgba(5,150,105,0.85)')
              : (isDark ? 'rgba(239,68,68,0.85)'  : 'rgba(220,38,38,0.85)')
          ),
          pointBorderWidth: 0,
          tension: 0.32,
          yAxisID: 'yCum',
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
            generateLabels: (chart) => {
              return chart.data.datasets.map((ds, i) => ({
                text: ds.label,
                fillStyle: ds.type === 'line' ? 'transparent' : (Array.isArray(ds.backgroundColor) ? ds.backgroundColor[0] : ds.backgroundColor),
                strokeStyle: ds.borderColor,
                lineDash: ds.type === 'line' ? [5, 3] : [],
                lineWidth: ds.borderWidth,
                hidden: !chart.isDatasetVisible(i),
                datasetIndex: i,
                pointStyle: ds.type === 'line' ? 'line' : 'rectRounded'
              }));
            }
          }
        },
        tooltip: {
          ...baseTooltip(isDark),
          callbacks: {
            label: (ctx) => {
              const v = Number(ctx.raw) || 0;
              if (ctx.dataset.label === 'Netto Cumulato')
                return ` Netto cumulato: ${v >= 0 ? '+' : ''}€ ${Math.round(v).toLocaleString('it-IT')}`;
              return ` ${ctx.dataset.label}: € ${Math.round(v).toLocaleString('it-IT')}`;
            }
          }
        }
      },
      scales: {
        x: {
          grid: { display: false },
          border: { display: false },
          ticks: {
            font: { size: 10, weight: '600', family: 'Inter, sans-serif' },
            color: isDark ? '#64748b' : '#94a3b8',
            maxRotation: 0
          }
        },
        y: {
          position: 'left',
          beginAtZero: true,
          grace: '10%',
          border: { display: false },
          grid: { color: isDark ? 'rgba(255,255,255,0.04)' : 'rgba(0,0,0,0.04)' },
          ticks: {
            font: { size: 10, family: 'Inter, sans-serif' },
            color: isDark ? '#64748b' : '#94a3b8',
            callback: (v) => `€ ${v >= 1000 ? (v/1000).toFixed(0)+'k' : v}`
          },
          title: {
            display: true,
            text: 'Mensile',
            color: isDark ? '#475569' : '#94a3b8',
            font: { size: 9, weight: '600', family: 'Inter, sans-serif' }
          }
        },
        yCum: {
          position: 'right',
          grace: '10%',
          border: { display: false },
          grid: { display: false },
          ticks: {
            font: { size: 10, family: 'Inter, sans-serif' },
            color: isDark ? '#64748b' : '#94a3b8',
            callback: (v) => `€ ${v >= 1000 ? (v/1000).toFixed(1)+'k' : v < -1000 ? (v/1000).toFixed(1)+'k' : v}`
          },
          title: {
            display: true,
            text: 'Cumulato',
            color: isDark ? '#475569' : '#94a3b8',
            font: { size: 9, weight: '600', family: 'Inter, sans-serif' }
          }
        }
      }
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
const storicoSummary = ref({ totalNet: 0, maxCumulative: 0, months: 0, avgMonthly: 0, deltaVsTarget: 0, isAbove: true });

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
      WHERE CAST(ZDATE AS REAL) <= ${Date.now()}
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

    // Linea obiettivo cumulativa: media entrate storiche × targetSavingsPct% per ogni mese
    const avgInc = rows.reduce((s, [,, inc]) => s + (inc || 0), 0) / rows.length;
    const targetPerMonth = avgInc * (targetSavingsPct.value / 100);
    let cumTarget = 0;
    const targetCumulative = rows.map(() => { cumTarget += targetPerMonth; return Math.round(cumTarget); });

    // Colore area: verde se cumulativo >= obiettivo, rosso altrimenti
    const lastReal = cumulative[cumulative.length - 1] || 0;
    const lastTarget = targetCumulative[targetCumulative.length - 1] || 0;
    const isAbove = lastReal >= lastTarget;
    const areaColor = isAbove
      ? (isDark ? 'rgba(16,185,129,0.15)' : 'rgba(16,185,129,0.12)')
      : (isDark ? 'rgba(239,68,68,0.15)'  : 'rgba(239,68,68,0.10)');
    const lineColor = isAbove ? '#10b981' : '#ef4444';

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
          yAxisID: 'yMonthly',
          order: 3
        },
        {
          label: 'Obiettivo',
          data: targetCumulative,
          borderColor: isDark ? 'rgba(251,191,36,0.7)' : 'rgba(217,119,6,0.6)',
          backgroundColor: 'transparent',
          borderWidth: 2,
          borderDash: [5, 4],
          pointRadius: 0, pointHoverRadius: 4,
          tension: 0.3, fill: false,
          yAxisID: 'yCumulative',
          order: 2
        },
        {
          label: 'Cumulativo',
          data: cumulative,
          borderColor: lineColor,
          backgroundColor: areaColor,
          borderWidth: 2.5,
          pointRadius: 3, pointHoverRadius: 6,
          pointBackgroundColor: lineColor,
          pointBorderColor: isDark ? '#1e293b' : '#fff',
          pointBorderWidth: 1.5,
          tension: 0.4,
          fill: { target: 1, above: areaColor, below: isDark ? 'rgba(239,68,68,0.15)' : 'rgba(239,68,68,0.10)' },
          yAxisID: 'yCumulative',
          order: 1
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
    const deltaVsTarget = totalNet - (targetCumulative[targetCumulative.length - 1] || 0);
    storicoSummary.value = {
      totalNet, maxCumulative,
      months: rows.length,
      avgMonthly: validMonthly.length ? validMonthly.reduce((a,b) => a+b,0) / validMonthly.length : 0,
      deltaVsTarget,
      isAbove
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

    // Prova 1: ctguid → sottocategoria figlia (s), risale al padre (c) — ZDATE
    let expRows = safeExec(`
      SELECT s.name as cat, SUM(i.ZMONEY) as tot
      FROM INOUTCOME i
      LEFT JOIN ZCATEGORY s ON i.ctguid = s.uid
      LEFT JOIN ZCATEGORY c ON c.uid = s.puid
      WHERE i.DO_TYPE = 1
        AND CAST(i.ZDATE AS REAL) >= ${start} AND CAST(i.ZDATE AS REAL) <= ${end}
        AND s.name IS NOT NULL AND s.name != ''
      GROUP BY s.uid ORDER BY tot DESC LIMIT 10
    `);

    // Prova 2: fallback WDATE
    if (!expRows.length) {
      expRows = safeExec(`
        SELECT s.name as cat, SUM(i.ZMONEY) as tot
        FROM INOUTCOME i
        LEFT JOIN ZCATEGORY s ON i.ctguid = s.uid
        LEFT JOIN ZCATEGORY c ON c.uid = s.puid
        WHERE i.DO_TYPE = 1
          AND CAST(i.WDATE AS REAL) >= ${start} AND CAST(i.WDATE AS REAL) <= ${end}
          AND s.name IS NOT NULL AND s.name != ''
        GROUP BY s.uid ORDER BY tot DESC LIMIT 10
      `);
    }

    // Prova 3: fallback ZCATEGORY senza gerarchia
    if (!expRows.length) {
      expRows = safeExec(`
        SELECT s.name as cat, SUM(i.ZMONEY) as tot
        FROM INOUTCOME i
        LEFT JOIN ZCATEGORY s ON i.ctguid = s.uid
        WHERE i.DO_TYPE = 1
          AND CAST(i.ZDATE AS REAL) >= ${start} AND CAST(i.ZDATE AS REAL) <= ${end}
          AND s.name IS NOT NULL AND s.name != ''
        GROUP BY s.uid ORDER BY tot DESC LIMIT 10
      `);
    }

    // Prova 4: fallback NIC_NAME
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
  if (tab === 'previsioni' && dbInstance) {
    loadPrevisioni();
  }
  if (tab === 'dettaglio' && dbInstance) {
    if (!dettaglioMonthOptions.value.length) buildDettaglioOptions();
    if (!dettaglioData.value) loadDettaglio();
  }
});
</script>

<style scoped>

/* ===== Header mobile rewrite + overflow hardening ===== */
html, body, #app {
  width: 100%;
  max-width: 100%;
  overflow-x: hidden;
}

*, *::before, *::after {
  box-sizing: border-box;
}

.mm-app,
.mm-header,
.header-inner,
.header-top,
.header-brand,
.brand-copy,
.header-actions,
.period-panel,
.period-panel-head,
.period-pill,
.period-pill-panel,
.period-select,
.custom-range-shell,
.custom-range,
.date-field,
.date-card,
.mm-main,
.dashboard-content,
.panel,
.chart-wrap,
.chart-wrap-tall,
.mid-grid,
.kpi-row,
.tabs-panel {
  min-width: 0;
  max-width: 100%;
}

.mm-app {
  width: 100%;
  overflow-x: clip;
}

.mm-header {
  width: 100%;
  overflow: hidden;
}

.header-inner {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  width: 100%;
}

.header-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  width: 100%;
  min-width: 0;
}

.header-brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  min-width: 0;
  flex: 1 1 auto;
}

.brand-copy {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.brand-name,
.brand-sub,
.user-name {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.header-actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 0.5rem;
  flex: 0 1 auto;
  min-width: 0;
  flex-wrap: nowrap;
}

.period-panel {
  display: flex;
  flex-direction: column;
  gap: 0.625rem;
  margin-bottom: var(--s3);
}

.hybrid-period-panel {
  padding: 0;
  border: none;
  background: transparent;
  box-shadow: none;
}

.hybrid-period-head {
  display: block;
}

.period-pill {
  width: 100%;
  min-width: 0;
}

.hybrid-period-pill {
  width: 100%;
  border-radius: var(--r-lg);
  overflow: hidden;
  background: var(--surface-2);
  border: 1px solid var(--border);
  box-shadow: var(--shadow-sm);
}

.period-select {
  width: 100%;
  min-width: 0;
}

.custom-range-shell {
  width: 100%;
  min-width: 0;
}

.hybrid-range-shell {
  width: 100%;
}

.hybrid-period-range {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
  gap: 0.625rem;
  width: 100%;
  min-width: 0;
  padding: 0;
  border: none;
  background: transparent;
  box-shadow: none;
}

.date-card {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  min-width: 0;
  padding: 0.625rem 0.75rem;
  border-radius: var(--r-lg);
  background: var(--surface-2);
  border: 1px solid var(--border);
  box-shadow: var(--shadow-sm);
}

.date-card-label {
  font-size: 0.68rem;
  font-weight: 800;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--text-muted);
}

.date-field {
  display: flex;
  align-items: center;
  gap: 0.55rem;
  min-width: 0;
}

.date-label {
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.02em;
  opacity: 0.72;
  flex: 0 0 auto;
}

.date-input {
  width: 100%;
  min-width: 0;
  max-width: 100%;
}

.date-input-wide {
  width: 100%;
  min-width: 0;
  display: block;
}

.date-sep {
  display: none;
}

.btn-update,
.theme-toggle,
.btn-logout,
.user-avatar {
  flex-shrink: 0;
}

@media (max-width: 720px) {
  .header-inner {
    padding-left: max(0.75rem, env(safe-area-inset-left));
    padding-right: max(0.75rem, env(safe-area-inset-right));
  }

  .btn-update-text,
  .user-name {
    display: none;
  }

  .btn-update {
    padding-inline: 0.7rem;
  }

  .user-chip {
    gap: 0.35rem;
    padding-inline: 0.35rem;
  }

  .hybrid-period-range {
    grid-template-columns: 1fr;
  }
}

@media (min-width: 721px) {
  .hybrid-period-range {
    grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
    align-items: stretch;
  }
}


*, *::before, *::after {
  box-sizing: border-box;
}

.mm-app,
.mm-header,
.header-inner,
.header-top,
.header-brand,
.brand-copy,
.header-actions,
.period-panel,
.period-panel-head,
.period-pill,
.period-pill-panel,
.period-select,
.custom-range-shell,
.custom-range,
.date-field,
.mm-main,
.dashboard-content,
.panel,
.chart-wrap,
.chart-wrap-tall,
.mid-grid,
.kpi-row,
.tabs-panel {
  min-width: 0;
  max-width: 100%;
}

.mm-app {
  width: 100%;
  overflow-x: clip;
}

.mm-header {
  width: 100%;
  overflow: hidden;
}

.header-inner {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  width: 100%;
}

.header-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  width: 100%;
  min-width: 0;
}

.header-brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  min-width: 0;
  flex: 1 1 auto;
}

.brand-copy {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.brand-name,
.brand-sub,
.user-name {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.header-actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 0.5rem;
  flex: 0 1 auto;
  min-width: 0;
  flex-wrap: nowrap;
}

.period-panel {
  display: flex;
  flex-direction: column;
  gap: 0.625rem;
  padding: 0.75rem;
  margin-bottom: var(--s3);
  background: linear-gradient(180deg, color-mix(in srgb, var(--surface) 84%, transparent), color-mix(in srgb, var(--surface-2) 92%, transparent));
  border: 1px solid color-mix(in srgb, var(--border) 88%, transparent);
}

.period-panel-head {
  display: grid;
  grid-template-columns: auto minmax(0, 1fr);
  align-items: center;
  gap: 0.75rem;
}

.period-panel-label {
  font-size: 0.7rem;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--text-muted);
  white-space: nowrap;
}

.period-pill {
  width: 100%;
  min-width: 0;
}

.period-pill-panel {
  width: 100%;
}

.period-select {
  width: 100%;
  min-width: 0;
}

.custom-range-shell {
  width: 100%;
  min-width: 0;
}

.compact-range {
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  gap: 0.5rem;
  width: 100%;
  min-width: 0;
  padding: 0.625rem 0.75rem;
  border-radius: 14px;
  background: color-mix(in srgb, var(--surface-2) 92%, transparent);
  border: 1px solid color-mix(in srgb, var(--border) 82%, transparent);
}

.period-panel-range {
  box-shadow: none;
}

.date-field {
  display: flex;
  align-items: center;
  gap: 0.55rem;
  min-width: 0;
}

.date-label {
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.02em;
  opacity: 0.72;
  flex: 0 0 auto;
}

.date-input {
  width: 100%;
  min-width: 0;
  max-width: 100%;
}

.date-sep {
  display: none;
}

.btn-update,
.theme-toggle,
.btn-logout,
.user-avatar {
  flex-shrink: 0;
}

@media (max-width: 720px) {
  .header-inner {
    padding-left: max(0.75rem, env(safe-area-inset-left));
    padding-right: max(0.75rem, env(safe-area-inset-right));
  }

  .btn-update-text,
  .user-name {
    display: none;
  }

  .btn-update {
    padding-inline: 0.7rem;
  }

  .user-chip {
    gap: 0.35rem;
    padding-inline: 0.35rem;
  }

  .period-panel-head {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }
}

@media (min-width: 721px) {
  .compact-range {
    grid-template-columns: minmax(0, 1fr) auto minmax(0, 1fr);
    align-items: center;
  }

  .date-field {
    min-width: 0;
  }

  .date-sep {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    opacity: 0.5;
    font-weight: 700;
    min-width: 1.25rem;
  }
}


*, *::before, *::after {
  box-sizing: border-box;
}

.mm-app,
.mm-header,
.header-inner,
.header-top,
.header-brand,
.brand-copy,
.header-actions,
.period-toolbar,
.period-toolbar-inner,
.period-pill,
.period-pill-standalone,
.period-select,
.custom-range-shell,
.custom-range,
.date-field,
.mm-main,
.dashboard-content,
.panel,
.chart-wrap,
.chart-wrap-tall,
.mid-grid,
.kpi-row,
.tabs-panel {
  min-width: 0;
  max-width: 100%;
}

.mm-app {
  width: 100%;
  overflow-x: clip;
}

.mm-header {
  width: 100%;
  overflow: hidden;
}

.header-inner {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  width: 100%;
}

.header-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  width: 100%;
  min-width: 0;
}

.header-brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  min-width: 0;
  flex: 1 1 auto;
}

.brand-copy {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.brand-name,
.brand-sub,
.user-name {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.header-actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 0.5rem;
  flex: 0 1 auto;
  min-width: 0;
  flex-wrap: nowrap;
}

.period-toolbar {
  padding: 0.625rem;
  margin-bottom: var(--s3);
  background: var(--surface);
  border: 1px solid var(--border);
}

.period-toolbar-inner {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  width: 100%;
}

.period-pill {
  width: 100%;
  min-width: 0;
}

.period-pill-standalone {
  width: 100%;
}

.period-select {
  width: 100%;
  min-width: 0;
}

.custom-range-shell {
  width: 100%;
  min-width: 0;
}

.compact-range {
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  gap: 0.5rem;
  width: 100%;
  min-width: 0;
  padding: 0.5rem 0.625rem;
  border-radius: 14px;
  background: var(--surface-2, rgba(148,163,184,0.08));
  border: 1px solid var(--border-color, rgba(148,163,184,0.18));
}

.toolbar-custom-range {
  box-shadow: none;
}

.date-field {
  display: flex;
  align-items: center;
  gap: 0.55rem;
  min-width: 0;
}

.date-label {
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.02em;
  opacity: 0.72;
  flex: 0 0 auto;
}

.date-input {
  width: 100%;
  min-width: 0;
  max-width: 100%;
}

.date-sep {
  display: none;
}

.btn-update,
.theme-toggle,
.btn-logout,
.user-avatar {
  flex-shrink: 0;
}

@media (max-width: 720px) {
  .header-inner {
    padding-left: max(0.75rem, env(safe-area-inset-left));
    padding-right: max(0.75rem, env(safe-area-inset-right));
  }

  .btn-update-text,
  .user-name {
    display: none;
  }

  .btn-update {
    padding-inline: 0.7rem;
  }

  .user-chip {
    gap: 0.35rem;
    padding-inline: 0.35rem;
  }
}

@media (min-width: 721px) {
  .compact-range {
    grid-template-columns: minmax(0, 1fr) auto minmax(0, 1fr);
    align-items: center;
  }

  .date-field {
    min-width: 0;
  }

  .date-sep {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    opacity: 0.5;
    font-weight: 700;
    min-width: 1.25rem;
  }
}


*, *::before, *::after {
  box-sizing: border-box;
}

.mm-app,
.mm-header,
.header-inner,
.header-top,
.header-brand,
.brand-copy,
.header-actions,
.header-filters,
.period-pill,
.period-select,
.custom-range-shell,
.custom-range,
.date-field,
.mm-main,
.dashboard-content,
.panel,
.chart-wrap,
.chart-wrap-tall,
.mid-grid,
.kpi-row,
.tabs-panel {
  min-width: 0;
  max-width: 100%;
}

.mm-app {
  width: 100%;
  overflow-x: clip;
}

.mm-header {
  width: 100%;
  overflow: hidden;
}

.header-inner {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  width: 100%;
}

.header-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  width: 100%;
  min-width: 0;
}

.header-brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  min-width: 0;
  flex: 1 1 auto;
}

.brand-copy {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.brand-name,
.brand-sub,
.user-name {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.header-actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 0.5rem;
  flex: 0 1 auto;
  min-width: 0;
  flex-wrap: nowrap;
}

.header-filters {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  width: 100%;
  min-width: 0;
}

.period-pill {
  width: 100%;
  min-width: 0;
}

.period-select {
  width: 100%;
  min-width: 0;
}

.custom-range-shell {
  width: 100%;
  min-width: 0;
}

.compact-range {
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  gap: 0.5rem;
  width: 100%;
  min-width: 0;
  padding: 0.5rem 0.625rem;
  border-radius: 14px;
  background: var(--surface-2, rgba(148,163,184,0.08));
  border: 1px solid var(--border-color, rgba(148,163,184,0.18));
}

.date-field {
  display: flex;
  align-items: center;
  gap: 0.55rem;
  min-width: 0;
}

.date-label {
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.02em;
  opacity: 0.72;
  flex: 0 0 auto;
}

.date-input {
  width: 100%;
  min-width: 0;
  max-width: 100%;
}

.date-sep {
  display: none;
}

.btn-update,
.theme-toggle,
.btn-logout,
.user-avatar {
  flex-shrink: 0;
}

@media (max-width: 720px) {
  .header-inner {
    padding-left: max(0.75rem, env(safe-area-inset-left));
    padding-right: max(0.75rem, env(safe-area-inset-right));
  }

  .btn-update-text,
  .user-name {
    display: none;
  }

  .btn-update {
    padding-inline: 0.7rem;
  }

  .user-chip {
    gap: 0.35rem;
    padding-inline: 0.35rem;
  }
}

@media (min-width: 721px) {
  .compact-range {
    grid-template-columns: minmax(0, 1fr) auto minmax(0, 1fr);
    align-items: center;
  }

  .date-field {
    min-width: 0;
  }

  .date-sep {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    opacity: 0.5;
    font-weight: 700;
    min-width: 1.25rem;
  }
}


*, *::before, *::after {
  box-sizing: border-box;
}

.mm-app,
.mm-header,
.header-inner,
.header-top,
.header-brand,
.brand-copy,
.header-actions,
.header-filters,
.period-pill,
.period-select,
.custom-range-card,
.custom-range,
.mm-main,
.dashboard-content,
.panel,
.chart-wrap,
.chart-wrap-tall,
.mid-grid,
.kpi-row,
.tabs-panel {
  min-width: 0;
  max-width: 100%;
}

.mm-app {
  width: 100%;
  overflow-x: clip;
}

.mm-header {
  width: 100%;
  overflow: hidden;
}

.header-inner {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  width: 100%;
}

.header-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  width: 100%;
  min-width: 0;
}

.header-brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  min-width: 0;
  flex: 1 1 auto;
}

.brand-copy {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.brand-name,
.brand-sub,
.user-name,
.custom-range-summary {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.header-actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 0.5rem;
  flex: 0 1 auto;
  min-width: 0;
  flex-wrap: nowrap;
}

.header-filters {
  display: flex;
  flex-direction: column;
  gap: 0.625rem;
  width: 100%;
  min-width: 0;
}

.period-pill {
  width: 100%;
  min-width: 0;
}

.period-select {
  width: 100%;
  min-width: 0;
}

.custom-range-card {
  width: 100%;
  min-width: 0;
  border: 1px solid color-mix(in srgb, var(--border-color, rgba(148,163,184,0.18)) 100%, transparent);
  background: color-mix(in srgb, var(--card-bg, rgba(255,255,255,0.82)) 88%, transparent);
  border-radius: 14px;
  padding: 0.75rem;
}

.custom-range-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  margin-bottom: 0.625rem;
}

.custom-range-title {
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.02em;
  opacity: 0.82;
}

.custom-range-summary {
  font-size: 0.78rem;
  opacity: 0.72;
  max-width: 60%;
  text-align: right;
}

.custom-summary-sep {
  margin: 0 0.25rem;
  opacity: 0.6;
}

.custom-range {
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  gap: 0.625rem;
  width: 100%;
  min-width: 0;
}

.date-input {
  width: 100%;
  min-width: 0;
  max-width: 100%;
}

.date-sep {
  display: none;
}

.btn-update,
.theme-toggle,
.btn-logout,
.user-avatar {
  flex-shrink: 0;
}

@media (max-width: 720px) {
  .header-inner {
    padding-left: max(0.75rem, env(safe-area-inset-left));
    padding-right: max(0.75rem, env(safe-area-inset-right));
  }

  .btn-update-text,
  .user-name {
    display: none;
  }

  .btn-update {
    padding-inline: 0.7rem;
  }

  .user-chip {
    gap: 0.35rem;
    padding-inline: 0.35rem;
  }

  .custom-range-head {
    flex-direction: column;
    align-items: flex-start;
  }

  .custom-range-summary {
    max-width: 100%;
    text-align: left;
  }
}

@media (min-width: 721px) {
  .custom-range {
    grid-template-columns: minmax(0, 1fr) auto minmax(0, 1fr);
    align-items: center;
  }

  .date-sep {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    opacity: 0.55;
    font-weight: 700;
    min-width: 1.5rem;
  }
}

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
/* ── LOGIN CARD ── */
.login-card {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: var(--r-xl); padding: var(--s8);
  max-width: 400px; width: 100%; box-shadow: var(--sh-md);
}
.login-header {
  display: flex; flex-direction: column; align-items: center;
  gap: var(--s2); margin-bottom: var(--s5); text-align: center;
}
.login-title  { font-size: 20px; font-weight: 700; color: var(--text); margin: 0; letter-spacing: -0.02em; }
.login-subtitle { font-size: 13px; color: var(--text-muted); margin: 0; }
.login-status {
  display: flex; align-items: center; gap: 6px;
  font-size: 12px; color: var(--text-muted);
  background: var(--surface-2); border: 1px solid var(--border);
  border-radius: var(--r-sm); padding: 8px 12px;
  margin-bottom: var(--s4); line-height: 1.4;
}
.login-section { padding: var(--s3) 0; }
.login-section-label {
  display: flex; align-items: center; gap: 6px;
  font-size: 13px; font-weight: 600; color: var(--text); margin-bottom: var(--s2);
}
.login-section-desc {
  font-size: 12px; color: var(--text-muted);
  margin: 0 0 var(--s3); line-height: 1.5;
}
.login-section-desc code {
  background: var(--surface-2); padding: 1px 5px;
  border-radius: 3px; font-size: 11px; font-family: monospace; color: #3b82f6;
}
.gsi-btn-wrap { display: flex; justify-content: flex-start; min-height: 44px; margin-top: var(--s2); }
.login-btn {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 9px 16px; border-radius: var(--r-md);
  font-size: 13px; font-weight: 600; cursor: pointer;
  transition: opacity 0.15s, background 0.15s; border: none; text-decoration: none;
}
.login-btn:disabled { opacity: 0.55; cursor: not-allowed; }
.login-btn-google {
  background: var(--text); color: var(--bg);
  width: 100%; justify-content: center;
}
.login-btn-google:hover:not(:disabled) { opacity: 0.85; }
.login-btn-drive {
  background: var(--surface-2); color: var(--text);
  border: 1px solid var(--border); width: 100%; justify-content: center;
}
.login-btn-drive:hover:not(:disabled) { background: var(--primary-hl); }
.login-btn-file {
  background: var(--surface-2); color: var(--text);
  border: 1px solid var(--border);
}
.login-btn-file:hover { background: var(--primary-hl); }
.login-divider {
  display: flex; align-items: center; gap: var(--s3);
  color: var(--text-faint); font-size: 11px; font-weight: 600;
  text-transform: uppercase; letter-spacing: 0.06em; padding: var(--s2) 0;
}
.login-divider::before, .login-divider::after {
  content: ''; flex: 1; height: 1px; background: var(--border);
}
@keyframes spin { to { transform: rotate(360deg); } }

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
  align-items: stretch;
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
.budget-sliders { display: flex; flex-direction: column; gap: var(--s5); }
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
  height: 16px;
  background: rgba(255,255,255,0.35);
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
  border-radius: 8px;
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
  height: 100%; border-radius: 8px;
  transition: width 0.4s cubic-bezier(0.16,1,0.3,1);
  box-shadow: 0 1px 4px rgba(0,0,0,0.15);
}
.bar-ok     { background: linear-gradient(90deg, #059669, #10b981); }
.bar-warn   { background: linear-gradient(90deg, #d97706, #f59e0b); }
.bar-danger { background: linear-gradient(90deg, #dc2626, #ef4444); }


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
.topcat-wrap { height: 100% !important; min-height: 260px; }
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
.cashflow-panel { display: flex; flex-direction: column; }
.cashflow-panel :deep(.p-tabs) { display: flex; flex-direction: column; flex: 1; min-height: 0; }
.cashflow-panel :deep(.p-tabpanels) { flex: 1; min-height: 0; padding: 0 !important; }
.cashflow-panel :deep(.p-tabpanel) { height: 100%; padding: 0 !important; }
.cashflow-panel .chart-wrap { height: 100%; min-height: 260px; padding: var(--s3) var(--s4) var(--s4); position: relative; }
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



/* ── Savings tip inline (dentro budget-savings-row) ────────────────────────── */
.budget-savings-row {
  display: flex;
  align-items: stretch;
  gap: var(--s3);
  background: var(--surface-2);
  border-radius: var(--r-md);
  padding: var(--s3);
  border: 1px solid var(--border);
}
.savings-left {
  display: flex; flex-direction: column; gap: 2px;
  min-width: 90px; flex-shrink: 0;
}
.savings-tip-inline {
  flex: 1;
  display: flex; flex-direction: column; justify-content: center; gap: 3px;
  padding: var(--s2) var(--s3);
  border-radius: var(--r-sm);
  border-left: 2px solid;
}
.sti-ok   { background: rgba(16,185,129,0.08); border-color: #059669; }
.sti-warn { background: rgba(239,68,68,0.08);  border-color: #dc2626; }
.mm-app[data-theme="dark"] .sti-ok   { background: rgba(16,185,129,0.12); }
.mm-app[data-theme="dark"] .sti-warn { background: rgba(239,68,68,0.12); }
.sti-delta {
  font-size: 13px; font-weight: 800; line-height: 1.2;
  letter-spacing: -0.02em;
}
.sti-ok   .sti-delta { color: #059669; }
.sti-warn .sti-delta { color: #dc2626; }
.sti-msg {
  font-size: 11px; color: var(--text-muted); line-height: 1.4;
}


/* ── Burn Rate / Ritmo di Spesa ─────────────────────────────────────────────── */
.burnrate-wrap {
  display: flex; flex-direction: column; align-items: center;
  padding: var(--s3) var(--s2) var(--s2);
  height: 100%; justify-content: center; gap: var(--s3);
}
.gauge-container {
  display: flex; flex-direction: column; align-items: center; gap: var(--s1);
  width: 100%; max-width: 220px;
}
.gauge-svg { width: 100%; max-width: 200px; overflow: visible; }
.gauge-arc { transition: stroke-dasharray 0.6s cubic-bezier(0.16,1,0.3,1), stroke 0.4s; }
.gauge-main-label {
  font-size: 22px; font-weight: 800;
  font-family: var(--font);
  letter-spacing: -0.03em;
}
.gauge-sub-label {
  font-size: 9px; font-weight: 500;
  font-family: var(--font);
  letter-spacing: 0.05em; text-transform: uppercase;
}
:root { --br-track: rgba(0,0,0,0.08); --br-sub: #94a3b8; }
.mm-app[data-theme="dark"] { --br-track: rgba(255,255,255,0.08); --br-sub: #64748b; }

.gauge-verdict {
  font-size: 12px; font-weight: 700;
  padding: 3px 10px; border-radius: var(--r-full);
  letter-spacing: 0.02em;
}
.verdict-ok   { background: rgba(16,185,129,0.12); color: #059669; }
.verdict-warn { background: rgba(245,158,11,0.12); color: #d97706; }
.verdict-bad  { background: rgba(239,68,68,0.12);  color: #dc2626; }
.mm-app[data-theme="dark"] .verdict-ok   { color: #10b981; }
.mm-app[data-theme="dark"] .verdict-warn { color: #f59e0b; }
.mm-app[data-theme="dark"] .verdict-bad  { color: #ef4444; }

.burnrate-stats {
  display: grid; grid-template-columns: 1fr 1fr;
  gap: var(--s1) var(--s4); width: 100%; max-width: 220px;
}
.br-stat { display: flex; flex-direction: column; gap: 1px; }
.br-stat-label { font-size: 10px; color: var(--text-muted); font-weight: 500; text-transform: uppercase; letter-spacing: 0.04em; }
.br-stat-val   { font-size: 14px; font-weight: 800; color: var(--text); letter-spacing: -0.02em; font-variant-numeric: tabular-nums; }


/* ── Periodo personalizzato ─────────────────────────────────────────────────── */
.custom-range {
  display: flex; align-items: center; gap: var(--s2);
  background: var(--surface-2);
  border: 1px solid var(--border);
  border-radius: var(--r-md);
  padding: 4px 8px;
}
.date-input {
  background: transparent; border: none; outline: none;
  font-size: 12px; font-weight: 600; font-family: var(--font);
  color: var(--text); cursor: pointer;
  width: 118px;
}
.date-input::-webkit-calendar-picker-indicator {
  opacity: 0.4; cursor: pointer;
  filter: var(--cal-filter, none);
}
.mm-app[data-theme="dark"] { --cal-filter: invert(1); }
.date-sep { font-size: 12px; color: var(--text-muted); font-weight: 600; }

/* Transizione comparsa input */
.custom-fade-enter-active, .custom-fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}
.custom-fade-enter-from, .custom-fade-leave-to {
  opacity: 0; transform: translateY(-4px);
}


/* ── Confronto periodo ──────────────────────────────────────────────────────── */
.confronto-wrap {
  display: flex; flex-direction: column; height: 100%; padding: var(--s2) var(--s3) var(--s3);
  gap: var(--s2);
}
.confronto-toggle {
  display: flex; gap: var(--s1); align-self: flex-end;
}
.ctg-btn {
  font-size: 11px; font-weight: 700; padding: 4px 10px;
  border-radius: var(--r-full); border: 1px solid var(--border);
  background: var(--surface-2); color: var(--text-muted);
  cursor: pointer; transition: all 0.15s;
}
.ctg-btn.active {
  background: var(--text); color: var(--bg);
  border-color: var(--text);
}
.confronto-kpis {
  display: flex; gap: var(--s3); justify-content: center;
  padding-top: var(--s1);
}
.ckpi {
  display: flex; flex-direction: column; align-items: center; gap: 1px;
  padding: 5px 12px; border-radius: var(--r-md); flex: 1;
}
.ckpi-pos { background: rgba(16,185,129,0.08); }
.ckpi-neg { background: rgba(239,68,68,0.08); }
.mm-app[data-theme="dark"] .ckpi-pos { background: rgba(16,185,129,0.12); }
.mm-app[data-theme="dark"] .ckpi-neg { background: rgba(239,68,68,0.12); }
.ckpi-label { font-size: 10px; font-weight: 600; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.04em; }
.ckpi-delta { font-size: 14px; font-weight: 800; letter-spacing: -0.02em; }
.ckpi-pos .ckpi-delta { color: #059669; }
.ckpi-neg .ckpi-delta { color: #dc2626; }
.mm-app[data-theme="dark"] .ckpi-pos .ckpi-delta { color: #10b981; }
.mm-app[data-theme="dark"] .ckpi-neg .ckpi-delta { color: #ef4444; }


/* ── Confronto header ───────────────────────────────────────────────────────── */
.confronto-header {
  display: flex; align-items: center; justify-content: space-between;
  gap: var(--s3); flex-wrap: wrap;
}
.confronto-range-label {
  display: flex; align-items: center; gap: 5px;
  font-size: 11px; font-weight: 600; color: var(--text-muted);
  background: var(--surface-2); border: 1px solid var(--border);
  border-radius: var(--r-full); padding: 3px 10px;
  white-space: nowrap;
}
.crl-prev { color: var(--text-muted); }
.crl-cur  { color: var(--text); }


/* ── Budget savings row ridisegnata ────────────────────────────────────────── */
.budget-savings-row {
  display: flex;
  align-items: stretch;
  gap: 0;
  background: var(--surface-2);
  border-radius: var(--r-md);
  border: 1px solid var(--border);
  overflow: hidden;
  min-height: 80px;
}
.savings-kpi-block {
  display: flex; flex-direction: column; justify-content: center;
  gap: 3px; padding: var(--s3) var(--s4);
  min-width: 110px;
}
.skb-label {
  font-size: 11px; font-weight: 700; color: var(--text-muted);
  text-transform: uppercase; letter-spacing: 0.04em;
}
.skb-value {
  font-size: 22px; font-weight: 800; letter-spacing: -0.03em;
  font-variant-numeric: tabular-nums; color: var(--text);
  line-height: 1.1;
}
.skb-sub {
  font-size: 11px; font-weight: 600; color: var(--text-muted);
}
.skb-target { color: #d97706; }
.mm-app[data-theme="dark"] .skb-target { color: #fbbf24; }
.skb-ok   { color: #059669 !important; }
.skb-warn { color: #e11d48 !important; }
.mm-app[data-theme="dark"] .skb-ok   { color: #10b981 !important; }
.mm-app[data-theme="dark"] .skb-warn { color: #f43f5e !important; }

.savings-divider {
  width: 1px; background: var(--border);
  flex-shrink: 0; align-self: stretch;
}
/* Override: il tip occupa lo spazio rimanente */
.budget-savings-row .savings-tip-inline {
  flex: 1; border-left: none; border-radius: 0;
  padding: var(--s3) var(--s4);
  border-left: 3px solid;
}
.budget-savings-row .sti-ok   { border-color: #059669; background: rgba(16,185,129,0.06); }
.budget-savings-row .sti-warn { border-color: #e11d48; background: rgba(225,29,72,0.06); }
.mm-app[data-theme="dark"] .budget-savings-row .sti-ok   { background: rgba(16,185,129,0.08); }
.mm-app[data-theme="dark"] .budget-savings-row .sti-warn { background: rgba(244,63,94,0.08); }


/* ── Heatmap Anno × Mese ────────────────────────────────────────────────────── */
.heatmap-wrap {
  display: flex; flex-direction: column; height: 100%;
  padding: var(--s3) var(--s3) var(--s2);
  gap: var(--s2);
}
.heatmap-header {
  display: flex; align-items: center; justify-content: space-between; gap: var(--s3);
  flex-shrink: 0;
}
.heatmap-toggle { display: flex; gap: var(--s1); }

.heatmap-legend {
  display: flex; align-items: center; gap: 6px;
  font-size: 10px; font-weight: 600; color: var(--text-muted);
  text-transform: uppercase; letter-spacing: 0.04em;
}
.hml-bar {
  width: 64px; height: 8px; border-radius: 4px;
  background: linear-gradient(to right, rgba(255,235,220,0.6), rgba(200,30,30,0.8));
  border: 1px solid var(--border);
}
.mm-app[data-theme="dark"] .hml-bar {
  background: linear-gradient(to right, rgba(40,15,15,0.6), rgba(230,50,30,0.9));
}

.heatmap-scroll {
  flex: 1; overflow: auto;
  border-radius: var(--r-md);
  border: 1px solid var(--border);
}
.heatmap-table {
  width: 100%; border-collapse: collapse; table-layout: fixed;
  font-size: 11px; font-variant-numeric: tabular-nums;
}
.heatmap-table thead th {
  position: sticky; top: 0; z-index: 2;
  background: var(--surface-2); border-bottom: 1px solid var(--border);
  padding: 4px 2px; text-align: center;
  font-size: 10px; font-weight: 700; color: var(--text-muted);
  text-transform: uppercase; letter-spacing: 0.04em;
}
.hm-year-col  { width: 44px; }
.hm-tot-col   { width: 44px; }
.hm-month-col { width: calc((100% - 88px) / 12); min-width: 34px; }

.hm-year-label {
  position: sticky; left: 0; z-index: 1;
  background: var(--surface-2); border-right: 1px solid var(--border);
  padding: 5px 6px; font-size: 11px; font-weight: 800;
  color: var(--text-muted); text-align: center; white-space: nowrap;
}
.hm-cell {
  padding: 5px 2px; text-align: center;
  transition: filter 0.15s; cursor: default;
  border: 1px solid var(--border);
}
.hm-cell:hover { filter: brightness(0.88); z-index: 1; position: relative; }
.hm-val {
  font-size: 10px; font-weight: 700; line-height: 1;
  display: block;
}
.hm-total {
  position: sticky; right: 0;
  padding: 5px 4px; text-align: center;
  font-size: 10px; font-weight: 800;
  border-left: 1px solid var(--border);
  border: 1px solid var(--border);
}
.heatmap-table tfoot td {
  background: var(--surface-2) !important;
  color: var(--text-muted) !important;
  border-top: 2px solid var(--border);
  font-size: 10px; font-weight: 600;
  padding: 4px 2px; text-align: center;
}
.hm-avg { font-style: italic; }


.hml-bar.hml-bar-inc {
  background: linear-gradient(to right, rgba(220,255,235,0.6), rgba(10,130,80,0.85));
}
.mm-app[data-theme="dark"] .hml-bar.hml-bar-inc {
  background: linear-gradient(to right, rgba(10,30,20,0.6), rgba(20,180,100,0.9));
}


.hm-future {
  background: repeating-linear-gradient(
    45deg,
    transparent,
    transparent 3px,
    var(--border) 3px,
    var(--border) 4px
  ) !important;
  opacity: 0.35;
  cursor: default;
}


/* ── Heatmap KPI row ────────────────────────────────────────────────────────── */
.heatmap-kpi-row {
  display: flex; gap: var(--s2); flex-shrink: 0;
}
.hm-kpi {
  flex: 1; display: flex; flex-direction: column; gap: 1px;
  background: var(--surface-2); border: 1px solid var(--border);
  border-radius: var(--r-lg); padding: var(--s2) var(--s3);
  box-shadow: var(--shadow-sm);
}
.hm-kpi-label {
  font-size: 10px; font-weight: 700; color: var(--text-muted);
  text-transform: uppercase; letter-spacing: 0.04em;
}
.hm-kpi-val {
  font-size: 15px; font-weight: 800; letter-spacing: -0.02em;
  font-variant-numeric: tabular-nums; color: var(--text);
}
.hm-kpi-sub {
  font-size: 10px; color: var(--text-muted); font-weight: 500;
}
.hm-kpi-low  { color: #059669; }
.hm-kpi-high { color: #e11d48; }
.mm-app[data-theme="dark"] .hm-kpi-low  { color: #10b981; }
.mm-app[data-theme="dark"] .hm-kpi-high { color: #f43f5e; }


/* ── Heatmap from-year selector ─────────────────────────────────────────────── */
.heatmap-header-left {
  display: flex; align-items: center; gap: var(--s2);
}
.hm-from-year {
  display: flex; align-items: center; gap: 5px;
  background: var(--surface-2); border: 1px solid var(--border);
  border-radius: var(--r-full); padding: 4px 12px;
  box-shadow: var(--shadow-sm);
}
.hm-from-label {
  font-size: 11px; font-weight: 700; color: var(--text-muted);
}
.hm-year-select {
  background: transparent; border: none; outline: none;
  font-size: 11px; font-weight: 700; font-family: var(--font);
  color: var(--text); cursor: pointer;
  padding: 0; appearance: none; -webkit-appearance: none;
}
.hm-year-select option {
  background: var(--bg); color: var(--text);
}


/* ── Anomalie & Sanguisughe ─────────────────────────────────────────────────── */
.anomalie-wrap {
  display: flex; flex-direction: column; height: 100%;
  padding: var(--s3); gap: var(--s3); overflow: hidden;
}
.anomalie-header {
  display: flex; align-items: center; justify-content: space-between; flex-shrink: 0;
}
.anomalie-title-group {
  display: flex; align-items: center; gap: var(--s2);
  background: var(--surface-2); border: 1px solid var(--border);
  border-radius: var(--r-full); padding: 4px 12px;
}
.anomalie-label { font-size: 11px; font-weight: 700; color: var(--text-muted); }
.anomalie-month-sel { font-size: 12px; font-weight: 700; }
.anomalie-sub { font-size: 11px; color: var(--text-muted); font-style: italic; }

.anomalie-body { display: flex; flex-direction: column; gap: var(--s3); flex: 1; overflow: hidden; }

.anomalie-split {
  display: grid; grid-template-columns: 1fr 1fr; gap: var(--s3); flex: 1; overflow: hidden; min-height: 0;
}
.anomalie-col {
  display: flex; flex-direction: column; gap: var(--s2);
  background: var(--surface-2); border: 1px solid var(--border);
  border-radius: var(--r-lg); padding: var(--s3); overflow-y: auto;
}
.anomalie-col-header {
  display: flex; align-items: center; gap: 5px;
  font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em;
  padding-bottom: var(--s2); border-bottom: 1px solid var(--border); flex-shrink: 0;
}
.anomalie-bad  .anomalie-col-header { color: #e11d48; }
.anomalie-good .anomalie-col-header { color: #059669; }
.mm-app[data-theme="dark"] .anomalie-bad  .anomalie-col-header { color: #f43f5e; }
.mm-app[data-theme="dark"] .anomalie-good .anomalie-col-header { color: #10b981; }

.anomalie-list { display: flex; flex-direction: column; gap: var(--s2); }
.anomalie-item { display: flex; flex-direction: column; gap: 3px; }
.ai-top { display: flex; justify-content: space-between; align-items: baseline; }
.ai-cat { font-size: 12px; font-weight: 700; color: var(--text); }
.ai-delta { font-size: 12px; font-weight: 800; font-variant-numeric: tabular-nums; }
.bad-delta  { color: #e11d48; }
.good-delta { color: #059669; }
.mm-app[data-theme="dark"] .bad-delta  { color: #f43f5e; }
.mm-app[data-theme="dark"] .good-delta { color: #10b981; }

.ai-bar-wrap {
  position: relative; height: 6px; background: var(--surface);
  border-radius: 3px; overflow: hidden;
}
.ai-bar-avg {
  position: absolute; left: 0; top: 0; height: 100%;
  background: var(--border); border-radius: 3px;
}
.ai-bar-cur {
  position: absolute; left: 0; top: 0; height: 100%;
  border-radius: 3px; opacity: 0.85;
}
.bad-bar  { background: #e11d48; }
.good-bar { background: #059669; }
.mm-app[data-theme="dark"] .bad-bar  { background: #f43f5e; }
.mm-app[data-theme="dark"] .good-bar { background: #10b981; }

.ai-vals { display: flex; justify-content: space-between; }
.ai-val-avg { font-size: 10px; color: var(--text-muted); }
.ai-val-cur { font-size: 10px; font-weight: 600; color: var(--text); }

.anomalie-empty {
  display: flex; align-items: center; justify-content: center;
  flex: 1; font-size: 12px; color: var(--text-muted); font-style: italic; padding: var(--s4);
}

/* ── Sanguisughe ── */
.sanguisuga-wrap {
  flex-shrink: 0; background: var(--surface-2);
  border: 1px solid var(--border); border-radius: var(--r-lg);
  padding: var(--s2) var(--s3);
}
.sanguisuga-title {
  display: flex; align-items: center; gap: 5px;
  font-size: 10px; font-weight: 800; color: var(--text-muted);
  text-transform: uppercase; letter-spacing: 0.05em;
  margin-bottom: var(--s2);
}
.sanguisuga-list { display: flex; flex-direction: column; gap: 4px; }
.sg-item {
  display: grid; grid-template-columns: 120px 28px 1fr 52px;
  align-items: center; gap: var(--s2);
}
.sg-cat  { font-size: 11px; font-weight: 600; color: var(--text); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.sg-freq { font-size: 10px; font-weight: 800; color: var(--text-muted); text-align: center; }
.sg-bar-wrap { height: 5px; background: var(--surface); border-radius: 3px; overflow: hidden; }
.sg-bar { height: 100%; background: #d97706; border-radius: 3px; opacity: 0.7; }
.mm-app[data-theme="dark"] .sg-bar { background: #fbbf24; }
.sg-tot { font-size: 11px; font-weight: 700; color: var(--text); text-align: right; font-variant-numeric: tabular-nums; }



/* ── PREVISIONI ── */
.prev-wrap { display: flex; flex-direction: column; gap: var(--s6); padding: var(--s4) 0; }
.prev-section { background: var(--surface); border: 1px solid var(--border); border-radius: var(--r-lg); padding: var(--s5); }
.prev-section-title { display: flex; align-items: center; gap: var(--s2); font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: var(--text-muted); margin-bottom: var(--s4); }

.prev-kpi-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: var(--s3); margin-bottom: var(--s4); }
@media (max-width: 640px) { .prev-kpi-row { grid-template-columns: repeat(2, 1fr); } }
.prev-kpi { background: var(--surface-2); border-radius: var(--r-md); padding: var(--s3) var(--s4); display: flex; flex-direction: column; gap: 2px; }
.prev-kpi-ok  { border-left: 3px solid var(--clr-income, #059669); }
.prev-kpi-warn{ border-left: 3px solid #ef4444; }
.prev-kpi-label { font-size: 11px; font-weight: 600; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.04em; }
.prev-kpi-val   { font-size: 18px; font-weight: 800; color: var(--text); font-variant-numeric: tabular-nums; letter-spacing: -0.02em; }
.prev-kpi-sub   { font-size: 11px; color: var(--text-faint); }

.prev-month-bar { margin-top: var(--s2); }
.prev-month-bar-track { position: relative; height: 8px; background: var(--surface-2); border-radius: 99px; overflow: visible; margin-bottom: var(--s2); }
.prev-month-bar-fill  { height: 100%; background: var(--border); border-radius: 99px; transition: width 0.4s ease; }
.prev-month-bar-pace  { position: absolute; top: 50%; transform: translate(-50%, -50%); width: 14px; height: 14px; border-radius: 50%; border: 2px solid white; }
.pace-ok   { background: #059669; }
.pace-warn { background: #ef4444; }
.prev-month-bar-labels { display: flex; justify-content: space-between; font-size: 11px; color: var(--text-muted); font-weight: 600; }
.clr-ok   { color: #059669; }
.clr-warn { color: #ef4444; }

.prev-chart-wrap { height: 220px; }

/* Ricorrenze */
.ric-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: var(--s3); }
.ric-card { background: var(--surface-2); border: 1px solid var(--border); border-radius: var(--r-md); padding: var(--s3) var(--s4); }
.ric-current { border-color: #d97706; background: color-mix(in oklch, #d97706 8%, var(--surface-2)); }
.ric-overdue  { border-color: #ef4444; background: color-mix(in oklch, #ef4444 6%, var(--surface-2)); }
.ric-header { display: flex; justify-content: space-between; align-items: center; gap: var(--s2); margin-bottom: var(--s1); }
.ric-cat    { font-size: 13px; font-weight: 700; color: var(--text); }
.ric-badge  { font-size: 10px; font-weight: 700; padding: 2px 7px; border-radius: 99px; white-space: nowrap; }
.badge-now    { background: #fef3c7; color: #92400e; }
.badge-past   { background: #fee2e2; color: #991b1b; }
.badge-future { background: var(--surface); color: var(--text-muted); border: 1px solid var(--border); }
.ric-body   { display: flex; flex-direction: column; gap: 2px; margin-bottom: var(--s1); }
.ric-amount   { font-size: 15px; font-weight: 800; color: var(--text); font-variant-numeric: tabular-nums; }
.ric-interval { font-size: 11px; color: var(--text-muted); }
.ric-last     { font-size: 10px; color: var(--text-faint); }


.prev-method-badge { font-size: 10px; font-weight: 600; background: var(--surface-2); border: 1px solid var(--border); border-radius: 99px; padding: 2px 8px; color: var(--text-muted); margin-left: auto; }
.prev-model-row { display: grid; grid-template-columns: repeat(4,1fr); gap: var(--s3); margin-top: var(--s4); padding-top: var(--s4); border-top: 1px solid var(--divider); }
@media(max-width:640px){ .prev-model-row { grid-template-columns: repeat(2,1fr); } }
.prev-model-item { display: flex; flex-direction: column; gap: 2px; }
.prev-model-label { font-size: 10px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: var(--text-faint); }
.prev-model-val   { font-size: 16px; font-weight: 800; font-variant-numeric: tabular-nums; }
.prev-model-sub   { font-size: 10px; color: var(--text-faint); }
.income-text { color: #059669; }
.expense-text { color: #ef4444; }


/* ── RICORRENZE: abbonamenti table ── */
.abb-table { display: flex; flex-direction: column; gap: 2px; }
.abb-row { display: grid; grid-template-columns: 2fr 1.2fr 1fr 1fr 1.2fr; gap: var(--s3); padding: var(--s2) var(--s3); border-radius: var(--r-sm); align-items: center; font-size: 13px; }
.abb-header { font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: var(--text-faint); padding-bottom: var(--s2); border-bottom: 1px solid var(--divider); margin-bottom: var(--s1); }
.abb-row:not(.abb-header):hover { background: var(--surface-2); }
.abb-missing { background: color-mix(in oklch, #ef4444 5%, var(--surface)); }
.abb-cat    { font-weight: 700; color: var(--text); }
.abb-amount { font-weight: 800; font-variant-numeric: tabular-nums; color: var(--text); }
.abb-months { color: var(--text-muted); }
.abb-cv     { color: var(--text-muted); }
.badge-ok      { font-size: 11px; font-weight: 700; color: #059669; background: color-mix(in oklch, #059669 12%, var(--surface)); padding: 2px 8px; border-radius: 99px; }
.badge-missing { font-size: 11px; font-weight: 700; color: #ef4444; background: color-mix(in oklch, #ef4444 12%, var(--surface)); padding: 2px 8px; border-radius: 99px; }
.badge-soon    { background: color-mix(in oklch, #3b82f6 15%, var(--surface)); color: #1d4ed8; font-size: 10px; font-weight: 700; padding: 2px 7px; border-radius: 99px; }
.ric-empty { font-size: 13px; color: var(--text-faint); padding: var(--s4) 0; text-align: center; }
@media(max-width:640px){ .abb-row { grid-template-columns: 1fr 1fr; } .abb-row > :nth-child(3), .abb-row > :nth-child(4) { display: none; } }

.user-chip { display:flex;align-items:center;gap:8px;background:var(--surface-2);border:1px solid var(--border);border-radius:20px;padding:3px 10px 3px 3px; }
.user-avatar { width:28px;height:28px;border-radius:50%;object-fit:cover;border:1.5px solid var(--border); }
.user-avatar-fallback {
  display:inline-flex;align-items:center;justify-content:center;
  width:28px;height:28px;border-radius:50%;
  background:var(--primary-hl);color:var(--primary);
  font-size:12px;font-weight:700;border:1.5px solid var(--border);
  flex-shrink:0;
}
.user-name { font-size:13px;font-weight:600;color:var(--text);max-width:110px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap; }
@media (max-width:479px) { .user-name { display:none; } }
.btn-logout { display:flex;align-items:center;justify-content:center;width:24px;height:24px;border-radius:50%;background:transparent;border:none;cursor:pointer;color:var(--text-muted); }
.btn-logout:hover { background:#fee2e2;color:#dc2626; }
</style>