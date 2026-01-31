from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "users" (
    "telegram_id" BIGSERIAL NOT NULL PRIMARY KEY,
    "course_paid" BOOL NOT NULL DEFAULT False,
    "is_message_blocked" BOOL NOT NULL DEFAULT False,
    "created_at" TIMESTAMPTZ NOT NULL
);
CREATE TABLE IF NOT EXISTS "scheduled_tasks" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "payload" JSONB NOT NULL,
    "type" VARCHAR(50) NOT NULL,
    "run_at" TIMESTAMPTZ NOT NULL,
    "processed" BOOL NOT NULL DEFAULT False,
    "user_id" BIGINT REFERENCES "users" ("telegram_id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "eJztmG1v2jAQgP8KyqdO6ioaSmHTNAkoXdkKTJBuU6sqMokJEYmd2s5aVPHfZzsJeSHJYO"
    "obGt+Se3HuHtu50z0qLjahQ4/GxgyavgNNDdC58rHyqCDgQv6Qb3BYUYDnxWohYGDiSA8a"
    "meqM20odmFBGgMG4egocCrnIhNQgtsdsjLgU+Y4jhNjghjayYpGP7Dsf6gxbkM0g4YqbWy"
    "62kQkfII1evbk+taFjpkK3TfFtKdfZwpOyHmLn0lB8baIb2PFdFBt7CzbDaGVtIyakFkSQ"
    "AAbF8oz4InwRXZhwlFEQaWwShJjwMeEU+A5LpLshAwMjwY9HQ2WClvjKe/X4pHHSrJ2eNL"
    "mJjGQlaSyD9OLcA0dJYKApS6kHDAQWEmPMzQMLB4MceF/Hw0E+vYRLBuEV4tndmLbBDiuO"
    "TdltFmiEr4xoJIiRxsfoaZiWABNZi6BdSu8cIRj8aI06F63RQb/1653QYH62g7M/6FwO25"
    "ICpswichW5QFsyjxlLPGuAOzNA8gFH9hm6PIW3yVNxwYPuQGSxGX+tV0v4RjTr1SzMUKNK"
    "VZof8ZEO2DrBM06B2S7Mpxh7ZTiaodtR9PA2qZZQ1Hr97lhr9b+njupZS+sKjSqli4z04D"
    "RDfLVI5WdPu6iI18r1cNDNnuiVnXatiJiAz7CO8L0OzGTakTgSpXbQI9iAlMKc/0wbYwcC"
    "VPCrSfpltnHCHZ9r57YtXJtvXXs4vEztWrunZW7CVb/dHR0cy+3iRjaDyV95DNWnkOh5da"
    "9tW4WlL+H09/qXgzMsby/5dwkq4AdVrdUaarV22qyfNBr1ZnVVCtdVZTWx3fsiWKaYB3BF"
    "czGd55ZJgW0d9Dkm0LbQN7iQsHs8boCMvH932Fldhcu8OcjL6JxE0jgKAu5X/Vby+PDseE"
    "4wOJ2d1rjTOusqkuEEGPN7QEw9BVNosIozkpXtuspV3awEIGDJ/EUWIuYk15xONuJd3MCK"
    "hF6xbWWcoEWAu/U9zjjuUi/7Aje5rOM1sE8o1D2Qi7ysGmU89/UoXY9sqru8WPMbqk8cbM"
    "y3rvb5C+wxpzEbBIq0/6EjTnu+VlesfJr6yBBsKwOM4BHvGT8r/2+bvNZ0FFfQ+Axkxi40"
    "56KFK5x/G0EHSKiFXcnavGdn2pPlczYVLUhsY5bXVoSa0sYCxDb7gdjTNxHPNhD7zfvB8L"
    "ZsOq9JuOzmyEat1zeY2XCrwqGN1KXrlLgaW0AMzXcT4HF1k6EXtyoEKHWZQo8RgyinyheP"
    "ZhMu+9Fs0Wh2i4r79OVl+QfcYirP"
)
