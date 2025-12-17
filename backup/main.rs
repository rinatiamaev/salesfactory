use axum::{
    routing::{get, post},
    Router,
    Json,
    extract::State,
};
use std::net::SocketAddr;

mod models;
mod db;

use db::Db;
use crate::models::{Row, CreateRow};

async fn list_rows(
    State(db): State<Db>,
) -> Json<Vec<Row>> {
    let rows = db.list_rows().await.unwrap();
    Json(rows)
}

async fn create_row(
    State(db): State<Db>,
    Json(payload): Json<CreateRow>,
) -> Json<i64> {
    let id = db.create_row(&payload.name).await.unwrap();
    Json(id)
}

#[tokio::main]
async fn main() {
    let db = Db::new("sqlite://data/app.db").await;

    let app = Router::new()
        .route("/rows", get(list_rows).post(create_row))
        .with_state(db);

    let addr = SocketAddr::from(([127, 0, 0, 1], 3000));
    println!("Server running on http://{}", addr);

    axum::serve(app, addr).await.unwrap();
}
