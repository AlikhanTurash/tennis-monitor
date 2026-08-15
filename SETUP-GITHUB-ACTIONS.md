# Setup Guide — GitHub Actions (Private & Free)

## Step 1: Create a Private GitHub Repo

1. Go to [github.com/new](https://github.com/new)
2. Name it something like `tennis-script` (private)
3. **Do NOT initialize** with README (we already have files)
4. Click **Create repository**

## Step 2: Push Your Code

```bash
cd /Users/alikhan/Development/Projects/tennis-script
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/tennis-script.git
git push -u origin main
```

## Step 3: Prepare Credentials for GitHub

You need to convert your `token.json` to a single-line JSON for GitHub Secrets:

```bash
# Run this command and copy the output
cat /Users/alikhan/Development/Projects/tennis-script/token.json | tr -d '\n'
```

## Step 4: Add GitHub Secret

1. Go to your repo → **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Name: `GOOGLE_CREDENTIALS_JSON`
4. Value: Paste the output from Step 3
5. Click **Add secret**

## Step 5: Enable the Workflow

1. Go to your repo → **Actions** tab
2. Click **I understand my workflows, go ahead and enable them**
3. The workflow will run automatically every Sunday at 10PM UTC

## Step 6: Test Manually

1. Go to **Actions** tab
2. Click **Weekly Sheet Check**
3. Click **Run workflow** → **Run workflow**
4. Watch it run — should complete in ~10 seconds

## How to Check Results

- **GitHub**: Actions tab → click any run → see logs
- **Google Sheet**: Check if H6:H21 was empty and B41:F42 was filled

## Timezone Note

The cron schedule runs at **10PM UTC**. To run at 10PM your local time:
- If you're in UTC+6 (Almaty): change cron to `0 16 * * 0` (4PM UTC = 10PM local)
- If you're in UTC+5 (Astana): change cron to `0 17 * * 0` (5PM UTC = 10PM local)

Edit `.github/workflows/weekly-check.yml` to change the cron time.
