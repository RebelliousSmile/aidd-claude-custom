# JavaScript data layers

SQL delivery separates schema migrations, reference data and mutable production content. `deploy:db` may run reviewed, forward migrations with backup and recovery preconditions; it must not silently copy a local database over production. A reverse content flow uses an explicit `pull:*` operation.

ORM signals such as Prisma, Drizzle, TypeORM, Sequelize or Knex select their existing project-native migration command; do not invent a second migration system.

IndexedDB belongs to each browser. Delivery ships versioned application migration code and tests it against representative old schemas. It never extracts, uploads or overwrites user browser data. Expose `deploy:db` only when it means shipping that migration code and this meaning is documented in the contract.
