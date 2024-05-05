# TMC

## 簡介
這是一個基於 Tabulation Method (Quine-McCluskey) 的布林函數簡化器。

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

## Screenshots

### Column step
![image](https://github.com/poyu39/BooleanAlgebraSimplifier/assets/42506064/93623943-619c-410c-88a1-cda2d6e79698)

### Prime implicant chart
![image](https://github.com/poyu39/BooleanAlgebraSimplifier/assets/42506064/768e5df8-6fad-4b4e-ae63-76d5f66b80c8)

### logic function
![image](https://github.com/poyu39/BooleanAlgebraSimplifier/assets/42506064/3b3ce00d-28c0-4dbb-873a-f8448bbb7081)


