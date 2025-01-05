import asyncio

from dotenv import load_dotenv
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import openai, silero, deepgram
from custom_stt import myClass
from livekit.plugins import turn_detector
from livekit import api
import os


load_dotenv()


async def entrypoint(ctx: JobContext):
    initial_ctx = llm.ChatContext().append(
        role="system",
        text=(
            "You are a US visa oficer ask them short questions and make sure they are not lying. please keep your questios short."
        ),
    )
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    assitant = VoiceAssistant(
        vad=silero.VAD.load(),
        # stt=myClass(),
        stt = deepgram.STT(),
        turn_detector=turn_detector.EOUModel(),
        llm=openai.LLM(),
        tts=openai.TTS(),
        interrupt_min_words=1,
        chat_ctx=initial_ctx,
    )


    # openai.realtime.realtime_model
    assitant.start(ctx.room)

    await asyncio.sleep(1)
    await assitant.say("Hey, I am your Visa Officer. Please be in a quite room for best experience.", allow_interruptions=True)
    
    await asyncio.sleep(60)
    await assitant.say("Timer is done!! Now we will close the connection", allow_interruptions=False)
    
    
    await asyncio.sleep(30)
    print("GOING TO CLOSE NOW!!")
    # ctx.shutdown(reason="Session ended")

    

    api_client = api.LiveKitAPI(
        os.getenv("LIVEKIT_URL"),
        os.getenv("LIVEKIT_API_KEY"),
        os.getenv("LIVEKIT_API_SECRET"),
    )
    await api_client.room.delete_room(api.DeleteRoomRequest(room=ctx.job.room.name))



    


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
