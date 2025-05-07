
Tetris in Python con Pygame

🎮 Panoramica del Progetto

Questo è un gioco completo di Tetris realizzato utilizzando Python e la libreria Pygame. Il gioco include due modalità:

Modalità Classica: La velocità aumenta con il punteggio.

Modalità a Livelli: Progredisci attraverso 15 livelli, ciascuno con una velocità crescente.

🚀 Caratteristiche

Due modalità di gioco: Classica e a Livelli

Punteggio e progressione dei livelli

Pezzi Tetris rotanti (I, O, S, Z, T, L, J)

Anteprima dei prossimi pezzi

Musica di sottofondo, con possibilità di attivare/disattivare l'audio

Schermata animata di game over

🖥️ Installazione e Configurazione

Assicurati di avere Python installato sul tuo sistema.

Installa Pygame utilizzando pip:

pip install pygame

Clona questo repository:

git clone <repository_url>

Posiziona i seguenti file necessari nella stessa directory:

Tetris.mp3 (Musica di sottofondo)

titlescreen.mp3 (Musica del menu)

gameover.mp3 (Suono del Game Over)

titlebg.webp (Immagine di sfondo del menu)

Pixelated.ttf (Font per il menu)

▶️ Come giocare

Avvia il gioco con:

python main.py

Utilizza i tasti freccia:

Sinistra/Destra: Muovi il pezzo

Giù: Accelerazione della caduta

Su: Ruota il pezzo

Attiva/disattiva la musica utilizzando il pulsante sullo schermo.

⚡ Come Funziona

La griglia di gioco è definita utilizzando una lista 2D (ROWS x COLUMNS).

I pezzi vengono generati casualmente e appaiono in alto.

I pezzi cadono a una velocità determinata dalla modalità.

Quando un pezzo atterra, viene aggiunto alla griglia.

Le righe complete vengono cancellate, assegnando punti.

Se un pezzo non può entrare, il gioco termina.
