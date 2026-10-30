---
marp: true
title: Plan de masse par arbre B*
paginate: true
---

# Plan de masse par arbre B*

Cinq blocs, un cadre, et un arbre qui dit où va chaque bloc

---

## Cinq blocs
- Une puce est faite de grandes pièces rectangulaires, appelées blocs
- Le nôtre a cinq blocs, nommés de A à E
- Ils sont sur du papier quadrillé : on peut compter chaque largeur et chaque hauteur
![snippet](assets/blocks-1.png)

---

## Le contour
- Un plan de masse dit où se trouve chaque bloc sur la puce
- Chaque bloc doit rester dans un cadre appelé le contour
- Notre contour fait dix cases de large et huit cases de haut
- Plus les blocs sont serrés, plus la puce peut être petite
![snippet](assets/blocks.png)

---

## Un arbre comme recette
- Noter chaque position est long, alors nous utilisons une recette : un arbre B-étoile
- Chaque bloc est un nœud de l'arbre
- Le nœud du haut, A, s'appelle la racine
- Chaque nœud peut avoir deux enfants : un enfant gauche et un enfant droit
![snippet](assets/tree-golden.png)

---

## La racine va dans le coin
- La racine va dans le coin inférieur gauche du contour
- À partir de ce coin, x compte les cases vers la droite, et y compte les cases vers le haut
![snippet](assets/rule-1.png)

---

## À gauche, à côté ; à droite, à l'étage
- Un enfant gauche va à côté : collé contre le côté droit de son parent
- Un enfant droit va à l'étage : sur son parent, avec le même bord gauche
- Les noms semblent inversés : gauche veut dire à côté, droite veut dire à l'étage
- Dans l'arbre, un trait plein veut dire à côté, un pointillé veut dire à l'étage
![snippet](assets/rule.png)

---

## Où va B ?
- A fait trois cases de large et deux cases de haut
- B est l'enfant gauche de A
- Faites une pause et devinez : où va le bord gauche de B ?
![snippet](assets/pause-b.png)

---

## B va à côté, en x = 3
![B va à côté, en x = 3](assets/steps/01-root.png)

---

## Le parcours : A, B, C, E, puis D
![Le parcours : A, B, C, E, puis D](assets/steps/02-left-chain.png)

---

## C et E vont à côté
![C et E vont à côté](assets/steps/03-right-d.png)

---

