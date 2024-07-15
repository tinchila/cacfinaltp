CREATE DATABASE sistema;

USE sistema;

CREATE TABLE bebidas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bebida VARCHAR(255) NOT NULL,
    marca VARCHAR(255) NOT NULL,
    variedad VARCHAR(255) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    imagen VARCHAR(255) NOT NULL,
    cantidad INT NOT NULL
);

INSERT INTO bebidas (id, bebida, marca, variedad, precio, imagen, cantidad)
VALUES 
    (1, 'Whisky', 'Jack Daniels', 'N° 7', 40000, 'img/WhiskyJackDaniels.png', 100),
    (2, 'Whisky', 'Jhonnie Walker', 'Red', 15000, 'img/WhiskyJhonnieWalkerRed.png', 100),
    (3, 'Whisky', 'Jhonnie Walker', 'Black', 15000, 'img/WhiskyJhonnieWalkerBlack.png', 100),
    (4, 'Gin', 'Tanqueray', 'Original', 15000, 'img/GinTanquerayOriginal.png', 100),
    (5, 'Gin', 'Bombay', 'Shapire', 13000, 'img/GinBombayShapire.png', 100),
    (6, 'Gancia', 'Americano', 'Original', 15000, 'img/GanciaAmericanoOriginal.png', 100),
    (7, 'Fernet', 'Branca', 'Original', 15000, 'img/FernetBrancaOriginal.png', 100),
    (8, 'Vodka', 'Absolut', 'Original', 15000, 'img/VodkaAbsolutOriginal.png', 100);
