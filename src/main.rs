use axum::{
    routing::get,
    Router,
    Json,
    extract::State,
};
use tokio::net::TcpListener;
use std::net::SocketAddr;

mod models;
mod db;

use db::Db;
use models::{Row, CreateRow};

async fn list_rows(
    State(db): State<Db>,
) -> Result<Json<Vec<Row>>, axum::http::StatusCode> {
    let rows = db.list_rows().await
        .map_err(|_| axum::http::StatusCode::INTERNAL_SERVER_ERROR)?;

    Ok(Json(rows))
}

async fn create_row(
    State(db): State<Db>,
    Json(payload): Json<CreateRow>,
) -> Json<Row> {
    let id = db.create_row(&payload.name).await.unwrap();

    Json(Row {
        id,
        name: payload.name,
    })
}


#[tokio::main]
async fn main() {
    let db = Db::new("sqlite://data/app.db").await;

    let app = Router::new()
        .route("/rows", get(list_rows).post(create_row))
        .with_state(db);


    let addr = SocketAddr::from(([127, 0, 0, 1], 3000));
    let listener = TcpListener::bind(addr).await.unwrap();

    println!("Server running on http://{}", addr);
    axum::serve(listener, app).await.unwrap();
}
