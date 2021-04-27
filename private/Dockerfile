FROM python:3.9-alpine

# RUN ls -la /etc/passwd

# Production flag
RUN echo -e '\n# Congrats! flag{Looking_For_Interesting_files}\n# Check /m4st3rfully_h1dd3n and try logging in with supreme_user:ezpz_passw0rd!' >> /etc/passwd

# Test version flag:
# RUN echo -e '\n# Congrats! flag{Include_that_file!}\n# Check /m4st3rfully_h1dd3n and try logging in with supreme_user:ezpz_passw0rd!' >> /etc/passwd

WORKDIR /chall
# RUN python -m pip install --upgrade pip

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY app/ app/

ENV PYTHONUNBUFFERED=1
CMD gunicorn -w $(( 2 * `nproc` + 1 )) --preload -b 0.0.0.0:${PORT:-8000} --chdir=app/ app:app

# CMD gunicorn -w 4 --preload -b 0.0.0.0:${PORT:-8000} --chdir=app/ app:app
# --preload fixes the issue with the secret being different between workers, but is not needed with just one worker
# CMD gunicorn -w 1 -b 0.0.0.0:${PORT:-8000} --chdir=app/ app:app
