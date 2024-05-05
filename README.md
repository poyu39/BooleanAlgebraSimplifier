# BooleanAlgebraSimplifier

## 簡介
這是一個基於 Tabulation Method 的布林代數簡化器，可以將輸入的布林代數表達式輸出成 POS 和 SOP。


## 使用方法

### CLI

```shell
python CLI.py -h
```
```
usage: CLI.py [-h] [-v V [V ...]] [-m M [M ...]] [-M M [M ...]] [-d D [D ...]]

Boolean Algebra Simplifier use Tabulation Method by poyu39

options:
  -h, --help    show this help message and exit
  -v V [V ...]  variables
  -m M [M ...]  minterms
  -M M [M ...]  maxterms
  -d D [D ...]  dontcares
```

#### Example
```shell
python CLI.py -v a b c d -m 0 1 2 3 4 6 7 11 12
python CLI.py -v a b c d -m 0 4 8 10 12 13 15 -d 1
python CLI.py -v a b c d -M 1 3 5 7 13
python CLI.py -v a b c d -M 0 8 10 12 13 15 -d 1 2 3
```

### GUI
TODO