# Kneeds.Knows on Squarespace — setup guide

These files turn your Squarespace site into the Kneeds.Knows multi-page
experience. Every file is a copy-paste snippet — nothing here gets uploaded
to Squarespace as a build artifact, you just paste it into the right field
in the Squarespace dashboard.

## 0. One-time prep

### 0a. Upload the logo
1. Squarespace dashboard → **Design → Custom CSS** (or **Settings → Advanced
   → File Manager**, depending on plan) → upload `assets/logo.png` (run the
   processor in `../assets/process_logo.py` first).
2. Click the uploaded file → **Use a different URL** → copy the URL. It
   looks like `https://static1.squarespace.com/static/<id>/.../logo.png`.
3. **In every snippet in this folder**, find/replace `__LOGO_URL__` with
   that URL. Tip: do this once in the global CSS injection (step 1) and
   the Code Blocks pick it up automatically.

### 0b. Confirm your API URL
The subscribe form posts to your Render API. Default URL in these files:
```
https://kneedsknows-newsletter.onrender.com
```
If yours is different, find/replace it in `06-subscribe.html`.

## 1. Install the global CSS (one time, site-wide)

1. Squarespace dashboard → **Settings → Advanced → Code Injection**.
2. Copy the entire contents of `00-header-code-injection.html`.
3. Paste it into the **HEADER** field. Save.

This loads the Montserrat font and defines every `.kk-*` style class the
page-specific Code Blocks use. Every page that contains a `kk-*` Code Block
will pick up the brand styling automatically.

## 2. Create the pages

For each of the five new pages, in Squarespace:

1. **Pages panel → "+" → Page → Blank Layout** (not a template).
2. Set the URL slug per the table below.
3. Add a **Section** with a black background (Edit Section → Colors → set
   background to `#0a0a0a`).
4. Inside that section, add a **Code Block**.
5. Paste the matching file from this folder into the Code Block.
6. Toggle **Display Source** OFF. Save.

| Page         | URL slug      | Code Block file              | Notes |
|--------------|---------------|------------------------------|-------|
| Home         | `/`           | `01-home.html`               | Make this the **Set as Homepage** page in the Pages panel |
| Store        | `/store`      | `02-store-hero.html`         | See **§3 Store** below for the Commerce side |
| Deals        | `/deals`      | `03-deals.html`              | Drop one card per affiliate partner |
| Newsletter   | `/newsletter` | `04-newsletter.html`         | Paste your Substack/Beehiiv embed in the slot |
| Book         | `/book`       | `05-book.html`               | Add your Calendly + GoFundMe URLs |
| Subscribe    | `/subscribe`  | `06-subscribe.html`          | Replaces your existing signup page |

## 3. Store page (Squarespace Commerce)

1. Make `/store` a **Products** page (Pages panel → "+" → **Products**),
   not a blank page.
2. At the top of the Products page, add a **Section** → **Code Block** and
   paste `02-store-hero.html`. This gives you a branded hero above
   Squarespace's native product grid.
3. Add products via Squarespace's normal Products UI. The grid styling is
   handled by your Squarespace template — the global CSS injection nudges
   it toward the brand palette but won't override Squarespace's checkout.

## 4. Site navigation

Once the pages exist:

1. **Pages panel** → drag the five new pages into the **Main Navigation**
   group in this order: Home · Store · Deals · Newsletter · Book ·
   Subscribe.
2. The Subscribe page can optionally live in the **Not Linked** group with
   a button in the header pointing to it — your call.
3. The global CSS gives the Squarespace nav itself the brand color
   treatment (magenta→cyan CTA pill on the Subscribe link, etc.) — see
   the `.header-nav` rules in `00-header-code-injection.html`.

## 5. Sanity check

- [ ] Logo shows in the header (and isn't a broken image — `__LOGO_URL__`
      replaced everywhere)
- [ ] Subscribe form actually submits (test once, then check Render logs)
- [ ] Calendly inline widget appears on /book (you replaced the
      `data-url` attribute)
- [ ] Substack/Beehiiv iframe shows recent posts on /newsletter
- [ ] GoFundMe button on /book goes to your real campaign URL
- [ ] Affiliate buttons on /deals open in a new tab and point at real
      affiliate URLs
- [ ] Products page shows your products with a clean hero on top

## 6. Updating later

Everything is plain copy/paste. To change a price, swap a card, or update
copy: edit the Code Block in Squarespace directly. To change colors site-
wide: edit the global CSS injection in **Settings → Advanced → Code
Injection → Header**. You don't need this repo at runtime.
