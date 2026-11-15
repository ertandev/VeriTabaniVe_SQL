/*
================================================================================
    PROJE ADI: NovaStore E-Ticaret Veri Yönetim Sistemi
    GELİŞTİRİCİ: Ertan Yolcu
    VERİ TABANI: Microsoft SQL Server (T-SQL)
    AÇIKLAMA: Bu betik, NovaStore e-ticaret sistemi için ilişkisel veri tabanı
              tasarımını, örnek veri girişini, analitik DQL sorgularını,
              görünüm (View) ve yedekleme (Backup) komutlarını içerir.
================================================================================
*/

-- =============================================================================
-- BÖLÜM 1: Veri Tabanı Tasarımı (Logical Design ve DDL)
-- =============================================================================

-- 1. Veri Tabanı Oluşturma
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = N'NovaStoreDB')
BEGIN
    CREATE DATABASE NovaStoreDB;
END;
GO

USE NovaStoreDB;
GO

-- Bağımlılık sırasına göre eski tablolar varsa temizleme (Drop in reverse dependency order)
IF OBJECT_ID('dbo.OrderDetails', 'U') IS NOT NULL DROP TABLE dbo.OrderDetails;
IF OBJECT_ID('dbo.Orders', 'U') IS NOT NULL DROP TABLE dbo.Orders;
IF OBJECT_ID('dbo.Products', 'U') IS NOT NULL DROP TABLE dbo.Products;
IF OBJECT_ID('dbo.Customers', 'U') IS NOT NULL DROP TABLE dbo.Customers;
IF OBJECT_ID('dbo.Categories', 'U') IS NOT NULL DROP TABLE dbo.Categories;
GO

-- A. Tablo: Categories (Kategoriler)
-- CategoryID: Birincil anahtar (Primary Key), otomatik artan (Identity 1,1)
-- CategoryName: Kategori adı, boş geçilemez (Not Null)
CREATE TABLE dbo.Categories (
    CategoryID INT IDENTITY(1,1) NOT NULL,
    CategoryName VARCHAR(50) NOT NULL,
    CONSTRAINT PK_Categories PRIMARY KEY (CategoryID)
);
GO

-- C. Tablo: Customers (Müşteriler)
-- Not: Bağımlılık zincirinde Orders tablosundan önce oluşturulmalıdır.
-- CustomerID: Birincil anahtar, otomatik artan
-- FullName: Müşteri adı soyadı
-- City: Şehir bilgisi
-- Email: Benzersiz e-posta adresi (Unique)
CREATE TABLE dbo.Customers (
    CustomerID INT IDENTITY(1,1) NOT NULL,
    FullName VARCHAR(50) NOT NULL,
    City VARCHAR(20) NOT NULL,
    Email VARCHAR(100) NOT NULL,
    CONSTRAINT PK_Customers PRIMARY KEY (CustomerID),
    CONSTRAINT UQ_Customers_Email UNIQUE (Email)
);
GO

-- B. Tablo: Products (Ürünler)
-- ProductID: Birincil anahtar, otomatik artan
-- ProductName: Ürün adı, boş geçilemez
-- Price: Ürün satış fiyatı
-- Stock: Stok adedi (Varsayılan değer: 0)
-- CategoryID: Categories tablosuna bağlanan Yabancı Anahtar (Foreign Key)
CREATE TABLE dbo.Products (
    ProductID INT IDENTITY(1,1) NOT NULL,
    ProductName VARCHAR(100) NOT NULL,
    Price DECIMAL(10,2) NOT NULL,
    Stock INT NOT NULL CONSTRAINT DF_Products_Stock DEFAULT (0),
    CategoryID INT NOT NULL,
    CONSTRAINT PK_Products PRIMARY KEY (ProductID),
    CONSTRAINT FK_Products_Categories FOREIGN KEY (CategoryID) 
        REFERENCES dbo.Categories(CategoryID)
);
GO

-- D. Tablo: Orders (Siparişler)
-- OrderID: Birincil anahtar, otomatik artan
-- CustomerID: Customers tablosuna bağlanan Yabancı Anahtar
-- OrderDate: Sipariş tarihi (Varsayılan değer: GETDATE())
-- TotalAmount: Toplam sipariş tutarı
CREATE TABLE dbo.Orders (
    OrderID INT IDENTITY(1,1) NOT NULL,
    CustomerID INT NOT NULL,
    OrderDate DATETIME NOT NULL CONSTRAINT DF_Orders_OrderDate DEFAULT (GETDATE()),
    TotalAmount DECIMAL(10,2) NOT NULL,
    CONSTRAINT PK_Orders PRIMARY KEY (OrderID),
    CONSTRAINT FK_Orders_Customers FOREIGN KEY (CustomerID) 
        REFERENCES dbo.Customers(CustomerID)
);
GO

-- E. Tablo: OrderDetails (Sipariş Detayları - Ara Tablo)
-- DetailID: Birincil anahtar, otomatik artan
-- OrderID: Orders tablosuna bağlanan Yabancı Anahtar
-- ProductID: Products tablosuna bağlanan Yabancı Anahtar
-- Quantity: Kaç adet alındığı bilgisi
CREATE TABLE dbo.OrderDetails (
    DetailID INT IDENTITY(1,1) NOT NULL,
    OrderID INT NOT NULL,
    ProductID INT NOT NULL,
    Quantity INT NOT NULL,
    CONSTRAINT PK_OrderDetails PRIMARY KEY (DetailID),
    CONSTRAINT FK_OrderDetails_Orders FOREIGN KEY (OrderID) 
        REFERENCES dbo.Orders(OrderID),
    CONSTRAINT FK_OrderDetails_Products FOREIGN KEY (ProductID) 
        REFERENCES dbo.Products(ProductID)
);
GO
