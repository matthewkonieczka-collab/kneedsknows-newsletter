# Site assets

## Adding your logo

1. Save your original logo (the JPEG you sent) into this folder as
   **`logo-source.png`** (or `.jpg`). Keep the original quality.

2. Make sure Pillow is installed:
   ```
   pip install Pillow
   ```

3. Run the processor:
   ```
   python content-pipeline/landing-page/assets/process_logo.py
   ```

It generates four cleaned files next to the source:

| File              | Where it's used               | Size       |
|-------------------|-------------------------------|------------|
| `logo.png`        | Top-left brand in every page nav | width ~800 |
| `logo-mark.png`   | Standalone "K" mark (large)    | 1024x1024  |
| `favicon.png`     | Browser tab icon               | 32x32      |
| `favicon-180.png` | iOS home-screen icon           | 180x180    |

The processor snaps near-white pixels to pure white (killing any JPEG fuzz
around the logo) and trims excess margin so the artwork sits cleanly in the
navigation bar.

If the "K" mark extraction misses the symbol on your particular file, edit
`TOP_PCT` in `process_logo.py` (currently 0.62) until the crop looks right.
