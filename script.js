const fs = require('fs');
const { execSync } = require('child_process');

const PATTERN_FILE = 'pattern.json';
const FILE_PATH = 'info.txt';
const COMMITS_PER_PIXEL = 5;

function gitCommit(message, commitDate) {
    fs.writeFileSync(FILE_PATH, message);
    execSync(`git add ${FILE_PATH}`, { stdio: 'pipe' });

    // Format ISO string date: YYYY-MM-DDT12:00:00
    const yearStr = commitDate.getFullYear();
    const monthStr = String(commitDate.getMonth() + 1).padStart(2, '0');
    const dayStr = String(commitDate.getDate()).padStart(2, '0');
    const dateStr = `${yearStr}-${monthStr}-${dayStr}T12:00:00`;

    const env = { ...process.env, GIT_AUTHOR_DATE: dateStr, GIT_COMMITTER_DATE: dateStr };

    execSync(`git commit --allow-empty -m "${message}" --date "${dateStr}"`, {
        env,
        stdio: 'pipe'
    });
    console.log(`${message} successful ✔️`);
}

function gitPush() {
    execSync('git push', { stdio: 'inherit' });
}

function loadPattern() {
    const raw = fs.readFileSync(PATTERN_FILE, 'utf8');
    const data = JSON.parse(raw);
    if (data && typeof data === 'object' && !Array.isArray(data) && data.pattern) {
        return data.pattern;
    }
    return data;
}

function firstSunday(year) {
    let d = new Date(year, 0, 1, 12, 0, 0); // Jan 1 of year, 12:00
    while (d.getDay() !== 0) { // 0 is Sunday
        d.setDate(d.getDate() + 1);
    }
    return d;
}

function makeCommitsFromPattern(year) {
    const pattern = loadPattern();
    const startSunday = firstSunday(year);

    let totalCommits = 0;

    for (let rowIdx = 0; rowIdx < pattern.length; rowIdx++) {
        const row = pattern[rowIdx];
        for (let colIdx = 0; colIdx < row.length; colIdx++) {
            const char = row[colIdx];
            if (char === ' ') continue;

            const commitDate = new Date(startSunday);
            commitDate.setDate(startSunday.getDate() + (colIdx * 7) + rowIdx);

            const commitsCount = /\d/.test(char) ? parseInt(char, 10) : COMMITS_PER_PIXEL;

            const yearStr = commitDate.getFullYear();
            const monthStr = String(commitDate.getMonth() + 1).padStart(2, '0');
            const dayStr = String(commitDate.getDate()).padStart(2, '0');
            const dateOnly = `${yearStr}-${monthStr}-${dayStr}`;

            for (let i = 1; i <= commitsCount; i++) {
                const msg = `${dateOnly} pixel commit ${i}`;
                gitCommit(msg, commitDate);
                totalCommits++;
            }
        }
    }

    console.log(`\nCreated ${totalCommits} commits. Pushing to GitHub...`);
    gitPush();
}

const year = process.argv[2] ? parseInt(process.argv[2], 10) : 2024;
console.log(`\n========================================`);
console.log(`  GitHub Contribution Graph Generator`);
console.log(`  Pattern: X E N O X C`);
console.log(`  Year: ${year}`);
console.log(`========================================\n`);

makeCommitsFromPattern(year);

console.log(`\n☑️ History Has Been Rewritten!`);
console.log(`☑️ All commits pushed to GitHub successfully.\n`);
