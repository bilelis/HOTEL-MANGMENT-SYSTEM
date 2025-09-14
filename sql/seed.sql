-- Seed data for Hotel/Restaurant POS

-- Employees with example PINs
INSERT INTO employees (name, pin_hash, role, interface)
VALUES
    ('Alice', fn_hash_pin('1111'), 'Bartender',   'Bar'),
    ('Bob',   fn_hash_pin('2222'), 'Waiter',      'Restaurant'),
    ('Carol', fn_hash_pin('3333'), 'Receptionist','Reception'),
    ('Dina',  fn_hash_pin('9999'), 'Manager',     'Restaurant')
ON CONFLICT (name) DO NOTHING;

-- Items per interface
INSERT INTO items (name, price, interface)
VALUES
    -- Bar
    ('Beer',     5.00,  'Bar'),
    ('Wine',     8.50,  'Bar'),
    ('Cocktail', 9.75,  'Bar'),
    -- Restaurant
    ('Pizza',   12.00,  'Restaurant'),
    ('Pasta',   10.50,  'Restaurant'),
    ('Salad',    7.00,  'Restaurant'),
    -- Reception
    ('Room Service', 15.00, 'Reception'),
    ('Extras',       5.00,  'Reception')
ON CONFLICT (name, interface) DO NOTHING;

-- Example orders
-- Open order in Bar for Alice with multiple items
WITH emp AS (
    SELECT id AS employee_id FROM employees WHERE name = 'Alice'
), o AS (
    INSERT INTO orders (employee_id, interface, status)
    SELECT employee_id, 'Bar', 'open' FROM emp
    RETURNING id
)
INSERT INTO order_items (order_id, item_id, quantity)
SELECT o.id, i.id, x.qty
FROM o
JOIN LATERAL (
    VALUES
        ((SELECT id FROM items WHERE name='Beer' AND interface='Bar'), 2),
        ((SELECT id FROM items WHERE name='Cocktail' AND interface='Bar'), 1)
) AS x(item_id, qty) ON TRUE
JOIN items i ON i.id = x.item_id;

-- Paid order in Restaurant for Bob with transaction
WITH emp AS (
    SELECT id AS employee_id FROM employees WHERE name = 'Bob'
), o AS (
    INSERT INTO orders (employee_id, interface, status)
    SELECT employee_id, 'Restaurant', 'open' FROM emp
    RETURNING id
), oi AS (
    INSERT INTO order_items (order_id, item_id, quantity)
    SELECT o.id, i.id, x.qty
    FROM o
    JOIN LATERAL (
        VALUES
            ((SELECT id FROM items WHERE name='Pizza' AND interface='Restaurant'), 1),
            ((SELECT id FROM items WHERE name='Pasta' AND interface='Restaurant'), 2)
    ) AS x(item_id, qty) ON TRUE
    JOIN items i ON i.id = x.item_id
    RETURNING order_id
)
SELECT * FROM fn_pay_order((SELECT DISTINCT order_id FROM oi), (SELECT employee_id FROM emp), 'card');

