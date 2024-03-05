#!/usr/bin/env bash

# Exit on error
set -o errexit
# Exit on use of an uninitialised variable
set -o nounset
# Exit if any statement returns a non-true return value
set -o pipefail
# Set the trace option for the entire script if the TRACE environment variable is set to 1
if [[ "${TRACE-0}" == "1" ]]; then
    set -o xtrace
fi

# write a main method that accepts two parameters called output_directory and election_id
main() {
    local output_directory="$1"
    local election_id="$2"

    # create the output directory if it does not exist
    mkdir -p "$output_directory"

    # grab the results and output
    curl "https://results.lavote.gov/electionresults/json?electionid=$election_id" |
      jq > "$output_directory/results.json"

    # grab the counter_data and output
    curl "https://results.lavote.gov/ElectionResults/GetCounterData?electionID=$election_id" |
      jq ".Data|=sort_by(.Number)" > "$output_directory/counter_data.json"

    # grab the election_data and output
    curl "https://results.lavote.gov/ElectionResults/GetElectionData?electionID=$election_id" |
      jq > "$output_directory/election_data.json"
}

main "$@"
