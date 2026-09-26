import React, { useState, useEffect } from 'react';
import ProductApi from "../../api/ProductApi.jsx";
import CategoryList from './CategoryList';
import ProductGrid from './ProductGrid';

function CustomerPage() {
  const [products, setProducts] = useState([]);
  const [title, setTitle] = useState('Our Star Products');

  useEffect(() => {
    // Fetch all products on initial load
    const loadAllProducts = async () => {
      try {
        const response = await ProductApi.fetchAllProducts();
        setProducts(response.data);
      } catch (error) {
        console.error("Failed to fetch products:", error);
      }
    };
    loadAllProducts();
  }, []);

  const handleCategorySelect = async (category) => {
    if (!category) {
        // If "All" is selected or component mounts
        const response = await ProductApi.fetchAllProducts();
        setProducts(response.data);
        setTitle('Our Star Products');
    } else {
        try {
            const response = await ProductApi.fetchProductsByCategory(category.id);
            setProducts(response.data);
            setTitle(`Products in ${category.name}`);
        } catch (error) {
            console.error("Failed to fetch products by category:", error);
            setProducts([]); // Clear products on error
        }
    }
  };

  return (
    <div>
      <CategoryList onCategorySelect={handleCategorySelect} />
      <h1 className="page-title">{title}</h1>
      <ProductGrid products={products} />
    </div>
  );
}

export default CustomerPage;