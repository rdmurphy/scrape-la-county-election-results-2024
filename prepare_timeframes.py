from json import dump, load
from pathlib import Path


def normalize_description(s):
    if "Supporters:" in s:
        description, positions = s.split("Supporters:")
        supporters, opponents = positions.split("Opponents:")

        supporters = supporters.strip().rstrip(".").split("; ")
        opponents = opponents.strip().rstrip(".").split("; ")

        return description.strip(), supporters, opponents
    
    return s, None, None


def normalize_number_vote_for(s):
    if s == "":
        return 1

    if s.endswith("than two"):
        return 2

    if s.endswith("than three"):
        return 3

    if s.endswith("than four"):
        return 4

    if s.endswith("than five"):
        return 5

    if s.endswith("than seven"):
        return 7

    raise ValueError(f'Could not determine number of votes: "{s}"')


def collect_votes(id, lookups):
    # Collect the votes for a given candidate
    return [lookup[id]['Value'] for lookup in lookups]


def prepare(directory):
    directory = Path(directory)

    # The file with all the election metadata
    with open(directory / 'election_data.json') as infile:
        contest_groups = load(infile)['Data']['ContestGroups']
        contest_groups = sorted(contest_groups, key=lambda x: x['Order'])
    
    # The directory where the counter data is stored
    counter_data_dir = directory / 'counter_data'
    counter_data_files = sorted(counter_data_dir.glob('*.json'))

    lookups = []
    dates = []

    for file in counter_data_files:
        [date, revision] = file.stem.rsplit('-', 1)
        dates.append([date, int(revision)])

        with open(file) as infile:
            counter_data = load(infile)['Data']
        
        # The counter data contains the lookup table
        lookups.append(
            {d["ReferenceID"]: d for d in counter_data if d["ReferenceID"]}
        )

    output = []
    
    for group in contest_groups:
        contest_group = group['Name']
        contests = group['Contests']

        for contest in contests:
            id = contest['ID']
            name = contest['Title']
            contest_type = contest['Type']
            measure_text = contest['MeasureText']
            description, supporters, opponents = normalize_description(measure_text)
            measure_pass_rate = contest['MeasurePassRate']
            vote_for = contest['VoteFor']
            candidates = contest['Candidates']

            candidates_output = []
            contest_is_non_partisan = True

            for candidate in candidates:
                candidate_id = candidate['ID']
                candidate_name = candidate['Name']
                party = candidate['Party']
                if party != "Non Partisan":
                    contest_is_non_partisan = False
                votes = collect_votes(candidate_id, lookups)
                adjusted_votes = [0] + votes
                changes = [adjusted_votes[i] - adjusted_votes[i-1] for i in range(1, len(adjusted_votes))]

                candidates_output.append({
                    'id': candidate_id,
                    'name': candidate_name,
                    'party': party,
                    'votes': votes,
                    'changes': changes,
                })

            cumulative_totals = []
            totals = []

            for candidate in candidates_output:
                for i, votes in enumerate(candidate['votes']):
                    if len(cumulative_totals) < i + 1:
                        cumulative_totals.append(0)
                    cumulative_totals[i] += votes

                for i, change in enumerate(candidate['changes']):
                    if len(totals) < i + 1:
                        totals.append(0)
                    totals[i] += change

            for candidate in candidates_output:
                candidate['votes_percent'] = []
                candidate['change_percent'] = []

                for i, votes in enumerate(candidate['votes']):
                    if cumulative_totals[i] > 0:
                        candidate['votes_percent'].append(votes / cumulative_totals[i])
                    else:
                        candidate['votes_percent'].append(0)

                for i, change in enumerate(candidate['changes']):
                    if totals[i] > 0:
                        candidate['change_percent'].append(change / totals[i])
                    else:
                        candidate['change_percent'].append(0)

            output.append({
                'id': id,
                'name': name,
                'type': contest_type,
                'group': contest_group,
                'non_partisan': contest_is_non_partisan,
                "description": description,
                "supporters": supporters,
                "opponents": opponents,
                "measure_pass_rate": measure_pass_rate,
                "vote_for": normalize_number_vote_for(vote_for),
                "cumulative_totals": cumulative_totals,
                "totals": totals,
                'candidates': candidates_output,
            })

    with open(directory / 'timeframes.json', 'w') as outfile:
        dump({'dates': dates, 'contests': output}, outfile, indent=2)


if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: python prepare_timeframes.py <directory>")
        sys.exit(1)
    
    directory = sys.argv[1]
    prepare(directory)
