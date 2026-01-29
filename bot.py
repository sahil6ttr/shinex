from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from price_engine import calculate_price


BOT_TOKEN = "8109112179:AAFOhMJF9XOfJPtWzCYClP7N28jcipPEb5Q"

user_sessions = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_sessions[update.effective_chat.id] = {}
    await update.message.reply_text(
        "🚗 Welcome to ShineX!\n\n"
        "Send vehicle and service like:\n"
        "Hatchback Basic\n"
        "Scooter Complete"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = update.message.text.strip().lower()

    if chat_id not in user_sessions:
        user_sessions[chat_id] = {}

    session = user_sessions[chat_id]

    # Step 1: Vehicle + Service
    if "vehicle" not in session:
        try:
            parts = text.split()
            vehicle = parts[0].capitalize()
            service = parts[1].capitalize()

            price = calculate_price(vehicle, service)

            session["vehicle"] = vehicle
            session["service"] = service
            session["price"] = price

            await update.message.reply_text(
                f"💰 Price for {vehicle} {service} wash is ₹{price}\n\n"
                "Type 'confirm' to continue."
            )
        except:
            await update.message.reply_text(
                "❌ Please send in format:\n"
                "Hatchback Basic"
            )

    # Step 2: Confirmation
    elif text == "confirm":
        await update.message.reply_text(
            "📅 Please send booking date (YYYY-MM-DD):"
        )
        session["step"] = "date"

    # Step 3: Date
    elif session.get("step") == "date":
        session["date"] = text
        session["step"] = "time"
        await update.message.reply_text(
            "⏰ Please send time (HH:MM):"
        )

    # Step 4: Time
    elif session.get("step") == "time":
        session["time"] = text

                import json
        from datetime import datetime

        booking = {
            "vehicle": session["vehicle"],
            "service": session["service"],
            "price": session["price"],
            "date": session["date"],
            "time": session["time"],
            "created_at": str(datetime.now())
        }

        try:
            with open("bookings.json", "r") as f:
                data = json.load(f)
        except:
            data = []

        data.append(booking)

        with open("bookings.json", "w") as f:
            json.dump(data, f, indent=4)


        await update.message.reply_text(
            "✅ Booking Confirmed!\n"
            f"{session['vehicle']} {session['service']} on {session['date']} at {session['time']}\n"
            f"Amount: ₹{session['price']}"
        )

        user_sessions.pop(chat_id)

    else:
        await update.message.reply_text("Type 'confirm' to continue.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 ShineX Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
