export interface SaleCreate {
    product_id: number
    quantity: number
}

export interface SaleHistoryItem {
    id: number
    sold_at: string
    username: string
    product_name: string
    quantity: number
}

export interface ProductSaleItem {
    name: string
    total: number
}

export interface CategorySaleItem {
    name: string
    total: number
}
