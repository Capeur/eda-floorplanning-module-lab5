# Plan de masse par arbre B*

**Module id:** module02-03-bstar-tree
**Lab:** bstar-tree
**Tracks:** A (implémentation) · B (lab dans le navigateur)

## Slide 1 — Plan de masse par arbre B*

Cinq blocs, un cadre, et un arbre qui dit où va chaque bloc. Pouvez-vous dessiner l'image à partir de l'arbre seul ? À la fin, oui, et vous trouverez même l'image la plus serrée de toutes.

## Slide 2 — Cinq blocs

![Les cinq blocs A à E sur du papier quadrillé](assets/blocks-1.png)

Une puce est faite de grandes pièces rectangulaires, appelées blocs. Le nôtre a cinq blocs, nommés de A à E. Ils sont sur du papier quadrillé : on peut compter chaque largeur et chaque hauteur.

## Slide 3 — Le contour

![Les cinq blocs à côté du contour vide, dix de large et huit de haut](assets/blocks.png)

Un plan de masse dit où se trouve chaque bloc sur la puce. Chaque bloc doit rester dans un cadre appelé le contour. Notre contour fait dix cases de large et huit cases de haut. Plus les blocs sont serrés, plus la puce peut être petite.

## Slide 4 — Un arbre comme recette

