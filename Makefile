test:
	@py.test -v choosealicense/test/

create:
	@python setup.py sdist bdist_wheel;

upload:
	@python setup.py sdist bdist_wheel upload;
