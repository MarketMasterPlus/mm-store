-- mm-store/db/mm-store.sql

-- Create the marketmaster database
CREATE DATABASE marketmaster;

\connect marketmaster;

-- Create a table for stores
CREATE TABLE IF NOT EXISTS store (
    id SERIAL PRIMARY KEY,
    ownerid VARCHAR(255) NOT NULL,
    addressid VARCHAR(255) NOT NULL,  -- Soft reference to an address in the mm-store service (e.g., ViaCEP address ID)
    cnpj VARCHAR(14) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    imageurl VARCHAR(255)
);

-- Optionally, add indexes for commonly queried columns
CREATE INDEX IF NOT EXISTS idx_stores_id ON store(id);
CREATE INDEX IF NOT EXISTS idx_stores_addressid ON store(addressid);
CREATE INDEX IF NOT EXISTS idx_stores_ownerid ON store(ownerid);
