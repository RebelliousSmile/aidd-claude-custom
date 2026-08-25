# Backlog

Synchronise la section `## Backlog` d'un document Markdown avec les issues ouvertes du dépôt GitHub ou GitLab déclaré par `git_repo` dans son frontmatter.

## Context required

- `$ARGUMENTS` doit désigner exactement un fichier `.md` existant. S'il manque, n'est pas un fichier Markdown ou est illisible, arrêter sans écrire et demander/citer le chemin fautif.
- Le premier bloc du fichier doit être un frontmatter délimité par `---` et contenir une clé scalaire `git_repo:` non vide. Si le bloc est absent, non fermé, ou si la clé manque, arrêter sans écrire et signaler l'erreur.

## Prompt

Exécute ce workflow sans modifier le dépôt distant.

### Step 1 — Read and validate

1. Lire `$ARGUMENTS` en entier et conserver exactement son encodage UTF-8, son éventuel BOM et son style de fins de ligne.
2. Lire uniquement le premier frontmatter, entre la première ligne `---` et sa fermeture `---`.
3. Extraire la valeur scalaire de `git_repo:` ; retirer seulement les guillemets YAML englobants, les espaces périphériques, un suffixe `.git` et un `/` final.
4. Conserver le contenu original en mémoire. Aucune écriture ne doit avoir lieu avant la réussite de la récupération et du parsing des issues.

### Step 2 — Resolve provider and repository

Accepter les URL HTTPS, SSH et la forme SCP Git habituelle (`git@host:groupe/projet.git`).

- Hôte `github.com` → provider `github`, outil `gh`, identifiant `owner/repo`.
- Hôte `gitlab.com` ou sous-domaine `*.gitlab.io` → provider `gitlab`, outil `glab`, identifiant `group[/subgroup]/repo`.
- Tout autre hôte, identifiant incomplet ou URL ambiguë → arrêter sans écrire et nommer la valeur `git_repo` refusée.

Vérifier que l'outil requis est disponible avant tout appel réseau. S'il manque, arrêter sans écrire avec l'installation attendue (`gh` ou `glab`).

### Step 3 — Fetch open issues

Utiliser l'identifiant normalisé comme argument séparé ; ne jamais construire une commande shell concaténée à partir de `git_repo`.

**GitHub**

```bash
gh issue list --repo <owner/repo> --state open --limit 1000 --json number,title,state
```

**GitLab**

```bash
glab issue list --repo <group/project> --output json
```

Parser le JSON avant toute écriture :

- GitHub : numéro `number`, titre `title`, état `state` ; ne conserver que `OPEN` (insensible à la casse).
- GitLab : numéro de projet `iid` (à défaut `number`), titre `title`, état `state` ; ne conserver que `opened` ou `open` (insensible à la casse).
- Rejeter toute réponse non JSON, non liste, ou toute issue retenue sans numéro/titre/état valide.
- Réduire les espaces et retours à la ligne d'un titre à un espace, sans en modifier le texte.
- Préserver l'ordre renvoyé par le CLI.

Si le CLI échoue, si l'authentification ou l'accès au dépôt échoue, ou si le JSON est invalide : laisser le fichier strictement inchangé et afficher l'avertissement avec le provider, le dépôt et la cause utile.

### Step 4 — Build the backlog

Construire le lien canonique à partir de l'URL HTTPS normalisée du dépôt :

- GitHub : `https://github.com/<owner/repo>/issues/<number>`
- GitLab : `https://<host>/<group/project>/-/issues/<iid>`

Une issue par ligne :

```markdown
- [#123](https://host/path/issues/123) — Titre de l'issue (open)
```

Le texte affiché commence toujours par `[#Numéro]`. Ne jamais répéter l'URL en clair ou en fin de ligne. Afficher l'état en minuscules. Si aucune issue ouverte n'est renvoyée, produire la ligne unique :

```markdown
_Aucune issue ouverte._
```

Ce Step produit le **bloc** seul : les lignes d'issues, ou cette ligne d'état vide. Le titre `## Backlog` et son placement relèvent exclusivement du Step 5.

### Step 5 — Replace or insert the section

**Bloc généré.** Dans une section `## Backlog`, titre exclu, le bloc généré est la première plage contiguë de lignes dont chacune est :

- une **ligne d'issue générée** : `- [#<numéro>](<url>) — <titre> (<état>)` où `<url>` est le lien canonique construit au Step 4 pour le dépôt résolu au Step 2, et où le numéro terminal de `<url>` est identique au `<numéro>` affiché ;
- la ligne `_Aucune issue ouverte._` ;
- une ligne vide encadrée des deux côtés par des lignes conformes.

La reconnaissance s'arrête à la première ligne non conforme. Les lignes vides de queue n'appartiennent pas au bloc. Une ligne de même forme pointant vers un autre dépôt n'est pas générée et n'est jamais remplacée. La reconnaissance est indépendante du style de fins de ligne et du BOM : une ligne CRLF conforme est reconnue comme telle.

Limites assumées de cette reconnaissance par motif, à ne pas présenter comme une garantie totale :

- une ligne manuelle strictement identique à une sortie de la skill pour ce dépôt est indiscernable et sera remplacée ;
- si une telle ligne manuelle précède le bloc réel dans la section, c'est elle qui est reconnue : le bloc réel devient orphelin et se duplique à chaque synchronisation ;
- `_Aucune issue ouverte._` est le seul motif non ancré au dépôt ; une note manuelle portant exactement cette phrase est donc remplaçable.

**Placement.**

- Si une section `## Backlog` existe (casse et espaces périphériques ignorés) et contient un bloc généré, remplacer cette seule plage. Aucune autre ligne de la section n'entre dans la zone de remplacement, qu'un titre suivant existe ou non.
- Si la section existe sans bloc généré, insérer le bloc en tête de section, avant tout contenu existant.
- S'il existe plusieurs sections `## Backlog`, arrêter sans écrire et signaler l'ambiguïté.
- Si la section n'existe pas :
  - lorsqu'un titre `# ...` ouvre le corps, insérer `## Backlog` après ce titre et son bloc introductif, juste avant le premier titre `##` ;
  - sinon, l'insérer immédiatement après le frontmatter.
- Espacement : exactement une ligne vide entre le titre `## Backlog` et le bloc, et exactement une ligne vide entre le bloc et la première ligne de contenu qui suit dans la section. Une resynchronisation ne doit jamais accumuler de lignes vides supplémentaires.
- Préserver byte-for-byte le frontmatter, tout contenu de la section extérieur au bloc généré, et tout contenu hors section, hormis les sauts de ligne imposés par la règle d'espacement ci-dessus.
- Effectuer une seule écriture atomique après construction et validation du document final.

### Step 6 — Verify and report

Relire le fichier et vérifier :

- frontmatter identique à l'original ;
- une seule section `## Backlog` ;
- une ligne par issue ouverte, sans URL redondante ;
- tout contenu non généré de la section `## Backlog` identique à l'original ;
- toutes les autres sections inchangées.

La ligne `Section:` du rapport vaut `replaced` lorsqu'un bloc généré préexistant a été remplacé, et `inserted` dans les deux autres cas : section créée, ou bloc posé en tête d'une section existante qui n'en avait pas.

Rapport final :

```text
Backlog updated: <fichier>
Repository: <provider> <owner-or-group/repo>
Open issues: <N>
Section: replaced|inserted
```

En cas d'échec, ne jamais afficher ce rapport de succès et confirmer explicitement : `File unchanged.`
