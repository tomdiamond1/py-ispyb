# ISPyB Backend prototype

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/2126d052de464a27bf9a60ef27012e2f)](https://app.codacy.com/manual/IvarsKarpics/ispyb_backend_prototype?utm_source=github.com&utm_medium=referral&utm_content=IvarsKarpics/ispyb_backend_prototype&utm_campaign=Badge_Grade_Dashboard)
[![Build Status](https://travis-ci.org/mxcube/mxcube.svg?branch=master)](https://travis-ci.org/IvarsKarpics/ispyb_backend_prototype)

```bash
sudo pip install -r requirements.txt
cd ..
gunicorn ispyb:server
```

## Create SQLAlchemy models from the existing db:
```bash
flask-sqlacodegen --flask --outfile models.py mysql://ispyb_api:password_1234@localhost/ispybtest
```

## Authentication
JWT (Jason web tokens) are used to authenticate requests. See jwt.io to test the token.

## Format code
```bash
autopep8 -a -r -j 0 -i --max-line-length 88 ./
black --safe ./
```

