clean:
	rm -f default.db

create_db:
	DJANGO_SETTINGS_MODULE='expense_track.settings_dev' ./manage.py syncdb --noinput

make_fixtures:
	DJANGO_SETTINGS_MODULE='expense_track.settings_dev' ./manage.py loaddata fixtures/test_data.json

generate_testdata:
	DJANGO_SETTINGS_MODULE='expense_track.settings_dev' ./manage.py createtestdata

make_assets:
	bower install
	grunt concat
	DJANGO_SETTINGS_MODULE='expense_track.settings_dev' ./manage.py collectstatic --noinput

install_pip:
	pip install -r requirements_dev.txt

all: install_pip clean create_db make_fixtures generate_testdata make_assets
