# Copyright 2023 LiveKit, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

import dataclasses
import os
from dataclasses import dataclass
from faster_whisper import WhisperModel
import io

MODEL_TYPE, RUN_TYPE, COMPUTE_TYPE, NUM_WORKERS, CPU_THREADS, WHISPER_LANG = "tiny.en", "cpu", "int8", 10, 8, "en"
model = WhisperModel(model_size_or_path="tiny.en", device="cpu")
whisper_model = WhisperModel (
    model_size_or_path=MODEL_TYPE,
    device=RUN_TYPE,
    compute_type=COMPUTE_TYPE,
    num_workers=NUM_WORKERS,
    cpu_threads=CPU_THREADS,
    download_root="./models"
)



import httpx
from livekit import rtc
from livekit.agents import (
    APIConnectionError,
    APIConnectOptions,
    APIStatusError,
    APITimeoutError,
    stt,
)
from livekit.agents.utils import AudioBuffer

import openai

from livekit.plugins.openai.models import WhisperModels

class myClass(stt.STT):
    def __init__(
        self,
        *,
        language: str = "en",
        detect_language: bool = False,
        model: WhisperModels | str = "whisper-1",
        base_url: str | None = None,
        api_key: str | None = None,
    ):
        """
        Create a new instance of OpenAI STT.

        ``api_key`` must be set to your OpenAI API key, either using the argument or by setting the
        ``OPENAI_API_KEY`` environmental variable.
        """

        super().__init__(
            capabilities=stt.STTCapabilities(streaming=False, interim_results=False)
        )

        self.cnt = 0

    # def update_options(
    #     self,
    #     *,
    #     model: WhisperModels | None = None,
    #     language: str | None = None,
    # ) -> None:
    #     self._opts.model = model or self._opts.model
    #     self._opts.language = language or self._opts.language

    async def _recognize_impl(
        self,
        buffer: AudioBuffer,
        *,
        language: str | None,
        conn_options: APIConnectOptions,
    ) -> stt.SpeechEvent:
        try:
            data = rtc.combine_audio_frames(buffer).to_wav_bytes()
            print(f"Receiving audio buffer for cnt={self.cnt} with size={len(data)}")
            # resp = await self._client.audio.transcriptions.create(
            #     file=(
            #         "file.wav",
            #         data,
            #         "audio/wav",
            #     ),
            #     model=self._opts.model,
            #     language=config.language,
            #     # verbose_json returns language and other details
            #     response_format="verbose_json",
            #     timeout=httpx.Timeout(30, connect=conn_options.timeout),
            # )
            
            # print(f"Transcribe Data: {data}")
            try:
                wav_bytes = io.BytesIO(data)
                segments, _ = whisper_model.transcribe(audio=wav_bytes, language=WHISPER_LANG)
                segments = [(print(f"Segment: {s}"), s.text)[1] for s in segments]
                transcription = " ".join(segments)
                print(f"Transcription: {transcription}")
            except Exception as e:
                print(f"Error in transcription: {e}")
                transcription = "Error in transcription"

            self.cnt += 1
            print(f"Going to return stt now cnt={self.cnt}")

            return stt.SpeechEvent(
                type=stt.SpeechEventType.FINAL_TRANSCRIPT,
                alternatives=[
                    stt.SpeechData(
                        text=transcription,
                        language="",
                    )
                ],
            )

        except openai.APITimeoutError:
            raise APITimeoutError()
        except openai.APIStatusError as e:
            raise APIStatusError(
                e.message,
                status_code=e.status_code,
                request_id=e.request_id,
                body=e.body,
            )
        except Exception as e:
            raise APIConnectionError() from e
