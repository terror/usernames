### How to contribute

#### Setup:

- Fork the repository and clone your fork.

- Install requirements (using pipenv)

```bash
$ pipenv install
```
- Generate a GitHub Access Token [here](https://github.com/settings/tokens) and place it in a .env file
  - See issue [#2](https://github.com/terror/usernames/issues/2) if you are having trouble
```
# .env file
TOKEN="token token_here" where token_here is your token
```

Now you can filter users based on your own wordlists by running:
```bash
$ python3 main.py -i input.txt -o output.txt
```

#### Contributing:

All inactive users are located in the [all.md](https://github.com/terror/usernames/blob/master/all.md) file. You can filter users and submit a pull request to add them to the markdown table as long as they are currently not present in the table.

Account creation date should be no less than 2012 ~ 8 years.

If you have claimed a username from the table you can submit a PR to remove it.
