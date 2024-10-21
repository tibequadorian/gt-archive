FROM capsulecode/singlefile:latest

USER root
RUN apk add --no-cache python3 py3-beautifulsoup4 py3-dateutil py3-feedparser py3-requests

COPY src/ /opt/

USER chrome
ENTRYPOINT ["sh", "/opt/run.sh"]
