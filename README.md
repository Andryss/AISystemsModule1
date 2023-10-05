# AISystemsModule1

База знаний, онтология, система поддержки принятия решений по настольной игре Мафия

## Content

[mafia.pl](./mafia.pl) - база знаний (можно открыть через [онлайн интерпретатор](https://swish.swi-prolog.org/))

[mafia.owl](./mafia.owl) - онтология (можно открыть при помощи [Protege](https://protege.stanford.edu/))

[main.py](./main.py) - система поддержки принятия решений


## Usage

Для запуска необходима библиотека `pyswip`:

```bash
pip install git+https://github.com/yuce/pyswip@master#egg=pyswip
```

Запуск системы поддержки принятия решений:

```bash
python main.py
```