---
paths:
  - "**/*.php"
  - "!vendor/**"
---

# SOLID violations — capability pivot for sc-php audit

Standalone pivot — initial content seeded from improve/01-analyze.md. May diverge over time.

#### SOLID violations

**Single Responsibility (SRP):**
- Controller methods > 30 lines → likely doing too much
- Model methods that query, transform, AND send email → fat model
- Look for: database queries + business logic + HTTP response formatting in the same method

**Open/Closed (OCP):**
- `switch ($type)` or `if ($type === 'X') ... elseif` chains that would require editing to add a new type → missing polymorphism
- Look for: `switch` on a type/status string that isn't backed by an enum or strategy pattern
- **Ne pas flaguer un `match ($enum)` exhaustif** : sur un `enum` (8.1+) le compilateur vérifie l'exhaustivité, ajouter un cas *force* la mise à jour — c'est la fermeture, pas une violation. La violation vise le branchement sur une *string libre* extensible sans contrôle, pas le dispatch enum-typé.

**Liskov Substitution (LSP):**
- Subclass overrides that throw exceptions the parent never throws
- Subclass that narrows parameter types or widens return types vs parent contract

**Interface Segregation (ISP):**
- Interfaces with > 7 methods that are only partially implemented by most classes
- Classes that implement an interface but leave several methods throwing `NotImplementedException`

**Dependency Inversion (DIP):**
- `new ClassName()` d'un **service** (comportement + effets de bord : mailer, repository, client HTTP, logger) à l'intérieur d'un constructeur ou d'une méthode → dépendance cachée.
- **Condition de mesure, pas de présomption.** N'émettre la violation que si (a) le type instancié est un service — **jamais** un value object, DTO, exception, collection ou type immuable, pour lesquels `new` est correct — **et** (b) le projet **pratique déjà l'injection** ailleurs (constructeurs typés, conteneur, autowiring mesuré). Sur une base sans conteneur DI, prescrire l'injection est un choix d'architecture, pas une correction : émettre `info`, pas une violation.
- `static::` calls to concrete classes for service access.
