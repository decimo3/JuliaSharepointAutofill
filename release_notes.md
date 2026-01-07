# Bug fixed: reserved URL characters on password

The program fail to navigate to URL due to use of reserved URL characters on password. Example:

* "pass#word" – it'll fail because the use of a hashtag character that's a fragment indicator character.
* "pass:word" – it'll fail because the colon character is used to separate the scheme, host, and port in URLs.
* "pass?word" – it'll fail because the question mark character starts the query string in URLs.
* "pass/word" – it'll fail because the slash character is used to separate path segments in URLs.
* "pass@word" – it'll fail because the at symbol separates credentials from the host in URLs.
* "pass%word" – it'll fail because the percent character is used to introduce percent-encoding sequences in URLs.
* "pass&word" – it'll fail because the ampersand character separates query parameters in URLs.
* "pass+word" – it'll fail because the plus character is often interpreted as a space in query strings.
* "pass=word" – it'll fail because the equals' character is used to assign values to query parameters.

To fix this, was added an instruction to encode password before navigate to the page.
