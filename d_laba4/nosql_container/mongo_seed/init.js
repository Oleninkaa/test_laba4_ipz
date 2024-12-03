db = db.getSiblingDB('car_sales');

// Клієнти
db.clients.insertMany([
  { FullName: "Іван Іванов", Age: 35, Gender: "Чоловік", CarType: "Седан", Price: 15000 },
  { FullName: "Олена Петрова", Age: 28, Gender: "Жінка", CarType: "Хетчбек", Price: 12000 }
]);

// Автомобілі
db.cars.insertMany([
  { CarType: "Седан", Price: 15000, Mileage: 80000, TechnicalCondition: "Гарний" },
  { CarType: "Хетчбек", Price: 12000, Mileage: 60000, TechnicalCondition: "Середній" }
]);

// Продавці
db.sellers.insertMany([
  { FullName: "Сергій Сергієнко", Age: 40, Gender: "Чоловік", AdditionalInfo: "Досвідчений продавець" }
]);

// Замовлення
db.orders.insertOne({
  ClientID: db.clients.findOne({ FullName: "Іван Іванов" })._id,
  CarID: db.cars.findOne({ CarType: "Седан" })._id,
  OrderDate: new Date()
});
