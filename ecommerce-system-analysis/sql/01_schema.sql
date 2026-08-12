-- Схема БД для pet-проекта "StyleShop"
-- Диалект: SQLite (совместимо с PostgreSQL с минимальными правками типов)

CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    phone TEXT,
    full_name TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE categories (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    parent_id INTEGER REFERENCES categories(id)
);

CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    category_id INTEGER NOT NULL REFERENCES categories(id),
    name TEXT NOT NULL,
    sku TEXT NOT NULL UNIQUE,
    price NUMERIC(10,2) NOT NULL,
    description TEXT
);

CREATE TABLE inventory (
    id INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantity_available INTEGER NOT NULL DEFAULT 0,
    quantity_reserved INTEGER NOT NULL DEFAULT 0,
    warehouse_location TEXT
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    status TEXT NOT NULL CHECK (status IN (
        'created', 'pending_payment', 'paid', 'packing',
        'shipped', 'delivered', 'cancelled'
    )),
    total_amount NUMERIC(10,2) NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE order_items (
    id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id),
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    price_at_purchase NUMERIC(10,2) NOT NULL
);

CREATE TABLE payments (
    id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id),
    amount NUMERIC(10,2) NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('pending', 'success', 'failed')),
    provider_transaction_id TEXT,
    paid_at TEXT
);

CREATE TABLE returns (
    id INTEGER PRIMARY KEY,
    order_item_id INTEGER NOT NULL REFERENCES order_items(id),
    reason TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('requested', 'received', 'approved', 'rejected')),
    requested_at TEXT NOT NULL DEFAULT (datetime('now')),
    resolved_at TEXT
);
