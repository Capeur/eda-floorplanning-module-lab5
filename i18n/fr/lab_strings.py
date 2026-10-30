"""French text for the Lab 05 browser lab (B*-tree), except the strings module.

Every word the tool shows lives in platform/tools/bstar-tree/bstar-tree-strings.js. Its French copy is
i18n/fr/bstar-tree-strings.js: build_site.py puts it in docs/fr/tools/bstar-tree/ in place of the English file,
after checking that both have the same keys and functions (tools/strings_shape.mjs).

What is left here are exact (file, English snippet, French text) replacements for the page of the lab
(index.html) and for the shared challenge chrome (assets/clustering-ui.js). If a snippet is no longer found
(the lab or the shared file changed in eda-learning), the build stops, so a half-translated lab is never published.

Paths are relative to docs/fr/. Challenge ids, CSS classes, block names (A-E) and numbers stay as they are.
Vocabulary: plan de masse (floorplan), bloc (block), contour (outline), arbre B* (B*-tree), enfant gauche / droit,
à côté / à l'étage (next door / upstairs), ligne d'horizon (skyline), boîte englobante (bounding box),
cases perdues (wasted squares), tourner (turn), échanger (swap), déplacer une feuille (move a leaf),
ordre de parcours (walk order).
"""

LAB = "tools/bstar-tree/"
UI = "assets/clustering-ui.js"

STRINGS = [
    # ---------------- page (index.html) ----------------
    (LAB + "index.html", '<html lang="en">', '<html lang="fr">'),
    (LAB + "index.html", "<title>B*-tree — EDA Algorithms Platform</title>",
     "<title>Arbre B* — EDA Algorithms Platform</title>"),
    (LAB + "index.html", ">Skip to content<", ">Aller au contenu<"),
    (LAB + "index.html", '<div class="eyebrow">Interactive tool</div>', '<div class="eyebrow">Outil interactif</div>'),
    (LAB + "index.html", "<h1>B*-tree</h1>", "<h1>Arbre B*</h1>"),
    (LAB + "index.html",
     "Edit a B*-tree, pack it, and watch each block drop onto the skyline: left child next door, right child upstairs.",
     "Modifiez un arbre B*, placez-le, et regardez chaque bloc tomber sur la ligne d'horizon : l'enfant gauche va à côté, l'enfant droit va à l'étage."),

    # ---------------- shared challenge chrome (clustering-ui.js) ----------------
    (UI, 'statusText: "Idle"', 'statusText: "En attente"'),
    (UI, '"Challenge armed — act, then Check"', '"Défi lancé : agissez, puis Vérifier"'),
    (UI, '"Starter loaded (reference)"', '"Exemple de départ chargé (référence)"'),
    (UI, '"Load a challenge with Start"', '"Lancez un défi avec Commencer"'),
    (UI, 'setStatus("pass", "PASS")', 'setStatus("pass", "RÉUSSI")'),
    (UI, '"Not yet — try again or show hint"', '"Pas encore : réessayez ou affichez l\'indice"'),
    (UI, '"Load starter example"', '"Charger l\'exemple de départ"'),
    (UI, "<h2>Challenges</h2>", "<h2>Défis</h2>"),
    (UI, "${challenges.length} cleared</span>", "${challenges.length} réussis</span>"),
    (UI, '<label for="lab-chal-sel">Pick one</label>', '<label for="lab-chal-sel">Choisir</label>'),
    (UI, '"Pick a challenge and click <strong>Start</strong>. The starter example above stays available as a reference — reload it anytime."',
     '"Choisissez un défi et cliquez sur <strong>Commencer</strong>. L\'exemple de départ reste disponible comme référence : rechargez-le quand vous voulez."'),
    (UI, "<strong>Hint:</strong>", "<strong>Indice :</strong>"),
    (UI, '"Restart" : "Start"', '"Recommencer" : "Commencer"'),
    (UI, '"Hide hint" : "Show hint"', '"Masquer l\'indice" : "Afficher l\'indice"'),
    (UI, '"disabled"}>Check</button>', '"disabled"}>Vérifier</button>'),
    (UI, ">Next challenge</button>", ">Défi suivant</button>"),
    (UI, ">Stop checking</button>", ">Arrêter le défi</button>"),
    (UI, 'el("h2", { text: "Graph" })', 'el("h2", { text: "Graphe" })'),
    (UI, 'el("h2", { text: "Reference / metrics" })', 'el("h2", { text: "Travail et mesures" })'),

]
