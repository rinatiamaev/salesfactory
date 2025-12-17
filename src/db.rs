use sqlx::{SqlitePool, sqlite::SqlitePoolOptions};
use crate::models::Row;

#[derive(Clone)]
pub struct Db {
    pool: SqlitePool,
}

impl Db {
    //connecting
    pub async fn new(database_url: &str) -> Self {
        let pool = SqlitePoolOptions::new()
            .max_connections(5)
            .connect(database_url)
            .await
            .expect("Failed to connect to database");

        Self { pool }
    }

    // =========================
    // ROWS
    // =========================


    pub async fn list_rows(&self) -> sqlx::Result<Vec<Row>> {
        let rows = sqlx::query_as!(
            Row,
            r#"
            SELECT id, name
            FROM rows
            ORDER BY id
            "#
        )
        .fetch_all(&self.pool)
        .await?;

        Ok(rows)
    }


    pub async fn create_row(&self, name: &str) -> sqlx::Result<i64> {
        let result = sqlx::query!(
            r#"
            INSERT INTO rows (name)
            VALUES (?)
            "#,
            name
        )
        .execute(&self.pool)
        .await?;

        Ok(result.last_insert_rowid())
    }
}
