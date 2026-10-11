# Framework deployment

Build from the repository root: `docker build -f deploy/framework/Dockerfile -t <reviewed-tag> .`.
The adaptation serves port 80 and adds `/up` for ONCE compatibility. ONCE must use `--auto-update=false`.
Compose is also supported: set APP_IMAGE to the reviewed immutable image and BIND_PORT to the
coordinator-assigned loopback port, then run `docker compose -f deploy/framework/compose.yaml up -d`.
No private runtime environment or persistent volumes are needed. All static assets are in the image.
Preserve all public URL paths and compare HTML/JS/CSS/media bytes to source before cutover.

The Framework coordinator owns ingress, host port allocation and ONCE/Compose selection.
Source stays running. VPS root owns Cloudflare routing and cutover release.
Rollback: restore the prior routing to the still-running source after verifying the source responds.
For Pesopesado, both endpoints use the same external database: do not restore an old database snapshot.
No service deletion, source stop, or DNS change is part of these artifacts.
