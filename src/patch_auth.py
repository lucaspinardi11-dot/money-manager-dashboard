#!/usr/bin/env python3
"""
Applica le 5 patch Google Auth al file MM-dashboard-v4.vue
Uso: python3 patch_auth.py MM-dashboard-v4.vue
"""
import sys, shutil, os

if len(sys.argv) < 2:
    print("Uso: python3 patch_auth.py <percorso/MM-dashboard-v4.vue>")
    sys.exit(1)

path = sys.argv[1]
if not os.path.exists(path):
    print(f"File non trovato: {path}")
    sys.exit(1)

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Backup
shutil.copy(path, path + '.backup')
print(f"Backup creato: {path}.backup")

# ── PATCH 1: onMounted nell'import ──
old = "import { ref, computed, watch } from \'vue\';"
new = "import { ref, computed, watch, onMounted } from \'vue\';"
content = content.replace(old, new, 1)

# ── PATCH 2: Blocco Google Auth dopo ChartJS.register ──
old = "ChartJS.register(annotationPlugin);\n\n// ── TEMA ──"
new = """ChartJS.register(annotationPlugin);

// ── GOOGLE AUTH ──
const GOOGLE_CLIENT_ID = '1045116249963-98lmpknvv2rcmi347cn87ju720182kjn.apps.googleusercontent.com';
const googleUser = ref(null);

const handleLogout = () => {
  googleUser.value = null;
  setTimeout(() => initGoogleSignIn(), 150);
};

const initGoogleSignIn = () => {
  if (!window.google?.accounts) return;
  window.google.accounts.id.initialize({
    client_id: GOOGLE_CLIENT_ID,
    callback: (response) => {
      try {
        const payload = JSON.parse(atob(response.credential.split('.')[1]));
        googleUser.value = { name: payload.name, given_name: payload.given_name, picture: payload.picture, email: payload.email };
      } catch (e) { console.error('Errore token Google:', e); }
    },
    auto_select: false,
    cancel_on_tap_outside: true,
  });
  const btnEl = document.getElementById('google-signin-btn');
  if (btnEl) {
    window.google.accounts.id.renderButton(btnEl, {
      theme: 'outline', size: 'large', shape: 'rectangular', text: 'signin_with', locale: 'it', width: 280,
    });
  }
  window.google.accounts.id.prompt();
};

onMounted(() => {
  const script = document.createElement('script');
  script.src = 'https://accounts.google.com/gsi/client';
  script.async = true; script.defer = true;
  script.onload = () => initGoogleSignIn();
  document.head.appendChild(script);
});

// ── TEMA ──"""
content = content.replace(old, new, 1)

# ── PATCH 3: user-chip nell'header dopo theme-toggle ──
old = """          </button>
        </div>
      </div>
    </header>"""
new = """          </button>
          <div v-if="googleUser" class="user-chip">
            <img :src="googleUser.picture" :alt="googleUser.name" class="user-avatar" referrerpolicy="no-referrer" />
            <span class="user-name">{{ googleUser.given_name || googleUser.name }}</span>
            <button class="btn-logout" @click="handleLogout" title="Esci">
              <svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><path d="M13 3h4v14h-4M8 7l-4 3 4 3M4 10h9"/></svg>
            </button>
          </div>
        </div>
      </div>
    </header>"""
content = content.replace(old, new, 1)

# ── PATCH 4: Login screen + v-else-if sull\'upload screen ──
old = """    <!-- ═══ MAIN ═══ -->
    <main class="mm-main">

      <!-- ── UPLOAD SCREEN ── -->
      <div v-if="!fileLoaded" class="upload-screen">"""
new = """    <!-- ═══ MAIN ═══ -->
    <main class="mm-main">

      <!-- ── LOGIN SCREEN ── -->
      <div v-if="!googleUser" class="upload-screen">
        <div class="upload-card" style="max-width:360px">
          <div style="display:flex;justify-content:center;margin-bottom:1.5rem">
            <svg style="width:52px;height:52px;color:var(--color-primary, #01696f)" viewBox="0 0 32 32" fill="none">
              <rect x="3" y="8" width="26" height="18" rx="3" stroke="currentColor" stroke-width="2"/>
              <path d="M3 13h26" stroke="currentColor" stroke-width="2"/>
              <circle cx="10" cy="20" r="2" fill="currentColor"/>
              <rect x="15" y="19" width="8" height="2" rx="1" fill="currentColor"/>
            </svg>
          </div>
          <h2 class="upload-title">Money Manager</h2>
          <p class="upload-desc">Accedi con Google per continuare alla dashboard.</p>
          <div id="google-signin-btn" style="display:flex;justify-content:center;margin:1.5rem 0 0.5rem;min-height:44px"></div>
          <p style="font-size:12px;color:var(--text-faint);text-align:center;margin-top:0.5rem">🔒 I tuoi dati rimangono solo sul tuo dispositivo.</p>
        </div>
      </div>

      <!-- ── UPLOAD SCREEN ── -->
      <div v-else-if="!fileLoaded" class="upload-screen">"""
content = content.replace(old, new, 1)

# ── PATCH 5: Stili user-chip prima di </style> ──
old = "</style>"
new = """.user-chip { display:flex;align-items:center;gap:8px;background:var(--surface-2);border:1px solid var(--border);border-radius:20px;padding:3px 10px 3px 3px; }
.user-avatar { width:28px;height:28px;border-radius:50%;object-fit:cover;border:1.5px solid var(--border); }
.user-name { font-size:13px;font-weight:600;color:var(--text);max-width:110px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap; }
@media (max-width:479px) { .user-name { display:none; } }
.btn-logout { display:flex;align-items:center;justify-content:center;width:24px;height:24px;border-radius:50%;background:transparent;border:none;cursor:pointer;color:var(--text-muted); }
.btn-logout:hover { background:#fee2e2;color:#dc2626; }
</style>"""
# Sostituisce l'ultima occorrenza (la </style> finale)
idx = content.rfind("</style>")
content = content[:idx] + new + content[idx+len("</style>"):]

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"✅ Patch applicate con successo!")
print(f"   File: {path}")
print(f"   Righe: {content.count(chr(10))}")
