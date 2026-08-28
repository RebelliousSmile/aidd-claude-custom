# Thin CI adapters

GitHub Actions and GitLab CI adapters perform only checkout, stack installation, locked dependency installation, provider prerequisites and the exact project command in its exact working directory.

- GitHub: default to `workflow_dispatch`; add a `push` event only for explicit contract `trigger: push`.
- GitLab: default to a manually started deploy job; add push rules only for explicit `trigger: push`.
- Railway/Heroku native automation follows the same manual-default policy where configurable.

Do not append `|| true`, reinterpret status, duplicate migrations or copy the script body into YAML. Environment entries reference declared secret names. Pin actions/images/tool versions according to repository policy. Expose contract source identity and post-delivery proof; keep its recovery instructions visible when the command fails.
