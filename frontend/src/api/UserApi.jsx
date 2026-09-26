import api from "./ApiService.jsx";

const UserApi = {
    login: (username, password) => {
        const formData = new FormData();
         formData.append("username", username);
         formData.append("password", password);
         return api.post("/api/v1/user/auth/token", formData)
    },
     getSession: (token) =>
         api.get("/api/v1/user/users/me", {
            headers: { Authorization: `Bearer ${token}` },
        }),
         singup: (username, password) =>
             api.post("/api/v1/user/", { username, password }),
};

export default UserApi