# Behind the Facade — thebtfpodcast.com

Official site for the Melbourne construction podcast hosted by **Jake Gorry** and **Daniel Alizzi**.

Video: [youtube.com/@BehindTheFacadeShow](https://www.youtube.com/@BehindTheFacadeShow)

Repo: https://github.com/jimmyalxndr/thebtfpodcast

Episodes are generated from the live RSS feed at build time. Audio stays on RSS.com.

## Deploy on Netlify

1. Open https://app.netlify.com and sign in.
2. **Add new site → Import an existing project → GitHub**.
3. Authorise Netlify if asked, then pick **jimmyalxndr/thebtfpodcast**.
4. Confirm:
   - Branch: `main`
   - Build command: `python3 build.py`
   - Publish directory: `dist`
5. Deploy.
6. **Domain management → Add a domain you already own → thebtfpodcast.com**
7. At your registrar, add:
   - `A` record `@` → `75.2.60.5`
   - `CNAME` `www` → `YOUR-SITE.netlify.app`
8. Provision HTTPS once DNS verifies.

Then set the podcast website field in RSS.com, Apple, Spotify and YouTube to `https://thebtfpodcast.com`.
