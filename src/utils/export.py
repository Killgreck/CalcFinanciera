import pandas as pd
from datetime import datetime
import os


def export_to_csv(dataframe, filename, folder="exports"):
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    filepath = os.path.join(folder, filename)
    dataframe.to_csv(filepath, index=False, encoding='utf-8-sig')
    return filepath


def export_to_excel(dataframe, summary_data, filename, folder="exports"):
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    filepath = os.path.join(folder, filename)
    
    with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
        summary_df = pd.DataFrame([summary_data])
        summary_df.to_excel(writer, sheet_name='Resumen', index=False)
        
        dataframe.to_excel(writer, sheet_name='Tabla de Amortización', index=False)
        
        workbook = writer.book
        
        for sheet in workbook.worksheets:
            for column in sheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                sheet.column_dimensions[column_letter].width = adjusted_width
    
    return filepath
