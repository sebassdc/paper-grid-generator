FROM busybox:1.36.1
COPY index.html README.md /www/
RUN printf 'ok\n' > /www/up
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD wget -q -O /dev/null http://127.0.0.1/up || exit 1
CMD ["httpd", "-f", "-p", "80", "-h", "/www"]
