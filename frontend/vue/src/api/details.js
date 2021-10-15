import axios from "axios";
import { authHeader } from "@/api";

export function DetailCPU(server_id) {
    return axios.get('/server/cpu/' + server_id, { headers: authHeader() })
}
