# Private Coolify pilot

Use this Compose file with the repository root as Coolify Base Directory and
`/deploy/coolify-pilot/compose.yaml` as Docker Compose Location. Select Raw
Compose, disable automatic/preview deployments, and leave all public domains
empty. Pin the reviewed Git commit in Coolify. The base image is pinned by digest.

An infrastructure owner must first create the external network
`coolify-paper-grid-pilot` using an explicitly reviewed unused subnet; this pilot
uses `10.253.84.0/24`. The app binds only `127.0.0.1:8303` and has no persistent data.

Deploy via Coolify's API, verify `/up`, then compare `/` bytes against the existing
Paper Grid origin on `127.0.0.1:8103`. Keep Cloudflare tunneling unchanged. Deploying
this branch never authorizes replacing the production origin or stopping it.

Rollback selects the previous tested Git commit and deploys it again. Keep image
and deployment IDs in the machine's pilot report. No automatic Docker cleanup.
