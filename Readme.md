# 🎙️ LiveKit Voice Agent with Custom Faster-Whisper STT

This project demonstrates a custom real-time voice assistant built using [LiveKit Agents](https://docs.livekit.io/agents/), featuring:

- Custom **Speech-to-Text (STT)** integration using [Faster-Whisper](https://github.com/guillaumekln/faster-whisper)
- OpenAI for **LLM** and **Text-to-Speech (TTS)**
- Real-time **voice interaction** using LiveKit SFU
- Visa interview simulation use-case

---

## 🚀 Features

- ✅ Plug-and-play custom STT using Faster-Whisper
- ✅ Real-time audio session management with LiveKit
- ✅ Configurable VAD, turn detection, LLM, and TTS
- ✅ Auto-cleanup of LiveKit rooms after session

---

## 📁 Project Structure

```bash
.
├── main.py               # Entry point for the LiveKit agent
├── custom_stt.py         # Custom STT module using Faster-Whisper
├── models/               # (Optional) Model download directory
├── .env                  # LiveKit credentials
└── README.md             # You're here!
```
