import axios from 'axios';
import { environment } from "@/environments/environment";
import type { UserCreate, ForgotPasswordRequest, ResetPasswordRequest } from '@/middleware/inteface/user';

export default class UserService {
    baseURL = environment.serverIp + "users/";

    register(data: UserCreate) {
        return axios.post(this.baseURL + "register", data, {
            headers: { 'Content-Type': 'application/json' }
        });
    }

    forgotPassword(data: ForgotPasswordRequest) {
        return axios.post(this.baseURL + "forgot-password", data, {
            headers: { 'Content-Type': 'application/json' }
        });
    }

    resetPassword(data: ResetPasswordRequest) {
        return axios.post(this.baseURL + "reset-password", data, {
            headers: { 'Content-Type': 'application/json' }
        });
    }
}
