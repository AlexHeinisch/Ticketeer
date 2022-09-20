run:
	flask run

migrate:
	flask db init
	flask db migrate
	flask db upgrade

test:
	python -m pytest .

clean:
	rm -f *.db
	rm -rf migrations/
