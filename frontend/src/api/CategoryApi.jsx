import api from "./ApiService.jsx";

const CategoryApi = {
    fetchCategory: () => api.get("/api/v1/category"),
    createCategory: (data) => api.post("/api/v1/category", data),

}
export default CategoryApi;