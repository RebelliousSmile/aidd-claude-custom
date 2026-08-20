# Functional Review for « réintégrer les actions du plugin obs en scripts sans appel LLM »

- **Plan**: plan validé en conversation le 2026-08-20 (aucun document de plan sur disque) — table `skill | sous-commandes scriptées | actions retirées` + deux réponses de cadrage : « on scripte ce qui peut l'être, on enlève le reste, sauf `extract-pdf` qu'il faut mettre dans un autre plugin » et « on enlève l'action, on fait juste un script qui a la même finalité ».
- **Diff scope**: `HEAD..working tree` (rien n'est commité) — 79 entrées, 73 fichiers modifiés/supprimés, +510 / −3026, plus 18 fichiers ajoutés sous `plugins/pdf/`.
- **Date**: 2026-08-20

## Verdict

PARTIAL — les 14 sous-commandes annoncées existent et s'exécutent sans modèle, mais `tree fix` et `tree sort` ont perdu la passe d'intégrité des liens que les actions supprimées imposaient, alors que `skills/tree/SKILL.md:54` continue de la garantir.

## Scoring Matrix

| Criterion | Files | Status | Severity | Notes |
| --------- | ----- | ------ | -------- | ----- |
| AC1 — `tree` : `index check fix sort destinations` scriptés, `judge` retiré | `scripts/tree.py:665-689`, `skills/tree/SKILL.md` | Met | — | `tree.py --help` expose exactement `{index,check,fix,sort,destinations}` ; aucune trace de `judge` hors CHANGELOG |
| AC2 — `filler` : `survey sort index merge clean`, `digest/condense/synthesize` retirés | `scripts/filler.py:800-826`, `skills/filler/SKILL.md` | Met | — | `--help` expose `{survey,sort,index,merge,clean}` |
| AC3 — `project` : `create invoice export-rag`, 5 actions retirées | `scripts/project.py:309-326` | Met | — | `--help` expose `{create,invoice,export-rag}` |
| AC4 — `mail` : `triage` (+ `init-config`), `analyze/propose/reply/summarize` retirés | `scripts/mail.py:376-381` | Met | — | `--help` expose `{triage,init-config}` |
| AC5 — `extract-pdf` déplacé dans un plugin dédié | `plugins/pdf/**` (18 fichiers) | Met | — | Skill, actions, prompts, scripts et références suivent ; gate marketplace : `✓ pdf/skills/extract-pdf — 4 action(s) routable(s)` |
| AC6 — exécution sans appel LLM | `scripts/*.py` | Met | — | Aucun `import requests/urllib/openai/anthropic`, aucun `api_key`, aucune URL sortante dans les 5 scripts (stdlib seule) |
| AC7 — « on enlève l'action, on fait juste un script qui a la même finalité » | `skills/*/actions/` (supprimés), `scripts/tree.py:494,551` | Partial | Major | Plus aucun répertoire `actions/` dans `obs`. Mais l'ancienne `03-fix` step 6 et `04-sort` step 5 imposaient une « Link-integrity pass » après chaque move/rename ; `tree.py` appelle `plan.execute()` sans aucun relink ni co-déplacement d'asset. Finalité amputée, pas seulement dégradée |
| AC8 — invariants de sécurité du plugin préservés | `scripts/obslib.py:85,150,159,163,552`, `skills/tree/SKILL.md:54` | Partial | Blocker | 5 gardes sur 6 tenues (credentials jamais lus + exception `_code/`, médias exclus, dotfiles jamais seuls, collision jamais écrasée via `Plan.execute`, aucune suppression hors `clean --delete --apply`). La 6e, « Link integrity on move », est **écrite comme garantie** dans `tree/SKILL.md` et **absente du code** : une garantie fausse est pire qu'une garantie retirée |
| AC9 — dry-run par défaut, écriture sous `--apply` | `tree.py`, `filler.py`, `project.py`, `mail.py`, `obslib.py:564` | Met | — | 11 sous-commandes écrivantes déclarent `--apply` ; `TestDryRunIsTheDefault` compare un snapshot du disque avant/après sur 9 commandes |
| AC10 — manifestes et gates du marketplace cohérents | `.claude-plugin/marketplace.json`, `.agents/plugins/marketplace.json`, `index.json` | Met | — | `✓ consistency — 10 plugins, manifestes et actions cohérents` ; couverture obs 5/5/3/1 verte |

### Rappel des valeurs

- `Met` / `Partial` / `Unmet` ; sévérité sur `Partial` et `Unmet` seulement : `Blocker` / `Major` / `Minor`.

## Missing Behaviors

- [ ] **Passe d'intégrité des liens dans `tree fix` et `tree sort`** — `tree.py:494` et `tree.py:551` exécutent le plan sans réécrire les wikilinks entrants, sans co-déplacer les embeds/pièces jointes et sans lister les références pendantes. `obslib.relink_moved()` existe et est utilisé par `filler.py:512,769` ; `tree.py` ne l'importe pas.
- [ ] **Co-déplacement des assets dans `tree`** — promis par la même ligne de `SKILL.md`, aucun code correspondant.
- [ ] **Test de non-régression sur les liens pour `tree`** — `test_obs_scripts.py:196` couvre le co-déplacement pour `filler` uniquement ; aucun test n'aurait rougi sur ce manque, ce qui explique qu'il soit passé.

## Unplanned Behaviors

Changements présents dans le diff qui ne tracent à aucun critère du plan annoncé — tous assumés, à confirmer comme périmètre :

- [ ] **Remplacement des 5 suites behave par 33 tests unittest** (`scripts/tests/test_obs_scripts.py`, +412 lignes). Décidé en cours de route : les specs supprimées portaient les invariants de sécurité, les laisser tomber sans substitut laissait les scripts sans preuve. A capturé deux bugs réels (exception `_code/` ignorée par `filler.credentials_in`, `--anchor` refusé après la sous-commande de `project`).
- [ ] **`references/email-md-format.md` remonté de `skills/filler/` à la racine du plugin** — maintenant partagé par `filler` et `mail`, section « Actions filler » réécrite en « Commandes ».
- [ ] **`references/domain-layout.md` supprimé d'`obs`** et recréé dans `plugins/pdf/` ; plus aucune référence pendante côté obs (vérifié : les seuls `references/*.md` cités par les SKILL.md existent tous).
- [ ] **`references/tree-convention.md` et `references/bank-yml.md` réécrits** pour purger les mentions des skills disparues (`brief`, `writing`, `research`).
- [ ] **Marketplace 3.16.0 → 3.17.0** + entrée `pdf` dans les trois manifestes + entrées CHANGELOG (obs 0.38.0, marketplace 3.17.0).

## Flow / Edge-case Gaps

- [ ] **`tree fix` renomme un `.md` vers un slug kebab-case (I3)** → tout `[[Ancien Nom]]` pointant dessus casse, sans avertissement ni ligne de rapport. C'est le cas nominal de la commande, pas un cas limite.
- [ ] **`tree sort` déplace une note portant `![[image.png]]` relatif** → la note part, l'image reste, l'embed casse.
- [ ] **`filler clean --delete --apply`** : l'avertissement « X référençait Y — lien à reprendre » est émis **après** `item.path.unlink()` (`filler.py`, boucle de suppression). En dry-run l'utilisateur voit bien le `⚠ cité par N fichiers`, donc l'information existe avant la décision ; en `--apply` direct elle arrive trop tard pour changer d'avis.
- [ ] **`mail triage` archive un email cité par un index `filler`** → lien pendant, non signalé. Contrairement à `tree`, ni le `SKILL.md` de `mail` ni l'ancienne action `04-execute` ne promettaient l'intégrité des liens : écart accepté, mentionné pour mémoire, pas un manquement.
- [ ] **Collision dans `mail triage`** : deux emails de même chemin relatif archivés le même jour → `Plan.execute` saute la seconde opération avec « destination déjà présente — collision » ; rien n'est perdu, mais le fichier reste en place et devra être retrié à la main. `unique_destination` (utilisé par `filler`) résoudrait le cas.

## Summary

- **Criteria covered**: 8/10 `Met`, 2 `Partial` (AC7, AC8)
- **Blockers**: 1 — garantie « Link integrity on move » annoncée dans `skills/tree/SKILL.md:54` et non implémentée dans `scripts/tree.py`
- **Follow-up actions**:
  1. ~~Soit implémenter la passe de liens dans `tree`, soit retirer la ligne 54 du `SKILL.md` et l'annoncer comme perte assumée dans le CHANGELOG.~~ **Tranché le 2026-08-20 : perte actée.** `skills/tree/SKILL.md:54` annonce désormais l'inverse de ce qu'il promettait (« Links are not rewritten »), une section `Removed — tree ne réécrit plus les liens au déplacement` du CHANGELOG 0.38.0 en donne la raison et la conséquence pratique, et `README.md:24` restreint la mention du relink d'`obslib` à `filler`. Le blocker devient un écart documenté.
  2. Pas de test ajouté : verrouiller l'absence de réécriture ferait rougir à tort le jour où quelqu'un l'implémente. Le comportement est décrit, pas gelé.
  3. Ouvert : `unique_destination` dans `mail triage` pour lever le cas de collision d'archive.
- **Additional notes**: revue statique uniquement, aucune exécution applicative. Preuves d'exécution collectées en marge : `python3 -m unittest discover -s scripts/tests` → `Ran 33 tests … OK` ; `npm test` → `✓ consistency — 10 plugins`. Un rouge subsiste dans `npm test` (`✗ sc-php-fse`, `ModuleNotFoundError: No module named 'playwright'`) : dépendance système absente de la machine, hors périmètre de cette revue.
