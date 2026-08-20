# Email converti en Markdown — format de référence

Les fichiers email convertis en Markdown suivent une convention stable. Cette fiche permet à `filler` d'identifier, trier, résumer, fusionner et nettoyer ces fichiers correctement.

## Nom de fichier

```
email_YYYY-MM-DD_<ExpéditeurCourt>_<SujetCourt>_to_<DestinataireCourt>.md
```

- `YYYY-MM-DD` — date de l'email (source canonique pour le tri)
- `<ExpéditeurCourt>` — 7-8 premiers caractères du nom de l'expéditeur (CamelCase, sans espaces)
- `<SujetCourt>` — 12 premiers caractères du sujet (sans espaces ni caractères spéciaux)
- `<DestinataireCourt>` — idem pour le destinataire

Exemples :
- `email_2026-06-01_DaviEspi_NouveauMessa_to_FranGuil.md`
- `email_2026-06-01_OnetCdg_MatérielSmar_to_Pro.md`

## Frontmatter YAML

```yaml
---
from: Prénom Nom <email@domaine.com>
to: Prénom Nom <email@domaine.com>          # ou alias court (ex: pro@fxguillois.email)
date: 2026-06-01T11:04:11+00:00             # ISO 8601 avec timezone
subject: 'Sujet complet de l'email'         # guillemets simples si caractères spéciaux
subject_hash: 8def16                        # 6 caractères — identifiant de thread
tags:
  - INBOX                                   # chemin de dossier (style IMAP)
  - INBOX/smartlockers/clients/onet
attachments:
  - 2026-06-01_nom-fichier.ext             # fichiers joints présents dans le même répertoire
email_type: direct | mailing_list
---
```

### Champs clés pour filler

| Champ | Usage dans filler |
|-------|-------------------|
| `date` | Tri chronologique, critère `old:<date>` dans clean |
| `from` | Tri par expéditeur, regroupement de conversations |
| `to` | Utilisé à la place de `from` quand l'expéditeur est le propriétaire du vault (voir ci-dessous) |
| `subject_hash` | Détection de threads (emails du même fil = même hash) |
| `tags` | Équivalent du dossier IMAP — tri par tag = tri par dossier |
| `email_type` | `mailing_list` = candidat prioritaire pour clean |
| `attachments` | Permet de ne pas supprimer un email si sa pièce jointe est unique |

### Emails envoyés — règle d'entité

Quand `from:` est l'adresse du propriétaire du vault, le fichier est une **réponse dans une conversation**. L'entité significative est le **correspondant**, pas l'expéditeur. Dans ce cas, `filler` utilise `to:` pour déterminer l'entité bucket.

- `from: moi@…` → entité = destinataire (`to:`)
- `from: quelqu'un@…` → entité = expéditeur (`from:`)

Le propriétaire est identifié par heuristique : les adresses email qui apparaissent le plus souvent en `from:` dans des fichiers dont le nom contient `GuilXavi` ou l'alias connu (`pro@`, `fx@`). Si ambiguïté, demander à l'utilisateur de confirmer ses adresses avant de trier.

### Bruit des citations répétées

L'objectif de convertir les emails en markdown est de **limiter le bruit**. La principale source de bruit est le **chaînage des citations** : chaque réponse inclut la réponse précédente, qui inclut celle d'avant, etc. Un fil de 5 échanges peut ainsi contenir 4 copies du premier message.

Aucune commande n'élague ces citations : les retirer sans perte demande de vérifier que le contenu cité survit ailleurs dans le fil, ce qui relève de la lecture. Le bruit est donc compté, jamais coupé — `survey` mesure le volume, `merge` reconstitue le fil dans l'ordre, et c'est au lecteur de trancher.

## Corps du document

Structure typique (ordre variable) :

1. **Corps principal** — texte libre, souvent en markdown léger
2. **Signature** — bloc texte avec nom, titre, coordonnées (identifiable par pattern nom+titre+téléphone)
3. **Message transféré** — introduit par `---------- Forwarded message ---------`
4. **Pièces jointes** — section `### Pieces jointes :` avec liens markdown vers les fichiers

## Commandes adaptées aux emails MD

### `filler survey`
- Détecte les threads : fichiers partageant le même `subject_hash`
- Flag `empty` : corps sous le seuil de mots, hors signature et pièces jointes
- Flag `duplicate` : titre **et** premier paragraphe identiques — six alertes d'un même système partagent leur sujet sans être des doublons
- Groupe homogène : même expéditeur, même forme, au moins cinq fichiers → candidat `merge`

### `filler sort`
- `--scheme entity` : un sous-répertoire par domaine enregistrable du `from:` (`onet.fr` → `onet`, `marie@smartlockers.io` → `smartlockers`), le nom affiché ne servant que pour les domaines génériques (gmail, outlook…)
- `--owner <adresse>` : sur un message envoyé par le propriétaire du coffre, l'entité est le `to:`
- `--scheme date` : sous-répertoires `AAAA-MM/` ; `--scheme type` : par extension

### `filler index`
- `--group-by thread` : une section par `subject_hash`, titrée par le sujet du plus ancien message
- Chaque entrée : `- [[nom-de-fichier]] — expéditeur, date`

### `filler merge`
- Trie par `date` croissante, une section par message
- Sources intactes ; sortie au niveau `<Subcategory>`, nommée d'après le répertoire d'origine

### `filler clean`
- `empty` — corps sous le seuil, hors signature
- `duplicate` — titre et premier paragraphe identiques
- `old:AAAA-MM-JJ` — antérieur à la date donnée
- `orphan` — ni titre ni lien entrant
- Les pièces jointes référencées par le fichier écarté partent avec lui dans `_archive/`

### `mail triage`
- La branche et les règles priment sur le contenu : `mail-config.yaml` décide, rien n'est inféré du corps
- Un email sans date lisible échappe aux règles d'âge et part au rapport

## Fichiers associés dans le répertoire

Les pièces jointes référencées dans `attachments:` sont dans le **même répertoire** que le fichier email, avec le même préfixe de date. Elles portent le suffixe `_2`, `_3` etc. si le même nom de fichier existe plusieurs fois (doublons d'import).

Exemple :
```
email_2026-06-01_DaviEspi_NouveauMessa_to_FranGuil.md
2026-06-01_msg0016_2.WAV          ← pièce jointe référencée
```
