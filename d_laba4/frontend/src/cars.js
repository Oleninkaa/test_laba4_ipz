import React, { useState, useEffect } from 'react';

function Cars() {
    const [cars, setCars] = useState([]);
    const [newCar, setNewCar] = useState({ car_type: '', price: '', mileage: '', technical_condition: '' });

    useEffect(() => {
        fetch(`${process.env.REACT_APP_API_URL}/cars`)
            .then(res => res.json())
            .then(data => setCars(data));
    }, []);

    const addCar = () => {
        fetch(`${process.env.REACT_APP_API_URL}/cars`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newCar)
        })
        .then(res => res.json())
        .then(data => {
            alert(data.message);
            setCars([...cars, { ...newCar, id: data.car_id }]);
        });
    };
    //print(cars)
    return (
        <div>
            <h2>Cars</h2>
            <ul>
                {cars.map(car => (
                    <li key={car.id}>{car.car_type} - ${car.price}</li>
                ))}
            </ul>
            <input
                type="text"
                placeholder="Car Type"
                onChange={e => setNewCar({ ...newCar, car_type: e.target.value })}
            />
            <input
                type="number"
                placeholder="Price"
                onChange={e => setNewCar({ ...newCar, price: e.target.value })}
            />
            <input
                type="number"
                placeholder="Mileage"
                onChange={e => setNewCar({ ...newCar, mileage: e.target.value })}
            />
            <input
                type="text"
                placeholder="Technical Condition"
                onChange={e => setNewCar({ ...newCar, technical_condition: e.target.value })}
            />
            <button onClick={addCar}>Add Car</button>
        </div>
    );
}

export default Cars;

