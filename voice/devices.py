"""
Audio device service - enumerate Windows input/output devices and select the
microphone + speaker safely (never picking a speaker/monitor as a mic).

Selection order for the microphone:
  1. saved valid microphone setting
  2. Windows default input device
  3. first input device with at least one input channel
"""
from voice import audio_log


def _sd():
    import sounddevice as sd
    return sd


def list_devices():
    """Return a list of dicts describing every device."""
    sd = _sd()
    out = []
    for index, dev in enumerate(sd.query_devices()):
        try:
            host = sd.query_hostapis(dev["hostapi"])["name"]
        except Exception:
            host = "?"
        out.append({
            "index": index,
            "name": dev["name"],
            "host_api": host,
            "input_channels": dev["max_input_channels"],
            "output_channels": dev["max_output_channels"],
            "default_samplerate": int(dev["default_samplerate"]),
        })
    return out


def input_devices():
    return [d for d in list_devices() if d["input_channels"] > 0]


def output_devices():
    return [d for d in list_devices() if d["output_channels"] > 0]


def default_input_index():
    try:
        return _sd().default.device[0]
    except Exception:
        return None


def default_output_index():
    try:
        return _sd().default.device[1]
    except Exception:
        return None


def _is_real_mic(device):
    """Exclude speaker/monitor/loopback sources from mic selection."""
    name = device["name"].lower()
    bad = ("speaker", "output", "monitor", "stereo mix", "loopback", "playback")
    return device["input_channels"] > 0 and not any(b in name for b in bad)


def resolve_microphone(saved=None):
    """
    Return (device_dict, note). Clears an invalid saved selection.
    """
    audio_log.log("Enumerating audio devices")
    devices = list_devices()
    for d in devices:
        audio_log.log(
            f"device {d['index']}: {d['name']} host={d['host_api']} "
            f"in={d['input_channels']} out={d['output_channels']} sr={d['default_samplerate']}"
        )

    # 1) saved valid setting
    if saved not in (None, "", "default"):
        for d in devices:
            if str(d["index"]) == str(saved) or d["name"] == saved:
                if d["input_channels"] > 0:
                    audio_log.log(f"Selected microphone from saved setting: {d['name']}")
                    return d, "saved"
                audio_log.log(f"Saved microphone '{saved}' is not an input device; clearing")
                break

    # 2) Windows default input
    di = default_input_index()
    if di is not None:
        for d in devices:
            if d["index"] == di and _is_real_mic(d):
                audio_log.log(f"Selected default input microphone: {d['name']}")
                return d, "default"

    # 3) first real input device
    for d in devices:
        if _is_real_mic(d):
            audio_log.log(f"Selected first available microphone: {d['name']}")
            return d, "first"

    audio_log.log_error("No usable microphone found")
    return None, "none"


def resolve_speaker(saved=None):
    """Return (device_dict, note)."""
    devices = list_devices()
    if saved not in (None, "", "default"):
        for d in devices:
            if str(d["index"]) == str(saved) or d["name"] == saved:
                if d["output_channels"] > 0:
                    audio_log.log(f"Selected speaker from saved setting: {d['name']}")
                    return d, "saved"
                break
    do = default_output_index()
    if do is not None:
        for d in devices:
            if d["index"] == do:
                audio_log.log(f"Selected default output speaker: {d['name']}")
                return d, "default"
    for d in devices:
        if d["output_channels"] > 0:
            return d, "first"
    return None, "none"