export interface Product {
    id?: number | null,
    name: string,
    price: number,
    expiration_date: Date | string,
    image: string | null,
    id_category: number | null
}