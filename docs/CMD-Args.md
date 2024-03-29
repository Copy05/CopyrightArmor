# Command Line Arguments

CopyrightArmor is very flexible to use by using it's command line arguments efficiently.

**Example:**
```bash
python CopyrightArmor.py -url entertainmasters.github.io --rate-limit
```

**Arguments**
- `-url` **REQUIRED:** Specifies the Start URL to scan

**Security Arguments**
- `--rate-limit` adds a 2 seconds pause between each action

**Logging Arguments**
- `--verbose` Additional logging to see what the programm does.
- `--debug` Additional Debug Information which verbose dosn't print

**URL Inclusion Arguments:**
- `--deep-search` allows links with query parameters "`.com?id=1`"
- `--external-visits` allows to visit external websites outside of your given domain
- `--include-socials` allows to visit social media links. see `filters.json` for the list

**Optimisation Arguments**
- `--google` optimizes the scraping engine for google search
- `--google-search` specifies a query to search. (ONLY WORKS WITHOUT `-url`)

**Report File Arguments**
- `--report-file` when exiting the app it outputs a file containing the scanned urls and domains. On Windows it gets outputed inside the TEMP folder.



# Unused

These Command Arguments have no functionality but are available.

- `--depth`
- `--file-types`
- `--keyword`