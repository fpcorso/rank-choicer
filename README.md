# rank-choicer

A Python package for calculating the winner of a poll using rank choice voting (Instant-runoff voting).

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
print(f"Eliminated in the first round: {results[0].eliminated_options}")
print(results[0].vote_counts)
```
```text
Eliminated in the first round: ['C']
{'A': 2, 'B': 2, 'C': 1}
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

## Contributing

Community made feature requests, patches, bug reports, and contributions are always welcome.

Please review [our contributing guidelines](https://github.com/fpcorso/rank-choicer/blob/main/CONTRIBUTING.md) if you decide to make a contribution.

## License

This project is licensed under the MIT License. See [LICENSE](https://github.com/fpcorso/rank-choicer/blob/main/LICENSE) for more details.