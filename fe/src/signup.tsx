import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Signup: React.FC = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [name, setName] = useState('');
    const [dob, setDob] = useState('');
    const [gender, setGender] = useState('');
    const [retypePassword, setRetypePassword] = useState('');
    const [contact, setContact] = useState('');
    const [message, setMessage] = useState('');

    const navigate = useNavigate();

    const handleSignup = async (e: React.FormEvent) => {
        e.preventDefault();

        if (password !== retypePassword) {
            setMessage('Passwords do not match.');
            return;
        }

        const response = await fetch('http://localhost:5000/patient/sign_up', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password, name, dob, gender, contact })
        });
        const data = await response.json();
        if (response.ok) {
            setMessage(data.message || 'Account registered successfully!');
            setTimeout(() => {
                navigate('/');
            }, 3000);
        } else {
            setMessage(data.error || 'Signup failed');
        }
    };

    return (
        <div style={{
            padding: '20px',
            minHeight: '100vh',
            backgroundImage: `url('background_loginpage.jpg')`,
            backgroundSize: 'cover',
            backgroundPosition: 'center',
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
        }}>
            <div style={{
                backgroundColor: 'rgba(255, 255, 255, 0.8)',
                padding: '50px',
                borderRadius: '10px',
                textAlign: 'center',
                width: '400px',
                backdropFilter: 'blur(5px)',
            }}>
                <h2>Sign up for patient account</h2>
                {message && <p style={{ color: 'red' }}>{message}</p>}
                <form onSubmit={handleSignup}>
                    <div style={{ marginBottom: '15px' }}>
                        <label style={{ display: 'block', marginBottom: '5px', textAlign: 'left' }}>Username: </label>
                        <input 
                            type="text" 
                            value={username} 
                            onChange={e => setUsername(e.target.value)} 
                            required
                            style={{ padding: '10px', width: 'calc(100% - 22px)' }}
                        />
                    </div>
                    <div style={{ marginBottom: '15px' }}>
                        <label style={{ display: 'block', marginBottom: '5px', textAlign: 'left' }}>Password: </label>
                        <input 
                            type="password" 
                            value={password} 
                            onChange={e => setPassword(e.target.value)} 
                            required
                            style={{ padding: '10px', width: 'calc(100% - 22px)' }}
                        />
                    </div>
                    <div style={{ marginBottom: '15px' }}>
                        <label style={{ display: 'block', marginBottom: '5px', textAlign: 'left' }}>Retype Password: </label>
                        <input 
                            type="password" 
                            value={retypePassword} 
                            onChange={e => setRetypePassword(e.target.value)} 
                            required
                            style={{ padding: '10px', width: 'calc(100% - 22px)' }}
                        />
                    </div>
                    <div style={{ marginBottom: '15px' }}>
                        <label style={{ display: 'block', marginBottom: '5px', textAlign: 'left' }}>Full name: </label>
                        <input 
                            type="text" 
                            value={name} 
                            onChange={e => setName(e.target.value)} 
                            required
                            style={{ padding: '10px', width: 'calc(100% - 22px)' }}
                        />
                    </div>
                    <div style={{ marginBottom: '15px' }}>
                        <label style={{ display: 'block', marginBottom: '5px', textAlign: 'left' }}>Date of birth (YYYY-MM-DD): </label>
                        <input 
                            type="date" 
                            value={dob} 
                            onChange={e => setDob(e.target.value)} 
                            required
                            style={{ padding: '10px', width: 'calc(100% - 22px)' }}
                        />
                    </div>
                    <div style={{ marginBottom: '15px' }}>
                        <label style={{ display: 'block', marginBottom: '5px', textAlign: 'left' }}>Gender: </label>
                        <select
                            value={gender}
                            onChange={e => setGender(e.target.value)}
                            required
                            style={{ padding: '10px', width: 'calc(100%)' }}
                        >
                            <option value="">Select Gender</option>
                            <option value="Male">Male</option>
                            <option value="Female">Female</option>
                            <option value="Other">Other</option>
                        </select>
                    </div>
                    <div style={{ marginBottom: '20px' }}>
                        <label style={{ display: 'block', marginBottom: '5px', textAlign: 'left' }}>Contact: </label>
                        <input 
                            type="text" 
                            value={contact} 
                            onChange={e => setContact(e.target.value)} 
                            required
                            style={{ padding: '10px', width: 'calc(100% - 22px)' }}
                        />
                    </div>
                    <button type="submit" style={{ padding: '10px 40px' }}>Sign Up</button>
                </form>
                <p style={{ marginTop: '20px' }}>
                    <a href="/" style={{ color: '#007bff', textDecoration: 'none' }}>Back to login</a>
                </p>
            </div>
        </div>
    );
};

export default Signup;