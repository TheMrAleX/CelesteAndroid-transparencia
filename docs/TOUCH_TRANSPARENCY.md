# Button transparency

Options → Button transparency opens a slider and a live preview.

- 0% transparency = solid buttons; 100% = invisible buttons that still accept touch.
- Save stores the value in the existing `touch_opacity` preference; Cancel/back leaves the saved value unchanged.
- The setting is applied when starting the game. The controls editor uses the same preference.
- Controls with an individual opacity keep their override. Select “Use global opacity” in the controls editor to include them.
- Button opacity now maps linearly: 45% opacity renders at 45%, rather than the previous 90%. Existing stored percentages are preserved.
- The controls editor keeps a faint global preview at very low opacity so controls can still be positioned.

## APK for Pixel 7 Pro

Build the `arm64-v8a` variant using the existing `Build APK` GitHub Actions workflow or `scripts/build-release.ps1 -Abi arm64-v8a`.
The repository does not contain the required Celeste FNA `Celeste.exe` or FMOD 1.10.14 Android libraries. For Actions, configure `CELESTE_ZIP_URL` and `FMOD_ZIP_URL` as documented in `BUILDING.md`. The existing workflow builds both ARM variants, so its FMOD archive must include both.
Download the `CelesteAndroid-apk-android-arm64` artifact after a successful run; unzip it to obtain the APK. The APK does not bundle the game.

## Validation status

Source diff and C# syntax are checked. APK compilation and on-device behavior require the missing build inputs and Android/.NET toolchain; they have not been verified.

Device checks after building:
1. Move the slider to 0%, 50%, 100% and verify the preview.
2. Save, reopen the dialog and restart the app: the percentage should persist.
3. Move the slider then Cancel/back: the saved percentage must stay unchanged.
4. Start the game and check the standard and custom buttons, including while pressed.
5. Check an individual opacity override and “Use global opacity”.
6. Verify the dialog scrolls in landscape on the phone.
