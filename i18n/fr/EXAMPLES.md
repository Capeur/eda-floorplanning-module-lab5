# Exemples — arbre B*

Parcours A (implémentation). Les cinq blocs sont dans `examples/tiny_modules.json`, les arbres d'exemple dans `examples/*.json`,
et le corrigé est `examples/bstar_check.py`.
Chaque nombre ci-dessous a été affiché par ce vérificateur (`python3 examples/bstar_check.py --show`, `--json`).
Lancez-le depuis le dossier du module ; il n'a besoin que de la bibliothèque standard de Python.

## Objectif

Un plan de masse à cinq blocs peut s'écrire comme un **arbre binaire**. On construit l'image à partir de l'arbre (**placer**, en anglais *pack*), on la note
(**boîte englobante**, **valide**), et on change l'image en changeant l'arbre (**échanger**, **tourner**, **déplacer**).
Le recuit simulé (un lab plus tard) fait exactement ces trois changements des milliers de fois.

## Définitions

- **Bloc** : un rectangle avec un nom, une largeur `w` et une hauteur `h`. Les tailles s'écrivent `w x h` : « 3 x 2 » fait 3 de large et 2 de haut.
  Les cinq blocs : A 3x2, B 2x3, C 2x2, D 3x1, E 2x2. Leurs aires font **23** au total.
- **Contour** : la boîte fixe dans laquelle les blocs doivent rester. Ici **10 x 8** (aire 80). L'origine est le coin inférieur gauche et
  y croît vers le haut.
- **Arbre** : chaque bloc apparaît exactement une fois. Un nœud a un **enfant gauche** et un **enfant droit**, tous deux facultatifs.
  Forme texte : `id(gauche,droit)`, `-` pour un enfant vide, un simple id pour une feuille. `A(B(C(E,-),-),D)` est l'arbre de référence :
  l'enfant gauche de A est B, celui de B est C, celui de C est E, et l'enfant droit de A est D.
- **Enfant gauche = à côté** : il commence au bord droit de son parent. **Enfant droit = à l'étage** : il commence au
  même bord gauche que son parent. Les noms sont à l'inverse de ce qu'on devine, alors dites « à côté » et « à l'étage ».
- **Ligne d'horizon** (le « contour » des articles scientifiques, à ne pas confondre avec le contour de la puce) : pour chaque x, le bord supérieur de ce qui est déjà placé (0 là où il n'y a rien).
  Placer un bloc relève la ligne d'horizon à `y + h` sur l'emprise du bloc `[x, x + w)`.
- **Valide** : chaque bloc est dans le contour et deux blocs ne se chevauchent pas (se toucher par un bord est permis).
- **Boîte englobante** : le plus petit rectangle autour de tous les blocs : largeur = plus grand `x + w`, hauteur = plus grand `y + h`.
  **Score = aire de la boîte englobante. Cases perdues = aire de la boîte englobante − 23.**
- **Deux espaces perdus différents** : l'espace perdu du *contour* vaut `80 − 23 = 57` et ne change jamais avec l'arbre. L'espace perdu de la
  *boîte englobante* (les cases perdues) est ce qu'un arbre change : 4 pour l'arbre de référence.

## API (ce que cherche `--impl`)

Un arbre est un dictionnaire imbriqué : `{"id": "A", "left": {...}, "right": {...}}`, un enfant absent est une clé absente.
`modules` est une liste de `{"id", "w", "h"}`, `outline` vaut `{"w", "h"}`. Un placement (pack) est `{id: {"x", "y", "w", "h"}}`.

```python
pack_bstar(tree, modules)            # le placement, selon la règle ci-dessous
bounding_box(pack)                   # (largeur, hauteur)
is_legal(pack, outline)              # dans le contour et sans chevauchement
swap(tree, a, b)                     # NOUVEL arbre, noms a et b échangés, forme inchangée
rotate(modules, id)                  # NOUVELLE liste de blocs, w et h de ce bloc échangés
move_leaf(tree, leaf, parent, side)  # NOUVEL arbre, feuille coupée et accrochée à la place libre "left" ou "right" de parent
```

Ne modifiez jamais l'arbre ni la liste reçus : renvoyez-en un nouveau. `move_leaf` lève une erreur si le nœud n'est pas une
feuille, s'il est la racine, ou si la place est prise. Les fonctions pas encore écrites sont signalées SKIP.

## La règle (exacte)

```text
walk(node, x):                        # PARCOURS EN PRÉORDRE
  y = highest skyline value over [x, x + node.w)
  place node at (x, y)
  raise the skyline to y + node.h over [x, x + node.w)
  walk(node.left,  x + node.w)        # TOUT le sous-arbre gauche d'abord (à côté)
  walk(node.right, x)                 # puis l'enfant droit (à l'étage)
walk(root, 0)
```

- Un bloc tombe jusqu'à toucher le point le plus haut sous son emprise, donc `y` ne se tape jamais à la main.
- Pour un enfant droit, `y >= parent.y + parent.h` (il est *au moins* sur son parent). C'est strictement plus quand un voisin plus
  haut dépasse sous lui : voir **lift**.
