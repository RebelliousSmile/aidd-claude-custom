# Wire-deploy compatibility route

This historical setup action no longer produces a deployment pipeline. Route the request to `sc-php:cd server` after scaffold verification.

## Inputs

Framework, project root, target facts, and any existing `scripts/deploy.mjs`, target file, package or Composer scripts.

## Process

1. Read existing delivery files and classify their custom targets and behavior.
2. Invoke the `server` action of the sibling `cd` skill through host-portable resolution.
3. Migrate or wrap the existing implementation behind the single Composer facade. Preserve custom code and request arbitration on conflicts.
4. Never create a second script, invent credentials, run a transfer, or import a database.

## Outputs

The files reported by `sc-php:cd server`, plus a migration note for legacy callers.

## Test

Confirm one root facade and one project contract remain after running compatibility twice.
