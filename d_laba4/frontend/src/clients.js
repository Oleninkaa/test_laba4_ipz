import React, { useState, useEffect } from "react";

function Clients() {
  const [clients, setClients] = useState([]);
  const [newClient, setNewClient] = useState({
    full_name: "",
    age: "",
    gender: "",
    car_type: "",
    price: "",
  });
  const [editingClient, setEditingClient] = useState(null);
  const [searchTerm, setSearchTerm] = useState(""); // New state for search term

  // Fetch clients from the backend
  useEffect(() => {
    fetch(`${process.env.REACT_APP_API_URL}/clients`)
      .then((res) => res.json())
      .then((data) => setClients(data));
  }, []);

  // Add a new client
  const addClient = () => {
    fetch(`${process.env.REACT_APP_API_URL}/clients`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(newClient),
    })
      .then((res) => res.json())
      .then((data) => {
        alert(data.message);
        setClients([...clients, { ...newClient, id: data.client_id }]);
        setNewClient({
          full_name: "",
          age: "",
          gender: "",
          car_type: "",
          price: "",
        });
      });
  };

  // Update an existing client
  const updateClient = (id) => {
    fetch(`${process.env.REACT_APP_API_URL}/clients/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(editingClient),
    })
      .then((res) => res.json())
      .then((data) => {
        alert(data.message);
        setClients(
          clients.map((client) =>
            client.id === id ? { ...client, ...editingClient } : client
          )
        );
        setEditingClient(null);
      });
  };

  // Delete a client
  const deleteClient = (id) => {
    if (!window.confirm("Are you sure you want to delete this client?")) return;

    fetch(`${process.env.REACT_APP_API_URL}/clients/${id}`, {
      method: "DELETE",
    })
      .then((res) => res.json())
      .then((data) => {
        alert(data.message);
        setClients(clients.filter((client) => client.id !== id));
      });
  };

  // Filter clients based on search term
  const filteredClients = clients.filter(
    (client) =>
      client.full_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      client.car_type.toLowerCase().includes(searchTerm.toLowerCase()) ||
      client.gender.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div>
      <h2>Clients</h2>

      {/* Search Input */}
      <input
        type="text"
        placeholder="Search Clients"
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)} // Update search term
      />

      <ul>
        {filteredClients.map((client) => (
          <li key={client.id}>
            {editingClient && editingClient.id === client.id ? (
              <span>
                <input
                  type="text"
                  defaultValue={client.full_name}
                  onChange={(e) =>
                    setEditingClient({
                      ...editingClient,
                      full_name: e.target.value,
                    })
                  }
                />
                <input
                  type="number"
                  defaultValue={client.age}
                  onChange={(e) =>
                    setEditingClient({
                      ...editingClient,
                      age: e.target.value,
                    })
                  }
                />
                <input
                  type="text"
                  defaultValue={client.gender}
                  onChange={(e) =>
                    setEditingClient({
                      ...editingClient,
                      gender: e.target.value,
                    })
                  }
                />
                <input
                  type="text"
                  defaultValue={client.car_type}
                  onChange={(e) =>
                    setEditingClient({
                      ...editingClient,
                      car_type: e.target.value,
                    })
                  }
                />
                <input
                  type="number"
                  defaultValue={client.price}
                  onChange={(e) =>
                    setEditingClient({
                      ...editingClient,
                      price: e.target.value,
                    })
                  }
                />
                <button onClick={() => updateClient(client.id)}>
                  Save Changes
                </button>
                <button onClick={() => setEditingClient(null)}>Cancel</button>
              </span>
            ) : (
              <span>
                {client.full_name} ({client.age} years) - {client.car_type} ($
                {client.price})
                <button onClick={() => setEditingClient(client)}>Edit</button>
                <button onClick={() => deleteClient(client.id)}>Delete</button>
              </span>
            )}
          </li>
        ))}
      </ul>

      <h3>Add New Client</h3>
      <input
        type="text"
        placeholder="Full Name"
        value={newClient.full_name}
        onChange={(e) =>
          setNewClient({ ...newClient, full_name: e.target.value })
        }
      />
      <input
        type="number"
        placeholder="Age"
        value={newClient.age}
        onChange={(e) => setNewClient({ ...newClient, age: e.target.value })}
      />
      <input
        type="text"
        placeholder="Gender"
        value={newClient.gender}
        onChange={(e) => setNewClient({ ...newClient, gender: e.target.value })}
      />
      <input
        type="text"
        placeholder="Car Type"
        value={newClient.car_type}
        onChange={(e) =>
          setNewClient({ ...newClient, car_type: e.target.value })
        }
      />
      <input
        type="number"
        placeholder="Price"
        value={newClient.price}
        onChange={(e) => setNewClient({ ...newClient, price: e.target.value })}
      />
      <button onClick={addClient}>Add Client</button>
    </div>
  );
}

export default Clients;

