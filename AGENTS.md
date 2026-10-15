# Working on this fork

Read `docs/MAINTAINER_HANDOFF.md` before choosing a branch or preparing an APK/PR.

- `main` is the user's complete app. Preserve its transparency controls, dynamic joystick, editor, custom buttons, application ID, and imported-game behavior.
- `touch-haptics` is the focused upstream contribution based on `KaliKylee/CelesteAndroid:main`. Keep its diff restricted to touch haptics, tests, and test CI.
- `touch-options` is the previous dynamic-joystick contribution, already merged upstream as PR #1. Preserve it as a historical reference.
- Start each new upstream contribution from a freshly fetched upstream default branch. Do not open PRs from this fork's `main`: it contains fork-specific releases, build tooling, and opacity changes.
- Never commit plaintext game executables, assets, signing keys, or secret values. The encrypted compile reference and Pixel 7 preparation workflow belong only to the complete-app branch.
- Do not claim a device test unless someone actually performed it. CI/build/signature verification and physical gameplay/haptic testing are separate evidence.
- Before publishing another APK, address the signing/version/release-tag limitations documented in the handoff. Never overwrite an already published release with a different APK.

For joystick logic: `dotnet run --project tests/TouchHaptics -c Release` (requires .NET 10). See the handoff for Android build requirements and verified CI links.
