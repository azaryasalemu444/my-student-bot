FROM python:3.10-slim
RUN pip install pyTelegramBotAPI
COPY bot.py .
CMD ["python", "bot.py"]
