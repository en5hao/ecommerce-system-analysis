-- ============================================================
-- Запрос 1: Топ-5 товаров по выручке
-- ============================================================
SELECT
    p.name AS product_name,
    SUM(oi.quantity) AS units_sold,
    SUM(oi.quantity * oi.price_at_purchase) AS revenue
FROM order_items oi
JOIN products p ON p.id = oi.product_id
JOIN orders o ON o.id = oi.order_id
WHERE o.status != 'cancelled'
GROUP BY p.id, p.name
ORDER BY revenue DESC
LIMIT 5;

-- ============================================================
-- Запрос 2: Средний чек по категориям
-- ============================================================
SELECT
    c.name AS category,
    ROUND(AVG(oi.price_at_purchase * oi.quantity), 2) AS avg_item_amount,
    COUNT(DISTINCT oi.order_id) AS orders_count
FROM order_items oi
JOIN products p ON p.id = oi.product_id
JOIN categories c ON c.id = p.category_id
JOIN orders o ON o.id = oi.order_id
WHERE o.status != 'cancelled'
GROUP BY c.id, c.name
ORDER BY avg_item_amount DESC;

-- ============================================================
-- Запрос 3: Доля отменённых заказов от общего числа
-- ============================================================
SELECT
    status,
    COUNT(*) AS orders_count,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM orders), 1) AS share_percent
FROM orders
GROUP BY status
ORDER BY orders_count DESC;

-- ============================================================
-- Запрос 4: Товары с низким остатком на складе (< 10 шт доступно)
-- ============================================================
SELECT
    p.name AS product_name,
    p.sku,
    i.quantity_available,
    i.quantity_reserved,
    i.warehouse_location
FROM inventory i
JOIN products p ON p.id = i.product_id
WHERE i.quantity_available < 10
ORDER BY i.quantity_available ASC;

-- ============================================================
-- Запрос 5: Доля возвратов от доставленных заказов и причины
-- ============================================================
SELECT
    r.reason,
    COUNT(*) AS returns_count,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM returns), 1) AS share_percent
FROM returns r
GROUP BY r.reason
ORDER BY returns_count DESC;

-- ============================================================
-- Запрос 6: Топ покупателей по сумме успешных заказов (без отменённых)
-- ============================================================
SELECT
    u.full_name,
    COUNT(DISTINCT o.id) AS orders_count,
    SUM(o.total_amount) AS total_spent
FROM orders o
JOIN users u ON u.id = o.user_id
WHERE o.status != 'cancelled'
GROUP BY u.id, u.full_name
ORDER BY total_spent DESC
LIMIT 5;

-- ============================================================
-- Запрос 7: Среднее время обработки возврата (от заявки до решения), в днях
-- ============================================================
SELECT
    ROUND(AVG(julianday(resolved_at) - julianday(requested_at)), 1) AS avg_days_to_resolve
FROM returns
WHERE resolved_at IS NOT NULL;
