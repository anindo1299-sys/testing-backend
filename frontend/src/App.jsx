import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Navbar from './components/Navber.jsx';
import AdminDashboard from './assets/admin/AdminDashboard.jsx';
import CustomerPage from './assets/customer/CustomerPage.jsx';
import Login from './components/Login.jsx';
import Signup from './components/Signup.jsx';
import api from './api/ApiService.jsx';
import './App.css';
import React, { useState } from "react";


function HomeRedirect() {
    const [redirect, setRedirect] = React.useState(null);

    React.useEffect(() => {
        const token = localStorage.getItem("token");
        if(!token) {
            setRedirect("/login");
            return;
        }
        api.get("/api/v1/user/users/me", {
            headers: { Authorization: `Bearer ${token}` }
        })
        .then(res => {
            if (res.data.role === "admin") {
                setRedirect("/admin");
            } else {
                setRedirect("/customer");
            }
        })
        .catch(() => {
            setRedirect("/login");
        });
    }, []);
    if (redirect) return <Navigate to={redirect} replace />;
    return <div>Loading...</div>;
}


function AdminRoute({ children }) {
    const [auth, setAuth] = React.useState(null);
    const [loading, setLoading] = React.useState(true);

    React.useEffect(() => {
        const token = localStorage.getItem("token");
        if (!token) {
            setAuth(false);
            setLoading(false);
            return;
        }
        api.get("/api/v1/user/users/me", {
            headers: { Authorization: `Bearer ${token}` }
        })
        .then(res => {
            setAuth(res.data.role === "admin");
            setLoading(false);
        })
        .catch(() => {
            setAuth(false);
            setLoading(false);
        });
    }, []);
    if (loading) return <div>Loading...</div>;
    if (!auth) return <div className="container"><h2>This page is for admin only.</h2></div>
    return children;
}


function CustomerRoute({ children }) {
    const [auth, setAuth] = React.useState(null);
    const [loading, setLoading] = React.useState(true);

    React.useEffect(() => {
        const token = localStorage.getItem("token");
        if(!token) {
            setAuth(false);
            setLoading(false);
            return;
        }
        api.get("/api/v1/user/users/me", {
            headers: { Authorization: `Bearer ${token}` }
        })
        .then(res => {
            setAuth(res.data.role !== "admin");
            setLoading(false);
        })
        .catch(() => {
            setAuth(false);
            setLoading(false);
        });
    }, []);
    if (loading) return <div>Loading...</div>;
    if (!auth) return <div className="container"><h2>This page is for customers only.</h2></div>
    return children;
}


export default function App() {
    return (
        <Router>
            <Navbar />
            <main className="container">
                <Routes>
                    <Route path="/" element={<HomeRedirect />} />
                    <Route path="/login" element={<Login />} />
                    <Route path="/signup" element={<Signup />} />
                    <Route
                      path="/admin"
                      element={
                        <AdminRoute>
                            <AdminDashboard />
                        </AdminRoute>
                      }
                    />
                    <Route
                      path="/customer"
                      element={
                        <CustomerRoute>
                            <CustomerPage />
                        </CustomerRoute>
                      }
                    />
                </Routes>
            </main>
        </Router>
    )
}
