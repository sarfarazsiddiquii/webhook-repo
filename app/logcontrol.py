import logging

def setup_logger(module_name):
    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.setLevel(logging.WARNING)

    logging.basicConfig(
        filename='logs/app.log',  
        filemode='a',
        level=logging.INFO,
        format="%(asctime)s - %(name)s -- %(message)s",
        datefmt='%Y-%m-%d | %H:%M:%S'
    )
    
    custom_logger = logging.getLogger(module_name)
    return custom_logger