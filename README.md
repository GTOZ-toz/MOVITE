# MOVITE

Orari ACTV di bus, tram e battelli a Venezia, con percorsi diretti o con un cambio.
Web app installabile (PWA): funziona anche offline.

## Contenuto

| File | A cosa serve |
|---|---|
| `index.html` | L'app |
| `data.json` | Gli orari, generati dai GTFS ACTV |
| `manifest.json`, `icon-*.png` | Nome e icona per l'installazione sul telefono |
| `sw.js` | Funzionamento offline |
| `scripts/build_data.py` | Converte gli zip GTFS in `data.json` |
| `.github/workflows/aggiorna-orari.yml` | Aggiorna gli orari ogni notte |

## Pubblicazione su GitHub Pages

1. Crea un account su github.com, se non ce l'hai.
2. Crea un nuovo repository pubblico chiamato `movite` (lascia vuote le opzioni README e .gitignore).
3. Nel repository: **Add file → Upload files**, trascina **tutto il contenuto** di questa cartella
   (non la cartella stessa) e conferma con **Commit changes**.
   La cartella `.github` è nascosta su Mac e Windows: se non la vedi, creala a mano su GitHub con
   **Add file → Create new file**, nome `.github/workflows/aggiorna-orari.yml`, e incolla il contenuto del file.
4. **Settings → Pages**: in *Source* scegli **Deploy from a branch**, branch `main`, cartella `/ (root)`, **Save**.
5. Dopo un paio di minuti l'app è online su `https://TUONOME.github.io/movite/`.

## Aggiornamento automatico degli orari

1. **Settings → Actions → General → Workflow permissions**: scegli **Read and write permissions** e salva.
2. Tab **Actions** → *Aggiorna orari ACTV* → **Run workflow** per provarlo subito.
   Da quel momento gira da solo ogni notte e ripubblica `data.json` solo quando ACTV cambia gli orari.

Se un giorno fallisce (per esempio il sito ACTV è giù o cambia gli indirizzi dei file), GitHub ti manda una email.
Gli orari già pubblicati restano validi fino alla loro scadenza.

Per aggiornare a mano: scarica `actv_aut.zip` e `actv_nav.zip` e lancia

```
python3 scripts/build_data.py actv_aut.zip actv_nav.zip data.json
```

poi carica il nuovo `data.json` nel repository.

## Installazione sul telefono

- **iPhone**: apri l'indirizzo in **Safari** → pulsante Condividi → **Aggiungi alla schermata Home**.
- **Android**: apri l'indirizzo in **Chrome** → menu ⋮ → **Installa app** (o *Aggiungi a schermata Home*).

## Provarla sul computer

Il file `index.html` aperto con doppio clic non funziona, perché il browser blocca la lettura di `data.json`.
Da questa cartella lancia `python3 -m http.server` e apri `http://localhost:8000`.

## Dati

Orari: open data ACTV (actv.avmspa.it). Controlla sul catalogo open data ACTV le condizioni di licenza
e riporta la fonte nell'app se richiesto. MOVITE non è un'app ufficiale ACTV.
