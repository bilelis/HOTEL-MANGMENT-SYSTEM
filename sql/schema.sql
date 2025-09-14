-- Hotel/Restaurant POS Schema (PostgreSQL)
-- Safe to run multiple times

-- Extensions
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Employees: 4-digit PIN stored as bcrypt hash
CREATE TABLE IF NOT EXISTS employees (
    id              BIGSERIAL PRIMARY KEY,
    name            TEXT NOT NULL,
    pin_hash        TEXT NOT NULL,
    role            TEXT NOT NULL CHECK (role IN ('Bartender','Waiter','Receptionist','Manager','Admin')),
    interface       TEXT NOT NULL CHECK (interface IN ('Bar','Restaurant','Reception')),
    is_active       BOOLEAN NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (name)
);

-- Items available for sale, scoped by interface
CREATE TABLE IF NOT EXISTS items (
    id              BIGSERIAL PRIMARY KEY,
    name            TEXT NOT NULL,
    price           NUMERIC(10,2) NOT NULL CHECK (price >= 0),
    interface       TEXT NOT NULL CHECK (interface IN ('Bar','Restaurant','Reception')),
    is_active       BOOLEAN NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (name, interface)
);

-- Orders: one order can contain multiple items via order_items
CREATE TABLE IF NOT EXISTS orders (
    id              BIGSERIAL PRIMARY KEY,
    employee_id     BIGINT NOT NULL REFERENCES employees(id),
    status          TEXT NOT NULL CHECK (status IN ('open','paid','cancelled')) DEFAULT 'open',
    interface       TEXT NOT NULL CHECK (interface IN ('Bar','Restaurant','Reception')),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    paid_at         TIMESTAMPTZ NULL,
    cancelled_at    TIMESTAMPTZ NULL
);

-- Order line items
CREATE TABLE IF NOT EXISTS order_items (
    id              BIGSERIAL PRIMARY KEY,
    order_id        BIGINT NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    item_id         BIGINT NOT NULL REFERENCES items(id),
    quantity        INTEGER NOT NULL CHECK (quantity > 0),
    price_each      NUMERIC(10,2) NOT NULL CHECK (price_each >= 0),
    is_cancelled    BOOLEAN NOT NULL DEFAULT FALSE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Prevent duplicate active line items per (order_id, item_id)
CREATE UNIQUE INDEX IF NOT EXISTS ux_order_items_unique_active
    ON order_items(order_id, item_id)
    WHERE (is_cancelled = FALSE);

-- Payment transactions
CREATE TABLE IF NOT EXISTS transactions (
    id              BIGSERIAL PRIMARY KEY,
    order_id        BIGINT NOT NULL REFERENCES orders(id) ON DELETE RESTRICT,
    employee_id     BIGINT NOT NULL REFERENCES employees(id),
    amount          NUMERIC(10,2) NOT NULL CHECK (amount >= 0),
    payment_method  TEXT NOT NULL CHECK (payment_method IN ('cash','card')),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Helpful indexes
CREATE INDEX IF NOT EXISTS idx_orders_employee ON orders(employee_id);
CREATE INDEX IF NOT EXISTS idx_items_interface ON items(interface);
CREATE INDEX IF NOT EXISTS idx_orders_interface ON orders(interface);
CREATE INDEX IF NOT EXISTS idx_transactions_order ON transactions(order_id);

-- Utility function: hash a plaintext 4-digit PIN
CREATE OR REPLACE FUNCTION fn_hash_pin(p_pin TEXT)
RETURNS TEXT
LANGUAGE SQL
AS $$
    SELECT crypt(p_pin, gen_salt('bf'))
$$;

-- Trigger to automatically set price_each from items.price when inserting order_items
CREATE OR REPLACE FUNCTION trg_set_price_each()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF NEW.price_each IS NULL THEN
        SELECT i.price INTO NEW.price_each FROM items i WHERE i.id = NEW.item_id;
    END IF;
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS before_insert_order_items_set_price ON order_items;
CREATE TRIGGER before_insert_order_items_set_price
BEFORE INSERT ON order_items
FOR EACH ROW
EXECUTE FUNCTION trg_set_price_each();

-- View: current bill lines (excluding cancelled) with extended price
CREATE OR REPLACE VIEW v_order_bill AS
SELECT
    oi.id                 AS order_item_id,
    oi.order_id,
    oi.item_id,
    it.name              AS item_name,
    oi.quantity,
    oi.price_each,
    (oi.quantity * oi.price_each) AS line_total,
    oi.is_cancelled
FROM order_items oi
JOIN items it ON it.id = oi.item_id
WHERE oi.is_cancelled = FALSE;

-- Function: compute order total (excluding cancelled items)
CREATE OR REPLACE FUNCTION fn_order_total(p_order_id BIGINT)
RETURNS NUMERIC(10,2)
LANGUAGE SQL
AS $$
    SELECT COALESCE(SUM(oi.quantity * oi.price_each), 0)::NUMERIC(10,2)
    FROM order_items oi
    WHERE oi.order_id = p_order_id AND oi.is_cancelled = FALSE;
$$;

-- Function: pay order atomically and log transaction
CREATE OR REPLACE FUNCTION fn_pay_order(
    p_order_id      BIGINT,
    p_employee_id   BIGINT,
    p_payment_method TEXT
) RETURNS TABLE (
    transaction_id BIGINT,
    amount NUMERIC(10,2)
) LANGUAGE plpgsql AS $$
DECLARE
    v_total NUMERIC(10,2);
BEGIN
    -- lock the order row to prevent races
    PERFORM 1 FROM orders WHERE id = p_order_id FOR UPDATE;

    -- only open orders can be paid
    IF (SELECT status FROM orders WHERE id = p_order_id) <> 'open' THEN
        RAISE EXCEPTION 'Order % is not open', p_order_id;
    END IF;

    v_total := fn_order_total(p_order_id);

    INSERT INTO transactions (order_id, employee_id, amount, payment_method)
    VALUES (p_order_id, p_employee_id, v_total, p_payment_method)
    RETURNING id, amount INTO transaction_id, amount;

    UPDATE orders
    SET status = 'paid', paid_at = now()
    WHERE id = p_order_id;

    RETURN;
END;
$$;

-- Convenience view for spec-compat: orders flattened with single item when applicable
CREATE OR REPLACE VIEW v_orders_flat AS
SELECT
    o.id,
    o.employee_id,
    COALESCE(oi.item_id, NULL) AS item_id,
    COALESCE(oi.quantity, NULL) AS quantity,
    o.status,
    o.interface
FROM orders o
LEFT JOIN LATERAL (
    SELECT oi.item_id, oi.quantity
    FROM order_items oi
    WHERE oi.order_id = o.id AND oi.is_cancelled = FALSE
    ORDER BY oi.id
    LIMIT 1
) oi ON TRUE;

