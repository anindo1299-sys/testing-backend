import React, { useState} from "react";
import { useNavigate, useLocation } from "react-router-dom";
import UserApi from "../api/UserApi.jsx";

export default function Login() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const Navigate = useNavigate();
    const location = useLocation();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");
        try {
            const loginRes = await UserApi.login(username, password);
            const token = loginRes.data.access_token;
            localStorage.setItem("token", token);
            const sessionRes = await UserApi.getSession(token);
            const role = sessionRes.data.role;

            if (role == "admin") {
                Navigate("/admin");
            } else {
                Navigate("/");
            }
        } catch (err) {
            setError(`Invalid credentials or server error: ${err}`);
        }
    };

    return (
        <div className="container">
            <h1 className="page-tittle">Login</h1>
            {location.state && location.state.signupSuccess && (
                <p style={{ color: "green" }}>User created successfully. Please login.</p>
            )}
            <form onSubmit={handleSubmit} style ={{ maxWidth: 400, margin: "0 auto" }}>
                <input
                  type="text"
                  placeholder="Username"
                  value={username}
                  onChange={e => setUsername(e.target.value)}
                  required
                />
                <input
                  type="password"
                  placeholder="Password"
                  value={password}
                  onChange={e => setPassword(e.target.value)}
                  required
                />
                <div className="model-actions">
                    <button type="submit">Login</button>
                </div>
                {error && <p style={{ color: "red" }}>{error}</p>}
                <p>
                    Don't have an Account? <a href="/signup">Signup</a>
                </p>
            </form>
        </div>
    )
}

