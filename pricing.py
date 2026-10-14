IN_PRICE, OUT_PRICE = 0.10, 0.50  # $ per 1M tokens (Haiku 5.5, prompts ≤100K)
CACHE_WRITE, CACHE_READ = 0.125, 0.01


def cost(usage) -> float:
    input_cost = usage.input_tokens * IN_PRICE / 1_000_000
    cache_write_cost = (
        (usage.cache_creation_input_tokens or 0) * CACHE_WRITE / 1_000_000
    )
    cache_read_cost = (usage.cache_read_input_tokens or 0) * CACHE_READ / 1_000_000
    output_cost = usage.output_tokens * OUT_PRICE / 1_000_000
    return input_cost + cache_write_cost + cache_read_cost + output_cost
