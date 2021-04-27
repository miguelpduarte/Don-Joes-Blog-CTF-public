if [ -e app/source.zip ]; then
    echo "Source zip already exists in app folder, pls delet dis";
    exit 1
fi

echo "Don't forget to change flag.py to hide the flag itself and app.py to hide the heroku hack"
echo "I'll hide fake_passwd.txt and pycache for you :)"
echo;

zip -x 'app/__pycache__/*' -x 'app/utils/__pycache__/*' -x app/fake_passwd.txt -r source.zip app/
