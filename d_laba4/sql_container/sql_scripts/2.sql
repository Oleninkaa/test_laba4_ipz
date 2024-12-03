ALTER TABLE orders
ADD CONSTRAINT fk_client_id
FOREIGN KEY (clientid)
REFERENCES clients(clientid)
ON DELETE CASCADE;


