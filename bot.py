import os
import asyncio
import sys
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CommandHandler
from openai import OpenAI

# =================== VERIFICACIÓN DE VARIABLES ===================
print("🔍 Verificando variables de entorno...")

# Obtener variables de entorno
BOT_TOKEN = os.getenv("8487751329:AAGvPfGAdfx32KkbURXiWz9SbL_r0Tc7pnc")
API_KEY = os.getenv("sk-90d4756307f947fea3a2bda3ece8414d")

# Verificar que existen
if not BOT_TOKEN:
    print("❌ ERROR: BOT_TOKEN no está definido")
    print("   Ve a Render → Environment → Añade variable BOT_TOKEN")
    sys.exit(1)

if not API_KEY:
    print("❌ ERROR: DEEPSEEK_API_KEY no está definido")
    print("   Ve a Render → Environment → Añade variable DEEPSEEK_API_KEY")
    sys.exit(1)

print("✅ Variables verificadas correctamente")

# ================ CLIENTE DEEPSEEK ===================
try:
    client = OpenAI(api_key=API_KEY, base_url="https://api.deepseek.com")
    print("✅ Cliente DeepSeek inicializado")
except Exception as e:
    print(f"❌ Error al crear cliente OpenAI: {e}")
    sys.exit(1)

# =============== MANEJADOR DE MENSAJES ===============
async def handle_message(update: Update, context):
    user_message = update.message.text
    
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "Eres un asistente útil en Telegram."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=500
        )
        
        bot_reply = response.choices[0].message.content
        await update.message.reply_text(bot_reply)
        
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)[:100]}")

# =============== COMANDOS ===============
async def start_command(update: Update, context):
    await update.message.reply_text("🤖 ¡Hola! Soy tu bot con DeepSeek AI. Escríbeme algo.")

async def help_command(update: Update, context):
    await update.message.reply_text("Simplemente escribe un mensaje y te responderé usando IA.")

# ================== INICIALIZACIÓN ==================
async def main():
    print("🚀 Iniciando bot de Telegram...")
    
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("✅ Bot iniciado. Esperando mensajes en Telegram...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
