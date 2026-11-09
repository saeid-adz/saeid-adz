# Profile artwork

These local graphics are used by the root GitHub profile README:

- `mission-control.gif`: a 6.4-second loop with a floating cloud and moving signals.
- `automation-loop.gif`: an 8.8-second illustrated terminal sequence.
- `*-still.png`: static alternatives linked from the profile.

Regenerate from the repository root with:

```sh
python3 -m pip install Pillow
python3 scripts/generate_profile_assets.py
```

The generator uses Arial on macOS or DejaVu Sans on Linux. The graphics use
GitHub-compatible GIFs, without JavaScript, embedded styles, or remote animation
services. The terminal is an illustration, not a real deployment or live status.