![L'arbre B* : A est la racine, avec un enfant gauche et un enfant droit](assets/tree-golden.png)

Noter chaque position est long, alors nous utilisons une recette : un arbre B-étoile. Chaque bloc est un nœud de l'arbre. Le nœud du haut, A, s'appelle la racine. Chaque nœud peut avoir deux enfants : un enfant gauche et un enfant droit.

## Slide 5 — La racine va dans le coin

![A placé dans le coin inférieur gauche ; x compte vers la droite, y compte vers le haut](assets/rule-1.png)

La racine va dans le coin inférieur gauche du contour. À partir de ce coin, x compte les cases vers la droite, et y compte les cases vers le haut.

## Slide 6 — À gauche, à côté ; à droite, à l'étage

![Un enfant gauche va à côté, un enfant droit va à l'étage](assets/rule.png)

Un enfant gauche va à côté : collé contre le côté droit de son parent. Un enfant droit va à l'étage : sur son parent, avec le même bord gauche. Les noms semblent inversés : gauche veut dire à côté, droite veut dire à l'étage. Dans l'arbre, un trait plein veut dire à côté, un pointillé veut dire à l'étage.

## Slide 7 — Où va B ?

![A fait trois de large et deux de haut ; B est l'enfant gauche de A](assets/pause-b.png)

A fait trois cases de large et deux cases de haut. B est l'enfant gauche de A. Faites une pause et devinez : où va le bord gauche de B ?

<!-- algorithm-walkthrough -->

## Slide 8 — B va à côté, en x = 3

![B va à côté, en x = 3](assets/steps/01-root.png)

B va à côté, en x égal trois : A commence à zéro, et A fait trois de large. Rien n'est sous B, donc il repose sur le sol, en y égal zéro.

## Slide 9 — Le parcours : A, B, C, E, puis D

![Le parcours : A, B, C, E, puis D](assets/steps/02-left-chain.png)

On place les blocs un par un, dans un ordre de parcours fixe. On place un nœud, puis tout son côté gauche, et seulement ensuite son enfant droit. Le parcours donne donc A, B, C et E, et D vient en dernier.

## Slide 10 — C et E vont à côté

![C et E vont à côté](assets/steps/03-right-d.png)

C est l'enfant gauche de B, donc il va à côté de B, en x égal cinq. E est l'enfant gauche de C, donc il arrive à côté de C, en x égal sept. Les largeurs s'additionnent : trois, plus deux, plus deux, font sept.

## Slide 11 — D monte à l'étage, sur A

![D monte à l'étage, sur A](assets/steps/04-legal.png)

Le côté gauche est fini, donc le parcours revient à D, l'enfant droit de A. D monte à l'étage, donc il commence en x égal zéro, comme A. Il se pose sur A, en y égal deux.

## Slide 12 — Cinq blocs placés

![Cinq blocs placés](assets/steps/05-takeaway.png)

Les cinq blocs sont placés, et chacun est dans le contour. Faites une pause et devinez : si on échange A et C dans l'arbre, D arrive-t-il encore en y égal deux ?

<!-- /algorithm-walkthrough -->

## Slide 13 — Échanger A et C

![L'arbre avec A et C échangés : C, B, A et E placés en rangée](assets/lift-1.png)

Non : D arrive une case plus haut. Voici l'arbre où A et C sont échangés : C est la racine, et A prend l'ancienne place de C. C, B, A et E vont toujours à côté, l'un après l'autre.

## Slide 14 — La ligne d'horizon

![La ligne d'horizon de C, B, A et E, avec D qui tombe d'en haut](assets/lift-2.png)

Imaginez maintenant les blocs comme une ville, vue de loin. Le bord supérieur de tout ce qui est déjà placé s'appelle la ligne d'horizon. Un nouveau bloc tombe du ciel, comme au Tetris, jusqu'à toucher la ligne d'horizon.

## Slide 15 — D se pose sur B

![D arrêté par B en y = 3, avec un trou au-dessus de C](assets/lift.png)

D fait trois de large, donc il passe au-dessus de C et d'une partie de B. B fait trois de haut, donc il arrête D en y égal trois. Cela laisse un trou de deux cases vides au-dessus de C.

## Slide 16 — La boîte englobante

![La boîte englobante du premier arbre : neuf sur trois, vingt-sept cases](assets/golden-box-1.png)

Alors, quel plan de masse est le meilleur ? Pour comparer, on dessine la boîte englobante, le plus petit rectangle autour des blocs. Pour le premier arbre, elle fait neuf de large et trois de haut : vingt-sept cases.

## Slide 17 — Les cases perdues

![Vingt-trois cases de blocs, quatre cases perdues](assets/golden-box.png)

Les cinq blocs couvrent vingt-trois cases. Les quatre autres cases de la boîte sont vides : ce sont des cases perdues. Moins il y a de cases perdues, plus le plan de masse est serré.

## Slide 18 — Un échange, un score moins bon

![L'arbre échangé : boîte neuf sur quatre, trente-six cases, treize perdues](assets/lift-box.png)

L'arbre échangé a une boîte de neuf sur quatre : trente-six cases, treize perdues. Un seul échange de deux noms a donc changé l'image et le score. Vingt-sept est devenu trente-six : le premier arbre est meilleur.

## Slide 19 — Une longue rangée

![Un arbre où chaque enfant est un enfant gauche, à côté du contour vide](assets/chain-1.png)

Prenons maintenant un arbre où chaque enfant est un enfant gauche. Faites une pause et devinez : cette longue rangée tient-elle dans le contour ?

## Slide 20 — Chaque bloc à côté

![A, B, C et D en rangée : trois, deux, deux et trois font dix](assets/chain-2.png)

Non, elle ne tient pas. Chaque bloc va à côté : trois, deux, deux et trois font dix. Le contour est déjà plein, et E attend encore.

## Slide 21 — Un bloc qui dépasse

![E dépasse du contour : la rangée fait douze de large](assets/chain.png)

E arrive en x égal dix, donc la rangée fait douze cases de large. E dépasse du contour de deux cases. Un plan de masse est valide seulement si chaque bloc est dans le contour. Cette rangée n'est donc pas valide.

## Slide 22 — Jamais de chevauchement

![Aucun chevauchement, mais E dépasse : la seule façon d'échouer pour un arbre B*](assets/chain-check.png)

Remarquez que les blocs ne se chevauchent jamais. Chaque bloc tombe sur la ligne d'horizon, donc il ne peut jamais atterrir dans un autre. Avec un arbre B-étoile, dépasser est la seule façon d'échouer.

## Slide 23 — Tourner un bloc

![D tourné sur le côté : une case de large et trois de haut, et la rangée tient](assets/turn.png)

On peut tourner un bloc sur le côté : sa largeur et sa hauteur s'échangent. Tournez D, et il fait une case de large et trois de haut. La rangée fait maintenant dix de large : elle tient pile, et elle est de nouveau valide.

## Slide 24 — Trois petits changements

Tourner est l'un des trois petits changements. On peut aussi échanger deux noms dans l'arbre, comme avec A et C. Ou déplacer une feuille, un bloc sans enfant, vers une place libre de l'arbre. Chaque changement donne un nouveau plan de masse, avec un nouveau score. Faites une pause et devinez : un arbre peut-il battre vingt-sept ? Et quelle est la plus petite boîte ?

## Slide 25 — Le plan de masse le plus serré

![L'un des meilleurs arbres, avant son dernier bloc, B](assets/best-1.png)

Oui : beaucoup d'arbres battent vingt-sept. Les meilleurs n'ont besoin que de vingt-quatre cases. Voici l'un des meilleurs arbres. Son parcours place A, D, C et E, et B vient en dernier.

## Slide 26 — B est soulevé par la ligne d'horizon

![B se pose sur D en y = 1 ; la boîte fait six sur quatre, vingt-quatre cases](assets/best.png)

Sous B, la ligne d'horizon est le haut de D, donc B arrive en y égal un. Il comble le trou, et la boîte fait six de large et quatre de haut : vingt-quatre cases. Une seule case est perdue.

## Slide 27 — Pourquoi pas vingt-trois ?

Une boîte de vingt-trois cases, sans case perdue, pourrait-elle contenir les cinq blocs ? Vingt-trois cases ne forment qu'un rectangle épais d'une seule case. Le bloc B est trop épais pour cela : vingt-quatre est donc le mieux possible.

## Slide 28 — Parcours lab dans le navigateur

![Départ du lab dans le navigateur](assets/lab-starter.png)

Construisez maintenant des plans de masse vous-même. Dans le lab du navigateur, vous modifiez l'arbre et vous regardez chaque bloc tomber sur la ligne d'horizon. Les défis vérifient l'arbre que vous avez construit. Soulevez D plus haut, faites tenir la longue rangée, et atteignez vingt-quatre.

## Slide 29 — Parcours implémentation

![Session de terminal réelle](assets/real-shell.png)

Si vous aimez programmer, écrivez la fonction de placement en Python. Le fichier d'exemples donne les règles exactes. Lancez une fois le vérificateur pour afficher toutes les bonnes réponses, puis lancez-le sur votre fichier. Il compare votre placement au bon sur les cinq mille quarante arbres.

```bash
# afficher toutes les bonnes réponses
python3 examples/bstar_check.py --show

# vérifier vos propres fonctions
python3 examples/bstar_check.py --impl my_bstar.py
```

## Slide 30 — À retenir

Enfant gauche : à côté. Enfant droit : à l'étage, avec le même bord gauche. Parcourez l'arbre : le nœud, tout son côté gauche, puis son enfant droit. Chaque bloc tombe jusqu'à toucher la ligne d'horizon. On note un plan de masse avec sa boîte englobante, et on compte les cases perdues. Un arbre ne chevauche jamais, mais il peut dépasser : vérifiez le contour.

## Slide 31 — À vous de jouer

Choisissez un parcours : le lab dans le navigateur, Python, ou les deux. Cochez chaque case de la liste de contrôle, puis faites le court quiz. La suite, c'est la paire de séquences : deux listes de noms au lieu d'un arbre. Faites une pause et devinez : deux listes décrivent-elles notre plan à vingt-quatre ? Oui : deux listes suffisent. C'est la paire de séquences, dans le prochain lab.
