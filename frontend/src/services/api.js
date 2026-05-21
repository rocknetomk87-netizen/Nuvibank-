import axios from "axios";

const api = axios.create({
  baseURL: "http://10.142.231.104:5000",
});

export default api;
