```
heroku login
```

Login into heroku docker registry
```
heroku container:login

or, since docker needs root:

sudo docker login --username=_ --password=$(heroku auth:token) registry.heroku.com
```

Push image
```
heroku container:push web

or, since docker needs root:

docker tag <image> registry.heroku.com/<app>/<process-type>
docker push registry.heroku.com/<app>/<process-type>

Specifically:

sudo docker build -t registry.heroku.com/oposec-april-chall-test/web .
sudo docker push registry.heroku.com/oposec-april-chall-test/web
```

Then, we need to release the image:
```
heroku container:release web -a oposec-april-chall-test
```

To get a shell and inspect stuff
```
heroku run sh --type=worker -a oposec-april-chall-test
```
Using sh instead of bash since this is alpine!

TODO: Probably create a script to do a docker build and push, to simplify these steps.
