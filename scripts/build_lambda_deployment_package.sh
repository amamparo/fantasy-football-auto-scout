rm -rf .build
mkdir .build
cp -r src .build
pipenv run pip freeze > .build/requirements.txt
pip install -r .build/requirements.txt -t .build --compile