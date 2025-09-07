import csv
import subprocess
from pydriller import Repository

repos = [
    "/home/set-iitgn-vm/Desktop/lab4 stt/ssh2",
    "/home/set-iitgn-vm/Desktop/lab4 stt/pycodestyle",
    "/home/set-iitgn-vm/Desktop/lab4 stt/ai-deadlines"
]

output_csv = "diff_dataset.csv"

def get_diff(repo_path, parent, commit, file_path, algo):
    cmd = [
        "git", "-C", repo_path, "diff",
        f"--diff-algorithm={algo}",
        "-w", "--ignore-blank-lines",
        parent, commit, "--", file_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()

with open(output_csv, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "old_file_path", "new_file_path",
        "commit_SHA", "parent_commit_SHA",
        "commit_message", "diff_myers", "diff_hist"
    ])

    for repo_path in repos:
        print(f"\nProcessing repo: {repo_path}")
        for commit in Repository(repo_path).traverse_commits():
            if len(commit.parents) != 1:
                continue
            parent_sha = commit.parents[0]

            for mod in commit.modified_files:
                old_path = mod.old_path or ""
                new_path = mod.new_path or ""
                file_path = new_path if new_path else old_path

                try:
                    diff_myers = get_diff(repo_path, parent_sha, commit.hash, file_path, "myers")
                    diff_hist = get_diff(repo_path, parent_sha, commit.hash, file_path, "histogram")

                    writer.writerow([
                        old_path, new_path,
                        commit.hash, parent_sha,
                        commit.msg.strip().replace("\n", " "),
                        diff_myers, diff_hist
                    ])
                except Exception as e:
                    print(f"Error processing {file_path} in commit {commit.hash}: {e}")