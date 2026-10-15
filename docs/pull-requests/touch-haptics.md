# Add haptic feedback to touch controls and 45-degree joystick axes

Touch buttons now provide haptic feedback when pressed and released, including custom buttons and D-pad arrows. Fixed and dynamic joysticks tick when reaching or crossing any of the eight axes spaced 45 degrees apart.

The joystick uses a 5-degree acquisition window and 9-degree rearm distance to suppress jitter, detects fast crossings between input samples, and resets in the dead zone. Android feedback runs on the UI thread, respects system touch-feedback settings, and stops while the activity is paused. Android 8.0 uses a compatible release-feedback fallback.

Validation:
- Automated .NET tests cover all eight axes, holding, jitter, fast crossings in both directions, angle wrapping, neutral reset, and repeated rotations.
- A GitHub Actions workflow runs these tests without game files or secrets.
- The same haptic implementation compiled successfully in the full fork's ARM64 Release APK, with its signature verified.
- Physical-device haptic feel and gameplay testing are still pending.

Based on the current upstream main after PR #1.

---

[Open the prefilled pull request](https://github.com/KaliKylee/CelesteAndroid/compare/main...TheMrAleX:touch-haptics?expand=1&title=Add%20haptic%20feedback%20to%20touch%20controls%20and%2045-degree%20joystick%20axes&body=Touch%20buttons%20now%20provide%20haptic%20feedback%20when%20pressed%20and%20released%2C%20including%20custom%20buttons%20and%20D-pad%20arrows.%20Fixed%20and%20dynamic%20joysticks%20tick%20when%20reaching%20or%20crossing%20any%20of%20the%20eight%20axes%20spaced%2045%20degrees%20apart.%0A%0AThe%20joystick%20uses%20a%205-degree%20acquisition%20window%20and%209-degree%20rearm%20distance%20to%20suppress%20jitter%2C%20detects%20fast%20crossings%20between%20input%20samples%2C%20and%20resets%20in%20the%20dead%20zone.%20Android%20feedback%20runs%20on%20the%20UI%20thread%2C%20respects%20system%20touch-feedback%20settings%2C%20and%20stops%20while%20the%20activity%20is%20paused.%20Android%208.0%20uses%20a%20compatible%20release-feedback%20fallback.%0A%0AValidation%3A%0A-%20Automated%20.NET%20tests%20cover%20all%20eight%20axes%2C%20holding%2C%20jitter%2C%20fast%20crossings%20in%20both%20directions%2C%20angle%20wrapping%2C%20neutral%20reset%2C%20and%20repeated%20rotations.%0A-%20A%20GitHub%20Actions%20workflow%20runs%20these%20tests%20without%20game%20files%20or%20secrets.%0A-%20The%20same%20haptic%20implementation%20compiled%20successfully%20in%20the%20full%20fork's%20ARM64%20Release%20APK%2C%20with%20its%20signature%20verified.%0A-%20Physical-device%20haptic%20feel%20and%20gameplay%20testing%20are%20still%20pending.%0A%0ABased%20on%20the%20current%20upstream%20main%20after%20PR%20%231.)
