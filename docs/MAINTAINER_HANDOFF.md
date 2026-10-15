# Guía de continuidad del fork

Estado verificado el 15 de octubre de 2026 (UTC).

## Repositorios y ramas

- Fork: https://github.com/TheMrAleX/CelesteAndroid-transparencia
- Upstream de Kyle: https://github.com/KaliKylee/CelesteAndroid

| Rama | Uso | Base/estado |
| --- | --- | --- |
| `main` | App completa del usuario; versiones APK | Transparencia + joystick dinámico + editor + botones personalizados + feedback háptico |
| `touch-options` | Contribución anterior de joystick dinámico | Integrada por Kyle en la PR #1; conservar como referencia histórica |
| `touch-haptics` | Nueva contribución de feedback háptico | Basada en upstream `f7e6759b68fadb4d16be164223ec8745abb34433`, posterior a la PR #1 |

No se han borrado ni renombrado ramas. Para una nueva función de la app personal, partir de `main`. Para contribuir a Kyle, actualizar upstream y crear una rama dedicada desde su `main`, pasando solo los cambios pertinentes. No fusionar toda la app personalizada en una rama para PR.

## Feedback háptico

Implementación inicial: `8e9914ada063581aac9ae710392c65e268203182`. Ajustes configurables: `f92325b7c5a9741648e849e077b0e0ab2807ac8f`.
Rama para PR: `touch-haptics`; ajustes configurables en `53672b9789b47e0397eace801c4468218bad2f39`.

- `src/Celeste.Android.Patches/TouchControls.cs`: detecta transiciones de botones táctiles antes de aplicar teclado; incluye hasta 12 botones personalizados y las cuatro flechas.
- `src/Celeste.Android.Patches/StickHaptics.cs`: ejes cada 45°, ventana de adquisición ±5°, rearme a más de 9°, cruces rápidos y continuidad al pasar entre -180° y +180°; silencio al mantener una dirección o entrar en zona muerta.
- `src/Celeste.Android/GameActivity.cs`: puente `AppContext` con `Action<int>`, despacho al hilo UI y control de pausa/destrucción. Códigos: 1=pulsar, 2=soltar, 3=eje. Delega en `TouchVibration` con los ajustes enviados por Intent desde el launcher.
- `src/Celeste.Android/HapticsSettings.cs`: Opciones → Vibración; activación, pulsar/soltar/ambos, intensidad 0–100%, joystick y prueba antes de guardar. Todos los textos están localizados en los diez idiomas de la app.
- `src/Celeste.Android/HapticPolicy.cs` y `TouchVibration.cs`: filtrado de eventos, intensidad por amplitud o duración de respaldo y respeto del ajuste táctil de Android. `GameOptions` guarda preferencias; el launcher las envía al proceso `:game` mediante Intent para evitar cachés desactualizadas entre procesos.
- `tests/TouchHaptics`: pruebas independientes de FNA, Android y archivos del juego. Ejecutar `dotnet run --project tests/TouchHaptics -c Release`.

La rama para PR incluye implementación háptica, panel de ajustes, localización, documentación, pruebas y `.github/workflows/test-touch-haptics.yml`. Conserva el comportamiento de opacidad de upstream. Los cambios de compilación, identidad de la app y releases del fork quedan en `main`.

## Evidencia y límites

- Build de la app completa, pruebas y firma: https://github.com/TheMrAleX/CelesteAndroid-transparencia/actions/runs/38673966966
- Pruebas de la rama PR: https://github.com/TheMrAleX/CelesteAndroid-transparencia/actions/runs/38673984176
- Configuración y prueba: `docs/VIBRATION.md`.
- APK publicado: https://github.com/TheMrAleX/CelesteAndroid-transparencia/releases/tag/v1.6.0-haptics.2
- SHA-256 APK ARM64: `51516a7d65c372cd52ea72e815d978dae3d8d194664171bb242bff9f338e065d`
- Application ID: `org.celesteandroid.transparencia`; versionCode 7; versionName `1.6.0-haptics.2`.
- La compilación se verificó; la sensación háptica y el gameplay en un dispositivo físico siguen pendientes. Los ajustes y su vista previa siguen pendientes de validación física.
- El APK requiere importar los archivos de la copia de Celeste del usuario.

## Firma y próximas versiones

La release `v1.6.0-haptics.2` cambia de la firma temporal de las versiones anteriores a una clave persistente RSA 3072. Al instalar sobre una versión anterior puede requerirse desinstalar: respaldar partidas antes de hacerlo. Desde esta release, las siguientes compilaciones pueden actualizar usando la misma firma.

`scripts/prepare-release-signing.py` recupera la clave desde el asset `CelesteAndroid-signing-key.enc` de **v1.6.0-haptics.2**. Esa referencia es canónica: no cambiar `signing_tag` al subir la versión de la app y no borrar ni reemplazar ese asset. La copia usa AES-GCM autenticado con una clave derivada por dominio del secreto `CELESTE_REFERENCE_KEY`; no contiene material de firma accesible en texto plano. La clave privada y contraseña descifradas solo existen en el runner. Si la referencia no se puede autenticar o falta en una release existente, el build falla en vez de cambiar de firma. No divulgar ni regenerar el secreto privado sin un plan de migración/recuperación.

En `.github/workflows/build-pixel7.yml`, subir `APP_VERSION_CODE` (actual: 7), `APP_VERSION_NAME` (actual: `1.6.0-haptics.2`) y `RELEASE_TAG` para publicar otra versión. La referencia canónica de firma permanece en v1.6.0-haptics.2. Los builds se serializan para evitar carreras al inicializar la firma. El build se activa con cambios de código; preparar primero un tag/versionCode nuevos. No borrar ni reemplazar una release publicada. `.github/workflows/publish-joystick.yml` es histórica: no reutilizarla.

`CELESTE_REFERENCE_KEY` también descifra la referencia de compilación, pero no es por sí misma una clave APK: se usa una derivación separada para proteger la copia de firma. No es necesario leer ni mostrar su valor. La rama PR no incorpora scripts de firma, backups cifrados ni workflows de release del fork.

El workflow de pruebas de la PR no requiere secretos ni archivos del juego. La compilación Android completa requiere .NET 10 con workload Android, Java 17, SDK 36 y las referencias/runtime descritas en `docs/BUILDING.md` y `scripts/prepare-pixel7.py`.

## Preparación de la PR

Título y descripción: `docs/pull-requests/touch-haptics.md`.
Comparar upstream `main` con `TheMrAleX:touch-haptics`. El usuario pidió abrir personalmente la PR; no se ha enviado automáticamente.

Comprobar nuevamente el estado de upstream y el diff antes de enviar o actualizar la PR. La PR #1 ya fusionada es https://github.com/KaliKylee/CelesteAndroid/pull/1.
