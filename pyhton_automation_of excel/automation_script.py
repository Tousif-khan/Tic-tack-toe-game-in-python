import pandas as pd
import numpy as np
from pandas import ExcelWriter
from pandas import ExcelFile
import time
import schedule
source = pd.ExcelFile('E:\pyhton_automation_of excel\BW_CPFR_OUTLET_HU10.xls')
sales = pd.read_excel(
    'E:\pyhton_automation_of excel\BW_SDS_HU10(006).xls', header=1)


def create_avg_sell(sales):
    ''' Create avg sell price for each material'''
    unique_material = sales['Material'].unique()
    num_of_unique_products = len(unique_material)
    prod_avg = {}
    for item in unique_material:
        small_sales = sales[sales['Material'] == item]
        total_sales = small_sales['P5 Net Sales EUR'].sum()
        total_quantity = small_sales['Sales Quantity'].sum()
        if total_quantity > 0:
            avg = round(total_sales/total_quantity, 4)
            prod_avg[item] = round(avg, 4)
    return prod_avg


def create_top_products(current_sheet, dict_prod_avg):
    material_list_current_sheet = current_sheet['Material'].unique()
    dict_sellout_NS = {}
    for item in material_list_current_sheet:
        filtered_sheet = current_sheet[current_sheet['Material'] == item]
        sell_through_quantity = filtered_sheet['Sellthru Qty'].sum()
        dict_sellout_NS[item] = round(
            sell_through_quantity*dict_prod_avg.get(item, 0), 2)
    sorted_sellout = sorted(dict_sellout_NS.items(),
                            key=lambda x: (-x[1], x[0]))
    return sorted_sellout


def create_sell_ratio(df_weekly_sale, sorted_sellout):
    total_weekly_sale = df_weekly_sale['P5 Net Sales EUR'].sum()
    product_profit_ratios = []
    if total_weekly_sale > 0:
        for i in range(len(sorted_sellout)):
            product_profit_ratios.append(
                round(sorted_sellout[i][1]/total_weekly_sale*100, 4))
    return product_profit_ratios


def create_customer_list(df_weekly_sale):
    dict_customer_earn = {}
    unique_customers = df_weekly_sale['Customer'].unique()
    for cus in unique_customers:
        df_weekly_sale_for_customers = df_weekly_sale[df_weekly_sale['Customer'] == cus]
        dict_customer_earn[cus] = round(
            df_weekly_sale_for_customers['P5 Net Sales EUR'].sum(), 2)
    sorted_customer_earn = sorted(
        dict_customer_earn.items(), key=lambda x: (-x[1], x[0]))
    return sorted_customer_earn


def generate_report():
    writer = ExcelWriter('E:\pyhton_automation_of excel\Top5NS_Report.xlsx')
    dict_prod_avg = create_avg_sell(sales)
    sheets = source.sheet_names
    for sheet in sheets:
        df_current_sheet = source.parse(sheet_name=sheet)
        list_sorted_sellout = create_top_products(
            df_current_sheet, dict_prod_avg)
        week = df_current_sheet['Calendar Year/Week'][1]
        df_weekly_sale = sales[sales['Calendar Year/Week'] == week]
        list_sell_ratio = create_sell_ratio(
            df_weekly_sale, list_sorted_sellout)
        list_sorted_customer_earn = create_customer_list(df_weekly_sale)
        output = []
        columns_names = ['Week', 'Top_5_products', 'Average_sellout',
                         'Net_sell_ratios', 'To5_5_Customers', 'Customer_Earnings']
        for i in range(5):
            row = [week, list_sorted_sellout[i][0], list_sorted_sellout[i][1], list_sell_ratio[i],
                   list_sorted_customer_earn[i][0], list_sorted_customer_earn[i][1]]
            output.append(row)
        df_top_5_NS = pd.DataFrame(output, columns=columns_names)
        df_top_5_NS.to_excel(writer, sheet_name=str(week), index=False)
    writer.save()
generate_report()
schedule.every().day.at("11:00").do(generate_report)
