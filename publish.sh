poetry version patch
git commit -am "Bump version"
# poetry config pypi-token.pypi <my-token>
# poetry config http-basic.pypi <username> <password>
poetry publish --build