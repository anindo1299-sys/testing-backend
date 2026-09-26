import React, { useState, useEffect, useCallback } from 'react';
import CategoryApi from "../../api/CategoryApi.jsx";
import ProductApi from "../../api/ProductApi.jsx";
import AddCategoryModal from "./AddCatogoryModel.jsx"
import AddProductModal from "./AddProductModels.jsx";

function AdminDashboard() {
  const [categoryCount, setCategoryCount] = useState(0);
  const [productCount, setProductCount] = useState(0);
  const [isCategoryModalOpen, setCategoryModalOpen] = useState(false);
  const [isProductModalOpen, setProductModalOpen] = useState(false);

  const updateCounts = useCallback(async () => {
    try {
      const catRes = await CategoryApi.fetchCategory();
      const prodRes = await ProductApi.fetchAllProducts();

      const categories = catRes?.data ?? catRes ?? [];
      const products = prodRes?.data ?? prodRes ?? [];

      setCategoryCount(Array.isArray(categories) ? categories.length : 0);
      setProductCount(Array.isArray(products) ? products.length : 0);
    } catch (error) {
      console.error("Failed to update counts:", error);
    }
  }, []);

  useEffect(() => {
    updateCounts();
  }, [updateCounts]);

  return (
    <div>
      <h1 className="page-title">Admin Dashboard</h1>
      <div className="dashboard-cards">
        <div className="dashboard-card">
          <h2>Total Categories</h2>
          <p>{categoryCount}</p>
        </div>
        <div className="dashboard-card">
          <h2>Total Products</h2>
          <p>{productCount}</p>
        </div>
      </div>
      <div className="admin-actions">
        <button onClick={() => setCategoryModalOpen(true)}>Add Category</button>
        <button onClick={() => setProductModalOpen(true)}>Add Product</button>
      </div>

      <AddCategoryModal
        isOpen={isCategoryModalOpen}
        onClose={() => setCategoryModalOpen(false)}
        onSuccess={updateCounts}
      />
      <AddProductModal
        isOpen={isProductModalOpen}
        onClose={() => setProductModalOpen(false)}
        onSuccess={updateCounts}
      />
    </div>
  );
}

export default AdminDashboard;