# Deploying to GitHub Pages

Step-by-step. The whole flow takes about 5 minutes once you have a GitHub account ready.

## Prerequisites

- A GitHub account with access to the `thepandanlabs` organization (or rename the repo to your own user/org).
- `git` installed locally.
- This directory on your machine.

## 1. Create the repository on GitHub

1. Go to https://github.com/organizations/thepandanlabs/repositories/new (or your user's New Repo page).
2. **Repository name:** `claude-code-workshop`
3. **Description:** *Do It Once, Then Never Again — a 3-hour Claude Code workshop kit by Pandan Labs.*
4. **Visibility:** Public (required for free GitHub Pages).
5. **Do NOT** initialize with a README, .gitignore, or license — this directory already has those.
6. Click **Create repository**.

## 2. Push this directory

From inside this folder:

```bash
cd /path/to/claude-code-workshop

git init
git add .
git commit -m "Initial workshop kit"

git branch -M main
git remote add origin https://github.com/thepandanlabs/claude-code-workshop.git
git push -u origin main
```

If you prefer SSH:

```bash
git remote add origin git@github.com:thepandanlabs/claude-code-workshop.git
```

## 3. Enable GitHub Pages

1. On GitHub, go to https://github.com/thepandanlabs/claude-code-workshop/settings/pages.
2. Under **Source**, choose **Deploy from a branch**.
3. **Branch:** `main`. **Folder:** `/ (root)`. Click **Save**.
4. GitHub starts the first Pages build. Refresh after about 60 seconds. You'll see a green "Your site is live at..." banner.

## 4. Verify

Open https://thepandanlabs.github.io/claude-code-workshop/ in a browser.

- The landing page should render with the dark theme and orange accent.
- Click any "Open Block" or "View Template" link — `viewer.html` should load the Markdown.
- Open DevTools → Network tab → reload. Confirm no 404s.

## 5. Common gotchas

**The page is blank or shows 404.**
First-time Pages builds take up to 5 minutes. Wait. If still broken after 5 minutes, check **Actions → Pages** for build errors.

**Links work on home but Markdown pages 404.**
You opened `index.html` via `file://` instead of `http://`. Markdown loading uses `fetch()` which is blocked on `file://`. Always use a server — locally `python3 -m http.server 8080`, in production GitHub Pages.

**Pages says "Your site is published at..." but URL returns 404.**
Wait another minute. The first deploy after enabling Pages is the slowest.

**You see your `README.md` rendered as the home page instead of `index.html`.**
That means Pages picked Jekyll. Add an empty `.nojekyll` file at the root, commit, push.

```bash
touch .nojekyll
git add .nojekyll
git commit -m "Disable Jekyll"
git push
```

(GitHub Pages auto-detects `index.html` and serves it as the root by default, so this is usually not needed — but if it happens, that's the fix.)

## 6. Iterating after the first deploy

Edit files locally. Then:

```bash
git add .
git commit -m "Update <whatever>"
git push
```

Pages rebuilds within 30–60 seconds. Hard-refresh your browser (`Cmd+Shift+R` or `Ctrl+Shift+R`) to bypass cache.

## 7. Custom domain (optional)

If you later want to put this at, say, `workshop.pandanlabs.io`:

1. Add a `CNAME` file at the repo root containing `workshop.pandanlabs.io` (no protocol, no path).
2. In your DNS provider, create a CNAME record for `workshop.pandanlabs.io` pointing to `thepandanlabs.github.io`.
3. In **Settings → Pages → Custom domain**, enter `workshop.pandanlabs.io` and save.
4. Wait for DNS to propagate (usually a few minutes). Then check **Enforce HTTPS**.

GitHub Pages handles the TLS certificate automatically via Let's Encrypt.

## 8. What about analytics?

Not included by default — this is a workshop site, not a product. If you want a count of views:

- The lightest path is to add Plausible (`<script defer data-domain="..." src="https://plausible.io/js/script.js"></script>`) inside `<head>` of both `index.html` and `viewer.html`.
- Alternatively, Cloudflare Web Analytics is free and similarly lightweight.

Neither tracks individuals. Both are GDPR-friendly. Avoid Google Analytics if your audience cares about privacy.

## 9. Sharing the site

Once live, share:

- The main URL: `https://thepandanlabs.github.io/claude-code-workshop/`
- The repo: `https://github.com/thepandanlabs/claude-code-workshop`

In the workshop WhatsApp group, pin both.

---

From Pandan Labs with ♥
