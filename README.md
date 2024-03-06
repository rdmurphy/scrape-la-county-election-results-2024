# L.A. County Election Results 2024

A repo that runs a GitHub Action to retrieve and store the L.A. County's 2024 election results feeds from [lavote.gov](https://results.lavote.gov).

See this data put to use in [an Observable notebook](https://observablehq.com/@rdmurphy/l-a-county-2024-primary-election-results-trends)!

## What's here

### March 5 Primary

| File/Directory  | Notes |
| ------------- | ------------- |
| [`primary/results.json`](./primary/results.json)  | A snapshot of the [JSON results file RR/CC makes available](https://www.lavote.gov/home/voting-elections/current-elections/election-results-file-downloads).   |
| [`primary/election_data.json`](./primary/election_data.json) | This file is loaded on the [dynamic updating results page](https://results.lavote.gov/#year=2024&election=4316). It gives every contest and candidate a unique ID. Despite having slots for vote counts, these are always zeroed out.   |
| [`primary/counter_data.json`](./primary/counter_data.json) | This file is loaded on the [dynamic updating results page](https://results.lavote.gov/#year=2024&election=4316). It provides the vote values (and other totals) found on a results page. The IDs that appear in this file sync up with the ones in `election_data.json`. |
| `primary/results/*.json` | These files represent each copy of `results.json` collected in a snapshot. |
| `primary/counter_data/*.json` | These files represent each copy of `counter_data.json` collected on a given day. |
| [`primary/timeframes.json`](./primary/timeframes.json) | This file is where all the historical data is brought together. It includes historical vote totals and changes for every single contest and candidate per snapshot. |

## License

MIT
