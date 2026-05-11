const functions = require('@google-cloud/functions-framework');

const CLIENT_ID = process.env.GOOGLE_CLIENT_ID;
const CLIENT_SECRET = process.env.GOOGLE_CLIENT_SECRET;
const ALLOWED_ORIGINS = (process.env.ALLOWED_ORIGINS || 'capacitor://localhost').split(',');

functions.http('exchangeToken', async (req, res) => {
  const origin = req.headers.origin || '';
  const allowed = ALLOWED_ORIGINS.includes(origin) || origin === '';
  res.set('Access-Control-Allow-Origin', allowed ? origin : ALLOWED_ORIGINS[0]);
  res.set('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.set('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') { res.status(204).send(''); return; }
  if (req.method !== 'POST') { res.status(405).json({ error: 'Method not allowed' }); return; }

  const { code, refresh_token, action } = req.body;

  try {
    let tokenResponse;

    if (action === 'refresh' && refresh_token) {
      tokenResponse = await fetch('https://oauth2.googleapis.com/token', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({
          client_id: CLIENT_ID,
          client_secret: CLIENT_SECRET,
          refresh_token: refresh_token,
          grant_type: 'refresh_token',
        }),
      });
    } else if (action === 'exchange' && code) {
      tokenResponse = await fetch('https://oauth2.googleapis.com/token', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({
          client_id: CLIENT_ID,
          client_secret: CLIENT_SECRET,
          code: code,
          grant_type: 'authorization_code',
          redirect_uri: 'postmessage',
        }),
      });
    } else {
      res.status(400).json({ error: 'Parametri mancanti' });
      return;
    }

    const data = await tokenResponse.json();

    if (!tokenResponse.ok || data.error) {
      res.status(400).json({ error: data.error_description || data.error });
      return;
    }

    res.status(200).json({
      access_token: data.access_token,
      refresh_token: data.refresh_token || null,
      expires_in: data.expires_in,
    });

  } catch (err) {
    console.error('Errore interno:', err);
    res.status(500).json({ error: 'Errore interno del server' });
  }
});