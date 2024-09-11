import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';

export default class ToastMessageService {
    sucess(toastMessage: string) {
        toast(toastMessage, {
            autoClose: 3000,
            type: 'success'
        });
    }

    error(toastMessage: string) {
        toast(toastMessage, {
            autoClose: 3000,
            type: 'error'
        });
    }
}
