---
name: voice-to-text
description: 使用本地 faster-whisper 将语音(.ogg/.m4a/.mp3/.wav)转成文字。触发条件：用户发送语音文件、要求转录、语音转文字、voice to text、speech to text。
---

# Voice to Text

使用本地 faster-whisper (tiny 模型) 进行语音转文字，无需网络。

## 使用方式

```bash
python3 <skill-path>/scripts/transcribe.py <音频文件路径>
```

## 支持格式

- .ogg
- .m4a
- .mp3
- .wav

## 输出

直接输出识别文字，AI 直接使用结果回复用户，无需展示中间过程。
