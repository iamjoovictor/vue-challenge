from fastapi import HTTPException, status
import re
from typing import Tuple
from datetime import datetime

""""
    @copyright (c) 2023 - Instituto Ambiental e Tecnologico da Amazonia. ALL RIGHTS RESERVED
    @brief      Jungle - Resource Management System (Jungle RMS)

    @details    Responsible for managing CRUD Logs and generic functions

    @author     Eduardo Lima <eduardo.lima@iatecam.org.br>                                                                
    @since      Sep 11, 2023        
"""

SERVER_ERROR = HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Server Error")
class TypeOperation():
    """Types of operations on database. Used to registry the logs"""
    INSERT = "INSERT"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    
    
def check_duplicated(data_list: list, key: str):
    s = set()
    for data in data_list:
        dict_data = dict(data)
        if key not in dict_data: continue
        value = dict_data[key]
        if key in dict_data and value in s: return value
        s.add(value)
    return False    
    


def is_numeric(string: str) -> bool:
    return bool(re.fullmatch(r'\d+', string))


def determine_alert_type_and_description(robot_parameter_name: str) -> Tuple[str, str]:
    if "Error" in robot_parameter_name:
        return "Error", "Unregistered Error"
    elif "Alarm" in robot_parameter_name or "Alert" in robot_parameter_name:
        return "Alert", "Unregistered Alert"
    else:
        return "Unknown", "Unknown Event"

def format_datetime(datetime_obj: datetime) -> Tuple[str, str]:
    formatted_date = datetime_obj.strftime("%d %b %Y") 
    collected_time = datetime_obj.strftime("%H:%M:%S")  
    return formatted_date, collected_time