# Backlog

Synchronise la section `## Backlog` d'un document Markdown avec les issues ouvertes du dépôt déclaré par `git_repo` dans son frontmatter. GitHub, GitLab.com et les instances GitLab auto-hébergées authentifiées sont pris en charge. Les milestones sont optionnellement filtrées, puis regroupées par échéance lorsque le projet en possède.

## Context required

Formes acceptées après le sélecteur d'action `backlog` :

```text
<fichier.md>
<fichier.md> --milestone <titre>
<fichier.md> --ml <titre>
```

- Exiger exactement un argument positionnel désignant un fichier `.md` existant et lisible.
- `--milestone` et `--ml` sont des synonymes stricts. Accepter au plus l'un des deux, une seule fois, avec une valeur non vide. Retirer seulement les espaces périphériques de cette valeur ; conserver sa casse et ses espaces internes pour la correspondance exacte.
- Refuser avant tout appel réseau : fichier absent ou illisible, argument positionnel surnuméraire, filtre dupliqué, filtre sans valeur ou option inconnue. Terminer par `File unchanged.`
- Le premier bloc du fichier doit être un frontmatter délimité par `---` et contenir une clé scalaire `git_repo:` non vide. S'il est absent, non fermé, ou si la clé manque, arrêter sans écrire.

Ne jamais construire ni évaluer une commande shell concaténée à partir des arguments. Les valeurs distantes, chemins, hôtes, identifiants, pages et filtres sont toujours transmis comme arguments séparés aux capacités natives de l'hôte.

## Prompt

Exécute ce workflow sans modifier le dépôt distant.

### Step 1 — Read and validate

1. Parser les arguments selon `Context required`, puis lire le fichier en entier. Conserver exactement son encodage UTF-8, son éventuel BOM et son style de fins de ligne.
2. Lire uniquement le premier frontmatter, entre la première ligne `---` et sa fermeture `---`.
3. Extraire la valeur scalaire de `git_repo:` ; retirer seulement les guillemets YAML englobants, les espaces périphériques, un suffixe `.git` et un `/` final.
4. Conserver le contenu original en mémoire. Aucune écriture ne doit avoir lieu avant la réussite de toutes les pages d'issues, de toutes les pages de milestones et de leur validation.

### Step 2 — Resolve provider and repository

Accepter les URL HTTPS, SSH et la forme SCP Git habituelle (`git@host:groupe/projet.git`).

Séparer l'hôte de l'identifiant de projet avant toute résolution. L'hôte doit être un nom DNS valide : labels alphanumériques ou tirets séparés par des points, comparés en minuscules ; port, identifiants d'authentification ou autre caractère le rendent invalide. L'identifiant doit compter au moins deux segments non vides. Une valeur invalide arrête l'action sans écrire.

- Hôte `github.com` → provider `github`, outil `gh`, identifiant `owner/repo`.
- Hôte `gitlab.com` ou sous-domaine `*.gitlab.io` → provider `gitlab`, outil `glab`, identifiant `group[/subgroup]/repo`.
- Tout autre hôte → instance GitLab auto-hébergée seulement une fois prouvée : exécuter `glab auth status --hostname <hôte>`. Code 0 → provider `gitlab`. Code non nul, ou `glab` indisponible → arrêter sans écrire en nommant l'hôte non prouvé et la valeur `git_repo` refusée.

Un hôte inconnu n'est jamais présumé GitLab sur la forme de son URL. La preuve d'authentification reconnaît l'hôte mais ne garantit pas l'accès au projet.

Vérifier que l'outil requis existe avant tout appel réseau. S'il manque, arrêter sans écrire avec l'installation attendue (`gh` ou `glab`).

### Step 3 — Fetch and validate open issues and milestones

Collecter les deux jeux de données avant toute construction de document.

#### GitHub

Les endpoints sont construits uniquement depuis les segments `owner/repo` validés au Step 2 et transmis comme un argument séparé.

```text
gh api --paginate repos/<owner>/<repo>/issues?state=open&per_page=100
gh api --paginate repos/<owner>/<repo>/milestones?state=all&per_page=100
```

