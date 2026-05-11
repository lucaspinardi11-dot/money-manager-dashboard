const functions = require('@google-cloud/functions-framework');
const { google } = require('googleapis');

functions.http('getBackupFile', async (req, res) => {
  // 1. Abilita i CORS per permettere alla tua dashboard Vue di comunicare con questa API
  res.set('Access-Control-Allow-Origin', '*');
  res.set('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.set('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  // Risposta per le richieste di preflight (CORS)
  if (req.method === 'OPTIONS') {
    res.status(204).send('');
    return;
  }

  try {
    // 2. Autenticazione automatica (usa le credenziali della Cloud Function)
    const auth = new google.auth.GoogleAuth({
      scopes: ['https://www.googleapis.com/auth/drive.readonly'],
    });
    const drive = google.drive({ version: 'v3', auth });

    // 3. Cerca l'ultimo file .mmbak
    const response = await drive.files.list({
      q: "name contains '.mmbak' and trashed = false",
      fields: 'files(id, name, createdTime)',
      orderBy: 'createdTime desc',
      pageSize: 1,
    });

    const files = response.data.files;
    if (!files || files.length === 0) {
      res.status(404).send('Nessun file .mmbak trovato nel Drive collegato.');
      return;
    }

    const fileId = files[0].id;

    // 4. Scarica il file e passalo in streaming come binario SQLite
    const fileStream = await drive.files.get(
      { fileId: fileId, alt: 'media' },
      { responseType: 'stream' }
    );

    res.set('Content-Type', 'application/x-sqlite3');
    res.set('Content-Disposition', `attachment; filename="${files[0].name}"`);

    fileStream.data.pipe(res);
  } catch (error) {
    console.error('Errore API Drive:', error);
    res.status(500).send('Errore durante il recupero del file');
  }
});