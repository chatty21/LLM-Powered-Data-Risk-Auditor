import pandas as pd

def generate_profile_summary(df: pd.DataFrame) -> str:
    summary = {
        "num_rows": df.shape[0],
        "num_columns": df.shape[1],
        "missing_values": int(df.isnull().sum().sum()),
        "columns": {}
    }

    for col in df.columns:
        col_data = df[col]
        summary["columns"][col] = {
            "dtype": str(col_data.dtype),
            "num_missing": int(col_data.isnull().sum()),
            "num_unique": int(col_data.nunique()),
            "example_values": col_data.dropna().unique().tolist()[:3]
        }

    # Build readable summary
    readable = f"📊 **Dataset Overview**\n- Rows: {summary['num_rows']:,}\n- Columns: {summary['num_columns']}\n- Total Missing Values: {summary['missing_values']:,}\n"
    readable += "\n🧩 **Column Details:**\n"

    for col, info in summary["columns"].items():
        readable += f"\n• **{col}** ({info['dtype']})\n"
        readable += f"   - Missing Values: {info['num_missing']:,}\n"
        readable += f"   - Unique Values: {info['num_unique']:,}\n"
        readable += f"   - Example Values: {info['example_values']}\n"

    return readable