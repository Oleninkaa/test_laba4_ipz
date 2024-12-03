import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Route, Link, Routes } from 'react-router-dom';
import ReactDOM from 'react-dom/client';
import Clients from "./clients.js"
import Cars from "./cars.js"
import Orders from "./orders.js"
import Sellers from "./sellers.js"
const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
<Router>
            <nav>
                <ul>
                    <li><Link to="/clients">Clients</Link></li>
                    <li><Link to="/sellers">Sellers</Link></li>
                    <li><Link to="/orders">Orders</Link></li>
                    <li><Link to="/cars">Cars</Link></li>
                </ul>
            </nav>
            <Routes>
                <Route path="/clients" element={<Clients />} />
                <Route path="/sellers" element={<Sellers />} />
                <Route path="/orders" element={<Orders />} />
                <Route path="/cars" element={<Cars />} />
            </Routes>
        </Router>
        )
