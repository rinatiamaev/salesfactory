use serde::{Serialize, Deserialize};


#[derive(Debug, Serialize)]
pub struct Row {
    pub id: i64,
    pub name: String,
}

#[derive(Debug, Deserialize)]
pub struct CreateRow {
    pub name: String,
}



#[derive(Debug, Serialize, Deserialize)]
pub struct Table {
    pub id: i64,
    pub name: String,
    pub row_id: i64,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Item {
    pub id: i64,
    pub name: String,
    pub price: f64,
    pub table_id: i64,
    pub barcode: Option<String>,
    pub photo_url: Option<String>,
}
