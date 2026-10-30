/**
 * Texte français du lab arbre B* (Lab 05). C'est une copie de platform/tools/bstar-tree/bstar-tree-strings.js du
 * cours : build_site.py la place à la place de l'original dans docs/fr/tools/bstar-tree/ et vérifie que les clés,
 * les sous-clés et les fonctions (même nombre d'arguments) sont exactement celles de l'original.
 * Noms de blocs (A-E), identifiants de défis, codes et nombres ne changent pas.
 * Vocabulaire : à côté = enfant gauche, à l'étage = enfant droit, ligne d'horizon, boîte englobante, cases perdues,
 * tourner, échanger, déplacer une feuille, ordre de parcours.
 */
export const T = {
  // ---------------- page chrome ----------------
  panelLeft: "Arbre et plan de masse",
  panelRight: "Modifier l'arbre",
  starterButton: "Réinitialiser l'espace de travail",
  idlePrompt: "Choisissez un défi et cliquez sur <strong>Commencer</strong>. Modifiez l'arbre, appuyez sur <strong>Placer</strong>, puis <strong>Vérifier</strong>. La révélation sert à réviser : elle ne compte jamais.",
  starterHtml: `<p><strong>Votre espace de travail :</strong> l'arbre à gauche est une recette pour le plan de masse à côté.
    Choisissez où chaque bloc s'accroche (son parent, et à côté ou à l'étage), échangez deux noms, tournez un bloc, déplacez une feuille,
    puis appuyez sur <strong>Placer</strong> pour faire tomber les blocs sur la ligne d'horizon. Les défis vérifient l'arbre que <em>vous</em> avez construit
    et placé : un changement après Placer demande un nouveau Placer, et la révélation de révision ne compte jamais.</p>`,

  // ---------------- tree view ----------------
  treeCaption: "L'arbre",
  treeLegendLeft: "trait plein = à côté (enfant gauche)",
  treeLegendRight: "trait en pointillé = à l'étage (enfant droit)",
  treeLegendWalk: "petit nombre = ordre de parcours",
  treeEmpty: "Arbre vide : choisissez une racine dans le tableau à droite.",
  loose: "hors de l'arbre :",
  rootTag: "racine",
  problems: {
    "no-root": () => "Pas encore de racine : un bloc doit être la racine.",
    "two-roots": (p) => `Deux racines (${p.ids.join(", ")}) : un seul bloc peut être la racine.`,
    "slot-twice": (p) => `${p.ids.join(" et ")} sont tous deux ${p.side === "left" ? "à côté de" : "à l'étage sur"} ${p.parent} : une place ne contient qu'un bloc.`,
    "parent-out": (p) => `${p.id} est accroché à ${p.parent}, mais ${p.parent} n'est pas dans l'arbre.`,
    "cut-off": (p) => `${p.id} n'est pas relié à la racine.`,
  },

  // ---------------- floor view ----------------
  floorCaption: "Le plan de masse (contour 10 × 8)",
  floorLegendSky: "ligne jaune = ligne d'horizon",
  floorLegendBox: "boîte en pointillé = boîte englobante",
  floorNotPacked: "Appuyez sur Placer pour faire tomber les blocs.",
  floorStale: "L'arbre a changé : appuyez de nouveau sur Placer.",
  floorBad: "Corrigez d'abord l'arbre (voir les lignes rouges).",
  bboxLabel: (bw, bh, area) => `${bw} × ${bh} = ${area}`,
  turnedMark: "↻",

  // ---------------- editor ----------------
  editorHelp: "Pour chaque bloc, choisissez son parent et son côté. Puis appuyez sur Placer.",
  colBlock: "Bloc",
  colSize: "Taille",
  colParent: "Parent",
  colSide: "Côté",
  optNone: "— hors de l'arbre",
  optRoot: "racine",
  optLeft: "à côté (gauche)",
  optRight: "à l'étage (droite)",
  sizeOf: (w, h, turned) => `${w}×${h}${turned ? " ↻" : ""}`,
  ariaParent: (id) => `Parent de ${id}`,
  ariaSide: (id) => `Côté de ${id}`,
  swapLabel: "Échanger",
  swapWith: "avec",
  swapBtn: "Échanger les noms",
  turnLabel: "Tourner",
  turnBtn: "Tourner le bloc",
  moveLabel: "Déplacer une feuille",
  moveTo: "vers",
  moveBtn: "Déplacer la feuille",
  guessLabel: "Devinez D.y avant de placer :",
  guessBtn: "Enregistrer",
  guessAria: "Votre estimation de D.y",
  guessNone: "aucune estimation enregistrée",
  guessShown: (g) => `estimation enregistrée D.y = ${g.value}${g.blind ? " (faite avant de placer cet arbre)" : " (faite après avoir placé cet arbre : ne compte pas)"}`,

  // ---------------- buttons above the workspace ----------------
  loadLabel: "Charger un arbre :",
  presets: {
    golden: "Référence",
    lift: "A et C échangés",
    order: "Arbre d'ordre de parcours",
    chain: "Longue rangée",
    swap: "Mauvais arbre (40)",
  },
  packBtn: "Placer",
  clearBtn: "Effacer l'arbre",
  revealBtn: "Révéler une réponse (révision)",

  // ---------------- numbers panel ----------------
  lines: {
    tree: (t) => `arbre : ${t}`,
    walk: (w) => `ordre de parcours : ${w}`,
    turned: (r) => `tournés : ${r.length ? r.join(", ") : "aucun"}`,
    positions: (p) => `positions : ${p}`,
    bbox: (bw, bh, area) => `boîte englobante : ${bw} × ${bh} = ${area}`,
    wasted: (w, blocks) => `cases perdues : ${w} (les blocs couvrent ${blocks})`,
    legalYes: "valide : oui (dans le contour 10 × 8)",
    legalNo: (ids) => `valide : non (${ids.join(", ")} dépasse du contour)`,
    deadspace: (d) => `espace perdu du contour : 80 − 23 = ${d} (le même pour tous les arbres)`,
    notPacked: "placement : pas encore placé",
    stale: "placement : périmé (l'arbre a changé après Placer)",
    base: (b) => `construit à partir de : ${b}`,
    ops: (n, list) => `changements depuis : ${n ? list : "aucun"}`,
    guess: (g) => `estimation : ${g}`,
  },
  bases: {
    empty: "un arbre vide (Effacer)",
    golden: "l'arbre de référence",
    lift: "l'arbre avec A et C échangés",
    order: "l'arbre d'ordre de parcours",
    chain: "la longue rangée",
    swap: "le mauvais arbre (40)",
    reveal: "la réponse révélée (révision : ne compte jamais)",
  },
  ops: {
    edit: (o) => `modifier ${o.id}`,
    swap: (o) => `échanger ${o.a},${o.b}`,
    turn: (o) => `tourner ${o.id}`,
    move: (o) => `déplacer ${o.leaf} vers ${o.parent} ${o.side === "left" ? "à côté" : "à l'étage"}`,
    pack: () => "placer",
  },
  checkHead: "Vérification :",

  // ---------------- messages after an action ----------------
  msg: {
    edited: (m) => `${m.id} déplacé dans l'arbre. Appuyez sur Placer pour voir le nouveau plan de masse.`,
    "fix-tree": () => "Corrigez d'abord l'arbre : chaque bloc de l'arbre a besoin d'une place, un bloc par place.",
    "empty-tree": () => "L'arbre est vide : choisissez d'abord une racine.",
    "swap-same": () => "Choisissez deux blocs différents à échanger.",
    "not-in-tree": (m) => `${m.id} n'est pas dans l'arbre.`,
    swapped: (m) => `Noms ${m.a} et ${m.b} échangés : la forme de l'arbre n'a pas changé.`,
    turned: (m) => `${m.id} tourné : il fait maintenant ${m.w} de large et ${m.h} de haut.`,
    "turned-back": (m) => `${m.id} retourné : de nouveau ${m.w} de large et ${m.h} de haut.`,
    moved: (m) => `Feuille ${m.leaf} déplacée ${m.side === "left" ? "à côté de" : "à l'étage sur"} ${m.parent}.`,
    "move-same": (m) => `${m.leaf} est déjà accrochée là : rien n'a changé.`,
    "move-root": (m) => `${m.leaf} est la racine : seule une feuille peut se déplacer.`,
    "move-self": (m) => `${m.leaf} ne peut pas s'accrocher à elle-même.`,
    "move-not-leaf": (m) => `${m.leaf} a des enfants : seule une feuille (un bloc sans enfant) peut se déplacer.`,
    "move-missing": (m) => `${m.id} n'est pas dans l'arbre.`,
    "move-taken": (m) => `${m.parent} a déjà un bloc ${m.side === "left" ? "à côté" : "à l'étage"}.`,
    "bad-side": () => "Choisissez à côté ou à l'étage.",
    packed: (m) => `Placé : boîte englobante ${m.bw} × ${m.bh} = ${m.area}, ${m.legal ? "valide" : "non valide"}.`,
    cleared: () => "Arbre effacé : tous les blocs sont hors de l'arbre. Choisissez une racine pour commencer.",
    preset: (m) => `Chargé : ${T.bases[m.name]}. Appuyez sur Placer pour le voir.`,
    revealed: () => "Une réponse est révélée (révision) : elle ne compte jamais. Effacez l'arbre, chargez un arbre ou appuyez sur Commencer pour continuer.",
    "guess-bad": () => "Tapez un nombre entier pour D.y, par exemple 2.",
    "guess-saved": (m) => `Estimation enregistrée : D.y = ${m.value}. Appuyez maintenant sur Placer.`,
    "guess-late": (m) => `Estimation enregistrée (D.y = ${m.value}), mais cet arbre était déjà placé : elle ne compte pas. Appuyez sur Commencer pour réessayer.`,
  },

  // ---------------- why a Check did not pass ----------------
  why: {
    pass: () => "RÉUSSI.",
    unknown: () => "Défi inconnu.",
    revealed: () => "Cet arbre vient de la révélation de révision : il ne compte jamais. Appuyez sur Commencer (ou Effacer) et construisez-le vous-même.",
    "other-start": (w) => `Partez de l'arbre que ce défi charge${w.start === "empty" ? " (un arbre vide)" : ""} : un arbre chargé avec un autre bouton ne compte pas. Appuyez de nouveau sur Commencer.`,
    "empty-tree": () => "L'arbre est vide.",
    "fix-tree": () => "L'arbre a un problème (voir les lignes rouges dessous).",
    "not-packed": () => "Appuyez d'abord sur Placer : la vérification lit le plan de masse placé.",
    stale: () => "L'arbre a changé après Placer : appuyez de nouveau sur Placer.",
    "not-all": (w) => `Mettez les cinq blocs dans l'arbre (il manque ${w.ids.join(", ")}).`,
    "not-legal": (w) => `Non valide : ${w.ids.join(", ")} dépasse du contour 10 × 8.`,
    "no-turns": () => "Aucun bloc tourné pour celui-ci : retournez-le.",
    "not-golden": () => "Pas encore l'arbre de référence : A est la racine, B, C et E vont à côté l'un après l'autre, D va à l'étage sur A.",
    "d-y": (w) => `D arrive en y = ${w.y}, pas 3.`,
    "tree-changed": () => "Gardez l'arbre que ce défi charge (appuyez sur Commencer pour le retrouver).",
    "no-guess": () => "Tapez votre estimation de D.y et appuyez sur Enregistrer avant de placer.",
    "guess-other": () => "Votre estimation a été faite pour un autre arbre : enregistrez-en une nouvelle, puis placez.",
    "guess-late": () => "Votre estimation a été enregistrée après avoir placé cet arbre : elle ne compte pas. Appuyez sur Commencer et devinez d'abord.",
    "guess-wrong": () => "Votre estimation n'est pas l'endroit où arrive D. Regardez de nouveau les blocs placés avant D, puis appuyez sur Commencer et devinez avant de placer.",
    turns: (w) => `Tournez exactement un bloc (maintenant ${w.n}).`,
    "no-change": () => "L'arbre n'a pas changé.",
    "not-one-swap": () => "Cet arbre n'est pas à un échange du mauvais arbre. Appuyez sur Commencer et faites un seul échange.",
    "not-one-move": () => "Cet arbre n'est pas à un déplacement de feuille du mauvais arbre. Appuyez sur Commencer et déplacez une seule feuille.",
    area: (w) => `Boîte englobante ${w.bw} × ${w.bh} = ${w.area} : la cible est ${w.target} ou moins.`,
    "not-below": (w) => `Boîte englobante ${w.bw} × ${w.bh} = ${w.area} : battez 27 (moins de 27).`,
  },

  // ---------------- challenges ----------------
  challenges: {
    "build-golden": {
      title: "Construire l'arbre de référence",
      prompt: "Commencer donne un arbre vide. Construisez vous-même l'arbre de référence avec les menus Parent et Côté : A est la racine, B est à côté de A, C à côté de B, E à côté de C, et D à l'étage sur A. Puis Placer et Vérifier.",
      hint: "Mettez d'abord le parent de A sur racine. Puis B : parent A, à côté. C : parent B, à côté. E : parent C, à côté. D : parent A, à l'étage.",
    },
    "d-at-3": {
      title: "Soulever D en y = 3",
      prompt: "Commencer charge l'arbre de référence, où D arrive en y = 2. Changez l'arbre pour que D arrive en y = 3, avec les cinq blocs dans le contour.",
      hint: "D est à l'étage sur la racine, trois cases de large. Quel bloc fait trois de haut ? Mettez-le sous l'emprise de D (essayez d'échanger deux noms).",
    },
    "predict-dy": {
      title: "Prédire D.y avant de placer",
      prompt: "Commencer charge l'arbre d'ordre de parcours. Avant d'appuyer sur Placer, tapez où D va arriver (son y) et appuyez sur Enregistrer. Puis Placer et Vérifier.",
      // two hints in one (the shared chrome shows one hint text): a question first, then the fact that answers it
      hint: "1. Quels blocs sont placés avant D ? Comptez-les dans l'ordre de parcours. 2. E est placé avant D, et une partie de E est sous D.",
    },
    "chain-turn": {
      title: "Faire tenir la longue rangée avec une rotation",
      prompt: "Commencer charge la longue rangée : chaque bloc à côté, 12 de large dans un contour de 10 de large. Gardez l'arbre, tournez exactement un bloc pour que la rangée tienne, puis Placer et Vérifier.",
      hint: "La rangée fait 3 + 2 + 2 + 3 + 2 = 12 de large. Quel bloc devient plus étroit quand on le tourne ? Il doit gagner deux cases.",
    },
    "fix-swap": {
      title: "Corriger le mauvais arbre. Un seul échange suffit.",
      prompt: "Commencer charge un mauvais arbre : boîte englobante 10 × 4 = 40. Un seul échange de deux noms suffit pour obtenir une boîte de 27. Puis Placer et Vérifier.",
      hint: "E est à l'étage sur A et rend la boîte haute de 4, alors que D est au bout de la rangée. Quels deux noms échangeraient leur place ?",
    },
    "move-leaf": {
      title: "Un seul déplacement de feuille suffit : 40 → 28.",
      prompt: "Commencer charge le même mauvais arbre (40). Un seul déplacement de feuille suffit : déplacez une feuille (un bloc sans enfant) vers une place libre pour que la boîte englobante tombe à 28. Puis Placer et Vérifier.",
      hint: "D est une feuille au bout de la rangée et rend la boîte large de 10. Accrochez-la à l'étage sur un bloc du milieu de la rangée.",
    },
    "reach-27": {
      title: "De la longue rangée à 27",
      prompt: "Commencer charge la longue rangée (12 de large, non valide). Reconstruisez l'arbre comme vous voulez jusqu'à ce que le plan de masse soit valide avec une boîte englobante de 27 ou moins.",
      hint: "L'arbre de référence donne 9 × 3 = 27 : mettez un bloc à l'étage au lieu du bout de la rangée.",
    },
    "beat-27": {
      title: "Battre 27",
      prompt: "Commencer charge l'arbre de référence (27). Trouvez un arbre dont la boîte englobante est plus petite que 27, avec les cinq blocs dans le contour. Tourner des blocs est permis.",
      hint: "Essayez une boîte large de 6 et haute de 4, ou large de 5 et haute de 5. Mettez un bloc bas (D) à côté de A et empilez d'autres blocs à l'étage.",
    },
    "reach-24": {
      title: "Atteindre 24 sans tourner",
      prompt: "Pour aller plus loin : atteignez la plus petite boîte possible, 24 cases, sans aucun bloc tourné. Seuls huit des 5040 arbres y arrivent.",
      hint: "Visez 6 × 4. A à la racine, D à côté (D ne fait que 1 de haut). Puis C à l'étage sur A, E à côté de C, et B à un endroit où la ligne d'horizon le soulève sur D.",
    },
  },
};