- Parser chaque page JSON séparément ; chacune doit être une liste.
- Issues : exclure tout objet portant la clé `pull_request`, puis exiger `number` entier positif et globalement unique, `title` chaîne non vide, `state` égal à `open` sans tenir compte de la casse. `milestone` vaut `null` ou un objet portant un `id` valide et un `title` non vide.
- Catalogue : exiger `id` entier positif et globalement unique entre toutes les pages, `title` non vide, `state` dans `open|closed`, et `due_on` nul ou timestamp ISO valide. Normaliser un `due_on` valide vers sa date civile `AAAA-MM-JJ`.

#### GitLab

Préfixer l'identifiant par l'hôte résolu, y compris `gitlab.com`, afin de ne jamais retomber sur l'hôte par défaut local.

Pour les issues, commencer à la page 1 et incrémenter jusqu'à la première page vide :

```text
glab issue list --repo <hôte>/<group/project> --opened --page <N> --per-page 100 --output json
```

Pour les milestones du projet et de ses groupes ancêtres assignables, appliquer la même boucle :

```text
glab milestone list --repo <hôte>/<group/project> --include-ancestors --page <N> --per-page 100 --output json
```

- Chaque page doit être une liste JSON ; un échec avant la première page vide invalide toute la collecte.
- Issues : exiger `iid` entier positif et globalement unique, `title` non vide, `state` dans `opened|open`. `milestone` vaut `null` ou un objet portant un `id` valide et un `title` non vide.
- Catalogue : exiger `id` entier positif et globalement unique, `title` non vide, `state` dans `active|closed`, et `due_date` nul ou date ISO `AAAA-MM-JJ` valide.

#### Normalisation commune

1. Le **titre brut** d'une milestone est son titre après retrait des seuls espaces périphériques. Il porte l'identité métier, le filtre et le tri.
2. Rattacher toute issue ayant une milestone à l'entrée du catalogue de même identifiant provider. Une référence absente du catalogue invalide la réponse.
3. Si un filtre est fourni, chercher le titre brut avec égalité exacte et sensible à la casse :
   - zéro correspondance → succès avec zéro issue retenue ;
   - une correspondance → conserver seulement les issues portant son identifiant ;
   - plusieurs correspondances → ambiguïté, arrêt sans écrire.
4. Sans filtre, conserver toutes les issues ouvertes validées.
5. Toute page invalide, tout identifiant d'issue ou de milestone répété, tout rattachement impossible, toute authentification ou commande en échec laisse le fichier strictement inchangé. Afficher provider, dépôt et cause utile.

### Step 4 — Build the backlog

Construire le lien canonique de chaque issue :

- GitHub : `https://github.com/<owner/repo>/issues/<number>`
- GitLab : `https://<hôte>/<group/project>/-/issues/<iid>`

Une ligne d'issue garde la forme historique :

```markdown
- [#123](https://host/path/issues/123) — Titre de l'issue
```

Réduire les espaces et retours du titre d'issue à un espace. Ne jamais répéter l'URL, suffixer l'état, ni répéter la milestone sur chaque ligne.

Si aucune issue n'est retenue, le bloc est la ligne unique :

```markdown
_Aucune issue ouverte._
```

Sinon :

- **Catalogue vide** → produire les lignes plates historiques dans l'ordre renvoyé par le provider, sans aucune donnée milestone.
- **Catalogue non vide** → grouper par identifiant provider de milestone. Garder l'ordre provider des issues dans chaque groupe. Les groupes datés sont triés par échéance croissante, puis titre brut, puis identifiant ; viennent ensuite les groupes sans échéance triés par titre brut puis identifiant ; le groupe non assigné vient en dernier.

Construire un **titre de rendu** distinct du titre brut : ramener retours et espaces internes à un espace ; échapper d'abord `\`, puis accents graves, crochets, astérisques, underscores et chevrons pour que la valeur distante reste du texte Markdown inline sur une seule ligne.

Chaque groupe non vide est contigu, sans ligne vide entre son sous-titre et sa première issue :

