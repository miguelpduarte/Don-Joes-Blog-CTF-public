#!/usr/bin/env sh

# APP_NAME="oposec-april-chall-test"
APP_NAME="don-joes-blog"

sudo docker build -t registry.heroku.com/$APP_NAME/web .
sudo docker push registry.heroku.com/$APP_NAME/web
heroku container:release web -a $APP_NAME

# Check container logs
heroku logs --tail -a $APP_NAME
