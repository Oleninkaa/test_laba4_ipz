import React, { useState, useEffect } from 'react';

function Sellers() {
    const [sellers, setSellers] = useState([]);
    const [newSeller, setNewSeller] = useState({
        full_name: '',
        age: '',
        gender: '',
        additional_info: ''
    });
    const [searchTerm, setSearchTerm] = useState('');

    useEffect(() => {
        fetch(`${process.env.REACT_APP_API_URL}/sellers`)
            .then(res => res.json())
            .then(data => setSellers(data));
    }, []);

    const addSeller = () => {
        fetch(`${process.env.REACT_APP_API_URL}/sellers`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newSeller)
        })
            .then(res => res.json())
            .then(data => {
                alert(data.message);
                setSellers([...sellers, { ...newSeller, id: data.seller_id }]);
            });
    };

    // Filter sellers based on the search term
    const filteredSellers = sellers.filter(seller =>
        seller.full_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        seller.gender.toLowerCase().includes(searchTerm.toLowerCase()) ||
        seller.additional_info.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div>
            <h2>Sellers</h2>

            {/* Search Input */}
            <input
                type="text"
                placeholder="Search Sellers"
                value={searchTerm}
                onChange={e => setSearchTerm(e.target.value)}
            />

            <ul>
                {filteredSellers.map(seller => (
                    <li key={seller.id}>
                        {seller.full_name} ({seller.age} years, {seller.gender}) - {seller.additional_info}
                    </li>
                ))}
            </ul>

            <input
                type="text"
                placeholder="Full Name"
                onChange={e => setNewSeller({ ...newSeller, full_name: e.target.value })}
            />
            <input
                type="number"
                placeholder="Age"
                onChange={e => setNewSeller({ ...newSeller, age: e.target.value })}
            />
            <input
                type="text"
                placeholder="Gender"
                onChange={e => setNewSeller({ ...newSeller, gender: e.target.value })}
            />
            <input
                type="text"
                placeholder="Additional Info"
                onChange={e => setNewSeller({ ...newSeller, additional_info: e.target.value })}
            />
            <button onClick={addSeller}>Add Seller</button>
        </div>
    );
}

export default Sellers;

