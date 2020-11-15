## usernames

A list of potential inactive accounts on github that possess
a `rare` username.

As per GitHub's official Name Squatting Policy:

> GitHub prohibits account name squatting, and account names may not be reserved or inactively held for future use. Accounts violating this name squatting policy may be removed or renamed without notice. Attempts to sell, buy, or solicit other forms of payment in exchange for account names are prohibited and may result in permanent account suspension.

So feel free to try and claim what you like!

### Usage

You can run the script with your own custom wordlist (and also tweak the filters)

#### Arguments:  
`--inp, -i`: input file  
`--out, -o`: output file

#### Access Token:
Generate a token [here](https://github.com/settings/tokens)
```
# .env file 

TOKEN="token [your token]"
```
#### Example:
```bash
$ python3 main.py -i users.txt -o output.txt
```

### Checks
- [x] No starred repositories
- [x] No repositories
- [x] No private contributions
- [x] No following
- [x] No public contributions
- [x] Created in year <= 2011

### Results
```
results/
├── output.txt <- https://github.com/first20hours/google-10000-english/blob/master/google-10000-english-no-swears.txt
├── output2.txt <- https://github.com/openethereum/wordlist/blob/master/res/wordlist.txt
├── output3.txt <- https://en.wikipedia.org/wiki/Wikipedia:List_of_two-letter_combinations
├── output4.txt <- http://www.scrabble.org.au/words/threes.htm
├── output5.txt <- https://www.ef.com/ca/english-resources/english-vocabulary/top-1000-words/
├── output6.txt <- https://www.reddit.com/r/leagueoflegends/comments/i2wmdg/list_of_words_so_you_can_play_skribbl_with_lol/
└── output7.txt <- https://www.enchantedlearning.com/wordlist/computer.shtml
```

### Note
*Not all activity on GitHub is publicly available, therefore users scraped here may still be active.*  

*If you are active and want to be removed from these lists, feel free to submit a PR!*

