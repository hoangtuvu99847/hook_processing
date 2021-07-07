import axios from "axios";
import {authHeader} from "@/api";

export function listServer() {
    return axios.get('/', {headers: authHeader()})
}
