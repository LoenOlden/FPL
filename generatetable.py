import pandas as pd

def generate_html_tables(file_path='fplreview.csv'):
    # Read CSV
    df = pd.read_csv(file_path)

    # Map position codes to names and limits
    position_map = {
        'G': ('Goalkeepers', 20),
        'D': ('Defenders', 50),
        'M': ('Midfielders', 50),
        'F': ('Forwards', 30)
    }

    # Extract only columns that are for gameweek points
    gw_columns = [col for col in df.columns if col.endswith('_Pts')]
    gw_labels = [col.split('_')[0] for col in gw_columns]  # Just '30', '31', ...

    html_output = ""

    for pos_code, (pos_name, limit) in position_map.items():
        # Filter for position
        df_pos = df[df['Pos'] == pos_code].copy()

        # Add player name with base value (BV)
        df_pos['Name'] = df_pos['Name'] + ' (' + df_pos['BV'].astype(str) + ')'

        # Calculate total points from GW columns
        df_pos['Total'] = df_pos[gw_columns].sum(axis=1)

        # Sort by total points descending
        df_pos = df_pos.sort_values(by='Total', ascending=False).head(limit)

        # Select and rename columns for display
        display_columns = ['Name'] + gw_columns + ['Total']
        df_display = df_pos[display_columns]

        # Rename GW column headers (e.g., '30_Pts' -> '30')
        col_rename = dict(zip(gw_columns, gw_labels))
        col_rename['Total'] = 'Total'
        df_display.rename(columns=col_rename, inplace=True)

        # Generate HTML table
        html_table = df_display.to_html(index=False, border=1, table_id=f'playersTable{pos_code}', classes='display')
        html_output += f"<h3>Top Players ({pos_name}) - Points per Gameweek</h3>\n{html_table}\n"

    return html_output

# Save to file
if __name__ == "__main__":
    html_code = generate_html_tables('fplreview.csv')
    with open("players_tables.html", "w", encoding="utf-8") as f:
        f.write(html_code)
    print("HTML tables generated and saved to players_tables.html.")