- Le `y` d'un enfant gauche n'est pas celui de son parent : il tombe sur ce qu'il y a dessous, jusqu'à 0 : voir **floor**.
- L'ordre compte. Placer l'enfant droit d'abord change le placement de 1764 arbres sur 5040 : voir **order**.

### Opérations

```text
swap(tree, a, b)                  échange les deux noms ; qui est enfant gauche ou droit de qui ne change pas
rotate(modules, id)               w, h = h, w pour ce bloc ; l'arbre ne change pas
move_leaf(tree, leaf, p, side)    coupe la feuille de son parent, l'accroche à p.side (cette place doit être libre)
```

## Tableaux de référence

### Les arbres d'exemple (`examples/*.json`)

| Exemple | Arbre | Positions (x,y) | Boîte | Aire | Perdues | Valide | Pourquoi |
|---|---|---|---|---|---|---|---|
| golden | `A(B(C(E,-),-),D)` | A(0,0) B(3,0) C(5,0) D(0,2) E(7,0) | 9x3 | 27 | 4 | oui | D repose exactement sur A : `D.y = A.y + A.h = 2` |
| lift | `C(B(A(E,-),-),D)` | A(4,0) B(2,0) C(0,0) D(0,3) E(7,0) | 9x4 | 36 | 13 | oui | l'arbre de référence avec A et C échangés : B fait 3 de haut et dépasse sous D, donc D arrive en 3, pas en 2, et laisse un trou de 2 cases |
| order | `A(B(C(-,E),D),-)` | A(0,0) B(3,0) C(5,0) D(3,4) E(5,2) | 7x5 | 35 | 12 | oui | E est placé avant D et le soulève à 4. Enfant droit d'abord : boîte 7x8 |
| floor | `A(B(C(-,D(E,-)),-),-)`, A tourné | A(0,0) B(2,0) C(4,0) D(4,2) E(7,0) | 9x3 | 27 | 4 | oui | E est l'enfant gauche de D mais tombe en y = 0 : il n'y a rien dessous |
| swap, départ | `A(B(C(D,-),-),E)` | A(0,0) B(3,0) C(5,0) D(7,0) E(0,2) | 10x4 | 40 | 17 | oui | un mauvais arbre pour les mêmes cinq blocs |
| swap, après `swap(D,E)` | `A(B(C(E,-),-),D)` | l'arbre de référence | 9x3 | 27 | 4 | oui | un échange enlève 13 cases perdues |
| rotate, départ | `A(B(C(D(E,-),-),-),-)` | A(0,0) B(3,0) C(5,0) D(7,0) E(10,0) | 12x3 | 36 | 13 | **non** | chaque bloc est un enfant gauche : 3+2+2+3+2 = 12 > 10, E dépasse |
| rotate, après `rotate(D)` | même arbre, D vaut 1x3 | D(7,0) E(8,0) | 10x3 | 30 | 7 | oui | 3+2+2+1+2 = 10 : la rangée tient |
| move, départ | `A(B(C(D,-),-),E)` | comme « swap, départ » | 10x4 | 40 | 17 | oui | |
| move, après `move_leaf(D,B,right)` | `A(B(C,D),E)` | A(0,0) B(3,0) C(5,0) D(3,3) E(0,2) | 7x4 | 28 | 5 | oui | D est maintenant à l'étage de B |
| best | `A(D,C(E(B,-),-))` | A(0,0) B(4,1) C(0,2) D(3,0) E(2,2) | 6x4 | 24 | 1 | oui | B est soulevé sur D : seule la ligne d'horizon peut donner y = 1 à B |

L'exemple `lift` est l'arbre de référence avec A et C échangés (`derived_from` dans `lift.json`).

### Pas à pas : l'arbre de référence

| Étape | Bloc | Depuis | En (x,y) | Retenu par | Ligne d'horizon après | Boîte après |
|---|---|---|---|---|---|---|
| 1 | A | racine | (0,0) | sol | `[0,3)=2` | 3x2 |
| 2 | B | gauche de A | (3,0) | sol | `[0,3)=2 [3,5)=3` | 5x3 |
| 3 | C | gauche de B | (5,0) | sol | `[0,3)=2 [3,5)=3 [5,7)=2` | 7x3 |
| 4 | E | gauche de C | (7,0) | sol | `[0,3)=2 [3,5)=3 [5,9)=2` | 9x3 |
| 5 | D | droit de A | (0,2) | A | `[0,5)=3 [5,9)=2` | 9x3 |

