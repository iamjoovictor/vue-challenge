from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config.config_db import origins
from logging import basicConfig, INFO, DEBUG, debug
from .routes.routes import routes

""""
    @copyright (c) ALL RIGHTS RESERVED
    @brief      Vue Challenge

    @details    Main file. Instance the FastAPI and include the main endpoints of application 

    @author     Joao Victor Silva de Sousa <jvsilva.fne@gmail.com>                                                                
    @since      Sep 07, 2024        
"""

description = """
`@copyright`  ALL RIGHTS RESERVED\n
`@brief`      Vue Challenge\n
`@author`     **Joao Victor Silva de Sousa** \<jvsilva.fne@gmail.com>\n
`@since`      Sep 07, 2024

## Introduction
"""

basicConfig(
    level=INFO,
    filename=f'logs/log_backend_api.txt',
    filemode='a',
    encoding='utf-8',
    format='%(asctime)s ; %(levelname)s ; %(message)s; %(filename)s'
)

app = FastAPI(
    title="Vue Challenge Application",
    description=description,
    version="0.0.1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for route in routes:
    app.include_router(route.router) 