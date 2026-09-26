import React, { useState} from "react";
import CategoryApi from "../../api/CategoryApi.jsx"

export default function AddCatogoryModel({ isOpen, onClose, onSuccess}) {
    const [name, setName] = useState('');
    if (!isOpen) return null;

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await CategoryApi.createCategory({ name });
            alert('Category created successfully!');
            setName('');
            onSuccess();
            onClose();
        } catch (error) {
            console.error('Feiled to create catagory:', error);
            alert('Failed to create category')
        }
    }

    return (
        <div className="modal-backdrop">
            <div className="modal-content">
                <h2>Add New Category</h2>
                <form onSubmit={handleSubmit}>
                    <input type="text"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        placeholder="Category Name"
                        required
                    />
                    <div className="modal-actions">
                        <button type="submit">Create</button>
                        <button type="button" onClick={onClose}>Cancel</button>
                    </div>
                </form>
            </div>
        </div>
    )
}