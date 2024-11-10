DROP TABLE IF EXISTS action_figures_summary;

CREATE TABLE IF NOT EXISTS action_figures_summary (
    action_figure_name VARCHAR(255) NOT NULL,
    total_quantity_sold INT,
    total_revenue_generated DECIMAL(10, 2),
    last_date_of_purchase DATE,
    most_sold_year INT,
    total_purchase_orders INT,
    number_of_films INT,
    earliest_debut_date DATE,
    last_appearance_date DATE,
    homeworld VARCHAR(255)
);