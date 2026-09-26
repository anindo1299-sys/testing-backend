import React, { useState, useEffect } from 'react';
import CategoryApi from "../../api/CategoryApi.jsx";

function CategoryList({ onCategorySelect }) {
  const [categories, setCategories] = useState([]);

  useEffect(() => {
    const loadCategories = async () => {
      try {
        const response = await CategoryApi.fetchCategory();
        setCategories(response.data);
      } catch (error) {
        console.error("Failed to fetch categories:", error);
      }
    };
    loadCategories();
  }, []);

  return (
    <div className="category-tabs">
      <button onClick={() => onCategorySelect(null)}>All Products</button>
      {categories.map((cat) => (
        <button key={cat.id} onClick={() => onCategorySelect(cat)}>
          {cat.name}
        </button>
      ))}
    </div>
  );
}

export default CategoryList;