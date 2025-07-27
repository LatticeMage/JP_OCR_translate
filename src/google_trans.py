# google_trans.py

import sys
import asyncio

# try async googletrans first
try:
    from googletrans import Translator as AsyncTranslator
    GOOGLETRANS_ASYNC_AVAILABLE = True
except ImportError:
    GOOGLETRANS_ASYNC_AVAILABLE = False

import requests

async def _translate_with_googletrans(text: str) -> str:
    async with AsyncTranslator() as translator:
        res = await translator.translate(text, src='ja', dest='zh-tw')
        return res.text

def _translate_with_web_api(text: str) -> str:
    url = "https://translate.googleapis.com/translate_a/single"
    params = {
        "client": "gtx",
        "sl": "ja",
        "tl": "zh-TW",
        "dt": "t",
        "q": text,
    }
    resp = requests.get(url, params=params, timeout=5)
    resp.raise_for_status()
    data = resp.json()
    # data[0] is list of [translated_segment, original, ...]
    return "".join(seg[0] for seg in data[0])

def translate_text(text: str) -> str:
    """
    Translate Japanese text into Traditional Chinese.
    Tries async googletrans first (if installed), otherwise falls back to the web API.
    """
    if GOOGLETRANS_ASYNC_AVAILABLE:
        try:
            return asyncio.run(_translate_with_googletrans(text))
        except Exception as e:
            # fallback on any failure
            print(f"[Warning] googletrans async failed: {e}", file=sys.stderr)

    # fallback to web API
    try:
        return _translate_with_web_api(text)
    except Exception as e:
        raise RuntimeError(f"Web‑API translation failed: {e}")
