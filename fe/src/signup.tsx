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
            <h2>Đăng ký tài khoản bệnh nhân</h2>
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
                    <label>Họ và tên: </label>
                    <input 
                        type="text" 
                        value={name} 
                        onChange={e => setName(e.target.value)} 
                        required 
                    />
                </div>
                <div>
                    <label>Ngày sinh (YYYY-MM-DD): </label>
                    <input 
                        type="date" 
                        value={dob} 
                        onChange={e => setDob(e.target.value)} 
                        required 
                    />
                </div>
                <div>
                    <label>Giới tính: </label>
                    <input 
                        type="text" 
                        value={gender} 
                        onChange={e => setGender(e.target.value)} 
                        required 
                    />
                </div>
                <div>
                    <label>Liên hệ: </label>
                    <input 
                        type="text" 
                        value={contact} 
                        onChange={e => setContact(e.target.value)} 
                        required 
                    />
                </div>
                <button type="submit">Đăng ký</button>
            </form>
            <p>
                <a href="/">Quay lại đăng nhập</a>
            </p>
        </div>
    );
};

export default Signup;