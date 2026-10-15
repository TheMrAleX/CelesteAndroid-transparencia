"""Restore a persistent APK key from its encrypted release backup, or bootstrap it.

The first settings release is the immutable key source for future builds. Only the
AES-GCM encrypted backup is published; the private key and password stay on runner.
"""
import base64
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess
import urllib.error
import urllib.request
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

root = Path(__file__).resolve().parent.parent
signing_tag = "v1.6.0-haptics.2"  # Keep this fixed when bumping the app release version.
repo = "TheMrAleX/CelesteAndroid-transparencia"
asset = "CelesteAndroid-signing-key.enc"
header = b"CELESTE-SIGN2"
aad = b"CelesteAndroid persistent APK signing backup v1"
raw_key = bytes.fromhex(os.environ["CELESTE_REFERENCE_KEY"].strip())
if len(raw_key) != 32:
    raise SystemExit("Invalid signing backup encryption input")
key = hashlib.sha256(aad + raw_key).digest()
work = root / "build/signing"
work.mkdir(parents=True, exist_ok=True)
store = work / "release.keystore"
out = root / "out"
out.mkdir(exist_ok=True)
backup = out / asset
url = f"https://github.com/{repo}/releases/download/{signing_tag}/{asset}"
try:
    with urllib.request.urlopen(url) as response:
        encrypted = response.read()
except urllib.error.HTTPError as error:
    if error.code != 404:
        raise
    # An existing canonical release without the key is an error, not permission
    # to silently generate a replacement key and break Android upgrades.
    try:
        urllib.request.urlopen(f"https://api.github.com/repos/{repo}/releases/tags/{signing_tag}")
    except urllib.error.HTTPError as release_error:
        if release_error.code != 404:
            raise
    else:
        raise SystemExit("Canonical signing release exists but its encrypted key is missing")
    password = secrets.token_urlsafe(32)
    os.environ["CELESTE_SIGN_PASS"] = password
    subprocess.run([
        "keytool", "-genkeypair", "-noprompt", "-storetype", "PKCS12",
        "-keystore", str(store), "-storepass:env", "CELESTE_SIGN_PASS",
        "-keypass:env", "CELESTE_SIGN_PASS", "-alias", "celeste",
        "-keyalg", "RSA", "-keysize", "3072", "-validity", "10000",
        "-dname", "CN=CelesteAndroid Personal Fork"
    ], check=True)
    payload = json.dumps({"password": password, "key": base64.b64encode(store.read_bytes()).decode()}).encode()
    nonce = secrets.token_bytes(12)
    encrypted = header + nonce + AESGCM(key).encrypt(nonce, payload, aad)
else:
    if not encrypted.startswith(header):
        raise SystemExit("Invalid signing backup header")
    start = len(header)
    try:
        payload = AESGCM(key).decrypt(encrypted[start:start+12], encrypted[start+12:], aad)
        bundle = json.loads(payload)
        password = bundle["password"]
        store.write_bytes(base64.b64decode(bundle["key"], validate=True))
    except Exception:
        raise SystemExit("Signing backup could not be authenticated; refusing to replace the APK key") from None
backup.write_bytes(encrypted)
print(f"::add-mask::{password}")
with open(os.environ["GITHUB_ENV"], "a") as env:
    env.write(f"CELESTE_SIGN_STORE={store}\nCELESTE_SIGN_PASS={password}\n")
print("Persistent release key ready; only its encrypted backup will be published.")
