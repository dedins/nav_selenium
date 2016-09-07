# nav_selenium
Automation tool for custom NavisionWeb CRM

## Installation
### Windows
 todo
 
### Linux
 todo

### OSX
```
brew install phantomjs
git clone https://github.com/dedins/nav_selenium.git
cd nav_selenium
sudo pip install -r requirements.txt
```

## Usage

```
nav_selenium_full-vX.X.py [-h] -f FILE_CSV
```


CSV syntax:

|      anno      |  mese   |   giorno1    |   giorno2    |   giorno3    |     ecc      |
|----------------|:--------|:------------:|-------------:|-------------:|-------------:|
| commessa-fase  | cliente | ore&#124;commento | ore&#124;commento | ore&#124;commento | ore&#124;commento |
| commessa-fase  | cliente | ore&#124;commento | ore&#124;commento | ore&#124;commento | ore&#124;commento |
| commessa-fase  | cliente | ore&#124;commento | ore&#124;commento | ore&#124;commento | ore&#124;commento |

example:

|     2016    |   gen    |      1      |      2       |     3      |     ecc     |
|-------------|:---------|:-----------:|-------------:|-----------:|------------:|
| N160000-001 | Società1 | 2&#124;attività  | 3&#124;riunione   | 4&#124;call     | 3&#124;riunione  |
| N160001-001 | Società2 | 8&#124;trasferta | 2&#124;attività   | 4&#124;call     | 8&#124;trasferta |
| N160002-004 | Società3 | 4&#124;call      | ore&#124;commento | 2&#124;attività | 2&#124;attività  |
