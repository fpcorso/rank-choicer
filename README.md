# rank-choicer

A Python package for calculating the winner of a poll using rank choice voting (Instant-runoff voting).

## Requirements

Python 3.10 or higher.

## Install

Use pip to install:

```shell
pip install rank-choicer
```

## Usage

First, set up the counter with the available options:

```python
from rank_choicer import RankChoiceCounter
counter = RankChoiceCounter(["A", "B", "C"])
```

Then, you can pass in the votes to its `count_votes` method which returns the winner:

```python
votes = {
    "voter1": ["A", "B", "C"],
    "voter2": ["B", "A", "C"],
    "voter3": ["C", "A", "B"],
    "voter4": ["A", "C", "B"],
    "voter5": ["B", "C", "A"],
}
winner = counter.count_votes(votes)
print(f"Winner is: {winner}")
```
```text
Winner is A
```

### Viewing Specific Rounds

Sometimes, you may want to review the different rounds of elimination for either analysis or visualization. You can do so by calling the `get_round_results` method:

```python
results = counter.get_round_results()
print(f"Round number: {results[0].round_number}")
print(f"Eliminated in the first round: {results[0].eliminated_options}")
print(f"Vote counts: {results[0].vote_counts}")
print(f"Winner (final round only): {results[-1].winner}")
```
```text
Round number: 1
Eliminated in the first round: ['C']
Vote counts: {'A': 2, 'B': 2, 'C': 1}
Winner (final round only): A
```

Each `RoundResult` has four fields: `round_number`, `vote_counts`, `eliminated_options`, and `winner`. Only the final round will have a `winner` set; only non-final rounds will have `eliminated_options` set.

You can also serialize a round result to a dictionary, which is useful for JSON responses or storage:

```python
import json

rounds = json.dumps([result.to_dict() for result in counter.get_round_results()])
```

### Handling Ties In Elimination

In rare cases, you may have more than one option with the lowest votes. In those cases, you can handle what to eliminate in two ways:

* Randomly eliminate one of the options with lowest votes
* Eliminate all options tied for lowest votes

The `RankChoiceCounter` defaults to random but you can change the strategy used using the `elimination_strategy` parameter:

```python
from rank_choicer import EliminationStrategy
counter = RankChoiceCounter(
    ["A", "B", "C", "D"], elimination_strategy=EliminationStrategy.BATCH
)
```

Note that when using `EliminationStrategy.BATCH`, if all remaining options are tied, `count_votes` will raise a `ValueError`. You can catch this and inspect the round results to determine how the tie occurred:

```python
try:
    winner = counter.count_votes(votes)
except ValueError:
    rounds = counter.get_round_results()
```

## Contributing

Community made feature requests, patches, bug reports, and contributions are always welcome.

Please review [our contributing guidelines](https://github.com/fpcorso/rank-choicer/blob/main/CONTRIBUTING.md) if you decide to make a contribution.

## License

This project is licensed under the MIT License. See [LICENSE](https://github.com/fpcorso/rank-choicer/blob/main/LICENSE) for more details.