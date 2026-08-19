import { useState } from "react";


export default function Login({
    onLogin,
    onShowSignup
}) {
    const [form, setForm] = useState({
        login_id: "",
        password: ""
    });

    const [error, setError] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");

        try {
            await onLogin(form);
        } catch (err) {
            setError(err.message);
        }
    };

    return (
        <div className="auth-page">
            <div className="auth-card">
                <h1>Chat</h1>

                <p className="subtitle">
                    Sign in to continue
                </p>

                <form onSubmit={handleSubmit}>
                    <input
                        placeholder="Login ID"
                        value={form.login_id}
                        onChange={(e) =>
                            setForm({
                                ...form,
                                login_id: e.target.value
                            })
                        }
                        required
                    />

                    <input
                        type="password"
                        placeholder="Password"
                        value={form.password}
                        onChange={(e) =>
                            setForm({
                                ...form,
                                password: e.target.value
                            })
                        }
                        required
                    />

                    {error && (
                        <div className="error">
                            {error}
                        </div>
                    )}

                    <button className="primary-button">
                        Login
                    </button>
                </form>

                <p className="auth-switch">
                    Don't have an account?

                    <button
                        type="button"
                        className="link-button"
                        onClick={onShowSignup}
                    >
                        Sign Up
                    </button>
                </p>
            </div>
        </div>
    );
}
