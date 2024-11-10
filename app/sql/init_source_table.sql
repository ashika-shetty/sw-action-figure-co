DROP TABLE IF EXISTS source;

CREATE TABLE source (
    action_figure_name VARCHAR(255) NOT NULL,
    quantity INT,
    price DECIMAL(10, 2),
    date_of_purchase DATE,
    email VARCHAR(255),
    sales_rep VARCHAR(255),
    promo_code VARCHAR(100)
);