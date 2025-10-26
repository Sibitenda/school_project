// import axios from "axios";

// /**
//  * If you are testing on your phone (Expo Go):
//  * - Run `ipconfig` (Windows) or `ifconfig` (Mac/Linux)
//  * - Copy your local network IP address, e.g. 192.168.1.102
//  * - Replace it below.
//  * 
//  * When you deploy or switch to Render, comment out the local line and
//  * uncomment the Render URL.
//  */

// // 🔹 LOCAL TESTING (Django on your machine)
// // const API_BASE_URL = "http://192.168.1.128:8000/api";

// // 🔹 RENDER DEPLOYMENT (when Django backend is live)
// const API_BASE_URL = "https://school-project-dk22.onrender.com/api";

// export const api = axios.create({
//   baseURL: API_BASE_URL,
//   timeout: 5000,
//   headers: { "Content-Type": "application/json" },
// });

// // -------------------------
// // Authentication API calls
// // -------------------------
// export const loginUser = async (username, password) => {
//   const response = await api.post("/token/", { username, password });
//   return response.data;
// };

// // -------------------------
// // Dashboard Data Fetch
// // -------------------------
// export const fetchDashboard = async (token) => {
//   const response = await api.get("/dashboard/", {
//     headers: { Authorization: `Bearer ${token}` },
//   });
//   return response.data;
// };
import axios from "axios";

// 🔹 Use your Render backend for now
const API_BASE_URL = "https://school-project-dk22.onrender.com/api/";

export const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 5000,
  headers: { "Content-Type": "application/json" },
});
