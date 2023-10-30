import logging

class Logger:

  def __init__(self, name, level):
    self.logger = logging.getLogger(name)
    self.logger.setLevel(level)
    
  def set_handler(self, filepath, formatter):
    filehandler = logging.FileHandler(filepath)
    log_formatter = logging.Formatter(formatter)
    filehandler.setFormatter(log_formatter)
    self.logger.addHandler(filehandler)
