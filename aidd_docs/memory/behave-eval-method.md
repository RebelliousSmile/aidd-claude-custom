# Méthode d'évaluation `behave` — ce que la refonte de `control` a appris

Établi le 2026-07-30, sur les huit suites de `overcode:control` (149 scénarios, deux fixtures).

## Un « 0 FAIL » ne dit rien de la couverture

Après une vague de correctifs, compter les **PASS→N/A** autant que les FAIL. Le rejeu de confirmation a rendu 0 FAIL et **six lignes passées de PASS à N/A**, toutes rendues injoignables par deux correctifs justes de la skill : une règle peut cesser d'être atteignable par toute fixture sans qu'aucune ligne rougisse.

Le Δ à rapporter est donc à trois colonnes — PASS, FAIL, **et le mouvement de N/A** — jamais le seul tally. Une ligne devenue injoignable est une dette de suite (fixture ou re-visée), pas un signal de corriger la règle qui vient de la fermer.

## Ne pas corriger la cible pendant qu'un run est en vol

Les juges lisent les fichiers de la skill. Éditer pendant qu'ils tournent fait des entrées de registre le portrait de **deux états différents** de la cible, et le run cesse d'être un instantané. Les correctifs partent quand tous les verdicts sont rentrés.

## Le registre dans le fichier de suite empêche le jugement à froid — ouvert

L'instruction de juger sans lire les verdicts antérieurs est **structurellement inapplicable** tant que le Results log vit dans le fichier de suite que le juge doit lire : **7 juges sur 8** ont vu les verdicts précédents, seul celui qui s'est arrêté avant la section a tenu froid. C'est un défaut de forme du harnais, pas des suites — il se corrige en sortant le registre du fichier de suite, pas en renforçant l'instruction.

## Les dénominateurs ne sont pas commensurables

Une suite peut compter des **cellules** (une situation à deux fixtures en vaut deux) là où les autres comptent des lignes. Ne jamais additionner les tallies en un total unique : chaque suite porte le sien, et une somme masque la correction de dénominateur.
