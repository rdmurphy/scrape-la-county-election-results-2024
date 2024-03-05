# L.A. County Election Results 2024

A repo that runs a GitHub Action to retrieve and store the L.A. County's 2024 election results feeds from [lavote.gov](https://results.lavote.gov).

## What's here

### March 5 Primary

| File/Directory  | Notes |
| ------------- | ------------- |
| [`primary/results.json`](./primary/results.json)  | A snapshot of the [JSON results file RR/CC makes available](https://www.lavote.gov/home/voting-elections/current-elections/election-results-file-downloads).   |
| [`primary/election_data.json`](./primary/election_data.json) | This file is loaded on the [dynamic updating results page](https://results.lavote.gov/#year=2024&election=4316). It gives every contest and candidate a unique ID. Despite having slots for vote counts, these are always zeroed out.   |
| [`primary/counter_data.json`](./primary/counter_data.json) | This file is loaded on the [dynamic updating results page](https://results.lavote.gov/#year=2024&election=4316). It provides the vote values (and other totals) found on a results page. The IDs that appear in this file sync up with the ones in `election_data.json`. |

## Notes

- The results for **March 5** will represent the initial ballot count release of the night. This means all of these votes are mail-in ballots tabulated prior to polls closing.
- The results for **March 6** represent the final ballot count release of election night. This means these totals include (at minimum) all the mail-in ballots tabulated prior to polls closing and all Election Day ballots cast. Technically this release will happen on March 6 at some point early in the morning, so these counts "belong" to this day just to keep this sane.

## License

MIT
