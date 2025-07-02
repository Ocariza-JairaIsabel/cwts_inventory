-- Table for inventory items
CREATE TABLE IF NOT EXISTS Item (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    quantity INTEGER DEFAULT 0
);

-- Table for item transactions (logs)
CREATE TABLE IF NOT EXISTS Log (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER NOT NULL,
    type TEXT NOT NULL CHECK (type IN ('IN', 'OUT')),
    qty INTEGER NOT NULL,
    date TEXT NOT NULL,
    FOREIGN KEY (item_id) REFERENCES Item(item_id)
);
