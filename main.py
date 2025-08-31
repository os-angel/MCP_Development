import asyncio
from dotenv import load_dotenv
import os
load_dotenv()


# Probamos si imprime la contraseña
print(os.getenv("OPENAI_API_KEY"))

async def main():
    print("Hello from project2!")


if __name__ == "__main__":
   asyncio.run( main())
