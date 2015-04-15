# ChooseALicense-cli

[![Latest Version][1]][2]
[![Build Status][3]][4]

Bring http://choosealicense.com to your terminal. Choose a license in your terminal.

![demo][]

## Install

    $ pip install choosealicense-cli

## Usage

List all the available licenses:

    $ license show

Show the info of the specified license:

    $ license info LICENSE(e.g. mit)

Show the default context for the license template:

    $ license context LICENSE(e.g. mit)

Generate a license:

    $ license generate LICENSE(e.g. mit)

Get detailed help message via `license -h` and `license show/info/context/generate -h`

## License

MIT.

[1]: http://img.shields.io/pypi/v/choosealicense-cli.svg
[2]: https://pypi.python.org/pypi/choosealicense-cli
[3]: https://travis-ci.org/lord63/choosealicense-cli.svg
[4]: https://travis-ci.org/lord63/choosealicense-cli
[demo]: https://cloud.githubusercontent.com/assets/5268051/7150903/b7f16168-e354-11e4-91b5-0965a86c8158.jpeg