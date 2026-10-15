FROM busybox:1.36.1@sha256:73aaf090f3d85aa34ee199857f03fa3a95c8ede2ffd4cc2cdb5b94e566b11662
COPY index.html README.md /www/
RUN printf 'ok\n' > /www/up
EXPOSE 80
HEALTHCHECK --interval=5s --timeout=3s --retries=6 CMD wget -q -O /dev/null http://127.0.0.1/up || exit 1
CMD ["httpd", "-f", "-p", "80", "-h", "/www"]
