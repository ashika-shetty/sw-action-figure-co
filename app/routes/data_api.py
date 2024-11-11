import asyncpg
from fastapi import FastAPI, HTTPException


app = FastAPI()


@app.get("/action-figure/{action_figure_name}")
async def get_action_figure_details(action_figure_name: str):
    """

    :param action_figure_name:
    :return:
    """
    conn = await asyncpg.connect('postgres://user:password@localhost:5433/dw')
    query = """
    SELECT 
    action_figure_name,total_revenue_generated
    FROM 
        action_figures_summary
    WHERE 
        action_figure_name = $1
    GROUP BY 
        action_figure_name, total_revenue_generated;
    """
    result = await conn.fetchrow(query, action_figure_name)
    if result is None:
        raise HTTPException(status_code=404, detail="Action figure not found")
    return dict(result)



