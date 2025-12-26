import os
import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, filters
from openai import OpenAI

# =================== CONFIGURACIÓN ===================
# OBTÉN TUS PROPIAS CLAVES Y PÓNLAS EN RAILWAY COMO VARIABLES
BOT_TOKEN = os.getenv("8487751329:AAGvPfGAdfx32KkbURXiWz9SbL_r0Tc7pnc")  # Token de @BotFather
API_KEY = os.getenv("sk-90d4756307f947fea3a2bda3ece8414d")  # API Key de DeepSeek

# ================ CLIENTE DEEPSEEK ===================
client = OpenAI(api_key=API_KEY, base_url="https://api.deepseek.com")

# =============== MANEJADOR DE MENSAJES ===============
async def handle_message(update: Update, context):
    """Responde a mensajes usando DeepSeek."""
    user_message = update.message.text
    user_name = update.effective_user.first_name
    
    print(f"📩 Mensaje de {user_name}: {user_message[:50]}...")  # Log en Railway
    
    try:
        # 1. Llamamos a la API de DeepSeek
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "Eres un asistente útil y amigable en un bot de Telegram. Responde de forma concisa y natural."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=800,  # Límite de respuesta
            temperature=0.7  # Creatividad (0=preciso, 1=creativo)
        )
        
        # 2. Extraemos la respuesta
        bot_reply = response.choices[0].message.content
        
        # 3. Enviamos la respuesta (dividida si es muy larga para Telegram)
        if len(bot_reply) > 4000:  # Límite de Telegram
            chunks = [bot_reply[i:i+4000] for i in range(0, len(bot_reply), 4000)]
            for chunk in chunks:
                await update.message.reply_text(chunk)
                await asyncio.sleep(0.5)  # Pequeña pausa entre mensajes
        else:
            await update.message.reply_text(bot_reply)
            
        print(f"✅ Respondido a {user_name}")
        
    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        print(error_msg)
        await update.message.reply_text("Lo siento, hubo un error al procesar tu mensaje. Inténtalo de nuevo.")

# =============== COMANDOS ADICIONALES ===============
async def start_command(update: Update, context):
    """Maneja el comando /start."""
    welcome_text = """
    🤖 *¡Hola! Soy tu asistente con DeepSeek*
    
    Puedes hablarme directamente y te responderé usando IA.
    
    *Comandos disponibles:*
    /start - Muestra este mensaje
    /help - Muestra ayuda
    
    ¡Escribe cualquier cosa para comenzar!
    """
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

async def help_command(update: Update, context):
    """Maneja el comando /help."""
    help_text = """
    *¿Cómo usar este bot?*
    
    1. Simplemente escríbeme cualquier mensaje
    2. Usaré DeepSeek AI para responderte
    3. Puedo ayudarte con:
       - Preguntas generales
       - Programación
       - Traducciones
       - Análisis de texto
       - Y mucho más...
    
    *Límites:* 
    - Respuestas hasta 800 tokens
    - No guardo historial de conversación entre mensajes
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')

# ================== INICIALIZACIÓN ==================
async def main():
    """Función principal que inicia el bot."""
    print("🚀 Iniciando bot de Telegram con DeepSeek...")
    
    # 1. Crear la aplicación del bot
    app = Application.builder().token(BOT_TOKEN).build()
    
    # 2. Añadir manejadores de comandos
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    
    # 3. Añadir manejador para mensajes de texto normales
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # 4. Iniciar el bot
    print("✅ Bot iniciado. Esperando mensajes...")
    await app.run_polling()

# ================== PUNTO DE ENTRADA ==================
if __name__ == "__main__":
    # Este bloque se ejecuta cuando el archivo se corre directamente
    asyncio.run(main())
