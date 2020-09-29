import asyncpg
import constant
import ssl
from typing import Dict, Any


class Database:
    @staticmethod
    def _get_db_context() -> ssl.SSLContext:
        # 残念なことに、ここから--
        ctx = ssl.create_default_context(cafile="")
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        # --ここまでのコードがないと接続ができない。
        return ctx

    async def __ainit__(self) -> None:
        self.pool = await asyncpg.create_pool(
            constant.DATABASE_URL, ssl=get_db_context()
        )
        await self._setup()

    async def _setup(self) -> None:
        await self.pool.execute(
            """
            CREATE TABLE
                IF NOT EXISTS
                mii_channels (
                    channel_id bigint PRIMARY KEY,
                    author_id bigint,
                    channel_type text
                )
            """
        )

    async def update(self, table_name, changes: Dict[str, Any], **columns):
        return await self.pool.fetchrow(
            f"""
            UPDATE {table_name}
                SET {", ".join(
                        f"{key} = ${index}" for (index, key) in enumerate(changes.keys(), start=1)
                    )}
                WHERE {" AND ".join(
                        f"{key} = ${index}" for (index, key) in enumerate(columns.keys(), start=len(changes) + 1)
                    )}
                RETURNING *;
            """,
            *changes.values(),
            *columns.values(),
        )

    async def fetch_row(self, table_name: str, **columns) -> asyncpg.Record:
        return await self.pool.fetchrow(
            f"""
            SELECT *
                FROM {table_name}
                WHERE
                    {" AND ".join(
                        f"{key} = ${index}" for (index, key) in enumerate(columns.keys(), start=1)
                    )}
            """,
            *columns.values(),
        )

    async def insert(self, table_name: str, **columns) -> asyncpg.Record:
        return await self.pool.fetchrow(
            f"""
            INSERT
                INTO {table_name} ({", ".join(columns.keys())})
                VALUES ({", ".join(f"${i}" for i in range(1, 1 + len(columns)))})
                RETURNING *;
            """,
            *columns.values(),
        )
