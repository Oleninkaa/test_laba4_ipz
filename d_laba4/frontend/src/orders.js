import React, { useState, useEffect } from 'react';

function Orders() {
    const [orders, setOrders] = useState([]);
    const [newOrder, setNewOrder] = useState({
        client_id: '',
        car_id: ''
    });

    useEffect(() => {
        fetch(`${process.env.REACT_APP_API_URL}/orders`)
            .then(res => res.json())
            .then(data => setOrders(data));
    }, []);
    //print(orders)
    const addOrder = () => {
        fetch(`${process.env.REACT_APP_API_URL}/orders`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newOrder)
        })
            .then(res => res.json())
            .then(data => {
                alert(data.message);
                setOrders([...orders, { ...newOrder, id: data.order_id }]);
            });
    };

    return (
        <div>
            <h2>Orders</h2>
            <ul>
                {orders.map(order => (
                    <li key={order.id}>
                        Order #{order.id}: Client {order.client_id} - Car {order.car_id} (Date: {order.order_date})
                    </li>
                ))}
            </ul>
            <input
                type="number"
                placeholder="Client ID"
                onChange={e => setNewOrder({ ...newOrder, client_id: e.target.value })}
            />
            <input
                type="number"
                placeholder="Car ID"
                onChange={e => setNewOrder({ ...newOrder, car_id: e.target.value })}
            />
            <button onClick={addOrder}>Add Order</button>
        </div>
    );
}

export default Orders;

