import sqlite3
import random
from datetime import datetime, timedelta

random.seed(42)

DB_PATH = '/home/claude/ecommerce/db/styleshop.db'
SCHEMA_PATH = '/home/claude/ecommerce/sql/01_schema.sql'

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

with open(SCHEMA_PATH, encoding='utf-8') as f:
    cur.executescript(f.read())

# --- Users ---
names = ['Анна Иванова', 'Пётр Смирнов', 'Мария Кузнецова', 'Дмитрий Попов', 'Ольга Соколова',
         'Иван Лебедев', 'Екатерина Козлова', 'Сергей Новиков', 'Наталья Морозова', 'Алексей Волков',
         'Татьяна Егорова', 'Артём Зайцев', 'Юлия Павлова', 'Максим Семёнов', 'Виктория Голубева']
users = []
for i, name in enumerate(names, start=1):
    email = f"user{i}@example.com"
    created = (datetime(2025, 9, 1) + timedelta(days=random.randint(0, 300))).strftime('%Y-%m-%d %H:%M:%S')
    users.append((i, email, f"+7 900 000-{1000+i}", name, created))
cur.executemany("INSERT INTO users (id, email, phone, full_name, created_at) VALUES (?,?,?,?,?)", users)

# --- Categories ---
categories = [
    (1, 'Одежда', None),
    (2, 'Обувь', None),
    (3, 'Аксессуары', None),
    (4, 'Верхняя одежда', 1),
    (5, 'Футболки и рубашки', 1),
    (6, 'Кроссовки', 2),
]
cur.executemany("INSERT INTO categories (id, name, parent_id) VALUES (?,?,?)", categories)

# --- Products ---
products = [
    (1, 5, 'Футболка базовая белая', 'SKU-TS-001', 1290, 'Хлопок 100%'),
    (2, 5, 'Рубашка оксфорд синяя', 'SKU-SH-002', 3490, 'Хлопок, приталенный крой'),
    (3, 4, 'Куртка демисезонная', 'SKU-JK-003', 8990, 'Мембрана, утеплитель 100г'),
    (4, 4, 'Пуховик зимний чёрный', 'SKU-JK-004', 14990, 'Пух 90/10'),
    (5, 6, 'Кроссовки беговые', 'SKU-SN-005', 6490, 'Сетка, амортизация EVA'),
    (6, 6, 'Кроссовки повседневные', 'SKU-SN-006', 5290, 'Кожа PU'),
    (7, 3, 'Ремень кожаный', 'SKU-AC-007', 1990, 'Натуральная кожа'),
    (8, 3, 'Шапка вязаная', 'SKU-AC-008', 990, 'Шерсть 50%'),
    (9, 5, 'Худи серое', 'SKU-HD-009', 3290, 'Флис изнутри'),
    (10, 4, 'Плащ тренч бежевый', 'SKU-JK-010', 7490, 'Хлопок с водоотталкивающей пропиткой'),
]
cur.executemany("INSERT INTO products (id, category_id, name, sku, price, description) VALUES (?,?,?,?,?,?)", products)

# --- Inventory ---
inventory = []
for p in products:
    pid = p[0]
    qty_avail = random.randint(0, 60)
    qty_res = random.randint(0, 5)
    inventory.append((pid, pid, qty_avail, qty_res, f"Стеллаж {chr(65 + pid % 5)}-{pid}"))
cur.executemany("INSERT INTO inventory (id, product_id, quantity_available, quantity_reserved, warehouse_location) VALUES (?,?,?,?,?)", inventory)

# --- Orders, OrderItems, Payments, Returns ---
statuses_weighted = (
    ['delivered'] * 10 + ['shipped'] * 3 + ['packing'] * 2 +
    ['paid'] * 2 + ['cancelled'] * 4 + ['pending_payment'] * 2
)

order_id = 1
oi_id = 1
pay_id = 1
ret_id = 1
orders_rows, oi_rows, pay_rows, ret_rows = [], [], [], []

for _ in range(40):
    uid = random.choice(users)[0]
    status = random.choice(statuses_weighted)
    created = datetime(2025, 9, 1) + timedelta(days=random.randint(0, 330), hours=random.randint(0, 23))
    n_items = random.randint(1, 3)
    chosen_products = random.sample(products, n_items)
    total = 0
    items_for_order = []
    for prod in chosen_products:
        qty = random.randint(1, 2)
        price = prod[4]
        total += qty * price
        items_for_order.append((oi_id, order_id, prod[0], qty, price))
        oi_id += 1
    orders_rows.append((order_id, uid, status, total, created.strftime('%Y-%m-%d %H:%M:%S'),
                         (created + timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')))
    oi_rows.extend(items_for_order)

    if status not in ('created', 'pending_payment'):
        pay_status = 'success' if status != 'cancelled' else random.choice(['success', 'failed'])
        pay_rows.append((pay_id, order_id, total, pay_status,
                          f"TXN-{100000+order_id}", (created + timedelta(minutes=10)).strftime('%Y-%m-%d %H:%M:%S')))
        pay_id += 1

    # some delivered orders get returns
    if status == 'delivered' and random.random() < 0.35:
        oi_for_return = random.choice(items_for_order)
        ret_status = random.choice(['requested', 'received', 'approved', 'rejected'])
        reason = random.choice(['Не подошёл размер', 'Товар не соответствует описанию',
                                 'Брак', 'Передумал(а)', 'Долгая доставка'])
        req_at = created + timedelta(days=random.randint(5, 20))
        resolved = req_at + timedelta(days=random.randint(1, 5)) if ret_status in ('approved', 'rejected') else None
        ret_rows.append((ret_id, oi_for_return[0], reason, ret_status,
                          req_at.strftime('%Y-%m-%d %H:%M:%S'),
                          resolved.strftime('%Y-%m-%d %H:%M:%S') if resolved else None))
        ret_id += 1

    order_id += 1

cur.executemany("INSERT INTO orders (id, user_id, status, total_amount, created_at, updated_at) VALUES (?,?,?,?,?,?)", orders_rows)
cur.executemany("INSERT INTO order_items (id, order_id, product_id, quantity, price_at_purchase) VALUES (?,?,?,?,?)", oi_rows)
cur.executemany("INSERT INTO payments (id, order_id, amount, status, provider_transaction_id, paid_at) VALUES (?,?,?,?,?,?)", pay_rows)
cur.executemany("INSERT INTO returns (id, order_item_id, reason, status, requested_at, resolved_at) VALUES (?,?,?,?,?,?)", ret_rows)

conn.commit()

print(f"users: {len(users)}, products: {len(products)}, orders: {len(orders_rows)}, "
      f"order_items: {len(oi_rows)}, payments: {len(pay_rows)}, returns: {len(ret_rows)}")
conn.close()
