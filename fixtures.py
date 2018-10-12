import sqlite3

db = sqlite3.connect(':memory:')
db.execute("""
CREATE TABLE `trades` (
	`symbol`	TEXT NOT NULL,
	`timestamp`	NUMERIC NOT NULL,
	`quantity`	INTEGER NOT NULL,
	`price`	INTEGER NOT NULL,
	`ppu`	INTEGER,
	`type`	INTEGER DEFAULT 'sell'
);""")
db.execute("""CREATE INDEX `trades_symbol_idx` ON `trades` (`symbol`);""")
db.execute("""CREATE INDEX `trades_timestamp_idx` ON `trades` (`timestamp` DESC);""")
db.execute("""CREATE INDEX `trades_type_idx` ON `trades` (`type`);""")
db.commit()


STATIC_STOCK_DATA = {
    "TEA": {"Symbol": "TEA", "Type": "Common", "Last Dividend": 0, "Par Value": 100},
    "POP": {"Symbol": "POP", "Type": "Common", "Last Dividend": 8, "Par Value": 100},
    "ALE": {"Symbol": "ALE", "Type": "Common", "Last Dividend": 23, "Par Value": 60},
    "GIN": {"Symbol": "GIN", "Type": "Preferred", "Last Dividend": 8, "Par Value": 100, "Fixed Dividend": 0.02},
    "JOE": {"Symbol": "JOE", "Type": "Common", "Last Dividend": 13, "Par Value": 250},
}