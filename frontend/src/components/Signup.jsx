import { useState } from "react";


export default function Signup({
    onSignup,
    onShowLogin
}) {
    const [form, setForm] = useState({
        first_name: "",
        last_name: "",
        login_id: "",
        email: "",
        password: ""
    });

    const [error, setError] = useState("");

    function updateField(e) {
        setForm({
            ...form,
            [e.target.name]: e.target.value
        });
    }

    async function handleSubmit(e) {
        e.preventDefault();
        setError("");

        try {
            await onSignup(form);
        } catch (err) {
            setError(err.message);
        }
    }

    return (
        <div className="auth-page">
            <div className="auth-card">
                <h1>Create Account</h1>

                <p className="subtitle">
                    Start your conversations
                </p>

                <form onSubmit={handleSubmit}>
                    <input
                        name="first_name"
                        placeholder="First Name"
                        onChange={updateField}
                        required
                    />

                    <input
                        name="last_name"
                        placeholder="Last Name"
                        onChange={updateField}
                        required
                    />

                    <input
                        name="login_id"
                        placeholder="Login ID"
                        onChange={updateField}
                        required
                    />

                    <input
                        name="email"
                        type="email"
                        placeholder="Email"
                        onChange={updateField}
                        required
                    />

                    <input
                        name="password"
                        type="password"
                        placeholder="Password"
                        onChange={updateField}
                        minLength={8}
                        required
                    />

                    {error && (
                        <div className="error">
                            {error}
                        </div>
                    )}

                    <button className="primary-button">
                        Sign Up
                    </button>
                </form>

                <p className="auth-switch">
                    Already registered?

                    <button
                        type="button"
                        className="link-button"
                        onClick={onShowLogin}
                    >
                        Login
                    </button>
                </p>
            </div>
        </div>
    );
}
