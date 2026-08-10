import axios from 'axios';
import { environment } from "@/environments/environment";
import { httpOptionsJson } from '@/middleware/service/headers';
import type { SaleCreate } from '@/middleware/inteface/sale';

export default class SaleService {
    saleURL = environment.serverIp + "sale/";

    createSale(data: SaleCreate) {
        return axios.post(this.saleURL, data, httpOptionsJson());
    }

    getSalesHistory() {
        return axios.get(this.saleURL + "history", httpOptionsJson());
    }

    getTopProducts() {
        return axios.get(this.saleURL + "by-product", httpOptionsJson());
    }

    getCategorySales() {
        return axios.get(this.saleURL + "by-category", httpOptionsJson());
    }
}
