import React, { useState } from 'react';
import logo from './assets/paios.png';
import './Login.css';
import { useLogin, useNotify } from "react-admin"

const Login: React.FC = () => {
    const [email, setEmail] = useState('');

    const login = useLogin()
    const notify = useNotify()

    const handleUser = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault()
        if (!email.trim()) {
            notify('Email field cannot be empty', { type: 'error' });
            return;
        }

        try {
            const result = await login({ email });
            if (result?.stayOnLogin) {
                notify('Email verification sent! Please check your inbox.', { type: 'info' });
            }

        } catch (e) {
            console.error('Debug: Error in handleUser:', e);
            if (e instanceof Error) {
                if (e.name === 'InvalidStateError' || e.message.includes('The authenticator was previously registered')) {
                    notify('User already exists. Please login instead.', { type: 'error' });
                } else {
                    notify('An error occurred. Please try again.', { type: 'error' });
                }
            } else {
                notify('An unexpected error occurred. Please try again.', { type: 'error' });
            }
        }
    }

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setEmail(e.target.value)
    }

    return (
        <div className="auth-container">
            <h1 className="paios-heading">pAI-OS</h1>
            <img src={logo} alt="pAI-OS Logo" className="logo" />
            <form onSubmit={handleUser}>
                <input type="email" id="email" placeholder="Email" className="input-field" onChange={handleChange} value={email} />
                <button type="submit" className="auth-button">Enter pAI-OS</button>
            </form>
        </div>
    );
};

export default Login;