server.dev:
	./manage.py runserver --settings=config.settings.local

server.dev.plus:
	./manage.py runserver_plus --cert-file cert.crt

migraton.makemigrations:
	./manage.py makemigrations

migration.migrate:
	./manage.py migrate

# ---------
compose.dev.up:
	docker-compose -f docker-compose.dev.yml up --build

compose.dev.down:
	docker-compose -f docker-compose.dev.yml down

# ---------

compose.prod.up:
	docker-compose -f docker-compose.prod.yml up --build

compose.prod.down:
	docker-compose -f docker-compose.prod.yml down
# ---------


dump_file_name = "mysite_data.json"

dump:
	./manage.py dumpdata --indent=2 --output=${dump_file_name}

# before loading the dump execute delete_contenttypes
delete_contenttypes:
	./manage.py shell -c "\
	from django.contrib.contenttypes.models import ContentType; \
	ContentType.objects.all().delete();\
	"

dump.load:
	./manage.py loaddata ${dump_file_name}


createsuperuser:
	./manage.py createsuperuser

celery_app_name = "config.celery_app"

run.celeryworker:
	celery -A ${celery_app_name} worker -l info

run.celery.flower:
	celery -A ${celery_app_name} flower

install.secrets:  # https://github.com/awslabs/git-secrets
	git secrets --install

stripe.cli.login: # login stripe cli, if not installed: brew install stripe/stripe-cli/stripe
	stripe login

stripe.cli.listen:
	stripe listen --forward-to localhost:8000/payment/webhook/

manage.collectstatic: # copies all static files from all applications into STATIC_ROOT location
	./manage.py collectstatic


# https://docs.djangoproject.com/en/4.1/topics/testing/tools/#fixture-loading
table_to_dump=courses
output_dir=${table_to_dump}/fixtures
output_filename=subjects.json
manage.fixture.dumpdata:  # dumps data from database into json
	mkdir -p ${output_dir}
	./manage.py dumpdata ${table_to_dump} --indent=2 --output=${output_dir}/${output_filename}

manage.fixture.load:  # loads data from json file into database
	./manage.py loaddata ${output_dir}/${output_filename}


manage.check.prod:
	./manage.py check --deploy --settings=config.settings.prod
