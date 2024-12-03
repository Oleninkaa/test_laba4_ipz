-- Таблиця "Клієнти"
CREATE TABLE Clients (
    ClientID SERIAL PRIMARY KEY,
    FullName VARCHAR(100),
    Age INT,
    Gender VARCHAR(10),
    CarType VARCHAR(50),
    Price DECIMAL(10, 2)
);

-- Таблиця "Автомобілі"
CREATE TABLE Cars (
    CarID SERIAL PRIMARY KEY,
    CarType VARCHAR(50),
    Price DECIMAL(10, 2),
    Mileage INT,
    TechnicalCondition VARCHAR(100)
);

-- Таблиця "Продавці"
CREATE TABLE Sellers (
    SellerID SERIAL PRIMARY KEY,
    FullName VARCHAR(100),
    Age INT,
    Gender VARCHAR(10),
    AdditionalInfo TEXT
);

-- Таблиця "Замовлення"
CREATE TABLE Orders (
    OrderID SERIAL PRIMARY KEY,
    ClientID INT REFERENCES Clients(ClientID),
    CarID INT REFERENCES Cars(CarID),
    OrderDate DATE DEFAULT CURRENT_DATE
);

ALTER TABLE orders
DROP CONSTRAINT orders_client_id_fkey;

ALTER TABLE orders
ADD CONSTRAINT orders_client_id_fkey
FOREIGN KEY (client_id) REFERENCES clients(clientid) ON DELETE SET NULL;
