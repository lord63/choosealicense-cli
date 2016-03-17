test:
	@py.test -v choosealicense/test/;
	@py.test --flake8 choosealicense/test/ choosealicense/;

create:
	@python setup.py sdist bdist_wheel;

upload:
	@python setup.py sdist bdist_wheel upload;
