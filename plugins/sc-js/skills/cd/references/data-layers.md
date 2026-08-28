# JavaScript data layers

SQL delivery separates schema migrations, reference data and mutable production content. `deploy:db` may run reviewed, forward migrations with backup and recovery preconditions; it must not copy a local database over production. Production rows and server-managed media remain target-authoritative. Pull and target-to-target flows are refused by this delivery contract.

ORM signals such as Prisma, Drizzle, TypeORM, Sequelize or Knex select their existing project-native migration command; do not invent a second migration system.

IndexedDB belongs to each browser. Delivery ships versioned application migration code and tests it against representative old schemas. It never extracts, uploads or overwrites user browser data. Expose `deploy:db` only when it means shipping that migration code and this meaning is documented in the contract.

Staging may mirror named server data only when a deterministic export/import strategy exists, and may mirror media only when stable listing, hashes, resumable transfer and final verification are proven. Apply the shared manifest delta, report transferable bytes, and refuse missing capability instead of inventing storage or sending a full archive. Static sites have no mutable store unless project evidence declares one.
