# Publishing setup — Samira’s English Hub

The design and content system are already built. These are the one-time account steps needed to make the site live and enable the `/admin/` editor.

## 1. Create the GitHub repository

Create a public GitHub repository named `samiras-english-hub` and upload/push this project to its `main` branch.

Then edit `admin/config.yml` and replace:

- `andalib-sa/samiras-english-hub` with your real GitHub username/repository.

## 2. Enable GitHub Pages

In the GitHub repository:

**Settings → Pages → Build and deployment → Source → GitHub Actions**

The included workflow builds the site and publishes `_site` automatically whenever content is changed.

The default address will be similar to:

`https://andalib-sa.github.io/samiras-english-hub/`

## 3. Enable Decap CMS login

Decap's GitHub backend needs an OAuth authentication service. The official Decap documentation supports using Netlify for GitHub authentication even when the main site is hosted elsewhere.

Create a free Netlify project to use only for authentication. You do not need to move the main website to Netlify.

### GitHub OAuth app

In GitHub Developer Settings, create a new OAuth App.

- Homepage URL: your Netlify auth-project URL
- Authorization callback URL: `https://api.netlify.com/auth/done`

Generate a client secret and keep it private.

### Netlify

In your Netlify project, add GitHub as an authentication provider and enter the GitHub OAuth Client ID and Client Secret.

Then edit `admin/config.yml` and replace:

`YOUR_NETLIFY_AUTH_SITE.netlify.app`

with the Netlify project's real domain.

After the next GitHub Pages deploy, open:

`https://andalib-sa.github.io/samiras-english-hub/admin/`

and log in with the GitHub account that owns or has push access to the repository.

## 4. Editing the site after setup

From `/admin/` you can:

- Add, remove or edit learning resources
- Assign skills: listening, speaking, reading, writing or practice
- Assign learner levels
- Mark a resource as Australia-focused
- Feature a resource on the homepage
- Edit the homepage/about text
- Upload a welcome audio file

Every CMS publish creates a Git commit. The included GitHub Action then rebuilds and publishes the website automatically.

## 5. Contact form

During migration, the Contact button points to the existing Weebly contact page. When ready, replace `contact_url` in Site Settings with your preferred contact form or email service.

## 6. Optional custom domain

You can stay on the free `github.io` address. Later, if you buy a domain such as `samirasenglishhub.com`, GitHub Pages supports custom domains and HTTPS.