## D monte à l'étage, sur A
![D monte à l'étage, sur A](assets/steps/04-legal.png)

---

## Cinq blocs placés
![Cinq blocs placés](assets/steps/05-takeaway.png)

---

## Échanger A et C
- Non : D arrive une case plus haut
- Voici l'arbre où A et C sont échangés : C est la racine, et A prend l'ancienne place de C
- C, B, A et E vont toujours à côté, l'un après l'autre
![snippet](assets/lift-1.png)

---

## La ligne d'horizon
- Imaginez maintenant les blocs comme une ville, vue de loin
- Le bord supérieur de tout ce qui est déjà placé s'appelle la ligne d'horizon
- Un nouveau bloc tombe du ciel, comme au Tetris, jusqu'à toucher la ligne d'horizon
![snippet](assets/lift-2.png)

---

## D se pose sur B
- D fait trois de large, donc il passe au-dessus de C et d'une partie de B
- B fait trois de haut, donc il arrête D en y égal trois
- Cela laisse un trou de deux cases vides au-dessus de C
![snippet](assets/lift.png)

---

## La boîte englobante
- Alors, quel plan de masse est le meilleur ?
- Pour comparer, on dessine la boîte englobante, le plus petit rectangle autour des blocs
- Pour le premier arbre, elle fait neuf de large et trois de haut : vingt-sept cases
![snippet](assets/golden-box-1.png)

---

## Les cases perdues
- Les cinq blocs couvrent vingt-trois cases
- Les quatre autres cases de la boîte sont vides : ce sont des cases perdues
- Moins il y a de cases perdues, plus le plan de masse est serré
![snippet](assets/golden-box.png)

---

## Un échange, un score moins bon
- L'arbre échangé a une boîte de neuf sur quatre : trente-six cases, treize perdues
- Un seul échange de deux noms a donc changé l'image et le score
- Vingt-sept est devenu trente-six : le premier arbre est meilleur
![snippet](assets/lift-box.png)

---

## Une longue rangée
- Prenons maintenant un arbre où chaque enfant est un enfant gauche
- Faites une pause et devinez : cette longue rangée tient-elle dans le contour ?
![snippet](assets/chain-1.png)

---

## Chaque bloc à côté
- Non, elle ne tient pas
- Chaque bloc va à côté : trois, deux, deux et trois font dix
- Le contour est déjà plein, et E attend encore
![snippet](assets/chain-2.png)

---

## Un bloc qui dépasse
- E arrive en x égal dix, donc la rangée fait douze cases de large
- E dépasse du contour de deux cases
- Un plan de masse est valide seulement si chaque bloc est dans le contour
- Cette rangée n'est donc pas valide
![snippet](assets/chain.png)

---

## Jamais de chevauchement
- Remarquez que les blocs ne se chevauchent jamais
- Chaque bloc tombe sur la ligne d'horizon, donc il ne peut jamais atterrir dans un autre
- Avec un arbre B-étoile, dépasser est la seule façon d'échouer
![snippet](assets/chain-check.png)

---

## Tourner un bloc
- On peut tourner un bloc sur le côté : sa largeur et sa hauteur s'échangent
- Tournez D, et il fait une case de large et trois de haut
- La rangée fait maintenant dix de large : elle tient pile, et elle est de nouveau valide
![snippet](assets/turn.png)

---

## Trois petits changements
- Tourner est l'un des trois petits changements
- On peut aussi échanger deux noms dans l'arbre, comme avec A et C
- Ou déplacer une feuille, un bloc sans enfant, vers une place libre de l'arbre
- Chaque changement donne un nouveau plan de masse, avec un nouveau score
- Faites une pause et devinez : un arbre peut-il battre vingt-sept ?
- Et quelle est la plus petite boîte ?

---

## Le plan de masse le plus serré
- Oui : beaucoup d'arbres battent vingt-sept
- Les meilleurs n'ont besoin que de vingt-quatre cases
- Voici l'un des meilleurs arbres
- Son parcours place A, D, C et E, et B vient en dernier
![snippet](assets/best-1.png)

---

## B est soulevé par la ligne d'horizon
- Sous B, la ligne d'horizon est le haut de D, donc B arrive en y égal un
- Il comble le trou, et la boîte fait six de large et quatre de haut : vingt-quatre cases
- Une seule case est perdue
![snippet](assets/best.png)

---

## Pourquoi pas vingt-trois ?
- Une boîte de vingt-trois cases, sans case perdue, pourrait-elle contenir les cinq blocs ?
- Vingt-trois cases ne forment qu'un rectangle épais d'une seule case
- Le bloc B est trop épais pour cela : vingt-quatre est donc le mieux possible

---

## Parcours lab dans le navigateur
![Départ du lab dans le navigateur](assets/lab-starter.png)

---

## Parcours implémentation
![Session de terminal réelle](assets/real-shell.png)

---

## Parcours implémentation — try these

```
# afficher toutes les bonnes réponses
python3 examples/bstar_check.py --show

# vérifier vos propres fonctions
python3 examples/bstar_check.py --impl my_bstar.py
```

---

## À retenir
- Enfant gauche : à côté
- Enfant droit : à l'étage, avec le même bord gauche
- Parcourez l'arbre : le nœud, tout son côté gauche, puis son enfant droit
- Chaque bloc tombe jusqu'à toucher la ligne d'horizon
- On note un plan de masse avec sa boîte englobante, et on compte les cases perdues
- Un arbre ne chevauche jamais, mais il peut dépasser : vérifiez le contour

---

## À vous de jouer
- Choisissez un parcours : le lab dans le navigateur, Python, ou les deux
- Cochez chaque case de la liste de contrôle, puis faites le court quiz
- La suite, c'est la paire de séquences : deux listes de noms au lieu d'un arbre
- Faites une pause et devinez : deux listes décrivent-elles notre plan à vingt-quatre ?
- Oui : deux listes suffisent
- C'est la paire de séquences, dans le prochain lab

