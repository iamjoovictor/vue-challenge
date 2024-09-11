import axios from 'axios';
import { environment } from "@/environments/environment";
import { httpOptionsJson } from '@/middleware/service/headers';
import ToastMessageService from '@/middleware/components/toastMessage.service';
import type { Product } from '@/middleware/inteface/product';

export default class ProductService {
    toastMessageService = new ToastMessageService();

    productURL = environment.serverIp + "product/";

    getAllProducts() {
        const requisition = axios.get(this.productURL, httpOptionsJson());

        requisition.catch((error) => {
            this.toastMessageService.error("Server error");
        })

        return requisition;
    }

    createProduct(product: Product) {
        const productToCreate: Product = {
            name: product.name,
            price: product.price,
            expiration_date: product.expiration_date,
            image: product.image,
            id_category: product.id_category
        }

        const requisition = axios.post(this.productURL, productToCreate, httpOptionsJson());

        requisition.catch((error) => {
            if (error.response.status == 409) {
                this.toastMessageService.error(`Already exists product with name '${product.name}'`);
            }

            else {
                this.toastMessageService.error("Server error");
            }
        })

        return requisition;
    }

    updateProduct(product: Product) {
        const requisition = axios.put(this.productURL, product, httpOptionsJson());

        requisition.catch((error) => {
            if (error.response.status == 409) {
                this.toastMessageService.error(`Already exists product with name '${product.name}'`);
            }

            else if (error.response.status == 404) {
                this.toastMessageService.error("Product not found");
            }

            else {
                this.toastMessageService.error("Server error");
            }
        })

        return requisition;
    }

    deleteProduct(idProduct: number) {
        const requisition = axios.delete(`${this.productURL}?id_product=${idProduct}`, httpOptionsJson());

        requisition.catch((error) => {
            this.toastMessageService.error("Server error");
        })

        return requisition;
    }
}