```markdown
### Milestone: <titre rendu> — échéance <AAAA-MM-JJ>
- [#123](<url canonique>) — <titre>

### Milestone: <titre rendu> — sans échéance
- [#456](<url canonique>) — <titre>

### Sans milestone
- [#789](<url canonique>) — <titre>
```

Omettre tout groupe vide. Ce Step produit le **bloc** seul ; le titre `## Backlog` et son placement appartiennent au Step 5.

### Step 5 — Replace or insert the section

**Ligne canonique.** Une ligne d'issue générée suit `- [#<numéro>](<url>) — <titre>`, avec un suffixe d'état parenthésé facultatif toléré seulement à la reconnaissance. L'URL est le lien canonique du dépôt résolu et son numéro terminal est identique au numéro affiché. Une ligne pointant vers un autre dépôt est manuelle.

**Bloc généré.** Dans une section `## Backlog`, titre exclu, reconnaître la première des trois formes complètes suivantes :

1. bloc plat historique : une ou plusieurs lignes canoniques, avec une ligne vide interne seulement lorsqu'elle est encadrée par deux lignes canoniques ;
2. bloc groupé : un ou plusieurs groupes, chacun formé d'un sous-titre conforme immédiatement suivi d'au moins une ligne canonique, avec d'autres lignes canoniques contiguës et exactement une ligne vide entre deux groupes ;
3. la ligne `_Aucune issue ouverte._`.

Un sous-titre conforme est exactement l'une de ces formes :

- `### Milestone: <texte non vide> — échéance <AAAA-MM-JJ>` ;
- `### Milestone: <texte non vide> — sans échéance` ;
- `### Sans milestone`.

Un sous-titre réservé isolé, suivi de prose ou non suivi d'une ligne canonique n'est jamais généré. Toute autre ligne, dont `### Notes historiques`, arrête la reconnaissance. Les lignes vides de queue n'appartiennent pas au bloc.

Limites assumées du motif : une ligne manuelle identique à une ligne canonique pour ce dépôt reste indiscernable ; un sous-titre manuel au format réservé suivi d'une ligne canonique est indiscernable d'un groupe généré ; `_Aucune issue ouverte._` reste le seul motif non ancré au dépôt.

**Placement.**

- Une unique section `## Backlog` avec bloc généré → remplacer cette plage seule.
- Une unique section sans bloc généré → insérer le bloc en tête, avant le contenu manuel.
- Plusieurs sections `## Backlog` → arrêter sans écrire.
- Section absente avec un titre `# ...` ouvrant le corps → insérer `## Backlog` après le titre et son introduction, avant le premier `##`.
- Section absente sans titre `#` → insérer immédiatement après le frontmatter.

Imposer exactement une ligne vide entre `## Backlog` et le bloc, et entre le bloc et le premier contenu manuel suivant. Ne jamais accumuler de lignes vides. Préserver byte-for-byte le frontmatter, le contenu manuel de la section et tout contenu hors section, hormis ces sauts de ligne de bord. Effectuer une seule écriture atomique après validation du document final.

### Step 6 — Verify and report

Relire le fichier et vérifier :

- frontmatter identique ; une seule section `## Backlog` ; une ligne par issue retenue, sans doublon, URL redondante ni suffixe d'état écrit ;
- filtre respecté sans issue d'une autre milestone ; ordre des groupes et des issues conforme ; aucun sous-titre milestone lorsque le catalogue est vide ;
- ancien bloc plat ou groupé entièrement remplacé, sans sous-titre orphelin ; contenu manuel et autres sections inchangés.

`Section:` vaut `replaced` lorsqu'un bloc généré préexistait, `inserted` lorsqu'une section a été créée ou qu'un bloc a été ajouté à une section manuelle.

Rapport final :

```text
Backlog updated: <fichier>
Repository: <provider> <dépôt>
Milestone: <titre brut>        # ligne omise sans filtre
Open issues: <N>
Section: replaced|inserted
```

Sur GitLab, `<dépôt>` inclut toujours l'hôte. En cas d'échec, ne jamais afficher ce rapport et confirmer explicitement `File unchanged.`
