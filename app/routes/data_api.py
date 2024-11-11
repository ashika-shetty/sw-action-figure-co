import asyncpg
from fastapi import FastAPI, HTTPException


app = FastAPI()

DB_SOURCE_URL = 'postgres://user:password@localhost:5432/source'
DB_DW_URL = 'postgres://user:password@localhost:5433/dw'


@app.get("/action-figure/{action_figure_name}", summary="Get details for a specific action figure")
async def get_action_figure_details(action_figure_name: str):
    """
    Retrieve detailed information about a specific action figure, including current price and total sales value.

    - **action_figure_name**: The name of the action figure (e.g., 'Luke Skywalker')

    :param action_figure_name:
    :return:
    """
    conn = await asyncpg.connect(DB_SOURCE_URL)
    try:
        query = """
        SELECT 
            action_figure_name, 
            price AS current_price_per_unit,
            SUM(quantity * price) AS total_sales_value
        FROM 
            source
        WHERE 
            action_figure_name = $1
        GROUP BY 
            action_figure_name, price;
        """
        result = await conn.fetchrow(query, action_figure_name)
        if result is None:
            raise HTTPException(status_code=404, detail="Action figure not found")
        return dict(result)
    finally:
        await conn.close()


@app.get("/performance/summary")
async def get_performance_summary():
    """

    :return:
    """
    conn_source = await asyncpg.connect(DB_SOURCE_URL)
    conn_dw = await asyncpg.connect(DB_DW_URL)
    try:
        # Define the SQL query
        query = """
        WITH SalesRepPerformance AS (
            SELECT 
                sales_rep,
                SUM(quantity) AS total_figures_sold,
                SUM(quantity * price) AS total_sales_value
            FROM 
                source
            GROUP BY 
                sales_rep
        ),
        TopActionFigures AS (
            SELECT 
                action_figure_name,
                SUM(quantity) AS total_quantity_sold
            FROM 
                source
            GROUP BY 
                action_figure_name
            ORDER BY 
                total_quantity_sold DESC
            LIMIT 10
        )

        SELECT 
            'Top 10 Sales Reps by Figures Sold' AS Category,
            sales_rep AS Entity,
            total_figures_sold AS Metric
        FROM 
            (SELECT sales_rep, total_figures_sold FROM SalesRepPerformance ORDER BY total_figures_sold DESC LIMIT 10) AS TopFiguresSold

        UNION ALL

        SELECT 
            'Top 10 Sales Reps by Sales Value' AS Category,
            sales_rep AS Entity,
            total_sales_value AS Metric
        FROM 
            (SELECT sales_rep, total_sales_value FROM SalesRepPerformance ORDER BY total_sales_value DESC LIMIT 10) AS TopSalesValue

        UNION ALL

        SELECT 
            'Top 10 Action Figures Sold' AS Category,
            action_figure_name AS Entity,
            total_quantity_sold AS Metric
        FROM 
            TopActionFigures;
        """
        # Execute the query on the source database
        results = await conn_source.fetch(query)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Close both connections
        await conn_source.close()
        await conn_dw.close()