`python3 examples/bstar_check.py --show` affiche ce parcours pour chaque exemple, et `--json` l'affiche en données
(arbres, placements, boîtes englobantes et ligne d'horizon après chaque placement).

### Les 5040 arbres sur A à E

| Grandeur | Valeur |
|---|---|
| arbres étiquetés (Catalan(5) x 5!) | 5040 |
| valides dans le contour 10x8 | 4680 |
| avec chevauchement | **0** (un arbre B* ne peut pas se chevaucher, par construction) |
| non valides car trop larges / trop hauts | 120 / 240 (chaque arbre non valide dépasse, rien d'autre) |
| plus petite aire de boîte englobante | **24** (6x4), atteinte par 8 arbres ; 23 est impossible (23 est premier et B fait 3 de haut) |
| arbres valides avec une boîte plus petite que 27 | 216 |
| le placement change si l'enfant droit est placé d'abord | **1764** |
| le placement change si y est lu chez le parent au lieu de la ligne d'horizon | 2714 |
| un enfant droit soulevé au-dessus du bord supérieur de son parent | 360 |
| un enfant gauche soulevé au-dessus du y de son parent | 254 |

Les 8 arbres d'aire 24 (`examples/best.json`) :
`A(D,C(E(B,-),-))`, `A(D,E(C(B,-),-))`, `B(C(E,-),D(A,-))`, `B(E(C,-),D(A,-))`, `C(E(B,-),A(D,-))`,
`D(A,B(C(E,-),-))`, `D(A,B(E(C,-),-))`, `E(C(B,-),A(D,-))`. Chacun perd 1 case.

### Une opération à la fois

| Arbre | Meilleure aire après un échange (sur 10) | Meilleure après une rotation (sur 5) | Meilleure après un déplacement de feuille (sur 8) |
|---|---|---|---|
| référence (27) | 27 (4 échanges gardent 27) | 27 (2 gardent 27) | 27 (1 garde 27) |
| départ swap (40) | **27**, seulement `swap(D,E)` | 32 | 28 (deux déplacements : D vers B.right, D vers E.left) |

Aucune opération seule n'améliore donc l'arbre de référence, et depuis le départ swap, l'échange de D et E est le seul chemin vers 27.
Pour la chaîne où tout est enfant gauche, 12 des 32 ensembles de blocs tournés sont valides ; **D est le seul bloc** dont la rotation seule la rend valide.

## À essayer

```bash
python3 examples/bstar_check.py                              # reference: all PASS
python3 examples/bstar_check.py --show                       # every pack, step by step
python3 examples/bstar_check.py --vs-node                    # same packs as the browser lab's JS, all 5040 trees
python3 examples/bstar_check.py --impl my_bstar.py           # check YOUR functions
python3 examples/bstar_check.py --impl examples/wrong/right_first.py   # a deliberately wrong one
python3 examples/bstar_check.py --impl examples/wrong/no_contour.py    # another one
python3 examples/bstar_check.py --json > bstar.json          # trees, packs, skylines as data
```

`examples/wrong/` contient deux programmes de placement avec exactement un bogue chacun : l'enfant droit placé **avant** le sous-arbre gauche, et
**pas de ligne d'horizon** (y lu chez le parent). Les deux placent correctement l'arbre de référence, donc le seul test de l'arbre de référence ne peut pas les
attraper. Lancez-les et lisez quelles lignes sont FAIL. La ligne « all 5040 trees » attrape les deux.

## Questions de départ (demandez « pourquoi »)

1. Implémentez `pack_bstar` et affichez le tableau pas à pas de l'arbre de référence. Quel bloc retient D, et pourquoi `D.y` vaut-il 2 ?
2. Dans `lift`, D arrive en y = 3, pas en 2. Quel bloc le soulève ? Combien de cases contient le trou au-dessus de C ?
3. Dans `order`, pourquoi D finit-il en y = 4 ? Placez D avant le sous-arbre gauche à la main et dites quelle boîte vous obtenez.
4. Dans `floor`, E est l'enfant gauche de D mais se trouve en y = 0. Expliquez en une phrase pourquoi « enfant gauche » ne veut pas dire « même rangée ».
5. Depuis le départ swap, essayez les dix échanges et notez chaque aire. Pourquoi un seul atteint-il 27 ?
6. Dans la chaîne, tournez chacun des cinq blocs à tour de rôle. Quelle rotation seule la rend valide, et pourquoi les quatre autres n'aident-elles pas ?
7. Lancez `--impl examples/wrong/no_contour.py`. Quels exemples réussit-il, et qu'ont-ils en commun ?

## Livrables attendus

- Un `my_bstar.py` qui n'affiche aucun FAIL face à `bstar_check.py`.
- Le tableau pas à pas d'un exemple, avec la ligne d'horizon après chaque placement.
- Deux phrases : l'une sur la raison pour laquelle l'ordre de parcours compte, l'autre sur la raison pour laquelle la ligne d'horizon compte (utilisez `order` et `lift`).

## Pour aller plus loin

- Battez l'arbre de référence : trouvez un arbre valide avec une boîte plus petite que 27 (il en existe 216) sans regarder `best.json`.
- Atteignez 24 sans tourner aucun bloc. Combien des 5040 arbres y arrivent ? Quel bloc doit être soulevé sur un autre ?
- Écrivez `move_leaf` pour qu'il accepte aussi de déplacer une feuille de l'autre côté de son propre parent, et listez les 8 déplacements de feuille du départ swap avec leurs aires.
