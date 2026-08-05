# Codebase Audit: `design:harness` — code-quality

Le générateur contredit son propre contrat de codes de sortie sur les entrées mal formées, et accepte silencieusement des jeux de pages qui produisent un HTML faux.

- **Date**: 2026-08-05
- **Scope**: `plugins/design/adapters/harness/harness.py` (460 lignes) + `plugins/design/skills/harness/SKILL.md` + `plugins/design/references/harness-contract.md`
- **Health**: fair
- **Findings**: 1 critical, 3 warning, 2 minor

Toutes les ancres renvoient à la **source** (`plugins/design/`), jamais au cache installé. Chaque ligne a été reproduite en exécutant `harness.py` ; les commandes et les sorties sont données sous la table.

## Findings

| Sev | Category     | Location                                        | Issue                                                                                                                       | Suggested fix                                                                                                     | Effort |
| --- | ------------ | ----------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ------ |
| 🔴  | code-quality | `plugins/design/adapters/harness/harness.py:427` | `--pages-json` est lu par un `json.loads` nu, sans `try`/`except` ni validation de forme → **exit 1 + traceback Python**, alors que `references/harness-contract.md:26` écrit « Le harness n'émet **jamais** 1 ni 4 » et `skills/harness/SKILL.md:62` « (jamais 1, jamais 4) » | Encadrer la lecture et valider la forme (liste de dicts portant `key`/`label`) ; sortir en 2 avec un message nommant le fichier fautif, comme le fait déjà `:436` | S      |
| 🟡  | code-quality | `plugins/design/adapters/harness/harness.py:53-56` | `key_to_fn` écrase `-` et `_` sur le même séparateur : `my-page` et `my_page` produisent tous deux `pageMyPage`. La fonction est **déclarée deux fois** dans le fichier généré et les deux clés du registre pointent sur la seconde. Exit 0, aucun avertissement | Détecter la collision de noms de fonction avant écriture et sortir en 2 en nommant les deux clés ; ou dériver un suffixe stable | S      |
| 🟡  | code-quality | `plugins/design/adapters/harness/harness.py:38-50` | Aucune vérification d'unicité des clés : `--pages 'home:A,home:B'` est accepté, `pageHome` apparaît 5 fois dans la sortie, la dernière définition gagne | Refuser les clés dupliquées en 2, même chemin que « no pages defined » | S      |
| 🟡  | code-quality | `plugins/design/adapters/harness/harness.py:61-78` vs `:81-89` | Le **même label** est traité différemment selon la cible : `build_functions:87` échappe `<`/`>`, `build_options:72` et `:76` interpolent brut. Mesuré : `p1:Fiche <b>produit</b>` → le sélecteur affiche « Fiche produit » avec un vrai `<b>` injecté dans le DOM, la page affiche `Fiche &lt;b&gt;produit&lt;/b&gt;` — deux libellés pour une même page | Une seule fonction d'échappement HTML appliquée à `key`, `label` et `group` dans `build_options` (y compris l'attribut `value=`, aujourd'hui sans échappement de `"`) | S      |
| 🟢  | code-quality | `plugins/design/adapters/harness/harness.py:446` | `--title` est substitué **avant** `%%PAGE_OPTIONS%%` (`:447`) et sans échappement : un titre contenant une sentinelle `%%…%%` est lui-même balayé par les remplacements suivants, et un titre contenant `<` casse le `<title>`. Mesuré inoffensif sur `Ma "Marque" & Cie`, mais rien ne l'en empêche | Échapper `args.title` et faire les substitutions en une passe (`re.sub` sur `%%(\w+)%%` contre un dict) plutôt qu'en chaîne | S      |
| 🟢  | code-quality | `plugins/design/adapters/harness/harness.py:41` | `--pages` découpe sur `,` sans échappement possible : un label contenant une virgule crée silencieusement une page fantôme dont la clé est le fragment de droite | Documenter la limite dans `SKILL.md` et renvoyer vers `--pages-json` dès qu'un label porte une virgule | S      |

### Reproduction

```bash
cd plugins/design
# 🔴 exit 1 + traceback (attendu : 2)
echo 'pas du json' > bad.json
python adapters/harness/harness.py --out o.html --pages-json bad.json ; echo "exit=$?"
#   json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)   exit=1
echo '["home","contact"]' > shape.json
python adapters/harness/harness.py --out o.html --pages-json shape.json ; echo "exit=$?"
#   AttributeError: 'str' object has no attribute 'get'                       exit=1

# 🟡 collision de noms de fonction
python adapters/harness/harness.py --out c.html --pages 'my-page:A,my_page:B'
grep -n "function pageMyPage" c.html
#   159:  function pageMyPage() { return placeholder('my-page', 'A'); }
#   160:  function pageMyPage() { return placeholder('my_page', 'B'); }

# 🟡 double traitement du même label
python adapters/harness/harness.py --out h.html --pages 'p1:Fiche <b>produit</b>,p2:Autre'
grep -n '<option value="p1"\|function pageP1' h.html
#   127:        <option value="p1">Fiche <b>produit</b></option>
#   159:  function pageP1() { return placeholder('p1', 'Fiche &lt;b&gt;produit&lt;/b&gt;'); }
```

**Contre-épreuve du contrat** : `--pages ,,` sort bien en **2** avec `Error: no pages defined.` (`harness.py:436`). Le chemin correct existe donc déjà ; c'est `--pages-json` qui ne l'emprunte pas.

## Top actions

1. **Ramener `--pages-json` dans l'espace 0/2/3** (résout la ligne 🔴). C'est le seul écart qui contredit une phrase écrite du contrat, et il est atteignable par n'importe quel appel réel : un JSON produit par un agent est mal formé plus souvent qu'absent. Handoff : `aidd-dev:03-act` sur `harness.py:407-437`.
2. **Valider le jeu de pages avant génération** — unicité des clés, unicité des noms de fonction dérivés, clé non vide (résout les deux 🟡 de validation). Une seule fonction `validate_pages(pages)` appelée entre `:426-434` et `:439` couvre les trois.
3. **Unifier l'échappement** dans `build_options` sur celui de `build_functions` (résout le 🟡 d'incohérence et prépare le 🟢 sur `--title`). `html.escape` est stdlib, ce qui respecte la contrainte « stdlib only » du générateur.

## Coverage

- **Scanned**: code-quality
- **Skipped**: architecture, security, dependencies, performance — voir `tests.md § Coverage` pour les raisons, communes aux trois rapports de cette exécution.
