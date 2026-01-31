SCHEDULER_LOCK_ID = 7777

async def acquire_lock(conn) -> bool:
    result = await conn.execute_query(
        f"SELECT pg_try_advisory_lock({SCHEDULER_LOCK_ID})"
    )
    return result[1][0][0]

async def release_lock(conn) -> bool:
    result = await conn.execute_query(
        f"SELECT pg_advisory_unlock({SCHEDULER_LOCK_ID})"
    )
    print(f"Release result raw: {result}")
    return result[1][0][0]