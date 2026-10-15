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

Implementación de la app completa: `8e9914ada063581aac9ae710392c65e268203182`.
Rama para PR: `touch-haptics`, commit inicial `1f800749f9888b4711764294836123851889a17b`.

- `src/Celeste.Android.Patches/TouchControls.cs`: detecta transiciones de botones táctiles antes de aplicar teclado; incluye hasta 12 botones personalizados y las cuatro flechas.
- `src/Celeste.Android.Patches/StickHaptics.cs`: ejes cada 45°, ventana de adquisición ±5°, rearme a más de 9°, cruces rápidos y continuidad al pasar entre -180° y +180°; silencio al mantener una dirección o entrar en zona muerta.
- `src/Celeste.Android/GameActivity.cs`: puente `AppContext` con `Action<int>`, despacho al hilo UI y control de pausa/destrucción. Códigos: 1=pulsar, 2=soltar, 3=eje. Respeta los ajustes hápticos de Android; API 26 usa ClockTick para soltar.
- `tests/TouchHaptics`: pruebas independientes de FNA, Android y archivos del juego. Ejecutar `dotnet run --project tests/TouchHaptics -c Release`.

La rama para PR tiene seis archivos modificados/añadidos: tres de implementación, dos de pruebas y `.github/workflows/test-touch-haptics.yml`. Conserva el comportamiento de opacidad de upstream. Los cambios de compilación, identidad de la app y releases del fork quedan en `main`.

## Evidencia y límites

- Build de la app completa, pruebas y firma: https://github.com/TheMrAleX/CelesteAndroid-transparencia/actions/runs/38671843840
- APK publicado: https://github.com/TheMrAleX/CelesteAndroid-transparencia/releases/tag/v1.6.0-haptics.1
- SHA-256 APK ARM64: `bd550c11b484fcb8d0de74fe1774512c9945420ed8b01e8497ff3eb0443d4850`
- Application ID: `org.celesteandroid.transparencia`; versionCode 6; versionName `1.6.0-haptics.1`.
- La compilación se verificó; la sensación háptica y el gameplay en un dispositivo físico siguen pendientes. El usuario estaba descargando el APK al preparar esta guía.
- El APK requiere importar los archivos de la copia de Celeste del usuario.

## Antes de publicar otro APK

La compilación Pixel 7 usa una firma temporal del runner. La clave de la versión anterior no se conservó para futuras actualizaciones; no prometer instalación sobre esa versión. Android puede exigir desinstalarla, lo cual elimina los datos privados. Avisar al usuario que respalde partidas antes de desinstalar. Para próximas versiones, configurar una clave de firma persistente protegida y reutilizarla; no publicar claves en texto plano.

`.github/workflows/build-pixel7.yml` tiene versionCode 6, versionName y tag `v1.6.0-haptics.1` fijos. Antes de un nuevo cambio de código en `main`, actualizar estos valores y preparar la publicación para el nuevo tag: el build se activa con cambios de código, pero intentar crear otra vez el tag existente fallará al publicar. No borrar ni reemplazar la release existente. `.github/workflows/publish-joystick.yml` es una publicación histórica con run/tag fijos; no reutilizarla para nuevas versiones.

`CELESTE_REFERENCE_KEY` es un secreto de Actions usado para descifrar la referencia privada durante la compilación. No es una clave de firma. No es necesario leer ni mostrar su valor. El workflow de pruebas de la PR no necesita secretos ni archivos del juego. La compilación Android completa requiere .NET 10 con workload Android, Java 17, SDK 36, dependencias FNA/SDL y las referencias/runtime indicadas en `docs/BUILDING.md` y `scripts/prepare-pixel7.py`.

## Preparación de la PR

Título y descripción: `docs/pull-requests/touch-haptics.md`.
Comparar upstream `main` con `TheMrAleX:touch-haptics`. El usuario pidió abrir personalmente la PR; no se ha enviado automáticamente.

Comprobar nuevamente el estado de upstream y el diff antes de enviar o actualizar la PR. La PR #1 ya fusionada es https://github.com/KaliKylee/CelesteAndroid/pull/1.
