
#!/usr/bin/env python3
"""
Image Encryptor: simple, reversible pixel manipulation (XOR + Shuffle).

Usage examples:
  python main.py encrypt -i input.jpg -o encrypted.png -p "myPassword" -m both
  python main.py decrypt -i encrypted.png -o restored.jpg -p "myPassword" -m both

⚠️ Educational only. Not a replacement for strong cryptography.
"""
import argparse
import hashlib
import os
from typing import Tuple

import numpy as np
from PIL import Image


# ------------------ Key material helpers ------------------

def derive_key_byte(password: str) -> int:
    """Derive a single byte (0..255) from the password using SHA-256."""
    h = hashlib.sha256(password.encode("utf-8")).digest()
    return h[0]  # first byte


def derive_seed(password: str) -> int:
    """Derive a 64-bit seed from the password using SHA-256."""
    h = hashlib.sha256(password.encode("utf-8")).digest()
    # Map 256-bit hash to 64-bit integer
    return int.from_bytes(h[:8], "big", signed=False)


# ------------------ Core transforms ------------------

def xor_transform(arr: np.ndarray, key_byte: int) -> np.ndarray:
    """XOR every byte in the image array with key_byte (reversible)."""
    # arr is uint8, XOR works directly
    return arr ^ np.uint8(key_byte)


def permutation_for_length(n: int, seed: int) -> np.ndarray:
    """Return a deterministic permutation of range(n) from a seed."""
    rng = np.random.default_rng(seed)
    return rng.permutation(n)


def apply_shuffle(arr: np.ndarray, seed: int, encrypt: bool) -> np.ndarray:
    """
    Shuffle or unshuffle the flattened bytes of the image using
    a deterministic permutation derived from seed.
    """
    flat = arr.reshape(-1)
    perm = permutation_for_length(flat.size, seed)

    if encrypt:
        shuffled = flat[perm]
        return shuffled.reshape(arr.shape)
    else:
        inv = np.empty_like(perm)
        inv[perm] = np.arange(perm.size, dtype=perm.dtype)
        unshuffled = flat[inv]
        return unshuffled.reshape(arr.shape)


# ------------------ I/O helpers ------------------

ALLOWED_MODES = {"L", "RGB", "RGBA"}

def load_image_as_array(path: str) -> Tuple[np.ndarray, str]:
    """Load an image to a numpy uint8 array and return (array, mode)."""
    img = Image.open(path)
    mode = img.mode
    if mode not in ALLOWED_MODES:
        # Convert uncommon modes to RGBA for consistent, lossless bytes
        img = img.convert("RGBA")
        mode = img.mode
    arr = np.array(img, dtype=np.uint8)
    return arr, mode


def save_array_as_image(arr: np.ndarray, mode: str, out_path: str) -> None:
    """Save numpy array back to an image. Defaults to PNG if no extension."""
    root, ext = os.path.splitext(out_path)
    if not ext:
        out_path = root + ".png"
    img = Image.fromarray(arr, mode=mode)
    img.save(out_path)


# ------------------ Pipeline ------------------

def process(in_path: str, out_path: str, password: str, mode: str, action: str) -> None:
    """
    mode: "xor", "shuffle", or "both"
    action: "encrypt" or "decrypt"
    """
    arr, img_mode = load_image_as_array(in_path)

    key_byte = derive_key_byte(password)
    seed = derive_seed(password)

    if mode not in {"xor", "shuffle", "both"}:
        raise ValueError("mode must be one of: xor, shuffle, both")

    if action not in {"encrypt", "decrypt"}:
        raise ValueError("action must be 'encrypt' or 'decrypt'")

    # Apply transforms. "both" means XOR first, then Shuffle (encrypt),
    # and unshuffle then XOR (decrypt).
    if action == "encrypt":
        if mode in {"xor", "both"}:
            arr = xor_transform(arr, key_byte)
        if mode in {"shuffle", "both"}:
            arr = apply_shuffle(arr, seed, encrypt=True)
    else:  # decrypt
        if mode in {"shuffle", "both"}:
            arr = apply_shuffle(arr, seed, encrypt=False)
        if mode in {"xor", "both"}:
            arr = xor_transform(arr, key_byte)

    save_array_as_image(arr, img_mode, out_path)


# ------------------ CLI ------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Simple image encryption/decryption via pixel XOR and byte shuffling (educational)."
    )
    sub = p.add_subparsers(dest="command", required=True)

    def add_common(sp):
        sp.add_argument("-i", "--in", dest="in_path", required=True, help="Input image path")
        sp.add_argument("-o", "--out", dest="out_path", required=True, help="Output image path")
        sp.add_argument("-p", "--password", required=True, help="Password (used to derive key and seed)")
        sp.add_argument(
            "-m", "--mode",
            choices=["xor", "shuffle", "both"],
            default="both",
            help="Which transform(s) to apply (default: both)"
        )

    pe = sub.add_parser("encrypt", help="Encrypt an image")
    add_common(pe)

    pd = sub.add_parser("decrypt", help="Decrypt an image")
    add_common(pd)

    return p


def main():
    parser = build_parser()
    args = parser.parse_args()

    process(
        in_path=args.in_path,
        out_path=args.out_path,
        password=args.password,
        mode=args.mode,
        action=args.command,
    )


if __name__ == "__main__":
    main()
