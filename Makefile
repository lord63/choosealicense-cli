test:
	@py.test --flake8 choosealicense/test/ choosealicense/;
	@py.test -v --cov-report term-missing --cov=choosealicense choosealicense/test/;

create:
	@python setup.py sdist bdist_wheel;

upload:
	@python setup.py sdist bdist_wheel upload;
