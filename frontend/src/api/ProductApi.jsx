import api from "./ApiService.jsx";

const ProductApi = {
    fetchAllProducts: () => api.get("/api/v1/product"),
    fetchProductsByCategory: (categoryId) => api.get(`/api/v1/product/category/${categoryId}`),
    createProduct: (productData) => api.post("/api/v1/product", productData)

}
export default ProductApi;