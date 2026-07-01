# Ultra-light static server for the single self-contained index.html.
# busybox httpd = one tiny process, ~4MB image, no config, no workers.
FROM busybox:1.36

COPY index.html /www/index.html
COPY README.md /www/README.md

EXPOSE 80
# -f = foreground, -p = port, -h = document root
CMD ["httpd", "-f", "-p", "80", "-h", "/www"]
