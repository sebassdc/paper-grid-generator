# Coolify production deployment

Coolify's Paper Grid project deploys this Compose application automatically on pushes to main, using the repository's signed GitHub push webhook. GitHub Actions is not required. Pull-request previews are disabled.

The pinned BusyBox image serves the repository's index.html unchanged. Compose is evaluated with the repository root as its project directory, so build context is `.`. Keep image pinning and resource limits when updating.

Public traffic: Cloudflare Tunnel → loopback Coolify Traefik proxy80 → app Docker network. The existing tunnel connector runs independently of Coolify. The public HTTPS domain is configured in Coolify; its HTTP-to-HTTPS redirect must be disabled because the tunnel uses HTTP at the local origin. Direct loopback8303 is retained for rollback/verification.

Only POST /webhooks/source/github/events/manual on the public Paper Grid hostname routes to Coolify. It validates GitHub's HMAC signature before allowing deployment. The dashboard stays private over Tailscale; webhook secrets are stored only in GitHub settings and Coolify, never here.

Operational configuration and rollback live on the host in ~/dev/coolify-pilot/README.md. Do not use host-wide Docker cleanup. A failed push deployment does not automatically revert Git history; inspect Coolify deployment logs and redeploy a known-good commit if necessary.
