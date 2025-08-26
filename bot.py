from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import cairosvg

BOT_TOKEN = "8311824260:AAGXb5ZmpaROdX4qdLLyLZYF2QixX_KmKgk"

FONTS = [
    "arial.ttf",
    "comic.ttf",
    "times.ttf"
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎨 Welcome! Use /logo {name} to generate a fancy logo.")

async def logo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Usage: /logo YourBrandName")
        return

    name = " ".join(context.args)
    await update.message.reply_text(f"🖌 Generating logo for '{name}'...")

    img = Image.new('RGBA', (512, 512), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    for idx, font_name in enumerate(FONTS):
        try:
            font = ImageFont.truetype(font_name, 60 - idx*10)
        except:
            font = ImageFont.load_default()
        x = 50 + idx*10
        y = 200 + idx*10
        draw.text((x+2, y+2), name, font=font, fill=(0,0,0,150))
        draw.text((x, y), name, font=font, fill=(255, 50+idx*50, 100+idx*50, 255))

    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)

    svg_bytes = BytesIO()
    cairosvg.svg2png(bytestring=f'<svg height="512" width="512"><text x="10" y="250" font-size="60">{name}</text></svg>', write_to=svg_bytes)
    svg_bytes.seek(0)

    await update.message.reply_photo(photo=img_bytes, caption=f"Logo for '{name}'!")

    buttons = [
        [InlineKeyboardButton("Download PNG", url="https://via.placeholder.com/512.png?text="+name)],
        [InlineKeyboardButton("Download JPG", url="https://via.placeholder.com/512.jpg?text="+name)],
        [InlineKeyboardButton("Download SVG", url="https://via.placeholder.com/512.svg?text="+name)]
    ]
    await update.message.reply_text("Choose format:", reply_markup=InlineKeyboardMarkup(buttons))

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("logo", logo))

print("LogoBot is running...")
app.run_polling()
