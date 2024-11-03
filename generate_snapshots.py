from csv import DictReader
import subprocess
from pathlib import Path


def generate_snapshots(directory):
    """
    Generates a snapshot of results.json and counter_data.json at certain points
    in time.

    These two are generated separately because they do not consistently update
    together in a single commit, causing them to have different commit hashes.
    """
    directory = Path(directory)

    # results.json
    with open(directory / 'snapshots.csv') as f:
        rows = [row for row in DictReader(f)]
    
    for row in rows:
        date = row['date']
        release = row['release']
        commit_sha = row['results_commit_sha']

        if commit_sha == '':
            continue

        if commit_sha == 'latest':
            # use the current file
            with open(directory / 'results.json') as infile:
                output = infile.read()
        else:
            process = subprocess.run(
                ['git', 'show', f'{commit_sha}:{directory}/results.json'],
                capture_output=True,
                text=True,
            )
            output = process.stdout

        (directory / 'results').mkdir(parents=True, exist_ok=True)
        with open(directory / 'results' / f'{date}-{release}.json', 'w') as outfile:
            outfile.write(output)

    # counter_data.json
    with open(directory / 'snapshots.csv') as f:
        rows = [row for row in DictReader(f)]
    
    for row in rows:
        date = row['date']
        release = row['release']
        commit_sha = row['counter_commit_sha']

        if commit_sha == '':
            continue

        if commit_sha == 'latest':
            # use the current file
            with open(directory / 'counter_data.json') as infile:
                output = infile.read()
        else:
            process = subprocess.run(
                ['git', 'show', f'{commit_sha}:{directory}/counter_data.json'],
                capture_output=True,
                text=True,
            )
            output = process.stdout

        (directory / 'counter_data').mkdir(parents=True, exist_ok=True)
        with open(directory / 'counter_data' / f'{date}-{release}.json', 'w') as outfile:
            outfile.write(output)


if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: python generate_snapshots.py <directory>")
        sys.exit(1)
    
    directory = sys.argv[1]
    generate_snapshots(directory)
