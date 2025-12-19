import pandas as pd
from sqlalchemy import create_engine
from sklearn.linear_model import LinearRegression
from datetime import datetime

# Trino connection
engine = create_engine(
    "trino://admin@trino:8080/iceberg/db"
)

# Query revenue history
query = """
SELECT
  date_trunc('minute', event_time) AS ts,
  SUM(purchase_amount) AS revenue
FROM iceberg.db.clickstream_sink
WHERE purchase_amount IS NOT NULL
GROUP BY 1
ORDER BY 1
"""

df = pd.read_sql(query, engine)

# Simple time index feature
df["t"] = range(len(df))
X = df[["t"]]
y = df["revenue"]

# Train model
model = LinearRegression()
model.fit(X, y)

# Predict next interval
next_t = [[len(df)]]
predicted_revenue = float(model.predict(next_t)[0])

# Insert prediction back into Iceberg
insert_query = f"""
INSERT INTO iceberg.db.revenue_predictions
VALUES (
  CURRENT_TIMESTAMP,
  {predicted_revenue}
)
"""

from sqlalchemy import text

with engine.begin() as conn:
    conn.execute(text(insert_query))


print("[ML] Predicted revenue:", predicted_revenue)
