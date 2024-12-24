import asyncio

from dotenv import load_dotenv
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import openai, silero, deepgram
from custom_stt import myClass


load_dotenv()


async def entrypoint(ctx: JobContext):
    initial_ctx = llm.ChatContext().append(
        role="system",
        text=(
            "You tell them what they wanat to know"
        ),
    )
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    assitant = VoiceAssistant(
        vad=silero.VAD.load(),
        stt=myClass(),
        llm=openai.LLM(),
        tts=openai.TTS(),
        chat_ctx=initial_ctx,
    )

    # openai.realtime.realtime_model
    assitant.start(ctx.room)

    await asyncio.sleep(1)
    await assitant.say("Hey, I am your AI english teacher. Please be in a quite room for best experience. would you like to learn english!", allow_interruptions=True)


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
