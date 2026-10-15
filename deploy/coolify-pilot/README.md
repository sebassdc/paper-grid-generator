# Paper Grid on Coolify and Cloudflare

Production resource: Paper Grid, managed by Coolify on the Framework host.
Cloudflare Tunnel routes paper-grid.sebashurtado.com to http://127.0.0.1:8303.
Keep Coolify's proxy disabled and its domain configuration empty. The existing
Cloudflare DNS CNAME points to the Framework tunnel; no additional public ports.

Use repository root as Base Directory, /deploy/coolify-pilot/compose.yaml as
Compose Location, and Raw Compose. Pin a reviewed full Git commit. Automatic
and preview deployments stay off. The historical folder name is retained to
preserve the tested build layout.

The external network coolify-paper-grid-pilot uses10.253.84.0/24. No persistent
volumes or private app settings are needed. Verify /up, compare / HTML bytes,
and check /deployment.json to identify the new origin through Cloudflare.

Rollback deploys a previously verified commit; origin rollback can temporarily
restore the retained old container on8103. Stop calls must include
docker_cleanup=false. Never prune unrelated host Docker resources.
