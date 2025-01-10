import axios from "axios";
import { useAuth } from "./auth";


export async function fetchToken() {
    const auth = useAuth();

    try {
      const res = await axios.get('/api/get-token/');
      auth.setToken(res.data.token) ;
    } catch (error) {
      console.error(error);
    }
  }