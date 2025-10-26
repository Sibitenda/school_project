import axios from "axios";

const API_BASE_URL = "https://school-project-dk22.onrender.com/api"; //  No trailing slash here

export const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: { "Content-Type": "application/json" },
});

export const loginUser = async (username, password) => {
  const response = await api.post("/token/", { username, password });
  return response.data;
};

export const fetchDashboard = async (token) => {
  const response = await api.get("/dashboard/", {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
};
