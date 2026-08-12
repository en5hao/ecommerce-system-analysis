from PIL import Image, ImageDraw, ImageFont

W, H = 360, 720
GREY = (230, 230, 230)
DARK = (60, 60, 60)
LINE = (150, 150, 150)
ACCENT = (70, 110, 200)

def font(size=14):
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
    except Exception:
        return ImageFont.load_default()

def base_canvas(title):
    img = Image.new('RGB', (W, H), 'white')
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 44], fill=DARK)
    d.text((16, 14), title, fill='white', font=font(16))
    return img, d

def wrap_box(d, x1, y1, x2, y2, fill=None, outline=LINE, width=1):
    d.rectangle([x1, y1, x2, y2], fill=fill, outline=outline, width=width)

# --- 1. Каталог ---
img, d = base_canvas("StyleShop")
d.rectangle([16, 56, 344, 84], outline=LINE)
d.text((24, 63), "🔍 Поиск товара...", fill=LINE, font=font(13))
cats = ["Одежда", "Обувь", "Аксессуары"]
cx = 16
for c in cats:
    d.rounded_rectangle([cx, 96, cx + 90, 122], radius=12, outline=ACCENT)
    d.text((cx + 12, 102), c, fill=ACCENT, font=font(12))
    cx += 100
for row in range(3):
    for col in range(2):
        x1 = 16 + col * 168
        y1 = 140 + row * 172
        wrap_box(d, x1, y1, x1 + 156, y1 + 160, fill=GREY)
        d.text((x1 + 8, y1 + 66), "фото товара", fill=LINE, font=font(11))
        d.text((x1 + 8, y1 + 128), "Название товара", fill=DARK, font=font(12))
        d.text((x1 + 8, y1 + 144), "3 490 ₽", fill=ACCENT, font=font(13))
img.save('/home/claude/ecommerce/wireframes/01_catalog.png')

# --- 2. Карточка товара ---
img, d = base_canvas("Куртка демисезонная")
wrap_box(d, 16, 56, 344, 296, fill=GREY)
d.text((160, 170), "фото товара", fill=LINE, font=font(13))
d.text((16, 312), "Куртка демисезонная", fill=DARK, font=font(16))
d.text((16, 338), "8 990 ₽", fill=ACCENT, font=font(18))
d.text((16, 368), "Мембрана, утеплитель 100г", fill=LINE, font=font(12))
d.text((16, 388), "Размер:", fill=DARK, font=font(12))
sx = 16
for s in ["S", "M", "L", "XL"]:
    d.rounded_rectangle([sx, 408, sx + 44, 440], radius=6, outline=LINE)
    d.text((sx + 14, 416), s, fill=DARK, font=font(12))
    sx += 52
wrap_box(d, 16, 470, 344, 512, fill=ACCENT, outline=ACCENT)
d.text((120, 482), "Добавить в корзину", fill='white', font=font(14))
d.text((16, 540), "В наличии: 34 шт.", fill=LINE, font=font(11))
img.save('/home/claude/ecommerce/wireframes/02_product_card.png')

# --- 3. Корзина ---
img, d = base_canvas("Корзина (2)")
items = [("Куртка демисезонная", "8 990 ₽", "1 шт."),
         ("Футболка базовая белая", "1 290 ₽", "2 шт.")]
y = 60
for name, price, qty in items:
    wrap_box(d, 16, y, 344, y + 96, outline=LINE)
    wrap_box(d, 24, y + 8, 80, y + 88, fill=GREY)
    d.text((92, y + 12), name, fill=DARK, font=font(13))
    d.text((92, y + 36), price, fill=ACCENT, font=font(13))
    d.rounded_rectangle([92, y + 58, 160, y + 82], radius=6, outline=LINE)
    d.text((100, y + 63), f"− {qty} +", fill=DARK, font=font(11))
    y += 110
wrap_box(d, 16, y + 10, 344, y + 70, outline=LINE)
d.text((24, y + 22), "Итого:", fill=DARK, font=font(14))
d.text((260, y + 22), "11 570 ₽", fill=ACCENT, font=font(14))
wrap_box(d, 16, y + 90, 344, y + 132, fill=ACCENT, outline=ACCENT)
d.text((120, y + 102), "Оформить заказ", fill='white', font=font(14))
img.save('/home/claude/ecommerce/wireframes/03_cart.png')

# --- 4. Оформление заказа / оплата ---
img, d = base_canvas("Оформление заказа")
d.text((16, 60), "Адрес доставки", fill=DARK, font=font(13))
wrap_box(d, 16, 82, 344, 118, outline=LINE)
d.text((24, 92), "г. Москва, ул. Примерная, 12", fill=LINE, font=font(12))
d.text((16, 136), "Способ оплаты", fill=DARK, font=font(13))
for i, label in enumerate(["Банковская карта", "СБП (QR-код)"]):
    y = 160 + i * 46
    d.ellipse([16, y, 32, y + 16], outline=ACCENT, width=2)
    if i == 0:
        d.ellipse([20, y + 4, 28, y + 12], fill=ACCENT)
    d.text((40, y), label, fill=DARK, font=font(13))
d.text((16, 270), "Состав заказа: 2 позиции — 11 570 ₽", fill=LINE, font=font(12))
wrap_box(d, 16, 320, 344, 362, fill=ACCENT, outline=ACCENT)
d.text((110, 332), "Оплатить 11 570 ₽", fill='white', font=font(14))
d.text((16, 390), "* После оплаты товар резервируется,", fill=LINE, font=font(10))
d.text((16, 405), "  заказ переходит в статус «Оплачен».", fill=LINE, font=font(10))
img.save('/home/claude/ecommerce/wireframes/04_checkout.png')

# --- 5. Статус заказа ---
img, d = base_canvas("Заказ №1042")
steps = ["Создан", "Оплачен", "Собирается", "Отгружен", "Доставлен"]
active = 2
sy = 90
for i, s in enumerate(steps):
    y = sy + i * 56
    color = ACCENT if i <= active else LINE
    d.ellipse([24, y, 40, y + 16], outline=color, width=3, fill=(ACCENT if i <= active else 'white'))
    if i < len(steps) - 1:
        d.line([32, y + 16, 32, y + 56], fill=color, width=2)
    d.text((52, y), s, fill=(DARK if i <= active else LINE), font=font(13))
d.text((16, sy + 5 * 56 + 20), "Ожидаемая дата доставки: 18 августа", fill=LINE, font=font(11))
wrap_box(d, 16, sy + 5 * 56 + 50, 344, sy + 5 * 56 + 92, outline=LINE)
d.text((80, sy + 5 * 56 + 62), "Оформить возврат / отменить", fill=ACCENT, font=font(12))
img.save('/home/claude/ecommerce/wireframes/05_order_status.png')

print("wireframes saved")
