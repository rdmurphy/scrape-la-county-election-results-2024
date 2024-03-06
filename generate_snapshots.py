from csv import DictReader
import subprocess


def generate_snapshots():
    """
    Generates a snapshot of results.json and counter_data.json at certain points
    in time.

    These two are generated separately because they do not consistently update
    together in a single commit, causing them to have different commit hashes.
    """

    # results.json
    with open('primary/snapshots.csv') as f:
        rows = [row for row in DictReader(f)]
    
    for row in rows:
        date = row['date']
        release = row['release']
        commit_sha = row['results_commit_sha']

        if commit_sha == '':
            continue

        process = subprocess.run(
            ['git', 'show', f'{commit_sha}:primary/results.json'],
            capture_output=True,
            text=True,
        )

        with open(f'primary/results/{date}-{release}.json', 'w') as outfile:
            outfile.write(process.stdout)

    # counter_data.json
    with open('primary/snapshots.csv') as f:
        rows = [row for row in DictReader(f)]
    
    for row in rows:
        date = row['date']
        release = row['release']
        commit_sha = row['counter_commit_sha']

        if commit_sha == '':
            continue

        process = subprocess.run(
            ['git', 'show', f'{commit_sha}:primary/counter_data.json'],
            capture_output=True,
            text=True,
        )

        with open(f'primary/counter_data/{date}-{release}.json', 'w') as outfile:
            outfile.write(process.stdout)


if __name__ == '__main__':
    generate_snapshots()