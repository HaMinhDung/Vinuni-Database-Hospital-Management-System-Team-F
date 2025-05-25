import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Signup: React.FC = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [name, setName] = useState('');
    const [dob, setDob] = useState('');
    const [gender, setGender] = useState('');
    const [contact, setContact] = useState('');
    const [message, setMessage] = useState('');

    const navigate = useNavigate();

    const handleSignup = async (e: React.FormEvent) => {
        e.preventDefault();

        const response = await fetch('http://localhost:5000/patient/sign_up', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password, name, dob, gender, contact })
        });
        const data = await response.json();
        if (response.ok) {
            alert(data.message);
            navigate('/');
        } else {
            setMessage(data.error || 'Signup failed');
        }
    };

    return (
        <div style={{ padding: '20px' }}>
            <h2>Sign up for patient account</h2>
            {message && <p style={{ color: 'red' }}>{message}</p>}
            <form onSubmit={handleSignup}>
                <div>
                    <label>Username: </label>
                    <input 
                        type="text" 
                        value={username} 
                        onChange={e => setUsername(e.target.value)} 
                        required 
                    />
                </div>
                <div>
                    <label>Password: </label>
                    <input 
                        type="password" 
                        value={password} 
                        onChange={e => setPassword(e.target.value)} 
                        required 
                    />
                </div>
                <div>
                    <label>Full name: </label>
                    <input 
                        type="text" 
                        value={name} 
                        onChange={e => setName(e.target.value)} 
                        required 
                    />
                </div>
                <div>
                    <label>Date of birth (YYYY-MM-DD): </label>
                    <input 
                        type="date" 
                        value={dob} 
                        onChange={e => setDob(e.target.value)} 
                        required 
                    />
                </div>
                <div>
                    <label>Gender: </label>
                    <input 
                        type="text" 
                        value={gender} 
                        onChange={e => setGender(e.target.value)} 
                        required 
                    />
                </div>
                <div>
                    <label>Contact: </label>
                    <input 
                        type="text" 
                        value={contact} 
                        onChange={e => setContact(e.target.value)} 
                        required 
                    />
                </div>
                <button type="submit">Sign Up</button>
            </form>
            <p>
                <a href="/">Back to login</a>
            </p>
        </div>
    );
};

export default Signup;