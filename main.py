import asyncio
import time

from dotenv import load_dotenv

load_dotenv()  # must run before the client reads the API key

import anthropic
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from db import save_log
from pricing import cost

app = FastAPI()
client = anthropic.AsyncAnthropic()
MODEL = "claude-haiku-5-5"


class AskRequest(BaseModel):
    question: str
    max_tokens: int = 2048


@app.post("/ask")
async def ask(req: AskRequest):
    async def generate():  # an async generator: each `yield` goes straight to the client
        start = time.perf_counter()
        ttft = None
        async with client.messages.stream(
            model=MODEL,
            max_tokens=req.max_tokens,
            messages=[{"role": "user", "content": req.question}],
        ) as stream:
            async for text in stream.text_stream:
                if ttft is None:
                    ttft = time.perf_counter() - start
                yield text
            final = await stream.get_final_message()
        total = time.perf_counter() - start

        if final.stop_reason == "max_tokens":
            yield "\n\n[Answer cut off: max_tokens reached. Try increasing max_tokens or asking a shorter question.]"

        await asyncio.to_thread(
            save_log,
            model=MODEL,
            prompt_chars=len(req.question),
            input_tokens=final.usage.input_tokens,
            output_tokens=final.usage.output_tokens,
            cache_write_tokens=final.usage.cache_creation_input_tokens or 0,
            cache_read_tokens=final.usage.cache_read_input_tokens or 0,
            ttft_s=ttft,
            total_s=total,
            cost_usd=cost(final.usage),
            stop_reason=final.stop_reason,
        )

    return StreamingResponse(generate(), media_type="text/plain")
