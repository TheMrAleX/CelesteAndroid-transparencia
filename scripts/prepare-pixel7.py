"""Prepare private compile reference and verified ARM64 runtime libraries."""
import gzip
import hashlib
import os
from pathlib import Path
import subprocess
import urllib.request
import zipfile

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

root = Path(__file__).resolve().parent.parent
key = os.environ.get("CELESTE_REFERENCE_KEY", "").strip()
if len(key) != 64:
    raise SystemExit("Set the CELESTE_REFERENCE_KEY Actions secret to the supplied 64-character key.")
encrypted = (root / "build-inputs/celeste-reference.enc").read_bytes()
if encrypted[:8] != b"CELESTE1":
    raise SystemExit("Invalid encrypted reference format")
try:
    plain = gzip.decompress(AESGCM(bytes.fromhex(key)).decrypt(
        encrypted[8:20], encrypted[20:], b"CelesteAndroid build reference"
    ))
except Exception:
    raise SystemExit("The reference key is incorrect or the encrypted file is damaged.") from None
game = root / "Celeste"
game.mkdir(exist_ok=True)
(game / "Celeste.exe").write_bytes(plain)

work = root / "build/pixel7"
work.mkdir(parents=True, exist_ok=True)
apk = work / "upstream.apk"
url = "https://github.com/BelmanteGu/CelesteAndroid/releases/download/v1.0.1/CelesteAndroid-1.0.1.apk"
urllib.request.urlretrieve(url, apk)
if hashlib.sha256(apk.read_bytes()).hexdigest() != "3d5c5817d17611ae57e7a79be1311dddf9f966f597408273977134873932a146":
    raise SystemExit("Upstream APK checksum mismatch")
native = root / "natives/android-arm64"
fmod = root / "fmod/libs/android-arm64"
native.mkdir(parents=True, exist_ok=True)
fmod.mkdir(parents=True, exist_ok=True)
with zipfile.ZipFile(apk) as z:
    for name in ("libSDL3.so", "libFNA3D.so", "libFAudio.so", "libfmod.so", "libfmodstudio.so"):
        target = fmod if name.startswith("libfmod") else native
        (target / name).write_bytes(z.read("lib/arm64-v8a/" + name))

# Recover the matching FMOD Java helper from the same verified APK.
jadx_zip = work / "jadx.zip"
urllib.request.urlretrieve("https://github.com/skylot/jadx/releases/download/v1.5.3/jadx-1.5.3.zip", jadx_zip)
with zipfile.ZipFile(jadx_zip) as z:
    z.extractall(work / "jadx")
jar = work / "jadx/lib/jadx-1.5.3-all.jar"
sources = work / "recovered"
subprocess.run(["java", "-cp", str(jar), "jadx.cli.JadxCLI", "--no-res", "-d", str(sources), str(apk)], check=True)
java_dir = sources / "sources/org/fmod"
codec = java_dir / "MediaCodec.java"
text = codec.read_text()
# JADX introduces a conflicting import and loses this register's field name.
text = text.replace("import android.media.MediaCodec;\n", "")
text = text.replace("j2 * r2", "j2 * this.mSampleRate")
text = text.replace("MediaCodec.CryptoException", "android.media.MediaCodec.CryptoException")
text = text.replace("MediaCodec.BufferInfo", "android.media.MediaCodec.BufferInfo")
codec.write_text(text)
classes = work / "fmod-classes"
classes.mkdir(exist_ok=True)
sdk = Path(os.environ["ANDROID_HOME"])
subprocess.run(["javac", "--release", "8", "-classpath", str(sdk / "platforms/android-36/android.jar"), "-d", str(classes), *map(str, sorted(java_dir.glob("*.java")))], check=True)
subprocess.run(["jar", "cf", str(fmod / "fmod.jar"), "-C", str(classes), "."], check=True)
print("Compile reference and ARM64 libraries are ready.")
