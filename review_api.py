import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "store.db")

def get_product_reviews(product_id: int) -> dict:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT AVG(rating), COUNT(*) FROM reviews WHERE product_id = ?",
        (product_id,)
    )

    row = cursor.fetchone()
    conn.close()

    avg = round(row[0], 0) if row[0] is not None else None
    count = row[1] if row[1] is not None else 0

    return {
        "product_id": product_id,
        "average_rating": avg,
        "review_count": count
    }