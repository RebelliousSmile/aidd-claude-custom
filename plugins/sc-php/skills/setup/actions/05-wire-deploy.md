# Action 05 — wire-deploy

Câble un pipeline de déploiement SSH (rsync + optionnel export DB) vers une ou plusieurs cibles distantes de type hébergement mutualisé (alwaysdata/Scriptami ou équivalent). Optionnel — à proposer après le scaffold, jamais imposé.

## Inputs

- `framework` résolu par l'action 01/02/03/04.
- Informations de la ou des cibles : host SSH, user, remote path, URL publique — demander à l'utilisateur, ne jamais inventer une cible.

## Process

1. Lire `references/deploy-pipeline.md` et écrire `scripts/deploy.mjs` et `scripts/deploy-targets.mjs`.
2. Renseigner `deploy-targets.mjs` avec les cibles fournies par l'utilisateur. Si aucune cible n'est encore connue, laisser le fichier avec un exemple commenté (ne pas inventer de host/user).
3. Si `framework === 'wordpress'`, poser `wpExportDb: true` sur les cibles où un export/import de base est pertinent ; pour Laravel/Symfony, ne pas poser ce champ (migrations rejouées côté cible à la place, hors scope de ce script).
4. Ajouter au `package.json` les scripts `"deploy": "node scripts/deploy.mjs"` (usage : `pnpm deploy <cible> [--no-db]`).
5. Rappeler explicitement (`references/deploy-pipeline.md` § Notes) : jamais de secret en clair dans `deploy-targets.mjs`, jamais d'import DB automatique côté cible.

## Outputs

```
scripts/deploy.mjs
scripts/deploy-targets.mjs
package.json (script "deploy" ajouté)
```

## Test

`pnpm deploy <cible-inexistante>` échoue avec un message listant les cibles disponibles (pas une erreur JS non gérée) — confirme que `resolveTarget` est bien branché.
