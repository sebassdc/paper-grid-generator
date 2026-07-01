# Deploying Paper Grid Generator

This app is a single self-contained `index.html` — no build step and no
dependencies. It's served as static files by a tiny [busybox
httpd](https://busybox.net/) process (the `Dockerfile` in this repo, a ~4 MB
image running a single process).

It runs on a [Dokku](https://dokku.com/) host fronted by Cloudflare.

**Live:** https://paper-grid.sebashurtado.com

## Run locally

Open `index.html` directly in a browser — that's it. Or serve it:

```bash
# with the same image the server uses
docker build -t paper-grid .
docker run --rm -p 8080:80 paper-grid
# → http://localhost:8080

# or with no Docker at all
python3 -m http.server 8080
```

## Deploy to Dokku

Prerequisites: SSH access to the Dokku host as the `dokku` user, and DNS for the
target hostname pointing at the host (on `sebashurtado.com` a wildcard `*` A
record already covers any subdomain, so no DNS change is needed there).

### First-time setup (run on the Dokku host)

```bash
APP=paper-grid
DOMAIN=paper-grid.sebashurtado.com
CPORT=80                                  # container port busybox httpd listens on

dokku apps:create $APP
dokku domains:set  $APP $DOMAIN           # `set` (not `add`) also drops the default vhost
dokku ports:set    $APP http:80:$CPORT
```

### Deploy (push from a clone of this repo)

Dokku builds from the `Dockerfile` automatically. Push whatever branch you want
live to the app's `master`:

```bash
# from off-box  (replace <HOST_IP> with the host's public IP)
git remote add dokku dokku@<HOST_IP>:paper-grid
git push dokku main:master

# from on the host itself
git push dokku@localhost:paper-grid main:master
```

Subsequent deploys are just another `git push`. Dokku zero-downtime swaps the
container and reloads its nginx proxy.

### Verify

```bash
# on the host, straight through the proxy
curl -s -o /dev/null -w "%{http_code}\n" -H "Host: paper-grid.sebashurtado.com" http://localhost/

# public URL (through Cloudflare)
curl -sI https://paper-grid.sebashurtado.com/ | head -1
```

## Notes

- **TLS:** terminated at Cloudflare (SSL mode *Flexible*); the origin serves
  plain HTTP on port 80. Keep hostnames one level deep (e.g. `paper-grid.…`) so
  Cloudflare's Universal SSL covers them.
- **Keep it light:** this is a static file — no app server, database, or build
  toolchain is needed or wanted. busybox httpd is deliberately the whole stack.
