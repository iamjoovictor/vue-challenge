import axios from 'axios';
import { environment } from "@/environments/environment";
import { httpOptionsUrlEnconded } from '@/middleware/service/headers';

export default class LoginService {
    loginURL = environment.serverIp + "login/";

    login(username: string, password: string) {
        const loginData = `username=${username}&password=${password}`;
        return axios.post(this.loginURL, loginData, httpOptionsUrlEnconded())
    }
}
