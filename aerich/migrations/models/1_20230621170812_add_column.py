from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `document` ADD `create_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `document` DROP COLUMN `create_at`;"""
