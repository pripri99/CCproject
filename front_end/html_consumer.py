"""Dashboard service, it present stock quotes and recommendations."""

import asyncio
import logging
import typing

import uvicorn
from aiokafka import AIOKafkaConsumer

from fastapi import FastAPI, WebSocket
from starlette.endpoints import WebSocketEndpoint

import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.websocket_route("/ws")
class DashboardWebsocketService(WebSocketEndpoint):
    """DashboardWebsocketService."""

    consumer: AIOKafkaConsumer = None
    consumer_stock_quotes: asyncio.Task
    consumer_recommendation: asyncio.Task

    async def on_connect(self, websocket: WebSocket) -> None:
        print("hi")
        logger.info("hi")
        await websocket.accept()
        await websocket.send_json({"message": "connected"})

        loop = asyncio.get_event_loop()
        self.consumer = AIOKafkaConsumer(
            "task_signup",
            "localhost:9092",
            loop=loop,
        )
        print("WAITING FOR MESSAGES")

        await self.consumer.start()

        self.consumer_stock_quotes = asyncio.create_task(
            self.send_consumer_message(
                websocket=websocket, topicname=settings.STOCK_QUOTES_TOPIC
            )
        )

        self.consumer_recommendation = asyncio.create_task(
            self.send_consumer_message(
                websocket=websocket, topicname=settings.RECOMMENDATION_TOPIC
            )
        )
        print("connected")
        logger.info("connected")

    async def on_disconnect(self, websocket: WebSocket, close_code: int) -> None:
        self.consumer_stock_quotes.cancel()
        self.consumer_recommendation.cancel()

        await self.consumer.stop()

        logger.info("disconnected")

    async def on_receive(self, websocket: WebSocket, data: typing.Any) -> None:
        await websocket.send_json({"message": data})

    async def send_consumer_message(self, websocket: WebSocket, topicname: str) -> None:
        """Send message by WebSocket."""
        while True:
            data = await self.consume(self.consumer, topicname)
            logger.debug(data)

            await websocket.send_text(data)

    @staticmethod
    async def consume(consumer, topicname):
        """Consume message from broker."""
        _ = topicname
        async for msg in consumer:
            return msg.value.decode()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)