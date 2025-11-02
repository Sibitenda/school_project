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

// export const fetchDashboard = async (token) => {
//   const response = await api.get("/dashboard/", {
//     headers: { Authorization: `Bearer ${token}` },
//   });
//   return response.data;
// };
export const fetchDashboard = async (token) => {
  return api.get("/dashboard/", {
    headers: { Authorization: `Bearer ${token}` },
  }).then(res => res.data);
};

const BASE_URL = "https://school-project-dk22.onrender.com"; // Replace with your API base

export async function fetchProfiles(token) {
  const res = await fetch(`${BASE_URL}/api/profiles/`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error("Failed to fetch profiles");
  return res.json();
}

export async function createProfile(token, data) {
  const res = await fetch(`${BASE_URL}/api/profiles/`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to create profile");
  return res.json();
}

export async function deleteProfile(token, id) {
  const res = await fetch(`${BASE_URL}/api/profiles/${id}/`, {
    method: "DELETE",
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error("Failed to delete profile");
}
