import httpx

question = input("Ask: ")
max_tokens = int(input("max_tokens [2048]: ") or 2048)

with httpx.stream(
    "POST",
    "http://127.0.0.1:8000/ask",
    json={"question": question, "max_tokens": max_tokens},
    timeout=120,
) as r:
    for chunk in r.iter_text():
        print(chunk, end="", flush=True)
print()
