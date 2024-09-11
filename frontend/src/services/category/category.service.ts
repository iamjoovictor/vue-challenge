import axios from 'axios';
import { environment } from "@/environments/environment";
import { httpOptionsJson } from '@/middleware/service/headers';
import type { Category } from '@/middleware/inteface/category';
import ToastMessageService from '@/middleware/components/toastMessage.service';

export default class CategoryService {
    toastMessageService = new ToastMessageService();

    categoryURL = environment.serverIp + "category/";

    getAllCategories() {
        const requisition = axios.get(this.categoryURL, httpOptionsJson());

        requisition.catch((error) => {
            this.toastMessageService.error("Server error");
        })

        return requisition;
    }

    createCategory(category: Category) {
        const categoryToCreate: Category = {
            name: category.name
        }

        const requisition = axios.post(this.categoryURL, categoryToCreate, httpOptionsJson());

        requisition.catch((error) => {
            if (error.response.status == 409) {
                this.toastMessageService.error(`Already exists category with name '${category.name}'`);
            }

            else {
                this.toastMessageService.error("Server error");
            }
        })

        return requisition;
    }

    updateCategory(category: Category) {
        const requisition = axios.put(this.categoryURL, category, httpOptionsJson());

        requisition.catch((error) => {
            if (error.response.status == 409) {
                this.toastMessageService.error(`Already exists category with name '${category.name}'`);
            }

            else if (error.response.status == 404) {
                this.toastMessageService.error("Category not found");
            }

            else {
                this.toastMessageService.error("Server error");
            }
        })

        return requisition;
    }

    deleteCategory(idCategory: number) {
        const requisition = axios.delete(`${this.categoryURL}?id_category=${idCategory}`, httpOptionsJson());

        requisition.catch((error) => {
            if (error.response.status == 409) {
                this.toastMessageService.error('Category cannot be removed as there is a product associated with it.');
            }

            else if (error.response.status == 404) {
                this.toastMessageService.error("Category not found");
            }

            else {
                this.toastMessageService.error("Server error");
            }
        })

        return requisition
    }
}
